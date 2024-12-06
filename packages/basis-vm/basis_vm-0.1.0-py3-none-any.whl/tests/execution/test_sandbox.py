import unittest
import types
import builtins

from types import MappingProxyType

from basis_vm.execution.sandbox import create_safe_globals
from basis_vm.utils.constants import ALLOWED_BUILTINS

class TestSandbox(unittest.TestCase):
    def setUp(self):
        self.auth_user = 'user'
        self.contract_owner = 'owner'
        self.execution_logs = []

        def dummy_call_contract(contract_name, *args, **kwargs):
            self.execution_logs.append((contract_name, args, kwargs))
            return "Contract called"

        self.dummy_call_contract = dummy_call_contract

        self.safe_globals = create_safe_globals(
            self.auth_user,
            self.contract_owner,
            self.dummy_call_contract
        )

    def test_create_safe_globals(self):
        """
        Test that the safe global environment is created correctly.
        """
        # Check that safe_globals is a MappingProxyType (read-only)
        self.assertIsInstance(self.safe_globals, MappingProxyType)

        # Check that critical variables are set correctly
        self.assertEqual(self.safe_globals['auth_user'], self.auth_user)
        self.assertEqual(self.safe_globals['contract_owner'], self.contract_owner)
        self.assertEqual(self.safe_globals['call_contract'], self.dummy_call_contract)

        # Check that built-ins are restricted
        allowed_builtins = self.safe_globals['__builtins__']
        self.assertTrue(hasattr(allowed_builtins, 'len'))
        self.assertFalse(hasattr(allowed_builtins, 'eval'))

    def test_safe_globals_immutable(self):
        """
        Test that safe_globals cannot be modified.
        """
        with self.assertRaises(TypeError):
            self.safe_globals['new_var'] = 'value'

        with self.assertRaises(TypeError):
            del self.safe_globals['auth_user']

    def test_only_allowed_builtins_available(self):
        """
        Test that only the allowed built-ins are available.
        """
        allowed_builtins = self.safe_globals['__builtins__']
        for name in ALLOWED_BUILTINS:
            self.assertTrue(hasattr(allowed_builtins, name), f"Built-in {name} should be available")

        # Exclude special attributes that are allowed
        special_attrs = {
            '__name__', '__doc__', '__package__', '__loader__', '__spec__', '__file__',
            '__build_class__', '__import__'
        }
        disallowed_builtins = (set(dir(builtins)) - set(ALLOWED_BUILTINS)) - special_attrs
        for name in disallowed_builtins:
            self.assertFalse(hasattr(allowed_builtins, name), f"Built-in {name} should not be available")

    def test_safe_import_allows_allowed_modules(self):
        """
        Test that safe_import allows importing allowed modules.
        """
        safe_builtins = self.safe_globals['__builtins__']
        safe_import = safe_builtins.__import__

        module = safe_import('hashlib')
        self.assertIsNotNone(module)
        result = module.sha256(b'test').hexdigest()
        self.assertIsInstance(result, str)

    def test_safe_import_blocks_disallowed_modules(self):
        """
        Test that safe_import blocks importing disallowed modules.
        """
        safe_builtins = self.safe_globals['__builtins__']
        safe_import = safe_builtins.__import__

        with self.assertRaises(ImportError):
            safe_import('os')

        with self.assertRaises(ImportError):
            safe_import('sys')

    def test_read_only_decorator(self):
        """
        Test that the read_only decorator sets the attribute correctly.
        """
        read_only = self.safe_globals['read_only']

        @read_only
        def sample_function():
            pass

        self.assertTrue(hasattr(sample_function, 'read_only'))
        self.assertTrue(sample_function.read_only)

    def test_owner_only_decorator(self):
        """
        Test that the owner_only decorator sets the attribute correctly.
        """
        owner_only = self.safe_globals['owner_only']

        @owner_only
        def sample_function():
            pass

        self.assertTrue(hasattr(sample_function, 'owner_only'))
        self.assertTrue(sample_function.owner_only)

    def test_call_contract_functionality(self):
        """
        Test that call_contract can be invoked within the sandbox.
        """
        call_contract = self.safe_globals['call_contract']
        result = call_contract('AnotherContract', arg1='value1')
        self.assertEqual(result, "Contract called")
        self.assertEqual(len(self.execution_logs), 1)
        contract_name, args, kwargs = self.execution_logs[0]
        self.assertEqual(contract_name, 'AnotherContract')
        self.assertEqual(kwargs, {'arg1': 'value1'})

    def test_sandbox_execution_isolated(self):
        """
        Test that code executed in the sandbox cannot access external variables.
        """
        code = '''
result = []
for i in range(5):
    result.append(i)
'''
        sandbox_globals = dict(self.safe_globals)
        exec(code, sandbox_globals)
        self.assertIn('result', sandbox_globals)
        self.assertEqual(sandbox_globals['result'], [0, 1, 2, 3, 4])

        # Asegurarse de que 'result' no está en el ámbito global externo
        self.assertFalse('result' in globals())

    def test_cannot_escape_sandbox(self):
        """
        Test that code in the sandbox cannot escape to access restricted attributes.
        """
        code = '''
try:
    __builtins__.__dict__['eval']('1+1')
    escaped = True
except (AttributeError, KeyError, NameError):
    escaped = False
'''

        sandbox_globals = dict(self.safe_globals)
        exec(code, sandbox_globals)
        self.assertFalse(sandbox_globals['escaped'])

    def test_execution_of_disallowed_operations(self):
        """
        Test that disallowed operations raise exceptions.
        """
        code = '''
result = eval('1+1')
'''

        sandbox_globals = dict(self.safe_globals)
        with self.assertRaises(NameError):
            exec(code, sandbox_globals)

    def test_execution_of_allowed_operations(self):
        """
        Test that allowed operations can be executed successfully.
        """
        code = '''
total = sum([1, 2, 3, 4])
'''

        sandbox_globals = dict(self.safe_globals)
        exec(code, sandbox_globals)
        self.assertEqual(sandbox_globals['total'], 10)

if __name__ == '__main__':
    unittest.main()
