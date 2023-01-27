## Wahl Analyse

The query API has to be turned on and running in the background in order for the analysis and voting websites to work.
The API provides JSON data to the frontend which then displays it.

## Running the setup

Run the `run_setup.sh <hostname> <port> <name> <user> <password>` script - This will create the tables in the postgres database,
load the csv's, run the algorithm for calculating the Bundestag seating, and create token tables.

## Entering the generated erststimmen/zweitstimmen

In order to generate the votes, and fill the tables with the erstimmen/zweitstimmen, run the python script:
`python3 stimmzettelgenerator.py <hostname> <port> <name> <user> <password>`

## Usage query API (for now):

`python3 -m uvicorn query_api:app --reload`

## Usage Website:

In the project directory, you can run:

`npm start`

Runs the app in the development mode.

Open http://localhost:3000 to view it in the browser.

The page will reload if you make edits.
