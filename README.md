## Wahl Analyse

The query API has to be turned on and running in the background in order for the analysis and voting websites to work.
The API provides JSON data to the frontend which then displays it.

## Usage query API (for now):

`python3 -m uvicorn query_api:app --reload`

## Usage Website:

In the project directory, you can run:

`npm start`

Runs the app in the development mode.

Open http://localhost:3000 to view it in the browser.

The page will reload if you make edits.
