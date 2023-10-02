# Google Calandar Events Syncing Locally

## Introduction

This repository contains a Python script designed to synchronize Google Calendar events for the current month with a local SQLite database. The script utilizes the Google Calendar API to fetch events and stores them in a local SQLite database for efficient querying. The primary functionality of the code involves checking for events whose date and time match the current system time. When such an event is identified, the script triggers an alert, displaying the event details, and utilizes text-to-speech synthesis to audibly announce the event.

## Key Features:

1. **Google Calendar Integration:**
   - Utilizes the Google Calendar API to retrieve events for the current month.

2. **SQLite Database:**
   - Stores fetched events locally in an SQLite database for quick and efficient querying.

3. **Event Matching:**
   - Regularly checks for events whose date and time match the current system time.

4. **Alert Display:**
   - Displays an alert with detailed information when a matching event is found.

5. **Text-to-Speech Synthesis:**
   - Utilizes a text-to-speech library to audibly announce the details of the matching event.

## Usage:

1. **Google Calendar API Setup:**
   - Configure and obtain API credentials to access the Google Calendar API.

2. **SQLite Database Setup:**
   - Set up the SQLite database to store and manage events locally.

3. **Dependencies Installation:**
   - Install necessary Python dependencies, including the Google API client library and text-to-speech synthesis library.

4. **Run the Script:**
   - Execute the Python script to initiate the synchronization and event checking process.

Note: Ensure proper handling of API credentials, and follow any specific setup instructions provided in the repository. Customize the script according to your preferences, such as adjusting the alert mechanism or incorporating additional features.

Disclaimer: Keep in mind that interacting with external services like Google Calendar may involve privacy and security considerations. Always handle sensitive information and credentials with care, and review and adhere to relevant API usage policies.

## Installation
- pip install -r requirements.txt

## Envoirment Activation
- If you haven't created a virtual environment yet, you might want to do that first. Here's a recap of the steps:
    # On Windows
    python -m venv venv

    # On macOS/Linux
    python3 -m venv venv

- Activate the virtual environment:
 # On Windows:
   venv\Scripts\activate
 # On macOS/Linux
   source venv/bin/activate


