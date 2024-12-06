import ast

from basis_vm.config.db import database

from basis_vm.utils.serialization import serialize_state, deserialize_state

def get_contract(contract_id: str) -> dict:
    """
    Retrieve a smart contract from the database.

    Args:
        contract_id (str): The identifier of the smart contract.

    Returns:
        dict: The smart contract document.
    """
    contract = database.smart_contracts.find_one({'_id': contract_id})
    if contract and 'state' in contract:
        contract['state'] = deserialize_state(contract['state'])
    return contract

def is_function_read_only(contract_id: str, function_name: str) -> bool:
    """
    Determine whether a function in a smart contract is read-only.

    Args:
        contract_id (str): The identifier of the smart contract.
        function_name (str): The name of the function to check.

    Returns:
        bool: True if the function is read-only, False otherwise.

    Raises:
        ValueError: If the contract does not exist or the function is not found.
        SyntaxError: If there is a syntax error in the contract code.
    """
    # Retrieve the contract from the database
    contract = get_contract(contract_id)
    if not contract:
        raise ValueError(f"Contract with ID '{contract_id}' does not exist.")

    code_str = contract['code']

    # Parse the code into an AST
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        raise SyntaxError(f"Syntax error in contract code: {e}")

    # Walk through the AST to find the function definition
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            # Check if the function has the 'read_only' decorator
            for decorator in node.decorator_list:
                # Handle decorators that are simple names
                if isinstance(decorator, ast.Name):
                    if decorator.id == 'read_only':
                        return True
                # Handle decorators that are calls (e.g., @read_only())
                elif isinstance(decorator, ast.Call):
                    if isinstance(decorator.func, ast.Name) and decorator.func.id == 'read_only':
                        return True
            return False  # Function found but does not have 'read_only' decorator

    raise ValueError(f"Function '{function_name}' not found in contract '{contract_id}'.")

def update_contract_state(contract_id: str, new_state: dict) -> None:
    """
    Update the state of a smart contract in the database.

    Args:
        contract_id (str): The identifier of the smart contract.
        new_state (dict): The new state to be stored.
    """
    if not isinstance(new_state, dict):
        raise TypeError("new_state must be a dictionary.")
    serialized_state = serialize_state(new_state)
    database.smart_contracts.update_one(
        {'_id': contract_id},
        {'$set': {'state': serialized_state}}
    )

def save_smart_contract(contract_id: str, contract_data: dict) -> None:
    """
    Save a smart contract to the database.

    Args:
        contract_id (str): The identifier of the smart contract.
        contract_data (dict): The data to be stored for the contract.

    Raises:
        TypeError: If contract_data is not a dictionary.
    """
    if not isinstance(contract_data, dict):
        raise TypeError("contract_data must be a dictionary.")
    # Serialize the state before saving
    contract_data['state'] = serialize_state(contract_data.get('state', {}))
    database.smart_contracts.replace_one(
        {'_id': contract_id},
        contract_data,
        upsert=True
    )
