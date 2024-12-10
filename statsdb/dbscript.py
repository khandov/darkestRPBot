__package__ = "db"

import mysql.connector

def create_conn():
    conn = mysql.connector.connect(
        host='mysql.db.bot-hosting.net',
        port=3306,
        user='u230695_eE0kHIvC39',
        password='iw59b.Sx+Q@j91^AzDEHv9t^',
        database='s230695_dhDB'
    )
    if conn.is_connected():
        return conn

    return None
def drop_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        DROP TABLE IF EXISTS bonus
    """)
    cursor.execute("""
        DROP TABLE IF EXISTS tech
    """)
    cursor.execute("""
        DROP TABLE IF EXISTS nation
    """)
    conn.commit()

def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nation (
                nationId INT AUTO_INCREMENT PRIMARY KEY,
                nationName TEXT,
                population INTEGER,
                gdp INTEGER,
                popGrowth FLOAT,
                gdpGrowth FLOAT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bonus (
                bonusId INT AUTO_INCREMENT PRIMARY KEY,
                bonus VARCHAR(255),
                value TEXT,
                nationId INT,
                startYear DATE,
                endYear DATE,
                event TEXT,
                FOREIGN KEY (nationId) REFERENCES nation(nationId)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tech (
                techId INT AUTO_INCREMENT PRIMARY KEY,
                techName TEXT,
                techType TEXT,
                techTemplate TEXT,
                yearDesigned DATE,
                yearInService DATE,
                nationID INT,
                FOREIGN KEY (nationID) REFERENCES nation(nationId)
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def insert_nation(conn, nationName, population, gdp, popGrowth, gdpGrowth):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO nation (nationName, population, gdp, popGrowth, gdpGrowth)
            VALUES (%s, %s, %s, %s, %s)
        """, (nationName, population, gdp, popGrowth, gdpGrowth))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def read_nation(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nation")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")

def update_nation(conn, nationId, nationName, population, gdp, popGrowth, gdpGrowth):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE nation
            SET nationName = %s, population = %s, gdp = %s, popGrowth = %s, gdpGrowth = %s
            WHERE nationId = %s
        """, (nationName, population, gdp, popGrowth, gdpGrowth, nationId))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def delete_nation(conn, nationId):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM nation WHERE nationId = %s", (nationId,))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

# CRUD functions for the tech table
def insert_tech(conn, techName, techType, techTemplate, yearDesigned, yearInService, nationID):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tech (techName, techType, techTemplate, yearDesigned, yearInService, nationID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (techName, techType, techTemplate, yearDesigned, yearInService, nationID))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def read_tech(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tech")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")

def update_tech(conn, techId, techName, techType, techTemplate, yearDesigned, yearInService, nationID):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tech
            SET techName = %s, techType = %s, techTemplate = %s, yearDesigned = %s, yearInService = %s, nationID = %s
            WHERE techId = %s
        """, (techName, techType, techTemplate, yearDesigned, yearInService, nationID, techId))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def delete_tech(conn, techId):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tech WHERE techId = %s", (techId,))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def insert_bonus(conn, bonus, value, nationId, startYear, endYear, event):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bonus (bonus, value, nationId, startYear, endYear, event)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (bonus, value, nationId, startYear, endYear, event))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def read_bonus(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bonus")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")

def update_bonus(conn, bonus, value, nationId, startYear, endYear, event):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE bonus
            SET value = %s, nationId = %s, startYear = %s, endYear = %s, event = %s
            WHERE bonus = %s
        """, (value, nationId, startYear, endYear, event, bonus))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def delete_bonus(conn, bonus):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bonus WHERE bonus = %s", (bonus,))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")


def errorHandler(place):
    print("At"+ place + " An error occurred:")

def initiate():    
    try:
        with create_conn() as conn:
            drop_tables(conn)
            create_tables(conn)
            insert_nation(conn, "USA", 331002651, 21427700, 0.71, 2.27)
            insert_nation(conn, "China", 1439323776, 14342900, 0.39, 6.1)
            insert_tech(conn, "F-22", "Fighter", "Stealth", "2005-01-01", "2005-01-01", 1)
            insert_tech(conn, "J-20", "Fighter", "Stealth", "2011-01-01", "2011-01-01", 2)
            insert_bonus(conn, "GDP", "-1000000", 1, "2021-01-01", "2021-12-31", "Covid-19")
            insert_bonus(conn, "Population", "-1000000", 1, "2021-01-01", "2021-12-31", "Covid-19")
            insert_bonus(conn, "GDP", "-1000000", 2, "2021-01-01", "2021-12-31", "Covid-19")
            insert_bonus(conn, "Population", "-2000000", 2, "2021-01-01", "2021-12-31", "Covid-19")
            print(read_bonus(conn))
            print(read_nation(conn))
            print(read_tech(conn))


    except Exception as e:
        print("Failed to open database:",e)