import json
import hashlib
import resource
import traceback
import multiprocessing

from copy import deepcopy

from basis_vm.config.logging import logger

from basis_vm.utils.constants import CPU_LIMIT

from basis_vm.contract.management import get_contract, update_contract_state

from basis_vm.utils.constants import CPU_LIMIT, MEMORY_LIMIT, MAX_INPUT_SIZE

from basis_vm.security.validation import is_code_valid, is_code_safe

from basis_vm.execution.sandbox import create_safe_globals

def contract_execution_target(code_str, state, function_name, args, kwargs, timeout, auth_user, child_conn, state_lock, contract_owner, contract_id):
    """
    Target function for executing the smart contract code in a separate process.

    Security Decisions:
    - Runs in a separate process to sandbox execution.
    - Enforces resource limits to prevent DoS attacks.
    - Validates user permissions based on decorators and ownership.
    - Uses safe_globals to restrict available built-ins.

    Args:
        code_str (str): The smart contract code.
        state (dict): The state dictionary to be used by the smart contract.
        function_name (str): The name of the function to execute.
        args (tuple): Positional arguments for the function.
        kwargs (dict): Keyword arguments for the function.
        timeout (int): Maximum time allowed for execution in seconds.
        auth_user (str): The authenticated user executing the function.
        child_conn (multiprocessing.Pipe): The connection for sending the result back.
        state_lock (multiprocessing.Lock): The lock for synchronizing state access.
        contract_owner (str): The owner of the smart contract.
        contract_id (str): The identifier of the smart contract.
    """
    try:
        # Enforce resource limits (UNIX-specific)
        try:
            # Set CPU time limit
            resource.setrlimit(resource.RLIMIT_CPU, (timeout, timeout))
            resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT, MEMORY_LIMIT))
        except ImportError:
            logger.warning("Resource module not available. Resource limits not enforced.")

        # Create safe_globals inside the child process
        safe_globals = create_safe_globals(auth_user, contract_owner, call_contract)

        # Prepare the execution environment
        exec_globals = safe_globals.copy()
        exec_locals = {}

        # Execute the contract code to get the class
        try:
            exec(code_str, exec_globals, exec_locals)
        except Exception as e:
            logger.error(f"Error executing smart contract code: {e}\n\n{traceback.format_exc()}")
            child_conn.send({'error': f"Error executing smart contract code: {e}"})
            return

        # Retrieve the contract class
        contract_class = None
        for obj in list(exec_globals.values()) + list(exec_locals.values()):
            if isinstance(obj, type):
                contract_class = obj
                break
        if contract_class is None:
            child_conn.send({'error': "No contract class found in the code."})
            return

        # Instantiate or restore the contract instance
        contract_instance = contract_class()
        if state:
            contract_instance.__dict__.update(state)

        # Retrieve the function
        func = getattr(contract_instance, function_name, None)
        if func is None:
            child_conn.send({'error': f"La función '{function_name}' no se encontró en el contrato inteligente."})
            return

        # Authentication and Authorization
        # Check for owner_only decorator
        if getattr(func, 'owner_only', False):
            if auth_user != contract_owner:
                child_conn.send({'error': "El usuario no está autorizado para ejecutar esta función (solo el propietario puede ejecutarla)."})
                return

        # Enforce read-only behavior
        if getattr(func, 'read_only', False):
            # Provide a copy of the state
            result = func(*args, **kwargs)
            child_conn.send({'status': 'success', 'result': result})
            logger.info(f"Function '{function_name}' executed successfully by user '{auth_user}'. Result: {result}")
        else:
            # Use a lock to prevent race conditions
            with state_lock:
                original_state = deepcopy(contract_instance.__dict__)
                try:
                    result = func(*args, **kwargs)
                    # Prepare the new state
                    new_state = contract_instance.__dict__
                    child_conn.send({'status': 'state_modified', 'state': new_state, 'result': result})
                    logger.info(f"Function '{function_name}' executed successfully by user '{auth_user}'. State modified.")
                except Exception as e:
                    # Revert the state in case of an error
                    contract_instance.__dict__.clear()
                    contract_instance.__dict__.update(original_state)
                    logger.error(f"Error during execution: {e}")
                    child_conn.send({'error': "Ocurrió un error durante la ejecución."})
    except Exception as e:
        logger.error(f"Execution error: {e}\n\n{traceback.format_exc()}")
        child_conn.send({'error': "Ocurrió un error durante la ejecución."})

def execute_smart_contract(code_str, state, function_name, args=None, kwargs=None, timeout=CPU_LIMIT, auth_user=None, contract_owner=None, contract_id=None):
    """
    Execute a function from the smart contract code in a secure environment.

    Security Decisions:
    - Validates code syntax and safety before execution.
    - Uses separate process for execution to sandbox code.
    - Passes a deep copy of the state to prevent unintended modifications.

    Args:
        code_str (str): The smart contract code.
        state (dict): The state dictionary to be used by the smart contract.
        function_name (str): The name of the function to execute.
        args (tuple, optional): Positional arguments for the function.
        kwargs (dict, optional): Keyword arguments for the function.
        timeout (int): Maximum time allowed for execution in seconds.
        auth_user (str): The authenticated user executing the function.
        contract_owner (str): The owner of the smart contract.
        contract_id (str): The identifier of the smart contract.

    Returns:
        Any: The result of the function execution, or None if the function modifies state.

    Raises:
        ValueError: If unsafe code is detected or the function is not found.
        Exception: If an error occurs during execution.
        TimeoutError: If execution exceeds the specified timeout.
    """
    # Validate that the code is syntactically correct
    if not is_code_valid(code_str):
        raise ValueError("El código del contrato inteligente no es válido.")

    # Check for unauthorized code
    if not is_code_safe(code_str):
        raise ValueError("Se detectó código no seguro en el contrato inteligente.")

    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}

    # Validate inputs
    if not isinstance(args, (list, tuple)):
        raise ValueError("Los argumentos deben ser una lista o tupla.")
    if not isinstance(kwargs, dict):
        raise ValueError("Los argumentos de palabra clave deben ser un diccionario.")

    # Limit input sizes
    if len(json.dumps(args)) > MAX_INPUT_SIZE or len(json.dumps(kwargs)) > MAX_INPUT_SIZE:
        raise ValueError("Los argumentos de entrada son demasiado grandes.")

    # Use a lock to prevent race conditions
    state_lock = multiprocessing.Lock()

    # Create a pipe for safe communication
    parent_conn, child_conn = multiprocessing.Pipe()

    # Execute the code in a separate process
    process = multiprocessing.Process(
        target=contract_execution_target,
        args=(
            code_str, state, function_name, args, kwargs, timeout,
            auth_user, child_conn, state_lock, contract_owner, contract_id
        )
    )
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.kill()
        process.join()
        raise TimeoutError("Tiempo de ejecución excedido.")

    # Get the result from the child process
    if parent_conn.poll():
        response = parent_conn.recv()
        if 'error' in response:
            raise Exception(response['error'])
        elif response['status'] == 'success':
            return response['result']
        elif response['status'] == 'state_modified':
            # Update the state in the parent process
            with state_lock:
                state.clear()
                state.update(response['state'])
            # Update the state in the database
            update_contract_state(contract_id, state)
            return response.get('result')
    else:
        raise Exception("No se recibió ninguna respuesta del proceso hijo.")

def call_smart_contract(contract_id, function_name, args=None, kwargs=None, timeout=CPU_LIMIT, auth_user=None):
    """
    Call a function from a deployed smart contract.

    Security Decisions:
    - Verifies code integrity before execution.
    - Ensures that the contract exists and is accessible.

    Args:
        contract_id (str): The identifier of the smart contract.
        function_name (str): The name of the function to call.
        args (tuple, optional): Positional arguments for the function.
        kwargs (dict, optional): Keyword arguments for the function.
        timeout (int): Maximum time allowed for execution in seconds.
        auth_user (str): The authenticated user executing the function.

    Returns:
        Any: The result of the function execution.

    Raises:
        KeyError: If the contract_id does not exist.
    """
    contract = get_contract(contract_id)
    if contract is None:
        raise KeyError(f"El contrato inteligente con ID '{contract_id}' no existe.")

    code_str = contract['code']

    # Verify code integrity
    code_hash = hashlib.sha256(code_str.encode('utf-8')).hexdigest()
    if code_hash != contract['hash']:
        raise ValueError("La verificación de integridad del código del contrato inteligente falló.")
    
    state = contract.get('state')
    contract_owner = contract['owner']

    return execute_smart_contract(
        code_str,
        state,
        function_name,
        args,
        kwargs,
        timeout,
        auth_user,
        contract_owner,
        contract_id
    )

# Define a function to call other smart contract functions
def call_contract(contract_id, function_name, args=None, kwargs=None, timeout=CPU_LIMIT, auth_user=None):
    """
    Call a function from another smart contract.

    Args:
        contract_id (str): The identifier of the smart contract.
        function_name (str): The name of the function to call.
        args (list): Positional arguments for the function.
        kwargs (dict): Keyword arguments for the function.
        timeout (int): Maximum time allowed for execution in seconds.
        auth_user (str): The authenticated user executing the function.

    Returns:
        Any: The result of the function execution.
    """
    return call_smart_contract(contract_id, function_name, args=args, kwargs=kwargs, timeout=timeout, auth_user=auth_user)