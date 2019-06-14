# Events API

## Setup

### Prerequisites

Python version >= 3.6 is required. Using `virtualenv` is advised.

1. Install requirements

   `pip install -r requirements.txt`

2. Initialise database

   `python init_db.py` (uncomment `add_events()` in `main` block to insert some sample data)

3. Run the app

   `python events.py`

### Running

This app requires a PostgreSQL database instance running on port `5432` (can be changed in `settings.py`)

The easiest way to do it is by running Docker:

`docker run -d -p 5432:5432 postgres:11`

### Tests

To run tests you need a PostgreSQL database running and available on port `5433` (can be changed in `settings.py`)

To set it up using Docker, just run `create_test_db.sh`

To run tests simply run

`pytest`

To run tests with coverage, run

`pytest --cov`

## Shortcomings

The app is currently configured to run in a `DEBUG` mode. To run on production, some adjustments are necessary.
