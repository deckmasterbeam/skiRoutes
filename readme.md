<h1>Ski Routes</h1>

<h2>Monorepo layout</h2>

This repo uses a simple monorepo structure:

- `frontend/` = Vite + React UI
- `backend/` = Flask API + SQLite

Run commands from repo root with scoped scripts:

- `npm run dev:frontend`
- `npm run dev:backend`
- `npm run test:backend`

Notes:

- Flask database path is anchored to `backend/users.db`, so it stays consistent no matter which directory you run from.
- For Vercel backend deploys, target the backend folder (`vercel deploy backend ...`).

This project can currently take a user's submission and a route and show which waypoints from the route that the user hit.

This project is intended to be vibe code forward to learn more about working with AI agents.

Usage:

- define candidate_user_submission_filename pointing to a file name in testUserSubmissions

    - Ex: `candidate_user_submission_filename = os.path.join(project_root, 'testUserSubmissions', '3-23-2026-MissionRidge-Josh.gpx')`

- define target_route pointing to a file name in routes

    - Ex: `ctarget_route = os.path.join(project_root, 'routes', 'testRoute.gpx')`

- run `validateUserSubmissionAgainstRoute.py`


<h2>Goals:</h2>

1. (DONE) validate and present which waypoints from a route are hit by a user's submission

    - (TODO) validate that the user submission is genuine, they haven't just turned a route file into a submission file

    - (TODO) make this validation a CLI tool


2. (TODO) User submissions tied to a user account

3. (TODO) Routes have leaderboards that display users according to completion and time taken to complete

4. (TODO) User submitted routes

<h2>Dev notes:</h2>

1. How to visualize a .gpx file:

    Go to https://gpx.studio/app and load the file

2. How to generate a roue file:

    Go to https://gpx.studio/app and generate waypoints. No strict structure, just needs waypoints with lat and lon
