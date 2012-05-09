__all__ = ["create_database", "create_database_if_not_exists", "delete_database", "StateTransitionDatabase"]

from itertools import imap, izip, product
from parallel import parallel_map
from wmath import distribution
import numpy
import os
import sqlite3
from settings import *
from common import make_data_path

def make_db_path(database_name, database_dir=DB_DIR, database_extension=DB_EXTENSION):
    return make_data_path(database_dir, database_name + database_extension)

def euclidean_distance_inverse_squared(a, b):
    """UNTESTED Calculate 1/(the norm of (a-b))^2.
    
    @param a: a numpy array
    @param b: a numpy array of the same dimension as a
    @return: 1/(norm(a-b)^2)
    """
    zero_division_defense = 1e-9 * min(numpy.linalg.norm(a), numpy.linalg.norm(b))
    
    return 1.0/(zero_division_defense + (numpy.linalg.norm(a-b))**2)

def create_database(database_name, parameter_groups):
    db_file = make_db_path(database_name)
    
    if not isinstance(parameter_groups, (list, tuple)):
        parameter_groups = (parameter_groups,)
    
    if os.path.exists(db_file):
        raise IOError("File already exists: %s" % db_file)
    
    if not os.path.exists(os.path.dirname(db_file)):
        os.makedirs(os.path.dirname(db_file))
    
    con = sqlite3.connect(db_file)
    
    con.execute("CREATE TABLE metadata(total_number_of_parameters INTEGER NOT NULL, parameter_groups INTEGER NOT NULL);")
    con.execute("INSERT INTO metadata VALUES(?, ?);", [sum(parameter_groups), len(parameter_groups)])
    
    con.execute("CREATE TABLE parameter_group_definitions(id PRIMARY KEY, number_of_parameters INTEGER NOT NULL);")
    con.executemany("INSERT INTO parameter_group_definitions VALUES(?, ?);", enumerate(parameter_groups))
    
    for group_i, number_in_group in enumerate(parameter_groups):
        createTransitionsTableQuery = "CREATE TABLE %s%i ("%(TABLE_NAME, group_i)
        
        for prefix in PREFIXES:
            for i in xrange(number_in_group):
                createTransitionsTableQuery += (prefix + PARAMETER_NAME + str(i) + " " + PARAMETER_TYPE + ", ")
        
        createTransitionsTableQuery = createTransitionsTableQuery[:-2] # Remove the trailing ", "
        createTransitionsTableQuery += (");")
        con.execute(createTransitionsTableQuery)
        
        # Create indexes. Sample query resulting from this expression: CREATE INDEX index_g0 ON transitions_group_0(from_theta_0 ASC, from_theta_1 ASC);
        con.execute("CREATE INDEX index_g%i ON %s%i(%s);"%(group_i, TABLE_NAME, group_i, ", ".join(["%s%s%i ASC"%(PREFIXES[0], PARAMETER_NAME, i) for i in xrange(number_in_group)])))
    
    con.commit()
    
    print "Successfully created database " + db_file + "."

def create_database_if_not_exists(database_name, parameter_groups):
    db_file = make_db_path(database_name)

    if not os.path.exists(db_file):
        create_database(database_name, parameter_groups)

def delete_database(database_name):
    db_file = make_db_path(database_name)
    
    if os.path.exists(db_file):
        print "Deleting database", db_file
        os.remove(db_file)
        print "Database", db_file, "deleted."
    else:
        print "Did not delete database: file %s does not exist." % db_file

class StateTransitionDatabase:
    all_transitions = None
    def __init__(self, db_name):
        
        db_file = make_db_path(db_name)
        
        self.__con = sqlite3.connect(db_file)
        
        self.__param_groups = numpy.array([row[0] for row in self.__con.execute("SELECT number_of_parameters FROM parameter_group_definitions ORDER BY id ASC;").fetchall()])
        self.__num_params = sum(self.__param_groups)

        ### Build insert query string ###
        self.__insert_queries = []        
        
        for group, num_params in enumerate(self.__param_groups):
            insert_query_parts = ["INSERT INTO %s%i VALUES("%(TABLE_NAME, group)]
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
        
        self.__select_all_queries = []
        for group, num_params in enumerate(self.__param_groups):
            query = "SELECT %s FROM %s%i;"%(", ".join(["%s%s%i"%(prefix, PARAMETER_NAME, param) for prefix, param in product(PREFIXES, xrange(num_params))]), TABLE_NAME, group)
            self.__select_all_queries.append(query)
        
        self.__select_rectangle_queries = []
        for group, num_params in enumerate(self.__param_groups):
            query = ["SELECT %s FROM %s%i WHERE "%(", ".join(["%s%s%i"%(prefix, PARAMETER_NAME, param) for prefix, param in product(PREFIXES, xrange(num_params))]), TABLE_NAME, group)]
            where_clause_parts = []
            for param in xrange(num_params):
                where_clause_parts.append("%s%s%i BETWEEN ? AND ?"%(PREFIXES[0], PARAMETER_NAME, param))
            query += " AND ".join(where_clause_parts) + ";"
            self.__select_rectangle_queries.append(query)
        
        #parallel_map(self.get_all_transitions, xrange(len(self.__param_groups)))
        map(self.get_all_transitions, xrange(len(self.__param_groups)))
        
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
    
    def get_all_transitions(self, parameter_group):
        if self.all_transitions is None:
            self.all_transitions = [numpy.array(self.__con.execute(self.__select_all_queries[group]).fetchall()) for group in xrange(len(self.__param_groups))]
        return self.all_transitions[parameter_group]
    
    def get_transitions_in_rectangle(self, param_group, origin, max_diffs):
        """Return all transitions in the database sufficiently close to origin.
        """
        
        # This statement weaves origin and max_diffs into one long array, where query_args[i] = {origin[i/2] if i%2==0, otherwise max_diffs[(i-1)/2]}.
        query_args = numpy.hstack(zip(origin, origin-max_diffs, origin+max_diffs))
        
        return numpy.array(self.__con.execute(self.__select_rectangle_queries[param_group], query_args).fetchall())
        
    def __split_by_parameter_groups(self, particles):
        """Splits the given particles into subparticles of independent parameters"""
        if len(self.__param_groups) == 1:
            return numpy.array([particles])
        return numpy.hsplit(particles, self.__param_groups.cumsum()[:-1])

    def __split_transition(self, transition):
        return numpy.hsplit(transition, 2)
    
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
        
        split_particle = self.__split_by_parameter_groups(prev_particle)
        selected = []
        for group, subparticle in enumerate(split_particle):
            from_states, to_states = self.__split_transition(self.get_all_transitions(group))
            standard_deviations = numpy.std(from_states, axis=0)
            
            # HACK: Prevent division by zero
            zero_std_cols = numpy.where(standard_deviations == 0)[0]
            standard_deviations = numpy.delete(standard_deviations, zero_std_cols)
            diff = numpy.delete(from_states - subparticle, zero_std_cols, axis=1)
            
            weights = (((diff)/standard_deviations)**2).sum(axis=1)
            weights += numpy.min(weights[numpy.nonzero(weights)])*1e-6 # HACK: Prevent division by zero
            weights = 1.0/weights
            weights /= sum(weights)
            
            selected.append(numpy.average(to_states, axis=0, weights=weights))
        return numpy.hstack(selected)
