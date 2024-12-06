import os
import types
import builtins

from basis_vm.security.validation import is_code_valid, is_code_safe

from basis_vm.security.decorators import read_only, owner_only

from basis_vm.utils.constants import ALLOWED_LIBRARIES, INTERFACE_MODULES, INTERFACE_DIR, ALLOWED_BUILTINS

# Define a custom import function to restrict library imports
def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name in ALLOWED_LIBRARIES:
        return __import__(name, globals, locals, fromlist, level)
    elif name in INTERFACE_MODULES:
        # Import the module from the 'interfaces' directory
        module_filename = f'{name}.py'
        module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', INTERFACE_DIR, module_filename))

        if not os.path.isfile(module_path):
            raise ImportError(f"Module {name} not found in interfaces.")

        with open(module_path, 'r') as f:
            code_str = f.read()

        # Validate the code
        if not is_code_valid(code_str):
            raise ImportError(f"Invalid code in interface module {name}.")
        if not is_code_safe(code_str):
            raise ImportError(f"Unsafe code in interface module {name}.")

        # Prepare a safe environment for executing the code
        # Define secure builtins module
        safe_builtins_module = types.ModuleType('builtins')
        for allowed_builtin in ALLOWED_BUILTINS:
            setattr(safe_builtins_module, allowed_builtin, getattr(builtins, allowed_builtin))
        safe_builtins_module.__build_class__ = builtins.__build_class__
        # Use the custom import function for importing libraries avoiding circular imports
        safe_builtins_module.__import__ = safe_import

        # Get 'auth_user', 'contract_owner', 'call_contract' from globals if available
        auth_user = globals.get('auth_user', None) if globals else None
        contract_owner = globals.get('contract_owner', None) if globals else None
        call_contract = globals.get('call_contract', None) if globals else None

        # Prepare a safe global environment
        safe_globals = {
            '__builtins__': safe_builtins_module,
            'read_only': read_only,
            'owner_only': owner_only,
            'auth_user': auth_user,
            'contract_owner': contract_owner,
            'call_contract': call_contract,
        }

        # Execute the code in a safe environment
        module = types.ModuleType(name)
        exec(code_str, safe_globals, module.__dict__)

        # Manually add the class to the module's namespace if not present
        if name not in module.__dict__:
            for obj_name, obj in module.__dict__.items():
                if isinstance(obj, type) and obj_name == name:
                    setattr(module, name, obj)
                    break

        return module
    else:
        raise ImportError(f"Librería no permitida: {name}")