import builtins

# Constants for security and resource limits
MAX_INPUT_SIZE = 1024  # Define a reasonable limit
CPU_LIMIT = 5  # seconds
MEMORY_LIMIT = 100 * 1024 * 1024  # 100MB

# Directory where interface modules are stored
INTERFACE_DIR = 'interfaces'

# Define allowed built-in functions (security decision to limit available functions)
ALLOWED_BUILTINS = {
    'abs', 'bool', 'dict', 'enumerate', 'float', 'int', 'len', 'list', 'tuple',
    'range', 'str', 'zip', 'max', 'min', 'sum', 'sorted', 'reversed', 'set',
    'isinstance', 'type', 'all', 'any', 'map', 'filter', 'round', 'pow',
    'ValueError', 'KeyError', 'IndexError', 'TypeError', 'ZeroDivisionError',
    'object', 'super', 'Exception', 'AttributeError', 'NameError',
}

# Define allowed method names (to prevent method invocation on disallowed objects)
ALLOWED_METHOD_NAMES = {
    'get', 'setdefault', 'update', 'keys', 'values', 'items', 'append', 'extend',
    'insert', 'remove', 'pop', 'popitem', 'clear', 'copy', 'count', 'index',
    'join', 'split', 'replace', 'strip', 'lstrip', 'rstrip', 'lower', 'upper',
    'startswith', 'endswith', 'find', 'rfind', 'format', 'hexdigest', 'time',
    'sha256', 
}

# Add allowed method names to the set of allowed built-ins
ALLOWED_FUNCTIONS = ALLOWED_BUILTINS.union({
    'call_contract'
})

# Define allowed magic methods
ALLOWED_MAGIC_METHODS = {
    '__init__', '__str__', '__repr__', '__eq__', '__lt__', '__le__', '__gt__', '__ge__'
}

# Define allowed libraries (empty by default for security)
ALLOWED_LIBRARIES = {
    'hashlib', 'time', 'math'
}

# Define allowed interface modules
INTERFACE_MODULES = {
    'IBNS20', 'IBNS721', 'IBNS721Enumerable'
}

# Define critical names and update with built-in names
CRITICAL_NAMES = {
    'call_contract', 'auth_user', 'contract_owner'
}
CRITICAL_NAMES.update(dir(builtins))