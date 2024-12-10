import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import discord
from discord import Intents
from discord.ext import commands
import db.dbscript as db
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

@bot.command(name='update_time')
async def insert_bonus_command(startTime: str, multiplier: int):
    update_date(startTime, multiplier)

discord_token = os.getenv('DISCORD_TOKEN')
if discord_token is None:
    raise ValueError("DISCORD_TOKEN environment variable not set")
bot.run(os.getenv('DISCORD_TOKEN'))