import sys
import unittest
import importlib

from unittest.mock import patch

class TestEnv(unittest.TestCase):
    @patch('os.getenv')
    def test_environment_variables_present(self, mock_getenv):
        """
        Test that MONGO_CLIENT and DB_NAME are correctly set from environment variables.
        """
        mock_getenv.side_effect = lambda key: {
            'MONGO_CLIENT': 'mongodb://localhost:27017',
            'DB_NAME': 'test_db',
        }.get(key)

        # Import the env module
        if 'basis_vm.config.env' in sys.modules:
            importlib.reload(sys.modules['basis_vm.config.env'])
        else:
            import basis_vm.config.env

        from basis_vm.config.env import MONGO_CLIENT, DB_NAME

        self.assertEqual(MONGO_CLIENT, 'mongodb://localhost:27017')
        self.assertEqual(DB_NAME, 'test_db')

    @patch('os.getenv')
    def test_environment_variables_missing(self, mock_getenv):
        """
        Test that MONGO_CLIENT and DB_NAME are None when environment variables are missing.
        """
        mock_getenv.side_effect = lambda key: None

        # Import the env module
        if 'basis_vm.config.env' in sys.modules:
            importlib.reload(sys.modules['basis_vm.config.env'])
        else:
            import basis_vm.config.env

        from basis_vm.config.env import MONGO_CLIENT, DB_NAME

        self.assertIsNone(MONGO_CLIENT)
        self.assertIsNone(DB_NAME)

    @patch('os.getenv')
    def test_environment_variables_empty(self, mock_getenv):
        """
        Test that MONGO_CLIENT and DB_NAME are empty strings when environment variables are set to empty.
        """
        mock_getenv.side_effect = lambda key: {
            'MONGO_CLIENT': '',
            'DB_NAME': '',
        }.get(key)

        # Import the env module
        if 'basis_vm.config.env' in sys.modules:
            importlib.reload(sys.modules['basis_vm.config.env'])
        else:
            import basis_vm.config.env

        from basis_vm.config.env import MONGO_CLIENT, DB_NAME

        self.assertEqual(MONGO_CLIENT, '')
        self.assertEqual(DB_NAME, '')

    @patch('os.getenv')
    def test_environment_variables_partial_missing(self, mock_getenv):
        """
        Test that only one of MONGO_CLIENT or DB_NAME is set when the other is missing.
        """
        mock_getenv.side_effect = lambda key: {
            'MONGO_CLIENT': 'mongodb://localhost:27017',
            'DB_NAME': None,
        }.get(key)

        # Import the env module
        if 'basis_vm.config.env' in sys.modules:
            importlib.reload(sys.modules['basis_vm.config.env'])
        else:
            import basis_vm.config.env

        from basis_vm.config.env import MONGO_CLIENT, DB_NAME

        self.assertEqual(MONGO_CLIENT, 'mongodb://localhost:27017')
        self.assertIsNone(DB_NAME)

    @patch('os.getenv')
    def test_environment_variables_non_string(self, mock_getenv):
        """
        Test that MONGO_CLIENT and DB_NAME handle non-string environment variables.
        """
        # os.getenv returns strings or None, so simulating non-string is not straightforward
        # However, if someone sets environment variables to non-string via some other means, they could be converted
        # Since os.getenv only returns strings or None, we focus on those cases
        # Therefore, this test can be skipped or assert that only strings or None are handled

        mock_getenv.side_effect = lambda key: {
            'MONGO_CLIENT': 12345,  # non-string value
            'DB_NAME': ['list', 'of', 'values'],  # non-string value
        }.get(key)

        # Import the env module
        if 'basis_vm.config.env' in sys.modules:
            importlib.reload(sys.modules['basis_vm.config.env'])
        else:
            import basis_vm.config.env

        from basis_vm.config.env import MONGO_CLIENT, DB_NAME

        # Since os.getenv is mocked to return non-string, the module variables will have those non-string values
        self.assertEqual(MONGO_CLIENT, 12345)
        self.assertEqual(DB_NAME, ['list', 'of', 'values'])

if __name__ == '__main__':
    unittest.main()
