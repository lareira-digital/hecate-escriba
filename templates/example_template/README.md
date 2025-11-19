# Example Template - Conference Event Program

This template showcases all capabilities of the Escriba templating system.

## Features Demonstrated

### 1. Nested Objects
- **Speakers**: Array of speaker objects with name, title, company, bio, and email
- **Sessions**: Array of session objects with time, location, duration, and keynote flag
- **Sponsors**: Array of sponsor objects with name, level, and website

### 2. Data Types
- **Strings**: Most fields (names, descriptions, dates)
- **Integers**: `duration_minutes`, `max_attendees`
- **Booleans**: `is_keynote` flag for special session styling
- **Union Types**: `max_attendees` accepts string, int, or float

### 3. Optional Fields
- Document metadata (title, security level, creation date)
- Speaker bio and email
- Session description
- Registration URL and contact email
- Sponsors array (can be empty)
- WiFi information
- Special notes

### 4. Conditional Rendering
- Document info header (only shown if any field is present)
- Speaker bio and email (only shown if provided)
- Session descriptions (only shown if provided)
- Entire sponsors section (only shown if sponsors exist)
- WiFi section (only shown if SSID provided)
- Special notes section (only shown if notes provided)
- Footer contact info (only shown if provided)

### 5. Styling Features
- Custom CSS with gradient headers
- Grid layouts for speakers and sponsors
- Responsive table for schedule
- Special styling for keynote sessions (yellow background + badge)
- Sponsor level colors (Gold/Silver/Bronze)
- Page headers and footers via @page rules
- Code styling for WiFi credentials

### 6. Advanced Layout
- Multi-column grids (2 columns for speakers, 3 for sponsors)
- Table with alternating row colors
- Page break avoidance for cards
- Border and background styling
- Conditional CSS classes

## Use Case

This template is perfect for:
- Conference programs
- Event schedules
- Workshop agendas
- Seminar itineraries
- Training session calendars

## Generated Output

The test file generates a comprehensive 2-page PDF with:
- 4 speakers with detailed bios
- 6 sessions including 2 keynotes
- 6 sponsors at different levels
- WiFi information
- Special attendee notes

Check `tests/output_example_template.pdf` to see the result!
