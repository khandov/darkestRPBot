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
                nationName TEXT UNIQUE,
                population INTEGER,
                gdp INTEGER,
                popGrowth FLOAT,
                gdpGrowth FLOAT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bonus (
                bonusId INT AUTO_INCREMENT PRIMARY KEY,
                bonusName TEXT UNIQUE,
                bonus VARCHAR(255),
                value TEXT,
                nationId INT,
                startYear DATE,
                endYear DATE,
                post TEXT,
                FOREIGN KEY (nationId) REFERENCES nation(nationId)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tech (
                techId INT AUTO_INCREMENT PRIMARY KEY,
                techName TEXT UNIQUE,
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

def read_nation(conn, nation=None):
    if(nation == None):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM nation")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM nation WHERE nationName = %s", (nation,))
            result = cursor.fetchone()
            if result:
                nationId, nationName, population, gdp, popGrowth, gdpGrowth = result
                return {"nationId": nationId, "nationName": nationName, "population": population, "gdp": gdp, "popGrowth": popGrowth, "gdpGrowth": gdpGrowth}
            else: 
                return None
        except Exception as e:
            print(f"Error: {e}")


def update_nation(conn, nationName, population, gdp, popGrowth, gdpGrowth):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE nation
            SET nationName = %s, population = %s, gdp = %s, popGrowth = %s, gdpGrowth = %s
            WHERE nationName = %s
        """, (nationName, population, gdp, popGrowth, gdpGrowth, nationName))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def delete_nation(conn, nationName):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM nation WHERE nationName = %s", (nationName,))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

# CRUD functions for the tech table
def insert_tech(conn, techName, techType, techTemplate, yearDesigned, yearInService, nationName: None):
    try:
        cursor = conn.cursor()
        if nationName is None:
            print(f"Error: Nation '{nationName}' not found.")
            return
        nation = read_nation(conn, nationName)
        cursor.execute("""
            INSERT INTO tech (techName, techType, techTemplate, yearDesigned, yearInService, nationId)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (techName, techType, techTemplate, yearDesigned, yearInService, nation['nationId']))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def read_tech(conn,nation=None):
    if (nation == None):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tech")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tech WHERE nationName = %s", (nation,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error: {e}")

def update_tech(conn, techName, techType, techTemplate, yearDesigned, yearInService, nationName):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tech
            SET techName = %s, techType = %s, techTemplate = %s, yearDesigned = %s, yearInService = %s, nationName = %s
            WHERE techName = %s
        """, (techName, techType, techTemplate, yearDesigned, yearInService, nationName))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def delete_tech(conn, techName):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tech WHERE techId = %s", (techName,))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def insert_bonus(conn, bonus, value, nationName: None, startYear, endYear, post):
    try:
        cursor = conn.cursor()
        if nationName is None:
            print(f"Error: Nation '{nationName}' not found.")
            return
        nation = read_nation(conn, nationName)
        if nation['nationId']:
            cursor.execute("""
                INSERT INTO bonus (bonus, value, nationId, startYear, endYear, post)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (bonus, value, nation['nationId'], startYear, endYear, post))
            conn.commit()
        else :
            print(f"Error: Name '{nationName}' is invalid.")
    except Exception as e:
        print(f"Error: {e}")

def read_bonus(conn, nationName=None):
    if(nationName == None):
        print("No nation specified")
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bonus WHERE nationId = %s", (nationName,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")

def update_bonus(conn, bonusName, bonusType, value, startYear, endYear, event):
    try:
        cursor = conn.cursor()
        bonus = bonusName
        cursor.execute("""
            UPDATE bonus
            SET bonusName = %s, bonusType = %s, value = %s, startYear = %s, endYear = %s, event = %s
            WHERE bonus = %s
        """, (bonusName, bonusType, value, startYear, endYear, event, bonus))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

def delete_bonus(conn, bonusName):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bonus WHERE bonusName = %s", (bonusName,))
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
            insert_tech(conn, "F-22", "Fighter", "Stealth", "2005-01-01", "2005-01-01", "USA")
            insert_tech(conn, "J-20", "Fighter", "Stealth", "2011-01-01", "2011-01-01", "China")
            insert_bonus(conn, "GDP", "-1000000", "USA", "2021-01-01", "2021-12-31", "Covid-19")
            insert_bonus(conn, "Population", "-1000000", "USA", "2021-01-01", "2021-12-31", "Covid-19")
            insert_bonus(conn, "GDP", "-1000000", "China", "2021-01-01", "2021-12-31", "Covid-19")
            insert_bonus(conn, "Population", "-2000000", "China", "2021-01-01", "2021-12-31", "Covid-19")
            print(read_bonus(conn))
            print(read_nation(conn))
            print(read_tech(conn))


    except Exception as e:
        print("Failed to open database:",e)