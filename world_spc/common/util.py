# use this file for helper functions common across API
from flask import current_app
from datetime import datetime
import json
import os


def create_mock_payload():
    """
    Helper function for testing purposes. Loads and returns sample JSON
    taken from EIA grid data.
    """
    with open(
            os.path.join(current_app.instance_path, 'mock_raw_grid_data.json')
    ) as json_file:
        mock_payload = json.load(json_file)
    return mock_payload


def create_mock_game_state():
    """
    Helper to test game state interface.
    """
    state = {
        "ppm": 335,
        "currency": 2555,
        "xp": 23560
    }
    species_dict = {
        "fox": {
            "population": 20,
            "status": "OK"
        },
        "bluebird": {
            "population": 11,
            "status": "Struggling"
        },
        "bear": {
            "population": 8,
            "status": "Endangered"
        }
    }
    state.update({'species': species_dict})
    return state


def create_mock_carbon_readout():
    """
    Returns static readout for GUI hero space. For dev purposes
    only.
    """
    data = {}
    data.update({'username': 'ecogamer', 'ppm': 335,
                'co2': 30, 'miles_drive': 23})
    usage_dict = {
        'past24hours': {},
        'past10days': {}
    }
    data.update(usage_dict)
    return data


def format_timestamp(unformatted):
    """
    Takes the timestamp value from the EIA grid data and formats it
    for insertion into MongoDB. Date is separated from time. Time
    stored as integer (0-23) for hour-ending, where 0 corresponds to
    midnight.
    Args: The unformatted timestamp string.
    Yields: A list of the form [date: str, time: int, timezone: str]
    """
    parts = unformatted.split(' ')
    # format date part
    date_part = datetime.strptime(parts[0], '%m/%d/%Y')

    # format time part
    if parts[2] == 'a.m.':
        parts[1] = ' '.join((parts[1], 'AM'))
    else:
        parts[1] = ' '.join((parts[1], 'PM'))
    time_part = datetime.strptime(parts[1], '%I %p')
    formatted = ''.join((date_part.strftime('%Y-%m-%dT'),
                        time_part.strftime('%H:%M:%S')))
    return formatted


if __name__ == "__main__":
    print(create_mock_game_state())
