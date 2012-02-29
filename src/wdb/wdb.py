import sqlite3

def createDatabase(database_path = "../../data/transition-db/wdb.db", number_of_parameters = 2):
    con = sqlite3.connect(database_path)
    
    cur = con.cursor()
    
    createStateTableQuery = "CREATE TABLE states(id INTEGER PRIMARY KEY"
    for i in range(number_of_parameters):
        createStateTableQuery += ", theta"+str(i)+" REAL NOT NULL"
    createStateTableQuery += ");"
    
    cur.execute("PRAGMA foreign_keys = ON;");
    cur.execute(createStateTableQuery);
    cur.execute("CREATE TABLE transitions(" +
                "transitionId INTEGER PRIMARY KEY, " +
                "fromState INTEGER NOT NULL, " +
                "toState INTEGER NOT NULL, " +
                "FOREIGN KEY(fromState) REFERENCES states(id), " +
                "FOREIGN KEY(toState) REFERENCES states(id));")
    
    print("Successfully created database " + database_path + ".")
