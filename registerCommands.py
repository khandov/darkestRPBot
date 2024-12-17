import time
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
discord_bot_token = os.getenv('DISCORD_TOKEN')
discord_client_id = os.getenv('APP_ID')
def register_global_commands():
    url = f"https://discord.com/api/v10/applications/{discord_client_id}/commands"
    headers = {
        "Authorization": f"Bot {discord_bot_token}",
        "Content-Type": "application/json"
    }

    commands = [
        {
            "name": "insert_bonus",
            "description": "Insert a bonus into the database",
            "options": [
                {
                    "name": "bonus",
                    "description": "The name of the bonus",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "value",
                    "description": "The value of the bonus",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "nation_name",
                    "description": "The name of the nation",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "start_year",
                    "description": "The start year of the bonus",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "end_year",
                    "description": "The end year of the bonus",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "event",
                    "description": "The event associated with the bonus",
                    "type": 3,  # STRING
                    "required": False
                }
            ]
        },
        {
            "name": "read_bonus",
            "description": "Read bonuses of a nation from the database. Leave nation field blank to get list of all nations",
            "options": [
                {
                    "name": "nation",
                    "description": "The name of the nation",
                    "type": 3,  # STRING
                    "required": False
                }
            ]
        },
        {
            "name": "update_bonus",
            "description": "Update a bonus in the database",
            "options": [
                {
                    "name": "bonus",
                    "description": "The name of the bonus",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "value",
                    "description": "The value of the bonus",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "nation_name",
                    "description": "The name of the nation",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "start_year",
                    "description": "The start year of the bonus",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "end_year",
                    "description": "The end year of the bonus",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "event",
                    "description": "The event associated with the bonus",
                    "type": 3,  # STRING
                    "required": False
                }
            ]
        },
        {
            "name": "delete_bonus",
            "description": "Delete a bonus from the database",
            "options": [
                {
                    "name": "bonus",
                    "description": "The name of the bonus",
                    "type": 3,  # STRING
                    "required": True
                }
            ]
        },
        {
            "name": "insert_nation",
            "description": "Insert a nation into the database",
            "options": [
                {
                    "name": "nation_name",
                    "description": "The name of the nation",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "population",
                    "description": "The population of the nation",
                    "type": 4,  # INTEGER
                    "required": True
                },
                {
                    "name": "gdp",
                    "description": "The GDP of the nation",
                    "type": 4,  # INTEGER
                    "required": True
                },
                {
                    "name": "pop_growth",
                    "description": "The population growth rate of the nation",
                    "type": 10,  # FLOAT
                    "required": True
                },
                {
                    "name": "gdp_growth",
                    "description": "The GDP growth rate of the nation",
                    "type": 10,  # FLOAT
                    "required": True
                }
            ]
        },
        {
            "name": "update_nation",
            "description": "Update a nation in the database",
            "options": [
                {
                    "name": "nation_name",
                    "description": "The name of the nation",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "population",
                    "description": "The population of the nation",
                    "type": 4,  # INTEGER
                    "required": True
                },
                {
                    "name": "gdp",
                    "description": "The GDP of the nation",
                    "type": 4,  # INTEGER
                    "required": True
                },
                {
                    "name": "pop_growth",
                    "description": "The population growth rate of the nation",
                    "type": 10,  # FLOAT
                    "required": True
                },
                {
                    "name": "gdp_growth",
                    "description": "The GDP growth rate of the nation",
                    "type": 10,  # FLOAT
                    "required": True
                }
            ]
        },
        {
            "name": "delete_nation",
            "description": "Delete a nation from the database",
            "options": [
                {
                    "name": "nation_name",
                    "description": "The name of the nation",
                    "type": 3,  # STRING
                    "required": True
                }
            ]
        },
        {
            "name": "insert_tech",
            "description": "Insert a tech into the database",
            "options": [
                {
                    "name": "tech_name",
                    "description": "The name of the tech",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "tech_type",
                    "description": "The type of the tech",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "tech_template",
                    "description": "The template of the tech",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "year_designed",
                    "description": "The year the tech was designed",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "year_in_service",
                    "description": "The year the tech went into service",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "nation_name",
                    "description": "The name of the nation",
                    "type": 3,  # STRING
                    "required": True
                }
            ]
        },
        {
            "name": "update_tech",
            "description": "Update a tech in the database",
            "options": [
                {
                    "name": "tech_id",
                    "description": "The ID of the tech",
                    "type": 4,  # INTEGER
                    "required": True
                },
                {
                    "name": "tech_name",
                    "description": "The name of the tech",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "tech_type",
                    "description": "The type of the tech",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "tech_template",
                    "description": "The template of the tech",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "year_designed",
                    "description": "The year the tech was designed",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "year_in_service",
                    "description": "The year the tech went into service",
                    "type": 3,  # STRING
                    "required": True
                }
            ]
        },
        {
            "name": "delete_tech",
            "description": "Delete a tech from the database",
            "options": [
                {
                    "name": "tech_name",
                    "description": "The name of the tech",
                    "type": 3,  # STRING
                    "required": True
                }
            ]
        },
        {
            "name": "read_all_tech",
            "description": "Read entire tech database",
            "options": []
        },
        {
            "name": "read_one_tech",
            "description": "Read techs of one nation",
            "options": [
                {
                    "name": "nation",
                    "description": "The name of the nation",
                    "type": 3,  # STRING
                    "required": True
                }
            ]
        },
        {
            "name": "read_all_nation",
            "description": "Read every nation",
            "options": []
        },
        {
            "name": "read_one_nation",
            "description": "Read a single nation by nation name",
            "options": [
                {
                    "name": "nation_name",
                    "description": "The name of the nation",
                    "type": 3,  # STRING
                    "required": True
                }
            ]
        },
        {
            "name": "update_time",
            "description": "Update the time in the database",
            "options": [
                {
                    "name": "start_time",
                    "description": "The start time",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "multiplier",
                    "description": "The time multiplier",
                    "type": 4,  # INTEGER
                    "required": True
                }
            ]
        }
    ]

    for command in commands:
        response = requests.post(url, headers=headers, json=command)
        if response.status_code == 201:
            print(f"Successfully registered command: {command['name']}")
        else:
            print(f"Failed to register command: {command['name']}. Response: {response.text}")
        time.sleep(5)
if __name__ == "__main__":
    register_global_commands()