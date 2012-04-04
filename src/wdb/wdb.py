from itertools import imap, izip
from wmath import distribution
import numpy
import os
import sqlite3

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
        con.execute("CREATE INDEX index_g%i ON transitions_group_%i(%s);"%(group_i, group_i, ", ".join(["%s%s%i ASC"%(PREFIXES[0], PARAMETER_NAME, i) for i in xrange(number_in_group)])))
    
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

        ### Build insert query string ###
        self.__insert_queries = []        
        
        for group, num_params in enumerate(self.__param_groups):
            insert_query_parts = ["INSERT INTO transitions_group_" + str(group) + " VALUES("]
            insert_query_parts.append(("?, "*(num_params*2))[:-2]) # Remove the trailing ", "
            insert_query_parts.append(");")
            self.__insert_queries.append("".join(insert_query_parts))
        
        """
        ###Build select query string###
        Build a select query string that selects particles in a high-dimension rectangle around a given point.
        
        The query will need three arguments (the ?'s in the query) for each
        parameter. The first will be called "origin", the second "min" and the
        third "max". The query returns all particles such that
            min <= parameter - origin <= max
        is true for all parameters.
        """
        select_square_rectangle_parts = ["SELECT "]
        for prefix in PREFIXES:
            for group, num_params in enumerate(self.__param_groups):
                for param in xrange(num_params):
                    select_square_rectangle_parts.append("g%i.%s%s%i, "%(group, prefix, PARAMETER_NAME, param))
        select_square_rectangle_parts[-1] = select_square_rectangle_parts[-1][:-2] # Remove the trailing ", "
        
        select_square_rectangle_parts.append(" FROM ")
        for group in xrange(len(self.__param_groups)):
            select_square_rectangle_parts.append("transitions_group_%i AS g%i, "%(group, group))
        select_square_rectangle_parts[-1] = select_square_rectangle_parts[-1][:-2] # Remove the trailing ", "
        
        select_square_rectangle_parts.append(" WHERE ")
        for group, num_params in enumerate(self.__param_groups):
            for param in xrange(num_params):
                select_square_rectangle_parts.append("g%i.%s%s%i - ? BETWEEN ? AND ? AND "%(group, PREFIXES[0], PARAMETER_NAME, param))
        select_square_rectangle_parts[-1] = select_square_rectangle_parts[-1][:-5] # Remove the trailing " AND "
        
        select_square_rectangle_parts.append(";")
        self.__select_rectangle_query = "".join(select_square_rectangle_parts)
        
    def add_transitions(self, from_states, to_states):
        '''Add new transitions to the database.
        @param from_state: A numpy array where each row is a state before transition. Must be of type float.
        @param to_state: A numpy array where each row is a state after transition. Must be of type float.
        '''
        
        split_indices = numpy.cumsum(self.__param_groups)[:-1] # Don't create an empty split from the last index
        
        # This statement "weaves" from_states and to_states together into a list of big matrices with the same structure as the database tables
        args_list = imap(numpy.hstack, izip(numpy.hsplit(from_states, split_indices), numpy.hsplit(to_states, split_indices)))
        
        for query, args in izip(self.__insert_queries, args_list):
            if len(args.shape) == 1:
                args = [args]
            self.__con.executemany(query, args)
        
        self.__con.commit()
    
    def get_transitions_in_rectangle(self, origin, max_diffs):
        """Return all transitions in the database sufficiently close to origin.
        """
        
        # This statement weaves origin and max_diffs into one long array, where query_args[i] = {origin[i/2] if i%2==0, otherwise max_diffs[(i-1)/2]}.
        query_args = numpy.hstack(zip(origin, -max_diffs, max_diffs))
        
        return numpy.array(self.__con.execute(self.__select_rectangle_query, query_args).fetchall())
        

    def __split_transition(self, transition):
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
