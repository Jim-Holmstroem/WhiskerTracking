import os
import sqlite3

def create_database(database_path = "data/transition-db/wdb.db", number_of_parameters = 2):
    con = sqlite3.connect(database_path)
    
    cur = con.cursor()
    
    createStateTableQuery = "CREATE TABLE states(id INTEGER PRIMARY KEY"
    for i in range(number_of_parameters):
        createStateTableQuery += ", theta"+str(i)+" REAL NOT NULL"
    createStateTableQuery += ");"
    
    cur.execute("PRAGMA foreign_keys = ON;");
    cur.execute(createStateTableQuery);
    cur.execute("CREATE TABLE transitions(" +
                "id INTEGER PRIMARY KEY, " +
                "fromState INTEGER NOT NULL, " +
                "toState INTEGER NOT NULL, " +
                "FOREIGN KEY(fromState) REFERENCES states(id), " +
                "FOREIGN KEY(toState) REFERENCES states(id));")
    
    print("Successfully created database " + database_path + ".")

class StateTransitionDatabase:
    def __init__(self, database="data/transition-db/wdb.db"):
        self.__con = sqlite3.connect(database)
        self.__con.execute("PRAGMA foreign_keys = ON;")
    
    def add_state(self, state):
        '''
        @param state: A numpy array to insert into the database. Must be of type float.
        @return: The ID of the inserted state 
        '''
        cur = self.__con.cursor()
        
        insertQuery = "INSERT INTO states VALUES(NULL"
        for i in xrange(len(state)):
            insertQuery += ", ?"
        insertQuery += ");"
        
        cur.execute(insertQuery, state)
        self.__con.commit()
        
        return cur.lastrowid
    
    def add_transition(self, from_state_id, to_state_id):
        cur = self.__con.cursor()
        
        cur.execute("INSERT INTO transitions(fromState, toState) VALUES(?, ?);", (from_state_id, to_state_id))
        self.__con.commit()
        
        return cur.lastrowid

if __name__ == "__main__":
    create_database()
