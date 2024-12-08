import sqlite3

def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS bonus(bonus VARCHAR, value TEXT, nationId VARCHAR, startYear DATE, endYear DATE, event TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS nation(nationName TEXT, population INTEGER, id VARCHAR, gdp INTEGER, popGrowth FLOAT, gdpGrowth FLOAT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS tech(techName TEXT, techType TEXT, techTemplate TEXT, yearDesigned DATE, yearInService DATE, nationID VARCHAR)")
        conn.commit()
    except sqlite3.Error as e:
        errorHandler(e) 

def insert_bonus(conn, bonus, value, nationId, startYear, endYear, event):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bonus (bonus, value, nationId, startYear, endYear, event) VALUES (?, ?, ?, ?, ?, ?)", 
                    (bonus, value, nationId, startYear, endYear, event))
        conn.commit()
    except sqlite3.Error as e:
        errorHandler(e) 

def read_bonus(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bonus")
        return cursor.fetchall()
    except sqlite3.Error as e:
            errorHandler(e)

def update_bonus(conn, bonus, value, nationId, startYear, endYear, event):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE bonus SET value = ?, nationId = ?, startYear = ?, endYear = ?, event = ? WHERE bonus = ?", 
                       (value, nationId, startYear, endYear, event, bonus))
        conn.commit()
    except sqlite3.Error as e:
        errorHandler(e)

def delete_bonus(conn, bonus):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bonus WHERE bonus = ?", (bonus,))
        conn.commit()
    except sqlite3.Error:
        errorHandler(sqlite3.errcode())

def errorHandler(e):
    print("An error occurred:", e.args[0])
    
try:
    with sqlite3.connect('mysql.db.bot-hosting.net:3306') as conn:
        create_tables(conn)
        # Example CRUD operations
        insert_bonus(conn, 'Holiday Bonus', '1000', 'USA', '2023-01-01', '2023-12-31', 'New Year')
        bonuses = read_bonus(conn)
        print("Bonuses:", bonuses)
        update_bonus(conn, 'Holiday Bonus', '1500', 'USA', '2023-01-01', '2023-12-31', 'New Year')
        bonuses = read_bonus(conn)
        print("Updated Bonuses:", bonuses)
        delete_bonus(conn, 'Holiday Bonus')
        bonuses = read_bonus(conn)
        print("Bonuses after deletion:", bonuses)
except sqlite3.OperationalError as e:
    print("Failed to open database:", e)