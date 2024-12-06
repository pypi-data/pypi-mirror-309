import builtins
import unittest

from basis_vm.utils.constants import (
    ALLOWED_BUILTINS, ALLOWED_LIBRARIES, CRITICAL_NAMES,
    MAX_INPUT_SIZE, CPU_LIMIT, MEMORY_LIMIT, INTERFACE_DIR, INTERFACE_MODULES,
)

class TestConstants(unittest.TestCase):
    def test_allowed_builtins(self):
        """
        Test that ALLOWED_BUILTINS contains expected built-in functions.
        """
        expected_builtins = {
            'abs', 'bool', 'dict', 'enumerate', 'float', 'int', 'len', 'list', 'tuple',
            'range', 'str', 'zip', 'max', 'min', 'sum', 'sorted', 'reversed', 'set',
            'isinstance', 'type', 'all', 'any', 'map', 'filter', 'round', 'pow',
            'ValueError', 'KeyError', 'IndexError', 'TypeError', 'ZeroDivisionError',
            'object', 'super', 'Exception', 'AttributeError', 'NameError',
        }
        self.assertEqual(ALLOWED_BUILTINS, expected_builtins)

    def test_allowed_libraries(self):
        """
        Test that ALLOWED_LIBRARIES contains expected libraries.
        """
        expected_libraries = {'hashlib', 'time', 'math'}
        self.assertEqual(ALLOWED_LIBRARIES, expected_libraries)

    def test_critical_names(self):
        """
        Test that CRITICAL_NAMES contains expected names.
        """
        expected_names = {'call_contract', 'auth_user', 'contract_owner'}
        expected_names.update(dir(builtins))
        self.assertEqual(CRITICAL_NAMES, expected_names)

    def test_resource_limits(self):
        """
        Test that resource limits are set to expected values.
        """
        self.assertEqual(MAX_INPUT_SIZE, 1024)
        self.assertEqual(CPU_LIMIT, 5)
        self.assertEqual(MEMORY_LIMIT, 100 * 1024 * 1024)

    def test_interface_dir(self):
        """
        Test that INTERFACE_DIR is set to the expected directory.
        """
        expected_dir = 'interfaces'
        self.assertEqual(INTERFACE_DIR, expected_dir)

    def test_interface_modules(self):
        """
        Test that INTERFACE_MODULES contains expected modules.
        """
        expected_modules = {'IBNS20', 'IBNS721', 'IBNS721Enumerable'}
        self.assertEqual(INTERFACE_MODULES, expected_modules)

if __name__ == '__main__':
    unittest.main()
