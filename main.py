import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel
from weasyprint import HTML


app = FastAPI(
    title="Escriba",
    description="API to generate PDF documents with customizable templates",
    version="2025119",
)


class DocumentRequest(BaseModel):
    template: str
    payload: Dict[str, Any]


class TemplateManager:
    """Manages template loading and validation."""

    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.jinja_env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def get_template_path(self, template_name: str) -> Path:
        """Get the path to a template directory."""
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template '{template_name}' not found")
        return template_path

    def list_templates(self) -> list[str]:
        """
        List all available templates that are functional.

        Returns:
            List of template names that have both validator.py and template.html
        """
        templates = []

        for item in self.templates_dir.iterdir():
            if item.is_dir():
                validator_file = item / "validator.py"
                template_file = item / "template.html"

                if validator_file.exists() and template_file.exists():
                    templates.append(item.name)

        return sorted(templates)

    def load_validator(self, template_name: str):
        """Dynamically load the validator module for a template."""
        template_path = self.get_template_path(template_name)
        validator_path = template_path / "validator.py"

        if not validator_path.exists():
            raise FileNotFoundError(
                f"Validator not found for template '{template_name}'"
            )

        spec = importlib.util.spec_from_file_location(
            f"{template_name}.validator", validator_path
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load validator for '{template_name}'")

        validator_module = importlib.util.module_from_spec(spec)
        sys.modules[f"{template_name}.validator"] = validator_module
        spec.loader.exec_module(validator_module)

        return validator_module

    def validate_payload(self, template_name: str, payload: Dict[str, Any]) -> None:
        validator_module = self.load_validator(template_name)

        if not hasattr(validator_module, "validate_payload"):
            raise AttributeError(
                f"Validator for '{template_name}' missing 'validate_payload' function"
            )

        # This will raise ValidationError if validation fails
        validator_module.validate_payload(payload)

    def get_template_schema(self, template_name: str) -> Dict[str, Any]:
        """
        Get an example payload structure for a template.

        Args:
            template_name: Name of the template

        Returns:
            Dictionary with template name and example payload structure
        """
        validator_module = self.load_validator(template_name)

        if not hasattr(validator_module, "PayloadModel"):
            raise AttributeError(
                f"Validator for '{template_name}' missing 'PayloadModel' class"
            )

        pydantic_model = validator_module.PayloadModel
        schema = pydantic_model.model_json_schema()
        definitions = schema.get("$defs", {})

        def generate_example_value(field_schema: Dict[str, Any]) -> Any:
            """Generate an example value based on field schema."""
            field_type = field_schema.get("type")

            if field_type == "string":
                return "string"
            elif field_type == "integer":
                return 0
            elif field_type == "number":
                return 0.0
            elif field_type == "boolean":
                return False
            elif field_type == "array":
                items_schema = field_schema.get("items", {})

                # Handle $ref in array items
                if "$ref" in items_schema:
                    ref_name = items_schema["$ref"].split("/")[-1]
                    if ref_name in definitions:
                        item_example = {}
                        ref_properties = definitions[ref_name].get("properties", {})
                        for prop_name, prop_schema in ref_properties.items():
                            item_example[prop_name] = generate_example_value(
                                prop_schema
                            )
                        return [item_example]
                else:
                    return [generate_example_value(items_schema)]
            elif field_type == "object":
                return {}
            elif "anyOf" in field_schema:
                # For union types, use the first type
                return generate_example_value(field_schema["anyOf"][0])
            else:
                return "string"

        example_payload = {}
        properties = schema.get("properties", {})

        for field_name, field_schema in properties.items():
            example_payload[field_name] = generate_example_value(field_schema)

        return {
            "template": template_name,
            "required": schema.get("required", []),
            "payload": example_payload,
        }

    def get_stylesheets(self, template_name: str) -> list[str]:
        """
        Get the list of CSS files to use for a template.

        Templates can override the default by providing their own styles.css.
        Otherwise, the default Tailwind CSS (with Sen font) is used.

        Args:
            template_name: Name of the template

        Returns:
            List of absolute paths to CSS files
        """
        template_path = self.get_template_path(template_name)
        custom_css = template_path / "styles.css"
        default_css = Path(__file__).parent / "assets" / "css" / "tailwind.css"

        # Check if template has custom CSS
        if custom_css.exists():
            return [str(custom_css.absolute())]

        # Use default CSS
        return [str(default_css.absolute())]

    def render_template(
        self, template_name: str, payload: Dict[str, Any]
    ) -> tuple[str, str]:
        """
        Render the HTML template with the provided payload using Jinja2.

        Returns:
            Tuple of (rendered_html, base_url) where base_url is the template directory
            for resolving relative asset paths
        """
        template_path = self.get_template_path(template_name)

        # Load and render template using Jinja2
        jinja_template = self.jinja_env.get_template(f"{template_name}/template.html")
        rendered = jinja_template.render(**payload)

        # Return both rendered HTML and the base URL for resolving relative paths
        base_url = f"file://{template_path.absolute()}/"
        return rendered, base_url


# Initialize template manager
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
template_manager = TemplateManager(TEMPLATES_DIR)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Nothing to see here."}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/templates")
async def list_templates():
    """
    List all available templates.

    Returns:
        JSON object containing list of available template names

    Raises:
        HTTPException: If error occurs while listing templates
    """
    try:
        templates = template_manager.list_templates()
        return {"templates": templates, "count": len(templates)}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error listing templates: {str(e)}"
        )


@app.get("/generate/{template_name}/")
async def get_template_schema(template_name: str):
    """
    Get the required payload structure for a specific template.

    Args:
        template_name: Name of the template

    Returns:
        JSON object containing required fields and payload structure

    Raises:
        HTTPException: If template not found or schema cannot be retrieved
    """
    try:
        schema = template_manager.get_template_schema(template_name)
        return schema

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except AttributeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving schema: {str(e)}"
        )


@app.post("/generate")
async def generate_document(request: DocumentRequest):
    """
    Generate a PDF document based on the specified template and payload.

    Args:
        request: DocumentRequest containing template name and payload

    Returns:
        PDF document as bytes

    Raises:
        HTTPException: If validation fails or document generation fails
    """
    try:
        # Validate the payload
        template_manager.validate_payload(request.template, request.payload)

        # Render the HTML template
        html_content, base_url = template_manager.render_template(
            request.template, request.payload
        )

        # Get stylesheets for this template
        stylesheets = template_manager.get_stylesheets(request.template)

        # Generate PDF using WeasyPrint with stylesheets and base_url for resolving relative paths
        from weasyprint import CSS

        pdf_bytes = HTML(string=html_content, base_url=base_url).write_pdf(
            stylesheets=[CSS(filename=css_file) for css_file in stylesheets]
        )

        # Return PDF as response
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={request.template}.pdf"
            },
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        # Check if it's a ValidationError from the validator
        if e.__class__.__name__ == "ValidationError":
            raise HTTPException(status_code=400, detail=str(e))

        # Other errors
        raise HTTPException(
            status_code=500, detail=f"Error generating document: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
