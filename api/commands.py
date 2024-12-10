import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import discord
from discord import Intents
from discord.ext import commands
import statsdb.dbscript as db
from timeModule.timeflow import update_date
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command(name='insert_bonus')
async def insert_bonus_command(ctx, bonus: str, value: str, nationId: str, startYear: str, endYear: str, event: str):
    conn = db.create_conn()
    try:
        db.insert_bonus(conn, bonus, value, nationId, startYear, endYear, event)
        await ctx.send(f"Bonus '{bonus}' inserted successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()

@bot.command(name='read_bonus')
async def read_bonus_command(ctx):
    conn = db.create_conn()
    try:
        bonuses = db.read_bonus(conn)
        await ctx.send(f"Bonuses: {bonuses}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()

@bot.command(name='update_bonus')
async def update_bonus_command(ctx, bonus: str, value: str, nationId: str, startYear: str, endYear: str, event: str):
    conn = db.create_conn()
    try:
        db.update_bonus(conn, bonus, value, nationId, startYear, endYear, event)
        await ctx.send(f"Bonus '{bonus}' updated successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()

@bot.command(name='delete_bonus')
async def delete_bonus_command(ctx, bonus: str):
    conn = db.create_conn()
    try:
        db.delete_bonus(conn, bonus)
        await ctx.send(f"Bonus '{bonus}' deleted successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()
        
@bot.command(name='insert_nation')
async def insert_nation_command(ctx, nationName: str, population: int, gdp: int, popGrowth: float, gdpGrowth: float):
    conn = db.create_conn()
    try:
        db.insert_nation(conn, nationName, population, gdp, popGrowth, gdpGrowth)
        await ctx.send(f"Nation '{nationName}' inserted successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()

@bot.command(name='read_nation')
async def read_nation_command(ctx):
    conn = db.create_conn()
    try:
        nations = db.read_nation(conn)
        await ctx.send(f"Nations: {nations}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()

@bot.command(name='update_nation')
async def update_nation_command(ctx, nationId: int, nationName: str, population: int, gdp: int, popGrowth: float, gdpGrowth: float):
    conn = db.create_conn()
    try:
        db.update_nation(conn, nationId, nationName, population, gdp, popGrowth, gdpGrowth)
        await ctx.send(f"Nation '{nationName}' updated successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()

@bot.command(name='delete_nation')
async def delete_nation_command(ctx, nationId: int):
    conn = db.create_conn()
    try:
        db.delete_nation(conn, nationId)
        await ctx.send(f"Nation '{nationId}' deleted successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()

@bot.command(name='insert_tech')
async def insert_tech_command(ctx, techName: str, techType: str, techTemplate: str, yearDesigned: str, yearInService: str, nationID: int):
    conn = db.create_conn()
    try:
        db.insert_tech(conn, techName, techType, techTemplate, yearDesigned, yearInService, nationID)
        await ctx.send(f"Tech '{techName}' inserted successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()

@bot.command(name='read_tech')
async def read_tech_command(ctx):
    conn = db.create_conn()
    try:
        techs = db.read_tech(conn)
        await ctx.send(f"Techs: {techs}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()

@bot.command(name='update_tech')
async def update_tech_command(ctx, techId: int, techName: str, techType: str, techTemplate: str, yearDesigned: str, yearInService: str, nationID: int):
    conn = db.create_conn()
    try:
        db.update_tech(conn, techId, techName, techType, techTemplate, yearDesigned, yearInService, nationID)
        await ctx.send(f"Tech '{techName}' updated successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()

@bot.command(name='delete_tech')
async def delete_tech_command(ctx, techId: int):
    conn = db.create_conn()
    try:
        db.delete_tech(conn, techId)
        await ctx.send(f"Tech '{techId}' deleted successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()

@bot.command(name='update_time')
async def insert_bonus_command(startTime: str, multiplier: int):
    update_date(startTime, multiplier)

discord_token = os.getenv('DISCORD_TOKEN')
if discord_token is None:
    raise ValueError("DISCORD_TOKEN environment variable not set")
bot.run(os.getenv('DISCORD_TOKEN'))