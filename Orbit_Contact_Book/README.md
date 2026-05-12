# Orbit Contact Book

Orbit is a complete, fully functional, and modern Contact Book application built with **Python, Streamlit, and SQLite**. It features a clean, minimal UI inspired by SaaS platforms.

## Features

- **Add & Manage Contacts:** Store name, phone, email, address, notes, follow-up dates, and profile images.
- **Modern UI:** Clean card layout with a "Stitch" inspired design, and an alternative Table view.
- **Smart Search:** Easily search your contacts by name or phone number.
- **Relationship Strength Meter:** Visual progress bar indicating contact health.
- **Contact Categories:** Organize contacts into groups like Work, Family, Friends, etc.
- **Favorite System:** Quick toggle to mark your most important contacts.
- **Roast Generator:** A fun feature to generate harmless roasts for your contacts.
- **Profile Image Support:** Upload and store profile pictures (saved directly into the SQLite database as base64).
- **Auto-Generate Dummy Data:** Quickly populate the app with fake contacts for testing.

## Installation

1. Clone or download this repository.
2. Install the dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit application from the root directory:

```bash
streamlit run app.py
```

The app will automatically create the `contacts.db` SQLite database if it doesn't already exist.

## Project Structure

- `app.py`: The main Streamlit frontend application.
- `database.py`: Database initialization and connection management.
- `contact_service.py`: Business logic and database operations (CRUD).
- `requirements.txt`: Python package dependencies.
- `contacts.db`: Automatically generated SQLite database file.

## Screenshots
s
### Home Page
<img src="Screenshots/home-page.png" width="700">

### Add Contact
<img src="Screenshots/add-contact.png" width="700">

### Contact List
<img src="Screenshots/contact-list.png" width="700">
