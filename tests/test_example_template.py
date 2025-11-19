"""Test for example_template - Conference Event Program.

This test showcases all capabilities of the templating system.
"""

import sys
from pathlib import Path

# Add parent directory to path to import from main
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import template_manager


def test_example_template():
    """Generate a comprehensive example conference program PDF."""

    payload = {
        "template": "example_template",
        "payload": {
            # Optional document metadata
            "document_title": "TechConf 2025 Program",
            "document_security_level": "Public",
            "document_creation_date": "2025-01-15",

            # Event details
            "event_name": "TechConf 2025: Future of AI & Cloud Computing",
            "event_date": "March 15-17, 2025",
            "event_location": "San Francisco Convention Center, CA",
            "event_description": "Join us for three days of cutting-edge technology discussions, hands-on workshops, and networking with industry leaders. TechConf brings together innovators, developers, and tech enthusiasts from around the world.",

            # Optional event details
            "registration_url": "https://techconf2025.example.com/register",
            "contact_email": "info@techconf2025.example.com",
            "max_attendees": 500,

            # Speakers array
            "speakers": [
                {
                    "name": "Dr. Sarah Chen",
                    "title": "Chief AI Officer",
                    "company": "DataMind Technologies",
                    "bio": "Dr. Chen is a pioneer in machine learning with over 15 years of experience. She holds a PhD from MIT and has published 50+ papers on neural networks and deep learning.",
                    "email": "sarah.chen@datamind.example.com"
                },
                {
                    "name": "Marcus Johnson",
                    "title": "VP of Cloud Architecture",
                    "company": "CloudScale Systems",
                    "bio": "Marcus leads cloud infrastructure teams and has architected systems handling billions of requests daily. Former principal engineer at major tech companies.",
                    "email": "marcus.j@cloudscale.example.com"
                },
                {
                    "name": "Elena Rodriguez",
                    "title": "Security Researcher",
                    "company": "CyberGuard Institute",
                    "bio": "Elena specializes in cybersecurity and ethical hacking. She has discovered critical vulnerabilities in major platforms and advocates for secure software development practices."
                },
                {
                    "name": "Dr. James Park",
                    "title": "Quantum Computing Lead",
                    "company": "QuantumLeap Labs",
                    "bio": "Dr. Park works at the intersection of quantum computing and practical applications. He is developing algorithms for quantum advantage in optimization problems."
                }
            ],

            # Sessions array
            "sessions": [
                {
                    "time": "09:00 - 10:00",
                    "title": "The Future of Artificial Intelligence",
                    "speaker_name": "Dr. Sarah Chen",
                    "location": "Main Hall",
                    "duration_minutes": 60,
                    "description": "Explore the latest developments in AI, from large language models to autonomous systems. Understand the implications for businesses and society.",
                    "is_keynote": True
                },
                {
                    "time": "10:30 - 11:30",
                    "title": "Building Scalable Cloud Infrastructure",
                    "speaker_name": "Marcus Johnson",
                    "location": "Room A",
                    "duration_minutes": 60,
                    "description": "Learn architectural patterns for designing systems that scale from thousands to millions of users.",
                    "is_keynote": False
                },
                {
                    "time": "10:30 - 11:30",
                    "title": "Cybersecurity in the Modern Era",
                    "speaker_name": "Elena Rodriguez",
                    "location": "Room B",
                    "duration_minutes": 60,
                    "description": "Discover the latest threat vectors and defense strategies. Includes real-world case studies of security incidents.",
                    "is_keynote": False
                },
                {
                    "time": "13:00 - 14:00",
                    "title": "Quantum Computing: From Theory to Practice",
                    "speaker_name": "Dr. James Park",
                    "location": "Main Hall",
                    "duration_minutes": 60,
                    "description": "Demystify quantum computing and learn about current capabilities and near-term applications.",
                    "is_keynote": False
                },
                {
                    "time": "14:30 - 15:30",
                    "title": "AI Ethics and Responsible Development",
                    "speaker_name": "Dr. Sarah Chen",
                    "location": "Room A",
                    "duration_minutes": 60,
                    "description": "Panel discussion on ethical considerations in AI development, bias mitigation, and responsible deployment.",
                    "is_keynote": False
                },
                {
                    "time": "16:00 - 17:00",
                    "title": "Closing Keynote: Technology for Good",
                    "speaker_name": "Marcus Johnson",
                    "location": "Main Hall",
                    "duration_minutes": 60,
                    "description": "Inspiring stories of how technology is solving global challenges and creating positive impact.",
                    "is_keynote": True
                }
            ],

            # Optional sponsors array
            "sponsors": [
                {
                    "name": "DataMind Technologies",
                    "level": "Gold",
                    "website": "https://datamind.example.com"
                },
                {
                    "name": "CloudScale Systems",
                    "level": "Gold",
                    "website": "https://cloudscale.example.com"
                },
                {
                    "name": "CyberGuard Institute",
                    "level": "Silver",
                    "website": "https://cyberguard.example.com"
                },
                {
                    "name": "QuantumLeap Labs",
                    "level": "Silver"
                },
                {
                    "name": "TechStartup Inc",
                    "level": "Bronze",
                    "website": "https://techstartup.example.com"
                },
                {
                    "name": "InnovateCorp",
                    "level": "Bronze",
                    "website": "https://innovatecorp.example.com"
                }
            ],

            # Optional sections
            "special_notes": "Please arrive 30 minutes early for registration. Lunch will be provided on all three days. A networking reception will follow each day's sessions.",
            "wifi_ssid": "TechConf2025",
            "wifi_password": "Innovation2025!"
        }
    }

    # Validate payload
    template_manager.validate_payload(
        payload["template"],
        payload["payload"]
    )

    # Render template
    html_content, base_url = template_manager.render_template(
        payload["template"],
        payload["payload"]
    )

    # Generate PDF
    from weasyprint import HTML, CSS
    stylesheets = template_manager.get_stylesheets(payload["template"])

    pdf_bytes = HTML(string=html_content, base_url=base_url).write_pdf(
        stylesheets=[CSS(filename=css_file) for css_file in stylesheets]
    )

    # Save to file
    output_path = Path(__file__).parent / "output_example_template.pdf"
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)

    print(f"✓ PDF generated successfully: {output_path}")
    print(f"  File size: {len(pdf_bytes):,} bytes")


if __name__ == "__main__":
    test_example_template()
