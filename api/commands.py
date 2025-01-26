import sys
import os
from datetime import datetime, timezone

import time 
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import discord
from discord.ext import commands
import statsdb.dbscript as db
from timeModule.timeflow import update_date
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

def my_roles(ctx, which_role):
    roles = [role.name for role in ctx.author.roles]
    return which_role in roles

async def send_response(ctx, message, ephemeral=False):
    if isinstance(ctx, discord.Interaction):
        await ctx.response.send_message(message, ephemeral=ephemeral)
    else:
        await ctx.send(message, ephemeral=ephemeral)

@bot.hybrid_command(name='read_bonus', description='Read bonuses of a nation from the database. Leave nation field blank to get list of all nations')
async def read_bonus_command(ctx, nation_name: str = None):
    conn = db.create_conn()
    try:
        if nation_name is None:
            bonuses = db.read_bonus(conn)
        else:
            nation = db.read_nation(conn, nation_name)
            bonuses = db.read_bonus(conn, nation)
        formatted_bonuses = []
        if bonuses == None:
            await send_response(ctx, "No bonuses found for the specified nation.", ephemeral=False)
            return
        for bonus in bonuses:
            formatted_bonuses.append(
                f"**ID:** {bonus[0]}\n"
                f"**Nation:** {nation}\n"
                f"**Bonus:** {bonus[2]}\n"
                f"**Value:** {bonus[3]}\n"
                f"**Type:** {bonus[4]}\n"
                f"**Start Year:** {bonus[5]}\n"
                f"**End Year:** {bonus[6]}\n"
                f"**Event Link:** {bonus[7] if bonus[7] is not None else 'N/A'}\n"
                "-----------------------------"
            )
        
        response_message = "\n".join(formatted_bonuses)
        await send_response(ctx, response_message, ephemeral=False)
    except Exception as e:
        await send_response(ctx, f"An error occurred: {e}", ephemeral=False)
    finally:
        conn.close()

@bot.hybrid_command(name='read_all_nation', description='read every nation')
async def read_all_nation_command(ctx):
    conn = db.create_conn()
    try:
        nations = db.read_nation(conn)
        formatted_nations = []
        for nation in nations:
            formatted_nations.append(
                f"**ID:** {nation[0]}\n"
                f"**Name:** {nation[1]}\n"
                f"**Population:** {nation[2]}\n"
                f"**GDP:** {nation[3]}\n"
                f"**Population growth:** {nation[4]}\n"
                f"**GDP growth:** {nation[5]}\n"
                "-----------------------------"
            )
        
        response_message = "\n".join(formatted_nations)
        await send_response(ctx, response_message, ephemeral=False)
        
    except Exception as e:
        await send_response(ctx,f"An error occurred: {e}")
    finally:
        conn.close()

@bot.hybrid_command(name='read_one_nation', description='Read a single nation by nation name')
async def read_nation_command(ctx, nation_name: str):
    conn = db.create_conn()
    try:
        nation = db.read_nation(conn,nation_name)
        if nation:
            response_message = (
                f"**ID:** {nation[0]}\n"
                f"**Name:** {nation[1]}\n"
                f"**Population:** {nation[2]}\n"
                f"**GDP:** {nation[3]}\n"
                f"**Population growth:** {nation[4]}\n"
                f"**GDP growth:** {nation[5]}\n"
                "-----------------------------"
            )
        await send_response(ctx, response_message, ephemeral=False)
            
    except Exception as e:
        await send_response(ctx,f"An error occurred: {e}")
    finally:
        conn.close()
@bot.hybrid_command(name='read_all_tech', description='read entire tech database')
async def read_tech_command(ctx):
    conn = db.create_conn()
    try:
        techs = db.read_tech(conn)
        formatted_techs = []
        for tech in techs:
            formatted_techs.append(
                f"**Tech ID:** {tech[0]}\n"
                f"**Tech Name:** {tech[1]}\n"
                f"**Tech Type:** {tech[2]}\n"
                f"**Tech Template:** {tech[3]}\n"
                f"**Year Designed:** {tech[4]}\n"
                f"**Year In Service:** {tech[5]}\n"
                f"**Nation ID:** {tech[6]}\n"
                "-----------------------------"
            )
        
        response_message = "\n".join(formatted_techs)
        await send_response(ctx, response_message, ephemeral=True)

    except Exception as e:
        await send_response(ctx,f"An error occurred: {e}")
    finally:
        conn.close()
   
@bot.hybrid_command(name='read_one_tech', description='read techs of one nation')
async def read_one_tech_command(ctx, nation: str):
    conn = db.create_conn()
    try:
        techs = db.read_tech(conn,nation)
        if techs:
            formatted_techs = []
            for tech in techs:
                formatted_techs.append(
                    f"**Tech ID:** {tech[0]}\n"
                    f"**Tech Name:** {tech[1]}\n"
                    f"**Tech Type:** {tech[2]}\n"
                    f"**Tech Template:** {tech[3]}\n"
                    f"**Year Designed:** {tech[4]}\n"
                    f"**Year In Service:** {tech[5]}\n"
                    f"**Nation ID:** {tech[6]}\n"
                    "-----------------------------"
                )
            
            response_message = "\n".join(formatted_techs)
            await send_response(ctx, response_message, ephemeral=False)

    except Exception as e:
        await send_response(ctx,f"An error occurred: {e}")
    finally:
        conn.close()

@bot.hybrid_command(name='insert_bonus', description='Insert a bonus into the database')
async def insert_bonus_command(ctx, bonus: str, value: str, nation_name: str, start_year: str, end_year: str, event: str = None):  
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.insert_bonus(conn, bonus, value, nation_name, start_year, end_year, event)
            await send_response(ctx, f"Bonus '{bonus}' inserted successfully.", ephemeral=False)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='update_bonus', description='Update a bonus in the database')
async def update_bonus_command(ctx, id: int, bonus: str, value: str, nation_name: str, start_year: str, end_year: str, event: str = None):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.update_bonus(conn, id, bonus, value, start_year, end_year, event)
            await send_response(ctx, f"Bonus '{bonus}' updated successfully.", ephemeral=False)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='delete_bonus', description='Delete a bonus from the database')
async def delete_bonus_command(ctx, id: int):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.delete_bonus(conn, id)
            await send_response(ctx, f"Bonus '{id}' deleted successfully.", ephemeral=False)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)
    
@bot.hybrid_command(name='insert_nation', description='Insert a nation into the database')
async def insert_nation_command(ctx, nation_name: str, population: int, gdp: int, pop_growth: float, gdp_growth: float):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.insert_nation(conn, nation_name, population, gdp, pop_growth, gdp_growth)
            await send_response(ctx, f"Nation '{nation_name}' inserted successfully.", ephemeral=False)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='update_nation', description='Update a nation in the database')
async def update_nation_command(ctx, nation_name: str, population: int, gdp: int, pop_growth: float, gdp_growth: float):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.update_nation(conn, nation_name, population, gdp, pop_growth, gdp_growth)
            await send_response(ctx, f"Nation '{nation_name}' updated successfully.", ephemeral=False)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='delete_nation', description='Delete a nation from the database')
async def delete_nation_command(ctx, nation_name: str):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.delete_nation(conn, nation_name)
            await send_response(ctx, f"Nation '{nation_name}' deleted successfully.", ephemeral=False)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='insert_tech', description='Insert a tech into the database')
async def insert_tech_command(ctx, tech_name: str, tech_type: str, tech_template: str, year_designed: str, year_in_service: str, nation_name: str):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.insert_tech(conn, tech_name, tech_type, tech_template, year_designed, year_in_service, nation_name)
            await send_response(ctx, f"Tech '{tech_name}' inserted successfully.", ephemeral=False)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='update_tech', description='Update a tech in the database')
async def update_tech_command(ctx, tech_id: int, tech_name: str, tech_type: str, tech_template: str, year_designed: str, year_in_service: str, nation_name: str):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.update_tech(conn, tech_id, tech_name, tech_type, tech_template, year_designed, year_in_service, nation_name)
            await send_response(ctx, f"Tech '{tech_name}' updated successfully.", ephemeral=False)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='delete_tech', description='Delete a tech from the database')
async def delete_tech_command(ctx, tech_name: str):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.delete_tech(conn, tech_name)
            await send_response(ctx, f"Tech '{tech_name}' deleted successfully.", ephemeral=False)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='update_time')
async def insert_bonus_command(start_time: str, multiplier: int):
    update_date(start_time, multiplier)

@bot.event
async def on_message(message):
    if message.author.id == 1101035453710348339 and message.channel.id == 1326666766616625213:
        if message.embeds:
            for embed in message.embeds:
                for field in embed.fields:
                    timestamp_pattern = r'<t:(-?\d+):F>'
                    match = re.search(timestamp_pattern, field.value)
                    if match:
                        timestamp = float(match.group(1))
                        t = time.time()
                        date = datetime.fromtimestamp(timestamp)
                        print (date.year)
                        adjust_population_and_gdp(date.year)
    else:
        print ("Not Zukis message")

def adjust_population_and_gdp(year):
    conn = db.create_conn()
    nations = db.read_nation(conn)
    for nation in nations:
        bonuses = db.read_bonus(conn, nation[1])
        for bonus in bonuses:
            if bonus[5] <= year <= bonus[6]:
                if bonus[4] == 'population':
                    nation[2] += bonus[3]
                elif bonus[4] == 'gdp':
                    nation[3] += bonus[3]
                elif bonus[4] == 'gdp growth':
                    nation[3] *= (1+bonus[3]/100)
                elif bonus[4] == 'pop growth':
                    nation[2] *= (1+bonus[3]/100)
            db.update_nation(conn, nation[1], nation[2], nation[3], nation[4], nation[5])

discord_token = os.getenv('DISCORD_TOKEN')
if discord_token is None:
    raise ValueError("DISCORD_TOKEN environment variable not set")
bot.run(os.getenv('DISCORD_TOKEN'))