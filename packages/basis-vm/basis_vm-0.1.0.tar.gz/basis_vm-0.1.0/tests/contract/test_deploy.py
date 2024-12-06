import unittest
from unittest.mock import patch, MagicMock
from basis_vm.contract.deploy import deploy_smart_contract

class TestContractDeploy(unittest.TestCase):

    @patch('basis_vm.contract.deploy.save_smart_contract')
    @patch('basis_vm.contract.deploy.create_safe_globals')
    @patch('basis_vm.contract.deploy.is_code_safe')
    @patch('basis_vm.contract.deploy.is_code_valid')
    @patch('hashlib.sha256')
    def test_deploy_smart_contract_success(self, mock_sha256, mock_is_valid, mock_is_safe, mock_create_globals, mock_save_contract):
        """
        Test successful deployment of a valid and safe smart contract.
        """
        # Configure mocks for the success case
        mock_is_valid.return_value = True
        mock_is_safe.return_value = True
        mock_sha256.return_value.hexdigest.return_value = 'code_hash'
        mock_create_globals.return_value = {}

        code_str = """
class Contract:
    def __init__(self):
        self.state = 0
"""
        contract_id = 'contract_id'

        result = deploy_smart_contract(code_str, contract_id, auth_user='user')

        # Verify that the contract ID is as expected
        self.assertEqual(result, contract_id)

        # Verify that the contract is saved with the correct data
        mock_save_contract.assert_called_with(contract_id, {
            '_id': contract_id,
            'code': code_str,
            'hash': 'code_hash',
            'owner': 'user',
            'state': {'state': 0}
        })

    @patch('basis_vm.contract.deploy.is_code_valid')
    def test_deploy_smart_contract_invalid_code(self, mock_is_valid):
        """
        Test deployment with invalid smart contract code.
        """
        mock_is_valid.return_value = False
        code_str = "invalid code"
        contract_id = 'contract_id'

        with self.assertRaises(ValueError) as context:
            deploy_smart_contract(code_str, contract_id, auth_user='user')
        
        self.assertIn("El código del contrato inteligente no es válido.", str(context.exception))

    @patch('basis_vm.contract.deploy.is_code_valid')
    @patch('basis_vm.contract.deploy.is_code_safe')
    def test_deploy_smart_contract_unsafe_code(self, mock_is_safe, mock_is_valid):
        """
        Test deployment with unsafe smart contract code.
        """
        mock_is_valid.return_value = True
        mock_is_safe.return_value = False
        code_str = "unsafe code"
        contract_id = 'contract_id'

        with self.assertRaises(ValueError) as context:
            deploy_smart_contract(code_str, contract_id, auth_user='user')
        
        self.assertIn("Se detectó código no seguro en el contrato inteligente.", str(context.exception))

    @patch('basis_vm.contract.deploy.save_smart_contract')
    @patch('basis_vm.contract.deploy.create_safe_globals')
    @patch('basis_vm.contract.deploy.is_code_safe')
    @patch('basis_vm.contract.deploy.is_code_valid')
    @patch('hashlib.sha256')
    def test_deploy_smart_contract_execution_error(self, mock_sha256, mock_is_valid, mock_is_safe, mock_create_globals, mock_save_contract):
        """
        Test deployment where the execution of the smart contract code throws an exception.
        """
        # Configure mocks to simulate an exception during execution
        mock_is_valid.return_value = True
        mock_is_safe.return_value = True
        mock_sha256.return_value.hexdigest.return_value = 'code_hash'
        mock_create_globals.return_value = {}
        # Simulate exception during exec
        with patch('basis_vm.contract.deploy.exec') as mock_exec:
            mock_exec.side_effect = Exception("Error en la ejecución del contrato.")

            code_str = """
class Contract:
    def __init__(self):
        self.state = 0
    def faulty_method(self):
        raise Exception("Faulty method")
"""

            contract_id = 'contract_id'

            with self.assertRaises(Exception) as context:
                deploy_smart_contract(code_str, contract_id, auth_user='user')
            
            self.assertIn("Error ejecutando el contrato inteligente:", str(context.exception))

    @patch('basis_vm.contract.deploy.save_smart_contract')
    @patch('basis_vm.contract.deploy.create_safe_globals')
    @patch('basis_vm.contract.deploy.is_code_safe')
    @patch('basis_vm.contract.deploy.is_code_valid')
    @patch('hashlib.sha256')
    def test_deploy_smart_contract_no_contract_class(self, mock_sha256, mock_is_valid, mock_is_safe, mock_create_globals, mock_save_contract):
        """
        Test deployment where the smart contract code does not define a contract class.
        """
        # Configure mocks for the case where no contract class is found
        mock_is_valid.return_value = True
        mock_is_safe.return_value = True
        mock_sha256.return_value.hexdigest.return_value = 'code_hash'
        mock_create_globals.return_value = {}

        code_str = """
# No Contract class defined here
def some_function():
    pass
"""

        contract_id = 'contract_id'

        with self.assertRaises(ValueError) as context:
            deploy_smart_contract(code_str, contract_id, auth_user='user')
            
        self.assertIn("No se encontró una clase de contrato en el código.", str(context.exception))
        mock_save_contract.assert_not_called()

    @patch('basis_vm.contract.deploy.save_smart_contract', side_effect=Exception("Database Error"))
    @patch('basis_vm.contract.deploy.create_safe_globals')
    @patch('basis_vm.contract.deploy.is_code_safe')
    @patch('basis_vm.contract.deploy.is_code_valid')
    @patch('hashlib.sha256')
    def test_deploy_smart_contract_save_failure(self, mock_sha256, mock_is_valid, mock_is_safe, mock_create_globals, mock_save_contract):
        """
        Test deployment where an error occurs when trying to save the contract to the database.
        """
        # Configure mocks to simulate a failure when saving the contract
        mock_is_valid.return_value = True
        mock_is_safe.return_value = True
        mock_sha256.return_value.hexdigest.return_value = 'code_hash'
        mock_create_globals.return_value = {}

        code_str = """
class Contract:
    def __init__(self):
        self.state = 0
"""

        contract_id = 'contract_id'

        with self.assertRaises(Exception) as context:
            deploy_smart_contract(code_str, contract_id, auth_user='user')
        
        self.assertIn("Database Error", str(context.exception))

    @patch('basis_vm.contract.deploy.is_code_valid')
    def test_deploy_smart_contract_empty_code(self, mock_is_valid):
        """
        Test deployment with empty smart contract code.
        """
        mock_is_valid.return_value = False  # Assume empty code is invalid
        code_str = ""
        contract_id = 'contract_id'

        with self.assertRaises(ValueError) as context:
            deploy_smart_contract(code_str, contract_id, auth_user='user')
        
        self.assertIn("El código del contrato inteligente no es válido.", str(context.exception))

    @patch('basis_vm.contract.deploy.save_smart_contract')
    @patch('basis_vm.contract.deploy.create_safe_globals')
    @patch('basis_vm.contract.deploy.is_code_safe')
    @patch('basis_vm.contract.deploy.is_code_valid')
    @patch('hashlib.sha256')
    def test_deploy_smart_contract_initial_state(self, mock_sha256, mock_is_valid, mock_is_safe, mock_create_globals, mock_save_contract):
        """
        Test deployment to verify that the initial state of the contract is captured correctly.
        """
        # Configure mocks for the success case
        mock_is_valid.return_value = True
        mock_is_safe.return_value = True
        mock_sha256.return_value.hexdigest.return_value = 'code_hash'
        mock_create_globals.return_value = {}

        code_str = """
class Contract:
    def __init__(self):
        self.counter = 10
        self.name = "TestContract"
"""

        contract_id = 'contract_id'

        result = deploy_smart_contract(code_str, contract_id, auth_user='user')

        # Verify that the contract is saved with the correct initial state
        mock_save_contract.assert_called_with(contract_id, {
            '_id': contract_id,
            'code': code_str,
            'hash': 'code_hash',
            'owner': 'user',
            'state': {'counter': 10, 'name': 'TestContract'}
        })

    @patch('basis_vm.contract.deploy.save_smart_contract')
    @patch('basis_vm.contract.deploy.create_safe_globals')
    @patch('basis_vm.contract.deploy.is_code_safe')
    @patch('basis_vm.contract.deploy.is_code_valid')
    @patch('hashlib.sha256')
    def test_deploy_smart_contract_exec_exception(self, mock_sha256, mock_is_valid, mock_is_safe, mock_create_globals, mock_save_contract):
        """
        Test deployment where the exec function throws an unexpected exception.
        """
        # Configure mocks to simulate an unexpected exception during exec
        mock_is_valid.return_value = True
        mock_is_safe.return_value = True
        mock_sha256.return_value.hexdigest.return_value = 'code_hash'
        mock_create_globals.return_value = {}
        with patch('basis_vm.contract.deploy.exec') as mock_exec:
            mock_exec.side_effect = Exception("Unexpected exec error")

            code_str = """
class Contract:
    def __init__(self):
        self.state = 0
"""

            contract_id = 'contract_id'

            with self.assertRaises(Exception) as context:
                deploy_smart_contract(code_str, contract_id, auth_user='user')
            
            self.assertIn("Error ejecutando el contrato inteligente:", str(context.exception))
            mock_save_contract.assert_not_called()

    @patch('basis_vm.contract.deploy.is_code_valid')
    def test_deploy_smart_contract_non_string_code(self, mock_is_valid):
        """
        Test deployment with smart contract code that is not a string.
        """
        # Assume that is_code_valid will return False for non-string types
        mock_is_valid.return_value = False
        code_str = None  # Code is not a string
        contract_id = 'contract_id'

        with self.assertRaises(ValueError) as context:
            deploy_smart_contract(code_str, contract_id, auth_user='user')
        
        self.assertIn("El código del contrato inteligente no es válido.", str(context.exception))

    @patch('basis_vm.contract.deploy.save_smart_contract')
    @patch('basis_vm.contract.deploy.create_safe_globals')
    @patch('basis_vm.contract.deploy.is_code_safe')
    @patch('basis_vm.contract.deploy.is_code_valid')
    @patch('hashlib.sha256')
    def test_deploy_smart_contract_different_owner(self, mock_sha256, mock_is_valid, mock_is_safe, mock_create_globals, mock_save_contract):
        """
        Test deployment of a smart contract with a different user as the owner.
        """
        # Configure mocks for the success case
        mock_is_valid.return_value = True
        mock_is_safe.return_value = True
        mock_sha256.return_value.hexdigest.return_value = 'code_hash_2'
        mock_create_globals.return_value = {}

        code_str = """
class Contract:
    def __init__(self):
        self.state = 0
"""

        contract_id = 'contract_id_2'

        result = deploy_smart_contract(code_str, contract_id, auth_user='another_user')

        # Verify that the contract is saved with the correct owner
        mock_save_contract.assert_called_with(contract_id, {
            '_id': contract_id,
            'code': code_str,
            'hash': 'code_hash_2',
            'owner': 'another_user',
            'state': {'state': 0}
        })

if __name__ == '__main__':
    unittest.main()
