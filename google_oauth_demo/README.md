# Google OAuth Demo

This is a minimal Google OAuth example with a backend in Python/Flask and a simple frontend.

## What it does

- uses Google Sign-In with OAuth 2.0
- stores user identity in a server-side session
- protects a `/profile` page behind authentication
- keeps the Google client secret on the backend

## Files

- `app.py` — Flask web app and OAuth flow
- `templates/index.html` — main landing page
- `templates/profile.html` — protected authenticated page
- `requirements.txt` — Python dependencies

## Setup

1. Install dependencies:

```bash
python -m pip install -r google_oauth_demo/requirements.txt
```

2. Create environment variables:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `FLASK_SECRET_KEY`

Example (PowerShell):

```powershell
$env:GOOGLE_CLIENT_ID = "your-client-id"
$env:GOOGLE_CLIENT_SECRET = "your-client-secret"
$env:FLASK_SECRET_KEY = "a-random-secret-for-sessions"
python google_oauth_demo/app.py
```

## Running locally

1. Start the app:

```bash
python google_oauth_demo/app.py
```

2. Open `http://localhost:5000`
3. Click **Sign in with Google**
4. After authorization, you will see your authenticated profile page

## Google Cloud Console setup

1. Go to https://console.cloud.google.com/
2. Create a new project or select an existing one
3. Open **APIs & Services** > **OAuth consent screen**
   - Select **External** if you are testing with your own Google account
   - Add an app name and support email
   - Add `http://localhost:5000` to the authorized domains if required
   - Save the consent screen configuration
4. Open **APIs & Services** > **Credentials**
   - Click **Create Credentials** > **OAuth client ID**
   - Choose **Web application**
   - Name it `Local Flask Google OAuth`
   - Add `http://localhost:5000/auth/callback` under **Authorized redirect URIs**
   - Save and copy the **Client ID** and **Client Secret**

## Notes

- Keep `GOOGLE_CLIENT_SECRET` private. Do not commit it to source control.
- This app is a good starting point for learning how OAuth works.
- If you want a hosted auth service later, you can move to Firebase Auth or Auth0.

## Josh Notes

- py -m pip install <something>