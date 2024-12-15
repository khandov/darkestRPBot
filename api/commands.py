import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import discord
from discord.ext import commands
import statsdb.dbscript as db
from timeModule.timeflow import update_date
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

def my_roles(roles, which_role):
    roles = [role.name for role in roles]
    return which_role in roles

async def send_response(ctx, message, ephemeral=False):
    if isinstance(ctx, discord.Interaction):
        await ctx.response.send_message(message, ephemeral=ephemeral)
    else:
        await ctx.send(message, ephemeral=ephemeral)


@bot.hybrid_command(name='insert_bonus', description='Insert a bonus into the database')
async def insert_bonus_command(ctx, bonus: str, value: str, nationName: str, startYear: str, endYear: str, event: str = None):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.insert_bonus(conn, bonus, value, nationName, startYear, endYear, event)
            await send_response(ctx, f"Bonus '{bonus}' inserted successfully.", ephemeral=True)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='read_bonus', description='Read bonuses of a nation from the database. Leave nation field blank to get list of all nations')
async def read_bonus_command(ctx, nation: str = None):
    conn = db.create_conn()
    try:
        if nation is None:
            bonuses = db.read_bonus(conn)
            await send_response(ctx, f"Bonuses: {bonuses}", ephemeral=True)
        else:
            bonuses = db.read_bonus(conn, nation)
            await send_response(ctx, f"Bonuses of {nation}: {bonuses}", ephemeral=True)
    except Exception as e:
        await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
    finally:
        conn.close()

@bot.hybrid_command(name='update_bonus', description='Update a bonus in the database')
async def update_bonus_command(ctx, bonus: str, value: str, nationName: str, startYear: str, endYear: str, event: str = None):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.update_bonus(conn, bonus, value, nationName, startYear, endYear, event)
            await send_response(ctx, f"Bonus '{bonus}' updated successfully.", ephemeral=True)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='delete_bonus', description='Delete a bonus from the database')
async def delete_bonus_command(ctx, bonusName: str):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.delete_bonus(conn, bonusName)
            await send_response(ctx, f"Bonus '{bonusName}' deleted successfully.", ephemeral=True)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='read_all_nation', description='read every nation')
async def read_all_nation_command(ctx):
    conn = db.create_conn()
    try:
        nations = db.read_nation(conn)
        await send_response(ctx,f"Nations: {nations}", ephemeral=True)
    except Exception as e:
        await send_response(ctx,f"An error occurred: {e}")
    finally:
        conn.close()

@bot.hybrid_command(name='read_one_nation', description='read a single nation by nation name')
async def read_nation_command(ctx, nationName: str):
    conn = db.create_conn()
    try:
        nation = db.read_nation(conn,nationName)
        await send_response(ctx,f"Nation: {nation}", ephemeral=True)
    except Exception as e:
        await send_response(ctx,f"An error occurred: {e}")
    finally:
        conn.close()
    
@bot.hybrid_command(name='insert_nation', description='Insert a nation into the database')
async def insert_nation_command(ctx, nationName: str, population: int, gdp: int, popGrowth: float, gdpGrowth: float):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.insert_nation(conn, nationName, population, gdp, popGrowth, gdpGrowth)
            await send_response(ctx, f"Nation '{nationName}' inserted successfully.", ephemeral=True)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='update_nation', description='Update a nation in the database')
async def update_nation_command(ctx, nationId: int, nationName: str, population: int, gdp: int, popGrowth: float, gdpGrowth: float):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.update_nation(conn, nationId, nationName, population, gdp, popGrowth, gdpGrowth)
            await send_response(ctx, f"Nation '{nationName}' updated successfully.", ephemeral=True)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='delete_nation', description='Delete a nation from the database')
async def delete_nation_command(ctx, nationName: str):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.delete_nation(conn, nationName)
            await send_response(ctx, f"Nation '{nationName}' deleted successfully.", ephemeral=True)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='read_all_tech', description='read entire tech database')
async def read_tech_command(ctx):
    conn = db.create_conn()
    try:
        techs = db.read_tech(conn)
        await send_response(ctx,f"Techs: {techs}")
    except Exception as e:
        await send_response(ctx,f"An error occurred: {e}")
    finally:
        conn.close()
   
@bot.hybrid_command(name='read_one_tech', description='read techs of one nation')
async def read_one_tech_command(ctx, nation: str):
    conn = db.create_conn()
    try:
        techs = db.read_tech(conn,nation)
        await send_response(ctx,f"Techs of {nation}: {techs}")
    except Exception as e:
        await send_response(ctx,f"An error occurred: {e}")
    finally:
        conn.close()

@bot.hybrid_command(name='insert_tech', description='Insert a tech into the database')
async def insert_tech_command(ctx, techName: str, techType: str, techTemplate: str, yearDesigned: str, yearInService: str, nationName: str):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.insert_tech(conn, techName, techType, techTemplate, yearDesigned, yearInService, nationName)
            await send_response(ctx, f"Tech '{techName}' inserted successfully.", ephemeral=True)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='update_tech', description='Update a tech in the database')
async def update_tech_command(ctx, techId: int, techName: str, techType: str, techTemplate: str, yearDesigned: str, yearInService: str):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.update_tech(conn, techId, techName, techType, techTemplate, yearDesigned, yearInService)
            await send_response(ctx, f"Tech '{techName}' updated successfully.", ephemeral=True)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.hybrid_command(name='delete_tech', description='Delete a tech from the database')
async def delete_tech_command(ctx, techName: str):
    if my_roles(ctx, "Gamemaster"):
        conn = db.create_conn()
        try:
            db.delete_tech(conn, techName)
            await send_response(ctx, f"Tech '{techName}' deleted successfully.", ephemeral=True)
        except Exception as e:
            await send_response(ctx, f"An error occurred: {e}", ephemeral=True)
        finally:
            conn.close()
    else:
        await send_response(ctx, "You do not have the required role to perform this action. You need 'Gamemaster' role.", ephemeral=True)

@bot.command(name='update_time')
async def insert_bonus_command(startTime: str, multiplier: int):
    update_date(startTime, multiplier)

discord_token = os.getenv('DISCORD_TOKEN')
if discord_token is None:
    raise ValueError("DISCORD_TOKEN environment variable not set")
bot.run(os.getenv('DISCORD_TOKEN'))