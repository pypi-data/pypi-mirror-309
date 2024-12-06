import unittest

from basis_vm.security.validation import is_code_valid, is_code_safe

class TestValidation(unittest.TestCase):
    def test_is_code_valid_with_valid_code(self):
        """
        Test that valid Python code passes validation.
        """
        code_str = "print('Hello, World!')"
        self.assertTrue(is_code_valid(code_str))

    def test_is_code_valid_with_invalid_code(self):
        """
        Test that invalid Python code does not pass validation.
        """
        code_str = "print('Hello, World!'"  # Missing closing parenthesis
        self.assertFalse(is_code_valid(code_str))

    def test_is_code_safe_with_safe_code(self):
        """
        Test that code without unsafe constructs passes security checks.
        """
        code_str = "x = 1 + 2"
        self.assertTrue(is_code_safe(code_str))

    def test_is_code_safe_with_unsafe_import(self):
        """
        Test that code importing disallowed libraries fails security checks.
        """
        code_str = "import os"
        self.assertFalse(is_code_safe(code_str))

    def test_is_code_safe_with_disallowed_function_call(self):
        """
        Test that code calling disallowed functions fails security checks.
        """
        code_str = "eval('print(1)')"
        self.assertFalse(is_code_safe(code_str))

    def test_is_code_safe_with_assignment_to_critical_variable(self):
        """
        Test that code assigning to critical variables fails security checks.
        """
        code_str = "__import__ = 'malicious'"
        self.assertFalse(is_code_safe(code_str))

    def test_is_code_safe_with_definition_of_critical_function(self):
        """
        Test that code defining critical functions fails security checks.
        """
        code_str = """
def exec():
    pass
"""
        self.assertFalse(is_code_safe(code_str))

    def test_is_code_safe_with_private_attribute_access(self):
        """
        Test that code accessing private attributes fails security checks.
        """
        code_str = """
class MyClass:
    def __init__(self):
        self.__secret = 42

    def get_secret(self):
        return self.__secret
"""
        self.assertFalse(is_code_safe(code_str))

    def test_is_code_safe_with_allowed_import(self):
        """
        Test that code importing allowed libraries passes security checks.
        """
        code_str = "import math"
        self.assertTrue(is_code_safe(code_str))

    def test_is_code_safe_with_allowed_function_call(self):
        """
        Test that code calling allowed functions passes security checks.
        """
        code_str = "len([1, 2, 3])"
        self.assertTrue(is_code_safe(code_str))

    def test_is_code_safe_with_disallowed_method_call(self):
        """
        Test that code calling private methods fails security checks.
        """
        code_str = """
class MyClass:
    def method(self):
        self.__private_method()
"""
        self.assertFalse(is_code_safe(code_str))

    def test_is_code_safe_with_exec_call(self):
        """
        Test that code using exec fails security checks.
        """
        code_str = "exec('print(1)')"
        self.assertFalse(is_code_safe(code_str))

    def test_is_code_safe_with_use_of_globals(self):
        """
        Test that code using global variables fails security checks.
        """
        code_str = """
def func():
    global x
    x = 5
"""
        self.assertFalse(is_code_safe(code_str))

    def test_is_code_safe_with_dangerous_attribute(self):
        """
        Test that code accessing dangerous attributes fails security checks.
        """
        code_str = "(1).__class__.__bases__"
        self.assertFalse(is_code_safe(code_str))

    def test_is_code_safe_with_metaclass(self):
        """
        Test that code using metaclasses fails security checks.
        """
        code_str = """
class Meta(type):
    pass

class MyClass(metaclass=Meta):
    pass
"""
        self.assertFalse(is_code_safe(code_str))

    def test_is_code_safe_with_magic_methods(self):
        """
        Test that code defining magic methods fails security checks.
        """
        code_str = """
class MyClass:
    def __getattr__(self, name):
        pass
"""
        self.assertFalse(is_code_safe(code_str))

    def test_is_code_safe_with_complex_but_safe_code(self):
        """
        Test that complex but safe code passes security checks.
        """
        code_str = """
def fibonacci(n):
    a, b = 0, 1
    result = []
    while len(result) < n:
        result.append(b)
        a, b = b, a + b
    return result
"""
        self.assertTrue(is_code_safe(code_str))

    def test_is_code_safe_with_list_comprehension(self):
        """
        Test that code with list comprehensions passes security checks.
        """
        code_str = "[x * x for x in range(10)]"
        self.assertTrue(is_code_safe(code_str))

    def test_is_code_safe_with_generator_expression(self):
        """
        Test that code with generator expressions passes security checks.
        """
        code_str = "(x * x for x in range(10))"
        self.assertTrue(is_code_safe(code_str))

    def test_is_code_safe_with_nested_functions(self):
        """
        Test that code with nested functions passes security checks.
        """
        code_str = """
def outer():
    def inner():
        return 42
    return inner()
"""
        self.assertTrue(is_code_safe(code_str))

    def test_is_code_safe_with_lambda_functions(self):
        """
        Test that code with lambda functions passes security checks.
        """
        code_str = "add = lambda x, y: x + y"
        self.assertTrue(is_code_safe(code_str))

    def test_is_code_safe_with_property_decorator(self):
        """
        Test that code with the @property decorator passes security checks.
        """
        code_str = """
class MyClass:
    @property
    def value(self):
        return 42
"""
        self.assertTrue(is_code_safe(code_str))

    def test_is_code_safe_with_bns_20_import(self):
        """
        Test that code importing bns_20 interface passes security checks.
        """
        code_str = """
import IBNS20
"""
        self.assertTrue(is_code_safe(code_str))

    def test_is_code_safe_with_bns_721_import(self):
        """
        Test that code importing bns_721 interface passes security checks.
        """
        code_str = """
import IBNS721
"""
        self.assertTrue(is_code_safe(code_str))

    def test_is_code_safe_with_bns_721_enumerable_import(self):
        """
        Test that code importing bns_721_enumerable interface passes security checks.
        """
        code_str = """
import IBNS721Enumerable
"""
        self.assertTrue(is_code_safe(code_str))

    def test_is_code_safe_with_inherit_from_ibns_721(self):
        """
        Test that code inheriting from IBNS721 interface passes security checks.
        """
        code_str = """
import IBNS721

class MyContract(IBNS721):
    def transferFrom(self, from_account, to, tokenId):
        pass
"""
        self.assertTrue(is_code_safe(code_str))

    def test_is_code_safe_with_inherit_from_ibns_20(self):
        """
        Test that code inheriting from IBNS20 interfaces passes security checks.
        """
        code_str = """
import IBNS20

class MyContract(IBNS20):
    def transfer(self, to, value):
        pass
"""
        self.assertTrue(is_code_safe(code_str))

    def test_is_code_safe_with_inherit_from_ibns_721_enumerable(self):
        """
        Test that code inheriting from IBNS721Enumerable interface passes security checks.
        """
        code_str = """
import IBNS721Enumerable

class MyContract(IBNS721Enumerable):
    def totalSupply(self):
        pass
"""
        self.assertTrue(is_code_safe(code_str))

if __name__ == '__main__':
    unittest.main()
