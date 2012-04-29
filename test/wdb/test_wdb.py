from wdb import create_database, create_database_if_not_exists, delete_database
from wdb import StateTransitionDatabase
import numpy
import os
import sqlite3
import unittest

class TestDatabaseCreationAndDeletion(unittest.TestCase):
    db_dir = "tmp/test/test_db"
    db_name = "test_db"
    fileext = ".dbtest"
    db_path = os.path.join(db_dir, db_name + fileext)
    param_groups = [1,2,3]
    
    def setUp(self):
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
    
    def test_create_existent_database_throws_exception(self):
        try:
            if not os.path.exists(self.db_path):
                open(self.db_name, "w").close()
            create_database(self.db_name, [1,2,3], self.db_dir, self.fileext)
            self.fail("Exception not thrown when attempting to create database when file already exists.")
        except IOError:
            pass
    
    def test_delete_database(self):
        if not os.path.exists(self.db_path):
            open(self.db_path, "w").close()
        
        delete_database(self.db_name, self.db_dir, self.fileext)
        self.assertFalse(os.path.exists(self.db_path), "File still exists after deletion attempt: " + self.db_path)

    def test_create_database(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            
        create_database(self.db_name, [1,2,3], self.db_dir, self.fileext)
        self.assertTrue(os.path.exists(self.db_path), "Expected file does not exist: " + self.db_path)
        
        con = sqlite3.connect(self.db_path)
        
        db_param_groups = [row[0] for row in con.execute("SELECT number_of_parameters FROM parameter_group_definitions ORDER BY id ASC;").fetchall()]
        self.assertEquals(self.param_groups, db_param_groups, "Parameter groups in database are not as expected.")
    
    def test_create_database_if_not_exists_creates_database_if_it_does_not_exist(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        create_database_if_not_exists(self.db_name, [1,2,3], self.db_dir, self.fileext)
        self.assertTrue(os.path.exists(self.db_path), "Expected file does not exist: " + self.db_path)
    
    def test_create_database_if_not_exists_does_not_create_database_if_it_exists(self):
        filesize = 0
        if not os.path.exists(self.db_path):
            open(self.db_path, "w").close()
        filesize = os.stat(self.db_path).st_size
            
        create_database_if_not_exists(self.db_name, [1,2,3], self.db_dir, self.fileext)
        self.assertEquals(filesize, os.stat(self.db_path).st_size, "File size has changed though nothing should have happened.")
    
class TestStateTransitionDatabase(unittest.TestCase):
    
    def setUp(self):
        pass
        