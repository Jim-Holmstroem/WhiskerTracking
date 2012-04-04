import os
import sqlite3
import numpy
from wmath import distribution

DATABASE_DIR = "data/transition-db"
DEFAULT_EXTENSION = ".sqlite3"
PARAMETER_NAME = "theta_"
PARAMETER_TYPE = "FLOAT NOT NULL"
PREFIXES = ("from_", "to_")

def euclidean_distance_inverse_squared(a, b):
    """UNTESTED Calculate 1/(the norm of (a-b))^2.
    
    @param a: a numpy array
    @param b: a numpy array of the same dimension as a
    @return: 1/(norm(a-b)^2)
    """
    zero_division_defense = 1e-9 * min(numpy.linalg.norm(a), numpy.linalg.norm(b))
    
    return 1.0/(zero_division_defense + (numpy.linalg.norm(a-b))**2)

def create_database(database_name, parameter_groups, database_dir=DATABASE_DIR, database_extension=DEFAULT_EXTENSION):
    db_file = os.path.join(database_dir, database_name + database_extension)
    
    if not isinstance(parameter_groups, (list, tuple)):
        parameter_groups = (parameter_groups,)
    
    if os.path.exists(db_file):
        raise IOError("File already exists: %s" % db_file)
    
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
    
    con = sqlite3.connect(db_file)
    
    con.execute("CREATE TABLE metadata(total_number_of_parameters INTEGER NOT NULL, parameter_groups INTEGER NOT NULL);")
    con.execute("INSERT INTO metadata VALUES(?, ?);", [sum(parameter_groups), len(parameter_groups)])
    
    con.execute("CREATE TABLE parameter_group_definitions(id PRIMARY KEY, number_of_parameters INTEGER NOT NULL);")
    con.executemany("INSERT INTO parameter_group_definitions VALUES(?, ?);", enumerate(parameter_groups))
    
    for group_i, number_in_group in enumerate(parameter_groups):
        createTransitionsTableQuery = "CREATE TABLE transitions_group_" + str(group_i) + "("
        
        for prefix in PREFIXES:
            for i in xrange(number_in_group):
                createTransitionsTableQuery += (prefix + PARAMETER_NAME + str(i) + " " + PARAMETER_TYPE + ", ")
        
        createTransitionsTableQuery = createTransitionsTableQuery[:-2] # Remove the trailing ", "
        createTransitionsTableQuery += (");")
        con.execute(createTransitionsTableQuery)
    
    con.commit()
    
    print "Successfully created database " + db_file + "."

def create_database_if_not_exists(database_name, parameter_groups, database_dir=DATABASE_DIR, database_extension=DEFAULT_EXTENSION):
    db_file = os.path.join(database_dir, database_name + database_extension)

    if not os.path.exists(db_file):
        create_database(database_name, parameter_groups, database_dir, database_extension)

def delete_database(database_name, database_dir=DATABASE_DIR, database_extension=DEFAULT_EXTENSION):
    db_file = os.path.join(database_dir, database_name + database_extension)
    
    if os.path.exists(db_file):
        print "Deleting database", db_file
        os.remove(db_file)
        print "Database", db_file, "deleted."
    else:
        print "Did not delete database: file %s does not exist." % db_file

class StateTransitionDatabase:
    def __init__(self, db_name, db_dir=DATABASE_DIR, extension=DEFAULT_EXTENSION):
        
        db_file = os.path.join(db_dir, db_name + extension)
        self.__con = sqlite3.connect(db_file)
        
        self.__param_groups = numpy.array([row[0] for row in self.__con.execute("SELECT number_of_parameters FROM parameter_group_definitions ORDER BY id ASC;").fetchall()])
        self.__num_params = sum(self.__param_groups)
        
        insert_query_parts = ["BEGIN TRANSACTION;"]
        
        for group, num_params in enumerate(self.__param_groups):
            insert_query_parts.append("INSERT INTO transitions_group_")
            insert_query_parts.append(str(group))
            insert_query_parts.append(" VALUES(")
            for i in xrange(num_params*2):
                insert_query_parts.append("?, ")
            insert_query_parts[-1] = insert_query_parts[-1][:-2] # Remove the trailing ", "
            insert_query_parts.append(");\n")
        
        insert_query_parts.append("END TRANSACTION;")
        self.__insert_query = "".join(insert_query_parts)
        
        self.__select_query = ""
    
    def __format_states_for_database(self, states):
        split_indices = numpy.cumsum(self.__param_groups)
        return states.hsplit(split_indices)
    
    def __format_states_for_use(self, states_components_list):
        return numpy.concatenate(states_components_list, axis=1)
    
    def add_transition(self, from_state, to_state):
        '''Add a new transition to the database.
        @param from_state: A numpy array describing a state before transition. Must be of type float.
        @param from_state: A numpy array describing a state after transition. Must be of type float.
        '''
        self.__con.execute(self.__insert_query, self.combine_transition(from_state, to_state))
        self.__con.commit()
    
    def get_transitions(self):
        """Return all transitions in the database."""
        return numpy.array(self.__con.execute("SELECT * FROM transitions;").fetchall())
    
    def get_close_transitions(self, origin, thresholds):
        """Return all transitions in the database sufficiently close to origin.
        """
        
        query = "SELECT * FROM transitions WHERE from_theta_2 BETWEEN ? AND ? AND from_theta_3 BETWEEN ? and ?;"

        lower = origin - thresholds
        upper = origin + thresholds
#        print "Origin: %s, Lower bounds: %s, Upper bounds: %s"%(origin, lower, upper)

        return numpy.array(self.__con.execute(query, [lower[2], upper[2], lower[3], upper[3]]).fetchall())
#        result = cur.fetchall()
#        print len(result)
#        return numpy.array(result)
    
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
        from_states, to_states = [[], []]
        vel_threshold = 15
        while len(from_states) == 0 or len(to_states) == 0: 
            from_states, to_states = self.split_transition(self.get_close_transitions(prev_particle, numpy.array((0, 0, vel_threshold, vel_threshold))))
            vel_threshold += 15
        
#        print "Found %d close states"%len(from_states)
#        print from_states
#        print to_states
        
        weights = numpy.zeros((from_states.shape[0]))
        for i in xrange(from_states.shape[0]):
            weights[i] = weight_function(prev_particle, from_states[i,:])

        weights = weights/sum(weights)
        
        return numpy.average(to_states, axis=0, weights=weights)
