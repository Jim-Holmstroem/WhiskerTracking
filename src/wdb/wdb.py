import os
import sqlite3
import numpy

def create_database(database_path = "data/transition-db/wdb.db", number_of_parameters = 2):
    con = sqlite3.connect(database_path)
    
    cur = con.cursor()
    
    cur.execute("CREATE TABLE metadata(number_of_parameters INTEGER NOT NULL);")
    cur.execute("INSERT INTO metadata VALUES(?);", [number_of_parameters])
    
    parameter_name = "theta_"
    column_type = " FLOAT NOT NULL"
    createTransitionsTableQuery = "CREATE TABLE transitions("
    
    for prefix in ("from_", "to_"):
        for i in xrange(number_of_parameters):
            createTransitionsTableQuery += (prefix + parameter_name + str(i) + column_type + ", ")
    
    createTransitionsTableQuery = createTransitionsTableQuery[:-2] # Remove the trailing ", "
    createTransitionsTableQuery += (");")
    cur.execute(createTransitionsTableQuery)
    
    print("Successfully created database " + database_path + ".")

class StateTransitionDatabase:
    def __init__(self, database="data/transition-db/wdb.db"):
        self.__con = sqlite3.connect(database)
        self.__con.execute("PRAGMA foreign_keys = ON;")
        
        cursor = self.__get_cursor()
        cursor.execute("SELECT number_of_parameters FROM metadata;")
        metadata_row = cursor.fetchone()
        self.__num_params = metadata_row[0]
        
        self.__insert_query = "INSERT INTO transitions VALUES("
        for i in xrange(self.__num_params*2):
            self.__insert_query += ("?, ")
        self.__insert_query = self.__insert_query[:-2] # Remove the trailing ", "
        self.__insert_query += (");")
    
    def __get_cursor(self):
        return self.__con.cursor()
    
    def add_transition(self, from_state, to_state):
        '''
        @param from_state: A numpy array describing a state before transition. Must be of type float.
        @param from_state: A numpy array describing a state after transition. Must be of type float.
        '''
        cur = self.__get_cursor()
        cur.execute(self.__insert_query, self.combine_transition(from_state, to_state))
        self.__con.commit()
    
    def get_transitions(self):
        """
        Returns all transitions in the database.
        """
        cur = self.__get_cursor()
        cur.execute("SELECT * FROM transitions;")
        
        return numpy.array(cur.fetchall())
    
    def combine_transition(self, from_state, to_state):
        """
        Combines the two given states into a transition row.
        """
        return numpy.concatenate((from_state, to_state))
    
    def split_transition(self, transition):
        """
        Splits the given transition row into its two state parts.
        If transition is a matrix, splits the rows of the matrix and returns the two ("left" and "right") parts of the matrix.
        """
        return numpy.hsplit(transition, 2)
    
if __name__ == "__main__":
    create_database()
