"""Validator for example_template - Conference Event Program.

This template showcases all capabilities of the templating system:
- Nested objects (speakers, sessions, sponsors)
- Optional fields
- Union types (string/int/float)
- Boolean fields
- Arrays with complex objects
- Conditional rendering
"""

from typing import List, Union
from pydantic import BaseModel, Field


class Speaker(BaseModel):
    """Model for a conference speaker."""
    name: str = Field(..., min_length=1, description="Speaker's full name")
    title: str = Field(..., min_length=1, description="Speaker's job title")
    company: str = Field(..., min_length=1, description="Speaker's company/organization")
    bio: str = Field(default="", description="Speaker biography (optional)")
    email: str = Field(default="", description="Contact email (optional)")


class Session(BaseModel):
    """Model for a conference session."""
    time: str = Field(..., min_length=1, description="Session time (e.g., '09:00 - 10:00')")
    title: str = Field(..., min_length=1, description="Session title")
    speaker_name: str = Field(..., min_length=1, description="Name of the speaker")
    location: str = Field(..., min_length=1, description="Room/location name")
    duration_minutes: int = Field(..., gt=0, description="Session duration in minutes")
    description: str = Field(default="", description="Session description (optional)")
    is_keynote: bool = Field(default=False, description="Whether this is a keynote session")


class Sponsor(BaseModel):
    """Model for an event sponsor."""
    name: str = Field(..., min_length=1, description="Sponsor company name")
    level: str = Field(..., min_length=1, description="Sponsorship level (e.g., Gold, Silver, Bronze)")
    website: str = Field(default="", description="Sponsor website URL (optional)")


class PayloadModel(BaseModel):
    """Pydantic model for example_template payload."""

    # Optional document metadata
    document_title: str = Field(default="", description="Document title (optional)")
    document_security_level: str = Field(default="", description="Security classification (optional)")
    document_creation_date: str = Field(default="", description="Creation date (optional)")

    # Event details
    event_name: str = Field(..., min_length=1, description="Name of the conference/event")
    event_date: str = Field(..., min_length=1, description="Event date or date range")
    event_location: str = Field(..., min_length=1, description="Event venue/location")
    event_description: str = Field(..., min_length=1, description="Brief description of the event")

    # Optional event details
    registration_url: str = Field(default="", description="Registration URL (optional)")
    contact_email: str = Field(default="", description="Contact email (optional)")
    max_attendees: Union[str, int] = Field(default="", description="Maximum number of attendees (optional)")

    # Complex nested arrays
    speakers: List[Speaker] = Field(..., min_length=1, description="List of speakers")
    sessions: List[Session] = Field(..., min_length=1, description="List of conference sessions")
    sponsors: List[Sponsor] = Field(default=[], description="List of sponsors (optional)")

    # Optional sections
    special_notes: str = Field(default="", description="Special notes or instructions (optional)")
    wifi_ssid: str = Field(default="", description="WiFi network name (optional)")
    wifi_password: str = Field(default="", description="WiFi password (optional)")


def validate_payload(payload: dict) -> None:
    """
    Validate the payload using Pydantic model.

    Args:
        payload: Dictionary containing the event data

    Raises:
        Exception: If validation fails
    """
    try:
        PayloadModel(**payload)
    except Exception as e:
        raise Exception(f"Validation failed for example_template: {str(e)}") from e
