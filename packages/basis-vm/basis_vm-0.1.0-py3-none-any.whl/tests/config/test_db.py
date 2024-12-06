import unittest
from unittest.mock import patch, MagicMock
from pymongo.collection import Collection

from basis_vm.config.db import Database

class TestDatabase(unittest.TestCase):

    @patch('basis_vm.config.db.MongoClient', autospec=True)
    def test_database_initialization(self, mock_mongo_client_class):
        """
        Test that the Database class initializes correctly and connects to the specified database.
        """
        uri = 'mongodb://localhost:27017'
        db_name = 'test_db'
        
        # Create a mock MongoClient instance
        mock_mongo_client_instance = MagicMock()
        mock_mongo_client_class.return_value = mock_mongo_client_instance
        
        # Instantiate the Database
        db_instance = Database(uri, db_name)
        
        # Assert that MongoClient is called with the correct URI
        mock_mongo_client_class.assert_called_once_with(uri)
        
        # Assert that the database is accessed correctly
        mock_mongo_client_instance.__getitem__.assert_called_once_with(db_name)
        
        # Assert that the _db attribute is set correctly
        self.assertEqual(db_instance._db, mock_mongo_client_instance.__getitem__.return_value)

    @patch('basis_vm.config.db.MongoClient', autospec=True)
    def test_smart_contracts_property(self, mock_mongo_client_class):
        """
        Test that the smart_contracts property returns the correct collection.
        """
        uri = 'mongodb://localhost:27017'
        db_name = 'test_db'
        
        # Create a mock MongoClient instance and mock database
        mock_mongo_client_instance = MagicMock()
        mock_db = MagicMock()
        mock_mongo_client_class.return_value = mock_mongo_client_instance
        mock_mongo_client_instance.__getitem__.return_value = mock_db
        
        # Mock the 'smart_contracts' collection as a Collection instance
        mock_smart_contracts_collection = MagicMock(spec=Collection)
        mock_db.smart_contracts = mock_smart_contracts_collection
        
        # Instantiate the Database
        db_instance = Database(uri, db_name)
        
        # Access the smart_contracts property
        smart_contracts = db_instance.smart_contracts
        
        # Assert that the smart_contracts property returns the correct collection
        self.assertEqual(smart_contracts, mock_smart_contracts_collection)

    @patch('basis_vm.config.db.MongoClient', autospec=True)
    def test_multiple_database_instances_separate_clients(self, mock_mongo_client_class):
        """
        Test that multiple Database instances with different URIs use separate MongoClient instances.
        """
        uri1 = 'mongodb://localhost:27017'
        db_name1 = 'test_db1'
        uri2 = 'mongodb://localhost:27018'
        db_name2 = 'test_db2'
        
        # Create separate mock MongoClient instances
        mock_mongo_client_instance1 = MagicMock()
        mock_mongo_client_instance2 = MagicMock()
        mock_mongo_client_class.side_effect = [mock_mongo_client_instance1, mock_mongo_client_instance2]
        
        # Instantiate two Database instances
        db_instance1 = Database(uri1, db_name1)
        db_instance2 = Database(uri2, db_name2)
        
        # Assert that MongoClient was called with both URIs
        mock_mongo_client_class.assert_has_calls([
            unittest.mock.call(uri1),
            unittest.mock.call(uri2)
        ])
        
        # Assert that each Database instance has its own _db
        mock_mongo_client_instance1.__getitem__.assert_called_once_with(db_name1)
        mock_mongo_client_instance2.__getitem__.assert_called_once_with(db_name2)
        
        self.assertNotEqual(db_instance1._db, db_instance2._db)

    @patch('basis_vm.config.db.MongoClient', autospec=True)
    def test_smart_contracts_is_collection(self, mock_mongo_client_class):
        """
        Test that the smart_contracts property returns a pymongo Collection instance.
        """
        uri = 'mongodb://localhost:27017'
        db_name = 'test_db'
        
        # Create a mock MongoClient instance and mock database
        mock_mongo_client_instance = MagicMock()
        mock_db = MagicMock()
        mock_mongo_client_class.return_value = mock_mongo_client_instance
        mock_mongo_client_instance.__getitem__.return_value = mock_db
        
        # Mock the 'smart_contracts' collection as a Collection instance
        mock_smart_contracts_collection = MagicMock(spec=Collection)
        mock_db.smart_contracts = mock_smart_contracts_collection
        
        # Instantiate the Database
        db_instance = Database(uri, db_name)
        
        # Access the smart_contracts property
        smart_contracts = db_instance.smart_contracts
        
        # Assert that smart_contracts is an instance of Collection
        self.assertIsInstance(smart_contracts, Collection)

    @patch('basis_vm.config.db.MongoClient', autospec=True)
    def test_database_initialization_with_invalid_uri(self, mock_mongo_client_class):
        """
        Test that the Database class raises an exception when initialized with an invalid URI.
        """
        uri = 'invalid_uri'
        db_name = 'test_db'
        
        # Configure the mock to raise an exception when called with invalid URI
        mock_mongo_client_class.side_effect = Exception("Invalid URI")
        
        with self.assertRaises(Exception) as context:
            Database(uri, db_name)
        
        self.assertIn("Invalid URI", str(context.exception))
        mock_mongo_client_class.assert_called_once_with(uri)

    @patch('basis_vm.config.db.MongoClient', autospec=True)
    def test_database_initialization_with_non_string_uri(self, mock_mongo_client_class):
        """
        Test that the Database class handles non-string URIs appropriately.
        """
        uri = None  # Non-string URI
        db_name = 'test_db'
        
        # Configure the mock to raise TypeError when called with non-string URI
        mock_mongo_client_class.side_effect = TypeError("URI must be a string")
        
        with self.assertRaises(TypeError) as context:
            Database(uri, db_name)
        
        self.assertIn("URI must be a string", str(context.exception))
        mock_mongo_client_class.assert_called_once_with(uri)

    @patch('basis_vm.config.db.MongoClient', autospec=True)
    def test_smart_contracts_property_can_be_accessed_multiple_times(self, mock_mongo_client_class):
        """
        Test that the smart_contracts property can be accessed multiple times and returns the same collection.
        """
        uri = 'mongodb://localhost:27017'
        db_name = 'test_db'
        
        # Create a mock MongoClient instance and mock database
        mock_mongo_client_instance = MagicMock()
        mock_db = MagicMock()
        mock_mongo_client_class.return_value = mock_mongo_client_instance
        mock_mongo_client_instance.__getitem__.return_value = mock_db
        
        # Mock the 'smart_contracts' collection as a Collection instance
        mock_smart_contracts_collection = MagicMock(spec=Collection)
        mock_db.smart_contracts = mock_smart_contracts_collection
        
        # Instantiate the Database
        db_instance = Database(uri, db_name)
        
        # Access the smart_contracts property multiple times
        smart_contracts1 = db_instance.smart_contracts
        smart_contracts2 = db_instance.smart_contracts
        smart_contracts3 = db_instance.smart_contracts
        
        # Assert that all accesses return the same collection
        self.assertEqual(smart_contracts1, mock_smart_contracts_collection)
        self.assertEqual(smart_contracts2, mock_smart_contracts_collection)
        self.assertEqual(smart_contracts3, mock_smart_contracts_collection)

    @patch('basis_vm.config.db.MongoClient', autospec=True)
    def test_database_with_special_characters_in_uri_and_db_name(self, mock_mongo_client_class):
        """
        Test that the Database class initializes correctly with URIs and database names containing special characters.
        """
        uri = 'mongodb://user:pass@localhost:27017/special_db?authSource=admin'
        db_name = 'special_db_!@#$%^&*()'
        
        # Create a mock MongoClient instance
        mock_mongo_client_instance = MagicMock()
        mock_mongo_client_class.return_value = mock_mongo_client_instance
        
        # Instantiate the Database
        db_instance = Database(uri, db_name)
        
        # Assert that MongoClient is called with the correct URI
        mock_mongo_client_class.assert_called_once_with(uri)
        
        # Assert that the database is accessed correctly
        mock_mongo_client_instance.__getitem__.assert_called_once_with(db_name)
        
        # Assert that the _db attribute is set correctly
        self.assertEqual(db_instance._db, mock_mongo_client_instance.__getitem__.return_value)

if __name__ == '__main__':
    unittest.main()
