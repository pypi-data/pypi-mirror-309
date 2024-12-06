import types
import builtins

from types import MappingProxyType

from basis_vm.security.safe_import import safe_import
from basis_vm.security.decorators import read_only, owner_only

from basis_vm.utils.constants import ALLOWED_BUILTINS

def create_safe_globals(auth_user, contract_owner, call_contract) -> MappingProxyType:
    """
    Create a safe global environment for executing smart contracts.

    Security Decisions:
    - Restricts available built-in functions.
    - Provides safe functions for contract execution.
    - Restricts access to critical variables.

    Args:
        auth_user (str): The authenticated user executing the smart contract.
        contract_owner (str): The owner of the smart contract.

    Returns:
        MappingProxyType: A read-only mapping of safe global variables.
    """
    safe_builtins_module = types.ModuleType('builtins')
    for name in ALLOWED_BUILTINS:
        setattr(safe_builtins_module, name, getattr(builtins, name))
    safe_builtins_module.__build_class__ = builtins.__build_class__
    safe_builtins_module.__import__ = safe_import

    safe_globals = {
        '__builtins__': safe_builtins_module,
        'read_only': read_only,
        'owner_only': owner_only,
        'contract_owner': contract_owner,
        'auth_user': auth_user,
        'call_contract': call_contract,
    }

    return MappingProxyType(safe_globals)