import time
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
discord_bot_token = os.getenv('DISCORD_TOKEN')
discord_client_id = os.getenv('APP_ID')
def update_global_commands():
    commands_to_update = [
        {
            "name": "insert_bonus",
            "description": "Insert a bonus into the database",
            "options": [
                {
                    "name": "bonus",
                    "description": "The type of bonus",
                    "type": 3,  # STRING
                    "required": True,
                    "choices": [
                        {
                            "name": "population",
                            "value": "population"
                        },
                        {
                            "name": "gdp",
                            "value": "gdp"
                        },
                        {
                            "name": "population growth",
                            "value": "pop growth"
                        },
                        {
                            "name": "gdp growth",
                            "value": "gdp growth"
                        }
                    ]
                },
                {
                    "name": "value",
                    "description": "The value of the bonus. If for growth, treat it as a percentage, e.g. 5 for 5%",
                    "type": 4,  # INTEGER
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
                    "name": "nation_name",
                    "description": "The name of the nation",
                    "type": 3,  # STRING
                    "required": True
                }
            ]
        },
        {
            "name": "update_bonus",
            "description": "Update a bonus in the database",
            "options": [
                {
                    "name": "id",
                    "description": "The unique id of the bonus",
                    "type": 4,  # INTEGER
                    "required": True
                },
                {
                    "name": "bonus",
                    "description": "The value of the bonus. If for growth, treat it as a percentage, e.g. 5 for 5%",
                    "type": 3,  # STRING
                    "required": False,
                    "choices": [
                        {
                            "name": "population",
                            "value": "population"
                        },
                        {
                            "name": "gdp",
                            "value": "gdp"
                        },
                        {
                            "name": "population growth",
                            "value": "population growth"
                        },
                        {
                            "name": "gdp growth",
                            "value": "gdp growth"
                        }
                    ]
                },
                {
                    "name": "value",
                    "description": "The value of the bonus",
                    "type": 4,  # INTEGER
                    "required": False
                },
                {
                    "name": "nation_name",
                    "description": "The name of the nation",
                    "type": 3,  # STRING
                    "required": False
                },
                {
                    "name": "start_year",
                    "description": "The start year of the bonus",
                    "type": 3,  # STRING
                    "required": False
                },
                {
                    "name": "end_year",
                    "description": "The end year of the bonus",
                    "type": 3,  # STRING
                    "required": False
                },
                {
                    "name": "event",
                    "description": "The event associated with the bonus",
                    "type": 3,  # STRING
                    "required": False
                }
            ]
        }
    ]
    # Fetch the list of global commands
    headers = {
    'Authorization': f'Bot {discord_bot_token}',
    'Content-Type': 'application/json'
    }
    # URL to fetch global commands
    fetch_url = f'https://discord.com/api/v10/applications/{discord_client_id}/commands'

    response = requests.get(fetch_url, headers=headers)
    print(f'sending to "{fetch_url}"')
    if response.status_code == 200:
        commands = response.json()
        for command in commands:
            command_name = command['name']
            command_id = command['id']
            
            # Check if the command is present in the JSON object for updates
            if command_name in commands_to_update:
                update_url = f'https://discord.com/api/v10/applications/{discord_client_id}/commands/{command_id}'
                update_data = commands_to_update[command_name]
                
                # Send a request to update the command
                update_response = requests.patch(update_url, headers=headers, json=update_data)
                
                if update_response.status_code == 201:
                    print(f'Command "{command_name}" updated successfully')
                else:
                    print(f'Failed to update command "{command_name}": {update_response.status_code} - {update_response.text}')
    else:
        print(f'Failed to fetch commands: {response.status_code} - {response.text}')
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
                    "description": "The type of bonus. For growths: value of 5 means 5%)",
                    "type": 3,  # STRING
                    "required": True,
                    "choices": [
                        {
                            "name": "population",
                            "value": "population"
                        },
                        {
                            "name": "gdp",
                            "value": "gdp"
                        },
                        {
                            "name": "population growth",
                            "value": "population growth"
                        },
                        {
                            "name": "gdp growth",
                            "value": "gdp growth"
                        }
                    ]
                },
                {
                    "name": "value",
                    "description": "The value of the bonus",
                    "type": 3,  # STRING
                    "required": True
                },
                {
                    "name": "nation_name",
                    "description": "The name of the nation to be given bonus",
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
                    "description": "The event causing the bonus. Either leave blank or post discord link",
                    "type": 3,  # STRING
                    "required": False
                }
            ]
        },
        {
            "name": "read_bonus",
            "description": "Read bonuses of a nation from the database.",
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
            "name": "update_bonus",
            "description": "Update a bonus in the database. Use bonus ID to point which bonus to edit.",
            "options": [
                {
                    "name": "id",
                    "description": "The unique id of the bonus",
                    "type": 4,  # INTEGER
                    "required": True
                },
                {
                    "name": "bonus",
                    "description": "The name of the bonus",
                    "type": 3,  # STRING
                    "required": False
                },
                {
                    "name": "value",
                    "description": "The value of the bonus",
                    "type": 3,  # STRING
                    "required": False
                },
                {
                    "name": "nation_name",
                    "description": "The name of the nation",
                    "type": 3,  # STRING
                    "required": False
                },
                {
                    "name": "start_year",
                    "description": "The start year of the bonus",
                    "type": 3,  # STRING
                    "required": False
                },
                {
                    "name": "end_year",
                    "description": "The end year of the bonus",
                    "type": 3,  # STRING
                    "required": False
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
            "name": "insert_nation",
            "description": "Insert a nation into the database.",
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
            "description": "Update a nation in the database. Nation is identified by nation_name.",
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
                    "required": False
                },
                {
                    "name": "gdp",
                    "description": "The GDP of the nation",
                    "type": 4,  # INTEGER
                    "required": False
                },
                {
                    "name": "pop_growth",
                    "description": "The population growth rate of the nation",
                    "type": 10,  # FLOAT
                    "required": False
                },
                {
                    "name": "gdp_growth",
                    "description": "The GDP growth rate of the nation",
                    "type": 10,  # FLOAT
                    "required": False
                }
            ]
        },
        {
            "name": "delete_nation",
            "description": "Delete a nation from the database, referenced by nation_name.",
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
            "description": "Insert a tech into the database. Refer to tech owner by nation_name.",
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
                    "description": "The template of the tech. Should be discord link to template post",
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
            "description": "Update a tech in the database. Refer to ID of tech to update.",
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
                    "required": False
                },
                {
                    "name": "tech_type",
                    "description": "The type of the tech",
                    "type": 3,  # STRING
                    "required": False
                },
                {
                    "name": "tech_template",
                    "description": "The template of the tech",
                    "type": 3,  # STRING
                    "required": False
                },
                {
                    "name": "year_designed",
                    "description": "The year the tech was designed",
                    "type": 3,  # STRING
                    "required": False
                },
                {
                    "name": "year_in_service",
                    "description": "The year the tech went into service",
                    "type": 3,  # STRING
                    "required": False
                },
                {
                    "name": "nation_name",
                    "description": "The nation that owns the tech",
                    "type": 3,  # STRING
                    "required": False
                }
            ]
        },
        {
            "name": "delete_tech",
            "description": "Delete a tech from the database. Refer to tech_name as identifier",
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
            "description": "Read techs owned by one nation",
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
            "description": "List all existing nations",
            "options": []
        },
        {
            "name": "read_one_nation",
            "description": "Read a nation by nation name",
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
        response = requests.put(url, headers=headers, json=command)
        if response.status_code == 200:
            print(f"Successfully registered command: {command['name']}")
        else:
            print(f"Failed to register command: {command['name']}. Response: {response.text}")
        time.sleep(4)
def update_new_commands():
    commands = {
        "name": "read_bonus",
        "description": "Read bonuses of a nation from the database.",
        "options": [
            {
                "name": "nation_name",
                "description": "The name of the nation",
                "type": 3,  # STRING
                "required": True
            }
        ]
    }
    url = f"https://discord.com/api/v10/applications/{discord_client_id}/commands"
    headers = {
        "Authorization": f"Bot {discord_bot_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=commands)
    if response.status_code == 200:
        print(f"Successfully registered command: {commands['name']}")
    else:
        print(f"Failed to register command: {commands['name']}. Response: {response.text}")

update_new_commands()