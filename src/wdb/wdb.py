import os
import sqlite3
import numpy
from wmath import distribution

DATABASE_DIR = "data/transition-db"
DEFAULT_EXTENSION = ".sqlite3"

def euclidean_distance_inverse_squared(a, b):
    """Calculate 1/(the norm of (a-b))^2.
    
    @param a: a numpy array
    @param b: a numpy array of the same dimension as a
    @return: 1/(norm(a-b)^2)
    """
    zero_division_defense = 1e-9 * min(numpy.linalg.norm(a), numpy.linalg.norm(b))
    
    return 1.0/(zero_division_defense + (numpy.linalg.norm(a-b))**2)

def create_database(database_name, database_dir=DATABASE_DIR, database_extension=DEFAULT_EXTENSION, number_of_parameters=2):
    db_file = os.path.join(database_dir, database_name + database_extension)
    
    if os.path.exists(db_file):
        raise IOError("File already exists: %s" % db_file)
    
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
    
    con = sqlite3.connect(db_file)
    
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
    
    con.commit()
    
    print "Successfully created database " + db_file + "."

def create_database_if_not_exists(database_name, database_dir=DATABASE_DIR, database_extension=DEFAULT_EXTENSION, number_of_parameters=2):
    db_file = os.path.join(database_dir, database_name + database_extension)

    if not os.path.exists(db_file):
        create_database(database_name, number_of_parameters=number_of_parameters)

def delete_database(database_name, database_dir=DATABASE_DIR, database_extension=DEFAULT_EXTENSION):
    db_file = os.path.join(database_dir, database_name + database_extension)
    
    if os.path.exists(db_file):
        print "Deleting database", db_file
        os.remove(db_file)
        print "Database", db_file, "deleted."
    else:
        print "Did not delete database: file %s does not exist." % db_file

class StateTransitionDatabase:
    def __init__(self, db_name):
        
        db_file = os.path.join(DATABASE_DIR, db_name + DEFAULT_EXTENSION)
        self.__con = sqlite3.connect(db_file)
        
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
        '''Add a new transition to the database.
        @param from_state: A numpy array describing a state before transition. Must be of type float.
        @param from_state: A numpy array describing a state after transition. Must be of type float.
        '''
        cur = self.__get_cursor()
        cur.execute(self.__insert_query, self.combine_transition(from_state, to_state))
        self.__con.commit()
    
    def get_transitions(self):
        """Return all transitions in the database."""
        cur = self.__get_cursor()
        cur.execute("SELECT * FROM transitions;")
        
        return numpy.array(cur.fetchall())
    
    def combine_transition(self, from_state, to_state):
        """Combine the two given states into a transition row."""
        return numpy.concatenate((from_state, to_state))
    
    def split_transition(self, transition):
        """Split the given transition row into its two state parts.
        
        If transition is a matrix, splits the rows of the matrix and returns the two ("left" and "right") parts of the matrix.
        
        @param transition: A numpy array to split
        @return: The provided transition split in half as two numpy arrays
        @see: function numpy.hsplit
        """
        return numpy.hsplit(transition, 2)
    
    def sample_weighted_random(self, prev_particle, weight_function=euclidean_distance_inverse_squared):
        """Generate a new particle by taking a random one from the database.
        
        For each transition t in the database, a weight w[t] is calculated
        using the provided function as w[t] = weight_function(prev_particle,
        t.from). The returned particle is a randomly chosen element of
        {t.to for t in database}, weighted according to {w[t]}.
        
        @param prev_particle: the particle using which to create new particles
        @param weight_function: a function to use for weighting database
            entries. Will be called as weight_function(prev_particle, t) where
            t is the "from" part of a transition in the database.
        @return: A randomly chosen "to" part of a transition in the database.
        """
        from_states, to_states = self.split_transition(self.get_transitions())
        
        weights = numpy.zeros((from_states.shape[0], 1))
        for i in xrange(from_states.shape[0]):
            weights[i] = weight_function(prev_particle, from_states[i,:])
        
        weights = weights/sum(weights)
        
        dist = distribution(weights)
        
        return numpy.array(dist.sample(sample_set=to_states))
    
    def sample_weighted_average(self, prev_particle, weight_function=euclidean_distance_inverse_squared):
        """Generate a particle by taking the average of the database.
        
        For each transition t in the database, a weight w[t] is calculated
        using the provided function as w[t] = weight_function(prev_particle,
        t.from). The returned particle is the average of {t.from for t in
        database} with the weights {w[t]}.
        
        @param prev_particle: the particle using which to create new particles
        @param weight_function: a function to use for weighting database
            entries. Will be called as weight_function(prev_particle, t) where
            t is the "from" part of a transition in the database.
        @return: A weighted average of the database as a new particle 
        """
        from_states, to_states = self.split_transition(self.get_transitions())
        
        weights = numpy.zeros((from_states.shape[0]))
        for i in xrange(from_states.shape[0]):
            weights[i] = weight_function(prev_particle, from_states[i,:])

        weights = weights/sum(weights)
        
        return numpy.average(to_states, axis=0, weights=weights)
