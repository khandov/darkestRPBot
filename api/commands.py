import discord
from discord.ext import commands
import sqlite3
from db.dbscript import *
from time.timeflow import update_date
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
bot = commands.Bot(command_prefix='/')

@bot.command(name='insert_bonus')
async def insert_bonus_command(ctx, bonus: str, value: str, nationId: str, startYear: str, endYear: str, event: str):
    conn = sqlite3.connect(':memory:')
    try:
        insert_bonus(conn, bonus, value, nationId, startYear, endYear, event)
        await ctx.send(f"Bonus '{bonus}' inserted successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()

@bot.command(name='read_bonus')
async def read_bonus_command(ctx):
    conn = sqlite3.connect(':memory:')
    try:
        bonuses = read_bonus(conn)
        await ctx.send(f"Bonuses: {bonuses}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()

@bot.command(name='update_bonus')
async def update_bonus_command(ctx, bonus: str, value: str, nationId: str, startYear: str, endYear: str, event: str):
    conn = sqlite3.connect(':memory:')
    try:
        update_bonus(conn, bonus, value, nationId, startYear, endYear, event)
        await ctx.send(f"Bonus '{bonus}' updated successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()

@bot.command(name='delete_bonus')
async def delete_bonus_command(ctx, bonus: str):
    conn = sqlite3.connect(':memory:')
    try:
        delete_bonus(conn, bonus)
        await ctx.send(f"Bonus '{bonus}' deleted successfully.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
    finally:
        conn.close()

@bot.command(name='update_time')
async def insert_bonus_command(startTime: str, multiplier: int):
    update_date(startTime, multiplier)

bot.run(os.getenv('DISCORD_TOKEN'))