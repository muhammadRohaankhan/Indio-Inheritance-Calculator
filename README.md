# Inheritance Calculator Prototype

This project provides a proof of concept API for calculating intestate inheritance distributions in several U.S. states.  It is built with **FastAPI** and currently includes simplified rules for:

- Texas
- New York
- California
- Florida
- Michigan
- Illinois

The calculator determines how an estate is split among surviving spouses and descendants when no valid will exists.

## Installation

1. Ensure you have **Python 3.11+** installed.
<<<<<<< HEAD
2. Create a virtual environment and install dependencies:
=======
2. Create a virtual environment and install backend dependencies:
>>>>>>> feature-estate-laws

```bash
python -m venv venv
source venv/bin/activate
<<<<<<< HEAD
=======
cd backend
>>>>>>> feature-estate-laws
pip install -r requirements.txt
```

## Running the API

<<<<<<< HEAD
Start the FastAPI server with **uvicorn**:

```bash
uvicorn app:app --reload
```

=======
Start the FastAPI server with **uvicorn** from the `backend` package:

```bash
uvicorn backend.app:app --reload
```

## Frontend

With the server running, navigate to `http://localhost:8000/` in your browser.
FastAPI serves the `frontend` directory so the root URL shows the HTML form.
It submits the required fields to the `/calculate` endpoint and displays the
resulting distribution.

>>>>>>> feature-estate-laws
The `/calculate` endpoint accepts a JSON body matching the `EstateInput` model and returns each heir's share of the estate.

## Example Scenario

Below is the example discussed when planning the project.  Imagine your great‑grandfather lived in **Texas** and passed away without a will.  He had **four children**, and over the years the family has grown to **64 descendants** in total.  To compute each person's share you would construct an input describing the family tree.

A truncated request might look like:

```json
{
  "state": "TX",
  "date_of_death": "2024-01-01",
  "has_will": false,
  "total_estate": 1000000,
  "spouse_exists": false,
  "children_from_previous_marriage": false,
  "community_estate": 500000,
  "children": [
    {"name": "Child1", "is_alive": false, "children": [ {"name": "G1", "is_alive": true, "children": []} ]},
    {"name": "Child2", "is_alive": true,  "children": []},
    {"name": "Child3", "is_alive": true,  "children": []},
    {"name": "Child4", "is_alive": true,  "children": []}
  ],
  "parents_alive": false,
  "siblings_alive": false
}
```

Posting this JSON to `/calculate` will return a mapping of all descendants to their inheritance shares using Texas intestacy rules.  You would expand the `children` arrays to include all remaining generations (up to the 64 current heirs).

## Running Tests

Execute the unit tests with:

```bash
pytest -q
```

All tests should pass and confirm that each state's calculator returns a distribution, stepchildren are excluded, and predeceased branches inherit per stirpes.

