import ast

from basis_vm.config.logging import logger

from basis_vm.utils.constants import ALLOWED_FUNCTIONS, ALLOWED_LIBRARIES, ALLOWED_MAGIC_METHODS, CRITICAL_NAMES, INTERFACE_MODULES

def is_code_valid(code_str):
    """
    Check if the code is valid Python code.

    Args:
        code_str (str): The code to validate.

    Returns:
        bool: True if the code is valid, False otherwise.
    """
    try:
        compile(code_str, '<string>', 'exec')
        return True
    except SyntaxError as e:
        logger.error(f"Syntax error in smart contract code: {e}")
        return False

def is_code_safe(code_str):
    """
    Analyze the AST of the code to ensure it does not contain unauthorized code.

    Args:
        code_str (str): The code to analyze.

    Returns:
        bool: True if the code is safe, False otherwise.
    """
    allowed_node_types = (
        # Module and Function Definitions
        ast.Module,
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.ClassDef,
        ast.Return,
        ast.Delete,
        ast.Assign,
        ast.AugAssign,
        ast.AnnAssign,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.If,
        ast.With,
        ast.AsyncWith,
        ast.Raise,
        ast.Try,
        ast.Assert,
        ast.Import,
        ast.ImportFrom,
        ast.Global,
        ast.Nonlocal,
        ast.Expr,
        ast.Pass,
        ast.Break,
        ast.Continue,
        # Expressions
        ast.BoolOp,
        ast.BinOp,
        ast.UnaryOp,
        ast.Lambda,
        ast.IfExp,
        ast.Dict,
        ast.Set,
        ast.ListComp,
        ast.SetComp,
        ast.DictComp,
        ast.GeneratorExp,
        ast.Await,
        ast.Yield,
        ast.YieldFrom,
        ast.Compare,
        ast.Call,
        ast.Num,
        ast.Str,
        ast.FormattedValue,
        ast.JoinedStr,
        ast.Bytes,
        ast.NameConstant,
        ast.Ellipsis,
        ast.Constant,
        ast.Attribute,
        ast.Subscript,
        ast.Starred,
        ast.Name,
        ast.List,
        ast.Tuple,
        ast.Slice,
        ast.ExtSlice,
        ast.Index,
        ast.comprehension,
        ast.alias,
        # Operator Nodes
        ast.Not,
        ast.LtE,
        ast.GtE,
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.Gt,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
        ast.Pow,
        ast.FloorDiv,
        ast.UAdd,
        ast.USub,
        ast.And,
        ast.Or,
        ast.Invert,
        ast.In,
        ast.NotIn,
        ast.Is,
        ast.IsNot,
        ast.BitAnd,
        ast.BitOr,
        ast.BitXor,
        ast.RShift,
        ast.LShift,
        # Context Nodes
        ast.Load,
        ast.Store,
        ast.Del,
        ast.AugLoad,
        ast.AugStore,
        ast.Param,
        # Additional Nodes
        ast.arguments,
        ast.arg,
        ast.keyword,
        ast.withitem,
        ast.ExceptHandler,
    )
    
    # Delete ast.Global from allowed_node_types
    allowed_node_types = tuple(node for node in allowed_node_types if node != ast.Global)

    try:
        tree = ast.parse(code_str)

        # Recolect the names of the defined functions
        defined_functions = set()

        for node in ast.walk(tree):
            if not isinstance(node, allowed_node_types):
                logger.error(f"Disallowed AST node type: {type(node).__name__}")
                return False
            if isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    if isinstance(target, ast.Name) and target.id in CRITICAL_NAMES:
                        logger.error(f"Intento de asignar a variable crítica: {target.id}")
                        return False
            elif isinstance(node, ast.FunctionDef):
                if node.name in CRITICAL_NAMES:
                    logger.error(f"Intento de definir función crítica: {node.name}")
                    return False
                elif node.name.startswith('__') and node.name.endswith('__'):
                    if node.name not in ALLOWED_MAGIC_METHODS:
                        logger.error(f"Intento de definir método mágico no permitido: {node.name}")
                        return False
                # Add the defined function to the set of defined functions
                defined_functions.add(node.name)
            elif isinstance(node, ast.ClassDef):
                # Prohibir el uso de metaclases
                for keyword in node.keywords:
                    if keyword.arg == 'metaclass':
                        logger.error("Uso de metaclases no permitido")
                        return False
                # Prohibir clases que heredan de tipos no permitidos
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id in CRITICAL_NAMES:
                        logger.error(f"Herencia de clase crítica no permitida: {base.id}")
                        return False
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                # Allow imports from ALLOWED_LIBRARIES and INTERFACE_MODULES
                for alias in node.names:
                    if alias.name not in ALLOWED_LIBRARIES and alias.name not in INTERFACE_MODULES:
                        logger.error(f"Disallowed import: {alias.name}")
                        return False
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    # Disallow calling functions not in ALLOWED_FUNCTIONS or defined in the code
                    if node.func.id not in ALLOWED_FUNCTIONS and node.func.id not in defined_functions:
                        logger.error(f"Disallowed function call: {node.func.id}")
                        return False
                elif isinstance(node.func, ast.Attribute):
                    method_name = node.func.attr
                    # Allow method calls to methods not starting with an underscore
                    if method_name.startswith('__') and method_name not in ALLOWED_MAGIC_METHODS:
                        logger.error(f"Disallowed method call to private method: {method_name}")
                        return False
                else:
                    logger.error("Disallowed function call via unsupported type")
                    return False
            elif isinstance(node, ast.Attribute):
                attr_name = node.attr
                if attr_name.startswith('__') and attr_name not in ALLOWED_MAGIC_METHODS:
                    logger.error(f"Disallowed attribute access: {attr_name}")
                    return False
            elif isinstance(node, ast.Global):
                logger.error("Uso de variables globales no permitido")
                return False
        return True
    except Exception as e:
        logger.error(f"Error analyzing code: {e}")
        return False