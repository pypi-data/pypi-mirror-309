import hashlib
import traceback

from basis_vm.config.logging import logger

from basis_vm.contract.call import call_contract
from basis_vm.contract.management import save_smart_contract

from basis_vm.security.validation import is_code_valid, is_code_safe

from basis_vm.execution.sandbox import create_safe_globals

def deploy_smart_contract(code, contract_id, auth_user=None):
    """
    Deploy a smart contract by storing its code and returning its identifier.

    Security Decisions:
    - Validates code syntax and safety before deployment.
    - Stores a hash of the code for integrity verification.

    Args:
        code (str): The smart contract code.
        contract_id (str): The unique identifier of the contract.
        auth_user (str): The authenticated user deploying the contract.

    Returns:
        str: The unique identifier of the deployed smart contract.
    """
    # Validate that the code is syntactically correct
    if not is_code_valid(code):
        raise ValueError("El código del contrato inteligente no es válido.")

    # Check for unauthorized code
    if not is_code_safe(code):
        raise ValueError("Se detectó código no seguro en el contrato inteligente.")

    # Verify code integrity
    code_hash = hashlib.sha256(code.encode('utf-8')).hexdigest()
    
    safe_globals = create_safe_globals(auth_user, auth_user, call_contract)

    exec_globals = safe_globals.copy()
    exec_locals = {}

    # Execute code to get the contract class
    try:
        exec(code, exec_globals, exec_locals)
    except Exception as e:
        logger.error(f"Error executing smart contract code: {e}\n\n{traceback.format_exc()}")
        raise Exception(f"Error ejecutando el contrato inteligente: {e}")

    # Retrieve the contract class
    contract_class = None
    for obj in list(exec_globals.values()) + list(exec_locals.values()):
        if isinstance(obj, type):
            contract_class = obj
            break
    if contract_class is None:
        raise ValueError("No se encontró una clase de contrato en el código.")

    # Create an instance to get the initial state
    contract_instance = contract_class()
    initial_state = contract_instance.__dict__

    # Store the contract in MongoDB
    contract_data = {
        '_id': contract_id,
        'code': code,
        'hash': code_hash,
        'owner': auth_user,
        'state': initial_state,
    }
    save_smart_contract(contract_id, contract_data)

    logger.info(f"Smart contract deployed with ID: {contract_id} by user: {auth_user}")

    return contract_id