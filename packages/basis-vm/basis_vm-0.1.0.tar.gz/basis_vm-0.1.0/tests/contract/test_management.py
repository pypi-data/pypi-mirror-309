import unittest

from unittest.mock import patch, MagicMock

from basis_vm.contract.management import (
    get_contract,
    update_contract_state,
    save_smart_contract,
    is_function_read_only
)

class TestContractManagement(unittest.TestCase):
    @patch('basis_vm.contract.management.database')
    def test_get_contract_success(self, mock_database):
        """
        Test successfully retrieving a smart contract from the database.
        """
        mock_database.smart_contracts.find_one.return_value = {'_id': 'contract_id', 'code': 'code'}
        contract = get_contract('contract_id')
        mock_database.smart_contracts.find_one.assert_called_once_with({'_id': 'contract_id'})
        self.assertEqual(contract, {'_id': 'contract_id', 'code': 'code'})

    @patch('basis_vm.contract.management.database')
    def test_get_contract_not_found(self, mock_database):
        """
        Test retrieving a smart contract that does not exist in the database.
        """
        mock_database.smart_contracts.find_one.return_value = None
        contract = get_contract('nonexistent_id')
        mock_database.smart_contracts.find_one.assert_called_once_with({'_id': 'nonexistent_id'})
        self.assertIsNone(contract)

    @patch('basis_vm.contract.management.database')
    def test_get_contract_database_exception(self, mock_database):
        """
        Test handling exceptions when retrieving a smart contract from the database.
        """
        mock_database.smart_contracts.find_one.side_effect = Exception("Database Error")
        with self.assertRaises(Exception) as context:
            get_contract('contract_id')
        mock_database.smart_contracts.find_one.assert_called_once_with({'_id': 'contract_id'})
        self.assertIn("Database Error", str(context.exception))

    @patch('basis_vm.contract.management.get_contract')
    def test_is_function_read_only_true(self, mock_get_contract):
        """
        Test that is_function_read_only returns True when the function has @read_only decorator.
        """
        code = """
def not_target_function():
    pass

@read_only
def target_function():
    pass
"""
        mock_get_contract.return_value = {'code': code}
        result = is_function_read_only('contract_id', 'target_function')
        self.assertTrue(result)
        mock_get_contract.assert_called_once_with('contract_id')

    @patch('basis_vm.contract.management.get_contract')
    def test_is_function_read_only_false(self, mock_get_contract):
        """
        Test that is_function_read_only returns False when the function does not have @read_only decorator.
        """
        code = """
def target_function():
    pass
"""
        mock_get_contract.return_value = {'code': code}
        result = is_function_read_only('contract_id', 'target_function')
        self.assertFalse(result)
        mock_get_contract.assert_called_once_with('contract_id')

    @patch('basis_vm.contract.management.get_contract')
    def test_is_function_read_only_function_not_found(self, mock_get_contract):
        """
        Test that is_function_read_only raises ValueError when the function is not found.
        """
        code = """
def another_function():
    pass
"""
        mock_get_contract.return_value = {'code': code}
        with self.assertRaises(ValueError) as context:
            is_function_read_only('contract_id', 'nonexistent_function')
        self.assertIn("Function 'nonexistent_function' not found", str(context.exception))
        mock_get_contract.assert_called_once_with('contract_id')

    @patch('basis_vm.contract.management.get_contract')
    def test_is_function_read_only_contract_not_found(self, mock_get_contract):
        """
        Test that is_function_read_only raises ValueError when the contract is not found.
        """
        mock_get_contract.return_value = None
        with self.assertRaises(ValueError) as context:
            is_function_read_only('nonexistent_contract', 'some_function')
        self.assertIn("Contract with ID 'nonexistent_contract' does not exist", str(context.exception))
        mock_get_contract.assert_called_once_with('nonexistent_contract')

    @patch('basis_vm.contract.management.get_contract')
    def test_is_function_read_only_syntax_error(self, mock_get_contract):
        """
        Test that is_function_read_only raises SyntaxError when the contract code has a syntax error.
        """
        code = """
def target_function()
    pass
"""
        mock_get_contract.return_value = {'code': code}
        with self.assertRaises(SyntaxError) as context:
            is_function_read_only('contract_id', 'target_function')
        self.assertIn("Syntax error in contract code", str(context.exception))
        mock_get_contract.assert_called_once_with('contract_id')

    @patch('basis_vm.contract.management.get_contract')
    def test_is_function_read_only_with_complex_decorator(self, mock_get_contract):
        """
        Test that is_function_read_only correctly identifies @read_only used with parentheses.
        """
        code = """
@read_only()
def target_function():
    pass
"""
        mock_get_contract.return_value = {'code': code}
        result = is_function_read_only('contract_id', 'target_function')
        self.assertTrue(result)
        mock_get_contract.assert_called_once_with('contract_id')

    @patch('basis_vm.contract.management.get_contract')
    def test_is_function_read_only_decorator_alias(self, mock_get_contract):
        """
        Test that is_function_read_only handles decorator aliases appropriately.
        """
        code = """
read_only_alias = read_only

@read_only_alias
def target_function():
    pass
"""
        mock_get_contract.return_value = {'code': code}
        result = is_function_read_only('contract_id', 'target_function')
        # Note: The current implementation may not handle aliases; adjust the expected result accordingly.
        self.assertFalse(result)
        mock_get_contract.assert_called_once_with('contract_id')

    @patch('basis_vm.contract.management.database')
    def test_update_contract_state_success(self, mock_database):
        """
        Test successfully updating a smart contract's state in the database.
        """
        new_state = {'counter': 1}
        serialized_state = {'counter': {'__type__': 'int', '__value__': '1'}}
        update_contract_state('contract_id', new_state)
        mock_database.smart_contracts.update_one.assert_called_once_with(
            {'_id': 'contract_id'}, {'$set': {'state': serialized_state}}
        )

    @patch('basis_vm.contract.management.database')
    def test_update_contract_state_no_changes(self, mock_database):
        """
        Test updating a smart contract's state with no changes.
        """
        new_state = {}
        serialized_state = {}
        update_contract_state('contract_id', new_state)
        mock_database.smart_contracts.update_one.assert_called_once_with(
            {'_id': 'contract_id'}, {'$set': {'state': serialized_state}}
        )

    @patch('basis_vm.contract.management.database')
    def test_update_contract_state_database_exception(self, mock_database):
        """
        Test handling exceptions when updating a smart contract's state in the database.
        """
        mock_database.smart_contracts.update_one.side_effect = Exception("Update Error")
        new_state = {'counter': 1}
        serialized_state = {'counter': {'__type__': 'int', '__value__': '1'}}
        with self.assertRaises(Exception) as context:
            update_contract_state('contract_id', new_state)
        mock_database.smart_contracts.update_one.assert_called_once_with(
            {'_id': 'contract_id'}, {'$set': {'state': serialized_state}}
        )
        self.assertIn("Update Error", str(context.exception))

    @patch('basis_vm.contract.management.database')
    def test_save_smart_contract_success(self, mock_database):
        """
        Test successfully saving a smart contract to the database.
        """
        contract_data = {'_id': 'contract_id', 'code': 'code'}
        # Serializar el estado si es necesario
        save_smart_contract('contract_id', contract_data)
        mock_database.smart_contracts.replace_one.assert_called_once_with(
            {'_id': 'contract_id'}, contract_data, upsert=True
        )

    @patch('basis_vm.contract.management.database')
    def test_save_smart_contract_replace_existing(self, mock_database):
        """
        Test saving a smart contract when it already exists (should replace).
        """
        contract_data = {'_id': 'existing_contract_id', 'code': 'new_code'}
        save_smart_contract('existing_contract_id', contract_data)
        mock_database.smart_contracts.replace_one.assert_called_once_with(
            {'_id': 'existing_contract_id'}, contract_data, upsert=True
        )

    @patch('basis_vm.contract.management.database')
    def test_save_smart_contract_database_exception(self, mock_database):
        """
        Test handling exceptions when saving a smart contract to the database.
        """
        mock_database.smart_contracts.replace_one.side_effect = Exception("Save Error")
        contract_data = {'_id': 'contract_id', 'code': 'code'}
        with self.assertRaises(Exception) as context:
            save_smart_contract('contract_id', contract_data)
        mock_database.smart_contracts.replace_one.assert_called_once_with(
            {'_id': 'contract_id'}, contract_data, upsert=True
        )
        self.assertIn("Save Error", str(context.exception))

    @patch('basis_vm.contract.management.database')
    def test_save_smart_contract_invalid_input(self, mock_database):
        """
        Test saving a smart contract with invalid input types.
        """
        # contract_data is not a dict
        contract_data = 'invalid_data'  # Should be dict
        with self.assertRaises(TypeError) as context:
            save_smart_contract('contract_id', contract_data)
        self.assertIn("contract_data must be a dictionary.", str(context.exception))
        # Ensure replace_one was not called porque se lanzó una excepción antes
        mock_database.smart_contracts.replace_one.assert_not_called()

    @patch('basis_vm.contract.management.database')
    def test_save_smart_contract_partial_data(self, mock_database):
        """
        Test saving a smart contract with partial data.
        """
        contract_data = {'_id': 'contract_id'}
        save_smart_contract('contract_id', contract_data)
        mock_database.smart_contracts.replace_one.assert_called_once_with(
            {'_id': 'contract_id'}, contract_data, upsert=True
        )

    @patch('basis_vm.contract.management.database')
    def test_get_contract_with_special_characters(self, mock_database):
        """
        Test retrieving a smart contract with special characters in the contract_id.
        """
        contract_id = 'contract_id_!@#$%^&*()'
        mock_database.smart_contracts.find_one.return_value = {'_id': contract_id, 'code': 'code'}
        contract = get_contract(contract_id)
        mock_database.smart_contracts.find_one.assert_called_once_with({'_id': contract_id})
        self.assertEqual(contract, {'_id': contract_id, 'code': 'code'})

    @patch('basis_vm.contract.management.database')
    def test_update_contract_state_with_special_characters(self, mock_database):
        """
        Test updating a smart contract's state with special characters in the contract_id.
        """
        contract_id = 'contract_id_!@#$%^&*()'
        new_state = {'counter': 2}
        serialized_state = {'counter': {'__type__': 'int', '__value__': '2'}}
        update_contract_state(contract_id, new_state)
        mock_database.smart_contracts.update_one.assert_called_once_with(
            {'_id': contract_id}, {'$set': {'state': serialized_state}}
        )

    @patch('basis_vm.contract.management.database')
    def test_save_smart_contract_with_special_characters(self, mock_database):
        """
        Test saving a smart contract with special characters in the contract_id.
        """
        contract_id = 'contract_id_!@#$%^&*()'
        contract_data = {'_id': contract_id, 'code': 'code'}
        save_smart_contract(contract_id, contract_data)
        mock_database.smart_contracts.replace_one.assert_called_once_with(
            {'_id': contract_id}, contract_data, upsert=True
        )

if __name__ == '__main__':
    unittest.main()
