# escriba

Project status: Beta

Escriba is an API to generate PDF documents with whatever is needed. This project can work
standalone but it's also part of the Hecate ecosystem.

Escriba provides clean defaults. This softare does not make decisions for you,
it's meant for people or companies that need custom-tailored documents in
an easy way without using or paying external services.

# Features

* Sane defaults, this project is not opinionated
* Self-contained templates, each template has its own payload, HTML, CSS, fonts, images, validator, etc.
* Hot loading of templates! Just drop a new one and ask the API to use it!
* Payload validation

# How does it work?

The API has the following endpoints:

* GET `templates/` - Will return a list of the available templates
* GET `generate/<template_name>/` - Will return the necessary payload to use in the template and what fields are required
* POST `generate/` - With the payload, it will generate the PDF of the requested template

# Why not more functionality? A frontend? Forms? XYZ?

This is intended as a _tool_, tools don't decide for you, they only provide you the best way to use them.

If you can't figure out a use case for this, let's go with an example:

I'm a company that has plenty of documents and I want to integrate this application.
I've already developed the templates and now I want to integrate this into my systems.

The easiest implementation would be to create a section in whatever software you want that:

* Requests the list of templates available and shows it as buttons to generate each document

Once the user clicks one of those buttons, your software can go and ask Escriba:

* Hey, give me the necessary payload for this template.

Once it gets the payload two things can happen. The easiest is to tie the response
to some Javascript code and generate a form on the fly that the user can fill in.

The other is to elaborate the interaction a bit more and make your Javascript ask
your platforms for data and prepopulate part of the form, saving the user quite some time.

# Output mechanisms

This is out of the scope of this project. This project just generates PDF documents. There
is another system planned in the Hecate ecosystem that will handle outputs (PDF, printing, physical letters, etc.)

# Creating a template from scratch

Creating a template is really easy, create a folder and inside create the following files:

* `validator.py` - Contains a pydantic v2 model that defines the payload
* `template.html` - Just a regular old jinja2 template
* `styles.css` - Just a regular CSS file
* Any other file that you may need (images, fonts, other CSS files...)

There is a full example implementation in the `templates/example_template` folder.
It should be fairly easy to follow. The test file is in `tests/test_example_template.py`

# Running the project

Since this project is unopinionated, There are many ways of running it

## Local / Development / Fast

We use `uv` to handle the virtual environment and the dependencies, Thanks to
that you can just do:

```
$ uv run main.py
```

## Docker

At the time of writing there is not docker implementation yet.

## Running the tests

```
$ uv run tests/test_example_template.py
```

# Contributions

The guidelines to contribute to this project are in the CONTRIBUTING.md file

# License

Lareira Digital believes strongly in free software and open source, and as such
we've decided to democratize tooling for companies that want or need to use
it, this involves creating some of those tools from scratch to avoid collisions with
already existing commercial solutions.

As such, the whole Hecate ecosystem and services (which Escriba belongs to)
are licensed MIT License.