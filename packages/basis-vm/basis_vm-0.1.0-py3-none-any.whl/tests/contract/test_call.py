# test_contract_call.py

import unittest
from unittest.mock import patch, MagicMock
import hashlib
import multiprocessing

from basis_vm.contract.call import (
    contract_execution_target,
    execute_smart_contract,
    call_smart_contract,
    call_contract
)


class TestContractCall(unittest.TestCase):
    """
    Test suite for the basis_vm.contract.call module.
    This includes tests for executing smart contracts, calling deployed contracts,
    and interacting with other smart contracts.
    """

    # ===========================
    # Tests for execute_smart_contract
    # ===========================

    @patch('basis_vm.contract.call.update_contract_state')
    @patch('basis_vm.contract.call.is_code_safe')
    @patch('basis_vm.contract.call.is_code_valid')
    @patch('multiprocessing.Pipe')
    @patch('multiprocessing.Process')
    def test_execute_smart_contract_success(self, mock_process, mock_pipe, mock_is_valid, mock_is_safe, mock_update_state):
        """
        Test successful execution of a smart contract function that modifies the state.
        """
        # Configure mocks
        mock_is_valid.return_value = True
        mock_is_safe.return_value = True

        parent_conn = MagicMock()
        child_conn = MagicMock()
        mock_pipe.return_value = (parent_conn, child_conn)

        process_instance = MagicMock()
        mock_process.return_value = process_instance
        process_instance.is_alive.return_value = False  # Simulate that the process has finished

        # Simulate response from child process
        parent_conn.poll.return_value = True
        parent_conn.recv.return_value = {'status': 'state_modified', 'state': {'counter': 1}, 'result': None}

        code_str = """
class Contract:
    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter += 1
"""
        state = {'counter': 0}

        # Execute the function to test
        result = execute_smart_contract(
            code_str, state, 'increment',
            args=(), kwargs={}, auth_user='user',
            contract_owner='owner', contract_id='contract_id'
        )

        # Verifications
        self.assertEqual(state['counter'], 1)
        mock_update_state.assert_called_with('contract_id', {'counter': 1})
        self.assertIsNone(result)  # The function modifies state, does not return a value

    @patch('basis_vm.contract.call.update_contract_state')
    @patch('basis_vm.contract.call.is_code_safe')
    @patch('basis_vm.contract.call.is_code_valid')
    @patch('multiprocessing.Pipe')
    @patch('multiprocessing.Process')
    def test_execute_smart_contract_read_only(self, mock_process, mock_pipe, mock_is_valid, mock_is_safe, mock_update_state):
        """
        Test successful execution of a read-only smart contract function.
        """
        # Configure mocks
        mock_is_valid.return_value = True
        mock_is_safe.return_value = True

        parent_conn = MagicMock()
        child_conn = MagicMock()
        mock_pipe.return_value = (parent_conn, child_conn)

        process_instance = MagicMock()
        mock_process.return_value = process_instance
        process_instance.is_alive.return_value = False

        # Simulate response from child process
        parent_conn.poll.return_value = True
        parent_conn.recv.return_value = {'status': 'success', 'result': 42}

        code_str = """
class Contract:
    def __init__(self):
        self.counter = 42

    @read_only
    def get_counter(self):
        return self.counter
"""
        state = {'counter': 42}

        # Execute the function to test
        result = execute_smart_contract(
            code_str, state, 'get_counter',
            args=(), kwargs={}, auth_user='user',
            contract_owner='owner', contract_id='contract_id'
        )

        # Verifications
        self.assertEqual(result, 42)
        mock_update_state.assert_not_called()  # No state modification

    @patch('basis_vm.contract.call.execute_smart_contract')
    @patch('basis_vm.contract.call.get_contract')
    @patch('hashlib.sha256')
    def test_call_smart_contract_success(self, mock_sha256, mock_get_contract, mock_execute_smart_contract):
        """
        Test successful call to a deployed smart contract function.
        """
        # Configure mocks
        mock_get_contract.return_value = {
            'code': 'contract code',
            'hash': 'correct_hash',
            'owner': 'owner',
            'state': {}
        }
        mock_sha256.return_value.hexdigest.return_value = 'correct_hash'

        # Execute the function to test
        call_smart_contract('contract_id', 'function_name', args=(), kwargs={}, auth_user='user')

        # Verifications
        mock_execute_smart_contract.assert_called_with(
            'contract code', {}, 'function_name',
            (), {}, 5, 'user', 'owner', 'contract_id'
        )

    @patch('basis_vm.contract.call.call_smart_contract')
    def test_call_contract_success(self, mock_call_smart_contract):
        """
        Test successful call to another smart contract function.
        """
        # Execute the function to test
        call_contract('contract_id', 'function_name', args=(), kwargs={}, auth_user='user')

        # Verifications
        mock_call_smart_contract.assert_called_with(
            'contract_id', 'function_name',
            args=(), kwargs={}, timeout=5, auth_user='user'
        )

    @patch('basis_vm.contract.call.is_code_valid')
    def test_execute_smart_contract_invalid_code(self, mock_is_valid):
        """
        Test execution with invalid smart contract code.
        """
        mock_is_valid.return_value = False
        code_str = "invalid code"
        state = {}

        with self.assertRaises(ValueError) as context:
            execute_smart_contract(
                code_str, state, 'some_function',
                args=(), kwargs={}, auth_user='user',
                contract_owner='owner', contract_id='contract_id'
            )
        self.assertIn("El código del contrato inteligente no es válido.", str(context.exception))

    @patch('basis_vm.contract.call.is_code_valid')
    @patch('basis_vm.contract.call.is_code_safe')
    def test_execute_smart_contract_unsafe_code(self, mock_is_safe, mock_is_valid):
        """
        Test execution with unsafe smart contract code.
        """
        mock_is_valid.return_value = True
        mock_is_safe.return_value = False
        code_str = "unsafe code"
        state = {}

        with self.assertRaises(ValueError) as context:
            execute_smart_contract(
                code_str, state, 'some_function',
                args=(), kwargs={}, auth_user='user',
                contract_owner='owner', contract_id='contract_id'
            )
        self.assertIn("Se detectó código no seguro en el contrato inteligente.", str(context.exception))

    @patch('basis_vm.contract.call.execute_smart_contract', side_effect=TimeoutError("Tiempo de ejecución excedido."))
    @patch('basis_vm.contract.call.get_contract')
    @patch('hashlib.sha256')
    def test_execute_smart_contract_timeout(self, mock_sha256, mock_get_contract, mock_execute_smart_contract):
        """
        Test execution that exceeds the timeout.
        """
        mock_get_contract.return_value = {
            'code': 'contract code',
            'hash': 'correct_hash',
            'owner': 'owner',
            'state': {}
        }
        mock_sha256.return_value.hexdigest.return_value = 'correct_hash'

        with self.assertRaises(TimeoutError) as context:
            call_smart_contract('contract_id', 'function_name', args=(), kwargs={}, auth_user='user')

        self.assertIn("Tiempo de ejecución excedido.", str(context.exception))

    @patch('basis_vm.contract.call.execute_smart_contract', side_effect=Exception("Error de ejecución"))
    @patch('basis_vm.contract.call.get_contract')
    @patch('hashlib.sha256')
    def test_execute_smart_contract_execution_error(self, mock_sha256, mock_get_contract, mock_execute_smart_contract):
        """
        Test execution with an internal error in the contract function.
        """
        mock_get_contract.return_value = {
            'code': 'contract code',
            'hash': 'correct_hash',
            'owner': 'owner',
            'state': {}
        }
        mock_sha256.return_value.hexdigest.return_value = 'correct_hash'

        with self.assertRaises(Exception) as context:
            call_smart_contract('contract_id', 'function_name', args=(), kwargs={}, auth_user='user')

        self.assertIn("Error de ejecución", str(context.exception))

    @patch('basis_vm.contract.call.call_smart_contract', return_value=100)
    def test_call_contract_return_value(self, mock_call_smart_contract):
        """
        Test verifying the return value of `call_contract`.
        """
        result = call_contract('contract_id', 'function_name', args=(1, 2), kwargs={'key': 'value'}, auth_user='user')
        self.assertEqual(result, 100)
        mock_call_smart_contract.assert_called_with(
            'contract_id', 'function_name',
            args=(1, 2), kwargs={'key': 'value'},
            timeout=5, auth_user='user'
        )

    @patch('basis_vm.contract.call.execute_smart_contract')
    @patch('basis_vm.contract.call.get_contract')
    @patch('hashlib.sha256')
    def test_execute_smart_contract_function_not_found(self, mock_sha256, mock_get_contract, mock_execute_smart_contract):
        """
        Test execution of a function that does not exist in the smart contract.
        """
        mock_get_contract.return_value = {
            'code': 'contract code',
            'hash': 'correct_hash',
            'owner': 'owner',
            'state': {}
        }
        mock_sha256.return_value.hexdigest.return_value = 'correct_hash'
        mock_execute_smart_contract.side_effect = Exception("La función 'nonexistent_function' no se encontró en el contrato inteligente.")

        with self.assertRaises(Exception) as context:
            call_smart_contract('contract_id', 'nonexistent_function', args=(), kwargs={}, auth_user='user')

        self.assertIn("La función 'nonexistent_function' no se encontró en el contrato inteligente.", str(context.exception))

    @patch('basis_vm.contract.call.update_contract_state')
    @patch('basis_vm.contract.call.is_code_safe', return_value=True)
    @patch('basis_vm.contract.call.is_code_valid', return_value=True)
    @patch('multiprocessing.Pipe')
    @patch('multiprocessing.Process')
    def test_execute_smart_contract_authorization_failure(self, mock_process, mock_pipe, mock_is_valid, mock_is_safe, mock_update_state):
        """
        Test execution of a function protected by authorization where the user is not the owner.
        """
        # Configure mocks
        mock_is_valid.return_value = True
        mock_is_safe.return_value = True

        parent_conn = MagicMock()
        child_conn = MagicMock()
        mock_pipe.return_value = (parent_conn, child_conn)
        process_instance = MagicMock()
        mock_process.return_value = process_instance
        process_instance.is_alive.return_value = False
        parent_conn.poll.return_value = True
        error_message = "El usuario no está autorizado para ejecutar esta función (solo el propietario puede ejecutarla)."
        parent_conn.recv.return_value = {'error': error_message}

        code_str = """
class Contract:
    def __init__(self):
        self.counter = 0

    @owner_only
    def restricted_function(self):
        pass
"""
        state = {}

        with self.assertRaises(Exception) as context:
            execute_smart_contract(
                code_str, state, 'restricted_function',
                args=(), kwargs={}, auth_user='not_owner',  # User is not the owner
                contract_owner='owner', contract_id='contract_id'
            )

        self.assertIn(error_message, str(context.exception))
        mock_update_state.assert_not_called()

    def test_execute_smart_contract_invalid_args_type(self):
        """
        Test execution with invalid argument types.
        """
        code_str = """
class Contract:
    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter += 1
"""
        state = {}

        with self.assertRaises(ValueError) as context:
            execute_smart_contract(
                code_str, state, 'increment',
                args="not_a_tuple", kwargs={}, auth_user='user',
                contract_owner='owner', contract_id='contract_id'
            )
        self.assertIn("Los argumentos deben ser una lista o tupla.", str(context.exception))

    def test_execute_smart_contract_invalid_kwargs_type(self):
        """
        Test execution with invalid keyword argument types.
        """
        code_str = """
class Contract:
    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter += 1
"""
        state = {}

        with self.assertRaises(ValueError) as context:
            execute_smart_contract(
                code_str, state, 'increment',
                args=(), kwargs="not_a_dict", auth_user='user',
                contract_owner='owner', contract_id='contract_id'
            )
        self.assertIn("Los argumentos de palabra clave deben ser un diccionario.", str(context.exception))

    def test_execute_smart_contract_large_input(self):
        """
        Test execution with excessively large input arguments.
        """
        code_str = """
class Contract:
    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter += 1
"""
        state = {}
        large_args = ('a' * (10 ** 6),)  # Assuming MAX_INPUT_SIZE is smaller
        large_kwargs = {'key': 'b' * (10 ** 6)}

        with self.assertRaises(ValueError) as context:
            execute_smart_contract(
                code_str, state, 'increment',
                args=large_args, kwargs=large_kwargs, auth_user='user',
                contract_owner='owner', contract_id='contract_id'
            )
        self.assertIn("Los argumentos de entrada son demasiado grandes.", str(context.exception))

    @patch('basis_vm.contract.call.create_safe_globals', return_value={'call_contract': MagicMock()})
    @patch('basis_vm.contract.call.update_contract_state')
    @patch('basis_vm.contract.call.is_code_safe', return_value=True)
    @patch('basis_vm.contract.call.is_code_valid', return_value=True)
    @patch('multiprocessing.Pipe')
    @patch('multiprocessing.Process')
    def test_execute_smart_contract_read_only_behavior(self, mock_process, mock_pipe, mock_is_valid, mock_is_safe, mock_update_state, mock_create_globals):
        """
        Test that read-only functions behave correctly and do not modify the state.
        """
        # Configure mocks
        parent_conn = MagicMock()
        child_conn = MagicMock()
        mock_pipe.return_value = (parent_conn, child_conn)
        process_instance = MagicMock()
        mock_process.return_value = process_instance
        process_instance.is_alive.return_value = False  # Simulate that the process has finished
        parent_conn.poll.return_value = True
        parent_conn.recv.return_value = {'status': 'success', 'result': 'read_only_result'}

        code_str = """
class Contract:
    def __init__(self):
        self.counter = 0

    def get_value(self):
        return 'read_only_result'
"""
        state = {'counter': 0}

        # Execute the function to test
        result = execute_smart_contract(
            code_str, state, 'get_value',
            args=(), kwargs={}, auth_user='user',
            contract_owner='owner', contract_id='contract_id'
        )

        # Verifications
        self.assertEqual(result, 'read_only_result')
        mock_update_state.assert_not_called()

    @patch('basis_vm.contract.call.create_safe_globals')
    @patch('basis_vm.contract.call.update_contract_state')
    @patch('basis_vm.contract.call.is_code_safe', return_value=True)
    @patch('basis_vm.contract.call.is_code_valid', return_value=True)
    @patch('multiprocessing.Pipe')
    @patch('multiprocessing.Process')
    def test_execute_smart_contract_no_response(self, mock_process, mock_pipe, mock_is_valid, mock_is_safe, mock_update_state, mock_create_globals):
        """
        Test execution where no response is received from the child process.
        """
        # Configure mocks
        parent_conn = MagicMock()
        child_conn = MagicMock()
        mock_pipe.return_value = (parent_conn, child_conn)
        process_instance = MagicMock()
        mock_process.return_value = process_instance
        process_instance.is_alive.return_value = False  # Simulate that the process has finished
        parent_conn.poll.return_value = False  # No response

        code_str = """
class Contract:
    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter += 1
"""
        state = {'counter': 0}

        with self.assertRaises(Exception) as context:
            execute_smart_contract(
                code_str, state, 'increment',
                args=(), kwargs={}, auth_user='user',
                contract_owner='owner', contract_id='contract_id'
            )

        self.assertIn("No se recibió ninguna respuesta del proceso hijo.", str(context.exception))
        mock_update_state.assert_not_called()

    @patch('basis_vm.contract.call.create_safe_globals', return_value={'call_contract': MagicMock()})
    @patch('basis_vm.contract.call.update_contract_state')
    @patch('basis_vm.contract.call.is_code_safe', return_value=True)
    @patch('basis_vm.contract.call.is_code_valid', return_value=True)
    @patch('multiprocessing.Pipe')
    @patch('multiprocessing.Process')
    def test_execute_smart_contract_exception_handling(self, mock_process, mock_pipe, mock_is_valid, mock_is_safe, mock_update_state, mock_create_globals):
        """
        Test general exception handling during smart contract execution.
        """
        # Configure mocks to raise an exception
        parent_conn = MagicMock()
        child_conn = MagicMock()
        mock_pipe.return_value = (parent_conn, child_conn)
        process_instance = MagicMock()
        mock_process.return_value = process_instance
        process_instance.is_alive.return_value = False  # Simulate that the process has finished
        parent_conn.poll.return_value = True
        parent_conn.recv.side_effect = Exception("Error inesperado")

        code_str = """
class Contract:
    def __init__(self):
        self.counter = 0

    def increment(self):
        self.counter += 1
"""
        state = {'counter': 0}

        with self.assertRaises(Exception) as context:
            execute_smart_contract(
                code_str, state, 'increment',
                args=(), kwargs={}, auth_user='user',
                contract_owner='owner', contract_id='contract_id'
            )

        self.assertIn("Error inesperado", str(context.exception))
        mock_update_state.assert_not_called()

    # ===========================
    # Tests for contract_execution_target
    # ===========================

    @patch('resource.setrlimit')
    @patch('basis_vm.contract.call.logger')
    @patch('basis_vm.contract.call.create_safe_globals')
    @patch('basis_vm.contract.call.call_contract')
    def test_contract_execution_target_success(self, mock_call_contract, mock_create_globals, mock_logger, mock_setrlimit):
        """
        Test successful execution within contract_execution_target.
        """
        code_str = """
class Contract:
    def __init__(self):
        self.value = 10

    def add(self, amount):
        self.value += amount
"""
        state = {'value': 10}
        function_name = 'add'
        args = (5,)
        kwargs = {}
        timeout = 5
        auth_user = 'user'
        contract_owner = 'owner'
        contract_id = 'contract_id'

        # Configure mocks
        mock_create_globals.return_value = {'call_contract': mock_call_contract}

        # Mock child_conn and state_lock
        child_conn = MagicMock()
        state_lock = MagicMock()

        # Execute the function
        contract_execution_target(
            code_str, state, function_name, args, kwargs, timeout, auth_user,
            child_conn, state_lock, contract_owner, contract_id
        )

        # Verify that the modified state was sent
        expected_state = {'value': 15}
        child_conn.send.assert_called_with({'status': 'state_modified', 'state': expected_state, 'result': None})
        mock_logger.info.assert_called_with(f"Function '{function_name}' executed successfully by user '{auth_user}'. State modified.")

    @patch('resource.setrlimit')
    @patch('basis_vm.contract.call.logger')
    @patch('basis_vm.contract.call.create_safe_globals')
    @patch('basis_vm.contract.call.call_contract')
    def test_contract_execution_target_read_only(self, mock_call_contract, mock_create_globals, mock_logger, mock_setrlimit):
        """
        Test execution of a read-only function within contract_execution_target.
        """
        code_str = """
class Contract:
    def __init__(self):
        self.value = 42

    @read_only
    def get_value(self):
        return self.value
"""
        state = {'value': 42}
        function_name = 'get_value'
        args = ()
        kwargs = {}
        timeout = 5
        auth_user = 'user'
        contract_owner = 'owner'
        contract_id = 'contract_id'

        # Define the read_only decorator
        def read_only(func):
            func.read_only = True
            return func

        # Configure mocks
        mock_create_globals.return_value = {
            'read_only': read_only,
            'call_contract': mock_call_contract
        }

        # Mock child_conn and state_lock
        child_conn = MagicMock()
        state_lock = MagicMock()

        # Execute the function
        contract_execution_target(
            code_str, state, function_name, args, kwargs, timeout, auth_user,
            child_conn, state_lock, contract_owner, contract_id
        )

        # Verify that the correct result was sent
        child_conn.send.assert_called_with({'status': 'success', 'result': 42})
        mock_logger.info.assert_called_with(f"Function '{function_name}' executed successfully by user '{auth_user}'. Result: 42")

    @patch('resource.setrlimit')
    @patch('basis_vm.contract.call.logger')
    def test_contract_execution_target_function_not_found(self, mock_logger, mock_setrlimit):
        """
        Test when the specified function is not found in the contract.
        """
        code_str = """
class Contract:
    def __init__(self):
        self.value = 42
"""
        state = {'value': 42}
        function_name = 'nonexistent_function'
        args = ()
        kwargs = {}
        timeout = 5
        auth_user = 'user'
        contract_owner = 'owner'
        contract_id = 'contract_id'

        # Mock child_conn and state_lock
        child_conn = MagicMock()
        state_lock = MagicMock()
        safe_globals = {}

        # Execute the function
        contract_execution_target(
            code_str, state, function_name, args, kwargs, timeout, auth_user,
            child_conn, state_lock, contract_owner, contract_id
        )

        # Verify that the appropriate error was sent
        child_conn.send.assert_called_with({'error': "La función 'nonexistent_function' no se encontró en el contrato inteligente."})

    @patch('resource.setrlimit')
    @patch('basis_vm.contract.call.logger')
    def test_contract_execution_target_unauthorized_user(self, mock_logger, mock_setrlimit):
        """
        Test execution of a function protected by owner_only without proper authorization.
        """
        code_str = """
class Contract:
    def __init__(self):
        self.value = 0

    @owner_only
    def set_value(self, new_value):
        self.value = new_value
"""
        state = {'value': 0}
        function_name = 'set_value'
        args = (100,)
        kwargs = {}
        timeout = 5
        auth_user = 'not_owner'
        contract_owner = 'owner'
        contract_id = 'contract_id'

        # Define the owner_only decorator
        def owner_only(func):
            func.owner_only = True
            return func

        # Mock child_conn and state_lock
        child_conn = MagicMock()
        state_lock = MagicMock()

        # Create safe_globals with owner_only decorator
        safe_globals = {'owner_only': owner_only}

        # Execute the function
        contract_execution_target(
            code_str, state, function_name, args, kwargs, timeout, auth_user,
            child_conn, state_lock, contract_owner, contract_id
        )

        # Verify that the authorization error was sent
        child_conn.send.assert_called_with({'error': "El usuario no está autorizado para ejecutar esta función (solo el propietario puede ejecutarla)."})

    @patch('resource.setrlimit')
    @patch('basis_vm.contract.call.logger')
    def test_contract_execution_target_exception_in_function(self, mock_logger, mock_setrlimit):
        """
        Test handling of exceptions raised within the contract function during execution.
        """
        code_str = """
class Contract:
    def __init__(self):
        self.value = 0

    def error_function(self):
        raise ValueError("An error occurred")
"""
        state = {'value': 0}
        function_name = 'error_function'
        args = ()
        kwargs = {}
        timeout = 5
        auth_user = 'user'
        contract_owner = 'owner'
        contract_id = 'contract_id'

        # Mock child_conn and state_lock
        child_conn = MagicMock()
        state_lock = MagicMock()
        safe_globals = {}

        # Execute the function
        contract_execution_target(
            code_str, state, function_name, args, kwargs, timeout, auth_user,
            child_conn, state_lock, contract_owner, contract_id
        )

        # Verify that the execution error was sent
        child_conn.send.assert_called_with({'error': "Ocurrió un error durante la ejecución."})

    @patch('resource.setrlimit')
    @patch('basis_vm.contract.call.logger')
    def test_contract_execution_target_invalid_code(self, mock_logger, mock_setrlimit):
        """
        Test execution with invalid contract code in contract_execution_target.
        """
        code_str = "invalid code"
        state = {}
        function_name = 'some_function'
        args = ()
        kwargs = {}
        timeout = 5
        auth_user = 'user'
        contract_owner = 'owner'
        contract_id = 'contract_id'

        # Mock child_conn and state_lock
        child_conn = MagicMock()
        state_lock = MagicMock()
        safe_globals = {}

        # Execute the function
        contract_execution_target(
            code_str, state, function_name, args, kwargs, timeout, auth_user,
            child_conn, state_lock, contract_owner, contract_id
        )

        # Verify that a syntax error was sent
        self.assertTrue(child_conn.send.call_args[0][0]['error'].startswith("Error executing smart contract code:"))

    # ===========================
    # Additional Tests for Robustness
    # ===========================

    @patch('basis_vm.contract.call.update_contract_state')
    @patch('basis_vm.contract.call.is_code_safe')
    @patch('basis_vm.contract.call.is_code_valid')
    @patch('multiprocessing.Pipe')
    @patch('multiprocessing.Process')
    def test_execute_smart_contract_no_contract_found(self, mock_process, mock_pipe, mock_is_valid, mock_is_safe, mock_update_state):
        """
        Test execution when the specified contract does not exist.
        """
        # Configure mocks
        mock_is_valid.return_value = True
        mock_is_safe.return_value = True

        parent_conn = MagicMock()
        child_conn = MagicMock()
        mock_pipe.return_value = (parent_conn, child_conn)

        process_instance = MagicMock()
        mock_process.return_value = process_instance
        process_instance.is_alive.return_value = False

        # Simulate response from child process indicating no contract class found
        parent_conn.poll.return_value = True
        parent_conn.recv.return_value = {'error': "No contract class found in the code."}

        code_str = """
def standalone_function():
    pass
"""
        state = {}

        # Execute the function to test
        with self.assertRaises(Exception) as context:
            execute_smart_contract(
                code_str, state, 'standalone_function',
                args=(), kwargs={}, auth_user='user',
                contract_owner='owner', contract_id='contract_id'
            )

        self.assertIn("No contract class found in the code.", str(context.exception))
        mock_update_state.assert_not_called()

    @patch('basis_vm.contract.call.update_contract_state')
    @patch('basis_vm.contract.call.is_code_safe')
    @patch('basis_vm.contract.call.is_code_valid')
    @patch('multiprocessing.Pipe')
    @patch('multiprocessing.Process')
    def test_execute_smart_contract_no_owner_only_decorator(self, mock_process, mock_pipe, mock_is_valid, mock_is_safe, mock_update_state):
        """
        Test execution of a function without owner_only decorator.
        """
        # Configure mocks
        mock_is_valid.return_value = True
        mock_is_safe.return_value = True

        parent_conn = MagicMock()
        child_conn = MagicMock()
        mock_pipe.return_value = (parent_conn, child_conn)

        process_instance = MagicMock()
        mock_process.return_value = process_instance
        process_instance.is_alive.return_value = False

        # Simulate successful state modification
        parent_conn.poll.return_value = True
        parent_conn.recv.return_value = {'status': 'state_modified', 'state': {'counter': 2}, 'result': None}

        code_str = """
class Contract:
    def __init__(self):
        self.counter = 1

    def increment(self):
        self.counter += 1
"""
        state = {'counter': 1}

        # Execute the function to test
        result = execute_smart_contract(
            code_str, state, 'increment',
            args=(), kwargs={}, auth_user='user',
            contract_owner='owner', contract_id='contract_id'
        )

        # Verifications
        self.assertEqual(state['counter'], 2)
        mock_update_state.assert_called_with('contract_id', {'counter': 2})
        self.assertIsNone(result)  # The function modifies state, does not return a value

    # ===========================
    # Tests for is_function_read_only
    # ===========================

    @patch('basis_vm.contract.management.get_contract')
    def test_is_function_read_only_true(self, mock_get_contract):
        """
        Test that is_function_read_only returns True when the function has @read_only decorator.
        """
        from basis_vm.contract.management import is_function_read_only

        code_str = """
def not_target_function():
    pass

@read_only
def target_function():
    pass
"""
        mock_get_contract.return_value = {'code': code_str}

        # Execute the function to test
        result = is_function_read_only('contract_id', 'target_function')

        # Verifications
        self.assertTrue(result)
        mock_get_contract.assert_called_once_with('contract_id')

    @patch('basis_vm.contract.management.get_contract')
    def test_is_function_read_only_false(self, mock_get_contract):
        """
        Test that is_function_read_only returns False when the function does not have @read_only decorator.
        """
        from basis_vm.contract.management import is_function_read_only

        code_str = """
def target_function():
    pass
"""
        mock_get_contract.return_value = {'code': code_str}

        # Execute the function to test
        result = is_function_read_only('contract_id', 'target_function')

        # Verifications
        self.assertFalse(result)
        mock_get_contract.assert_called_once_with('contract_id')

    @patch('basis_vm.contract.management.get_contract')
    def test_is_function_read_only_function_not_found(self, mock_get_contract):
        """
        Test that is_function_read_only raises ValueError when the function is not found.
        """
        from basis_vm.contract.management import is_function_read_only

        code_str = """
def another_function():
    pass
"""
        mock_get_contract.return_value = {'code': code_str}

        # Execute the function to test
        with self.assertRaises(ValueError) as context:
            is_function_read_only('contract_id', 'nonexistent_function')

        # Verifications
        self.assertIn("Function 'nonexistent_function' not found", str(context.exception))
        mock_get_contract.assert_called_once_with('contract_id')

    @patch('basis_vm.contract.management.get_contract')
    def test_is_function_read_only_contract_not_found(self, mock_get_contract):
        """
        Test that is_function_read_only raises ValueError when the contract is not found.
        """
        from basis_vm.contract.management import is_function_read_only

        mock_get_contract.return_value = None

        # Execute the function to test
        with self.assertRaises(ValueError) as context:
            is_function_read_only('nonexistent_contract', 'some_function')

        # Verifications
        self.assertIn("Contract with ID 'nonexistent_contract' does not exist.", str(context.exception))
        mock_get_contract.assert_called_once_with('nonexistent_contract')

    @patch('basis_vm.contract.management.get_contract')
    def test_is_function_read_only_syntax_error(self, mock_get_contract):
        """
        Test that is_function_read_only raises SyntaxError when the contract code has a syntax error.
        """
        from basis_vm.contract.management import is_function_read_only

        code_str = """
def target_function()
    pass
"""
        mock_get_contract.return_value = {'code': code_str}

        # Execute the function to test
        with self.assertRaises(SyntaxError) as context:
            is_function_read_only('contract_id', 'target_function')

        # Verifications
        self.assertIn("Syntax error in contract code", str(context.exception))
        mock_get_contract.assert_called_once_with('contract_id')

    @patch('basis_vm.contract.management.get_contract')
    def test_is_function_read_only_with_complex_decorator(self, mock_get_contract):
        """
        Test that is_function_read_only correctly identifies @read_only used with parentheses.
        """
        from basis_vm.contract.management import is_function_read_only

        code_str = """
@read_only()
def target_function():
    pass
"""
        mock_get_contract.return_value = {'code': code_str}

        # Execute the function to test
        result = is_function_read_only('contract_id', 'target_function')

        # Verifications
        self.assertTrue(result)
        mock_get_contract.assert_called_once_with('contract_id')

    @patch('basis_vm.contract.management.get_contract')
    def test_is_function_read_only_decorator_alias(self, mock_get_contract):
        """
        Test that is_function_read_only handles decorator aliases appropriately.
        Note: The current implementation may not handle aliases, so it should return False.
        """
        from basis_vm.contract.management import is_function_read_only

        code_str = """
read_only_alias = read_only

@read_only_alias
def target_function():
    pass
"""
        mock_get_contract.return_value = {'code': code_str}

        # Execute the function to test
        result = is_function_read_only('contract_id', 'target_function')

        # Verifications
        self.assertFalse(result)  # Current implementation does not handle aliases
        mock_get_contract.assert_called_once_with('contract_id')

    # ===========================
    # Additional Robustness Tests
    # ===========================

    @patch('basis_vm.contract.call.update_contract_state')
    @patch('basis_vm.contract.call.is_code_safe')
    @patch('basis_vm.contract.call.is_code_valid')
    @patch('multiprocessing.Pipe')
    @patch('multiprocessing.Process')
    def test_execute_smart_contract_no_contract_found(self, mock_process, mock_pipe, mock_is_valid, mock_is_safe, mock_update_state):
        """
        Test execution when the specified contract does not exist.
        """
        # Configure mocks
        mock_is_valid.return_value = True
        mock_is_safe.return_value = True

        parent_conn = MagicMock()
        child_conn = MagicMock()
        mock_pipe.return_value = (parent_conn, child_conn)

        process_instance = MagicMock()
        mock_process.return_value = process_instance
        process_instance.is_alive.return_value = False

        # Simulate response from child process indicating no contract class found
        parent_conn.poll.return_value = True
        parent_conn.recv.return_value = {'error': "No contract class found in the code."}

        code_str = """
def standalone_function():
    pass
"""
        state = {}

        # Execute the function to test
        with self.assertRaises(Exception) as context:
            execute_smart_contract(
                code_str, state, 'standalone_function',
                args=(), kwargs={}, auth_user='user',
                contract_owner='owner', contract_id='contract_id'
            )

        self.assertIn("No contract class found in the code.", str(context.exception))
        mock_update_state.assert_not_called()

    @patch('basis_vm.contract.call.update_contract_state')
    @patch('basis_vm.contract.call.is_code_safe')
    @patch('basis_vm.contract.call.is_code_valid')
    @patch('multiprocessing.Pipe')
    @patch('multiprocessing.Process')
    def test_execute_smart_contract_no_owner_only_decorator(self, mock_process, mock_pipe, mock_is_valid, mock_is_safe, mock_update_state):
        """
        Test execution of a function without owner_only decorator.
        """
        # Configure mocks
        mock_is_valid.return_value = True
        mock_is_safe.return_value = True

        parent_conn = MagicMock()
        child_conn = MagicMock()
        mock_pipe.return_value = (parent_conn, child_conn)

        process_instance = MagicMock()
        mock_process.return_value = process_instance
        process_instance.is_alive.return_value = False

        # Simulate successful state modification
        parent_conn.poll.return_value = True
        parent_conn.recv.return_value = {'status': 'state_modified', 'state': {'counter': 2}, 'result': None}

        code_str = """
class Contract:
    def __init__(self):
        self.counter = 1

    def increment(self):
        self.counter += 1
"""
        state = {'counter': 1}

        # Execute the function to test
        result = execute_smart_contract(
            code_str, state, 'increment',
            args=(), kwargs={}, auth_user='user',
            contract_owner='owner', contract_id='contract_id'
        )

        # Verifications
        self.assertEqual(state['counter'], 2)
        mock_update_state.assert_called_with('contract_id', {'counter': 2})
        self.assertIsNone(result)  # The function modifies state, does not return a value

    # ===========================
    # Tests for the New Function is_function_read_only
    # ===========================

    @patch('basis_vm.contract.management.get_contract')
    def test_is_function_read_only_missing_decorator(self, mock_get_contract):
        """
        Test that is_function_read_only returns False when the decorator is missing.
        """
        from basis_vm.contract.management import is_function_read_only

        code_str = """
def target_function():
    pass
"""
        mock_get_contract.return_value = {'code': code_str}

        # Execute the function to test
        result = is_function_read_only('contract_id', 'target_function')

        # Verifications
        self.assertFalse(result)
        mock_get_contract.assert_called_once_with('contract_id')

    # ===========================
    # Clean Up
    # ===========================

    def tearDown(self):
        """
        Clean up after each test method.
        """
        pass  # Add any necessary cleanup here


if __name__ == '__main__':
    unittest.main()
