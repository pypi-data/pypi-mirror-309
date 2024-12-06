import unittest
import os
from unittest.mock import patch, mock_open

from basis_vm.security.safe_import import safe_import

class TestSafeImport(unittest.TestCase):
    def test_safe_import_allowed_library(self):
        """
        Test importing allowed libraries.
        """
        module = safe_import('hashlib')
        self.assertIsNotNone(module)

        module = safe_import('math')
        self.assertIsNotNone(module)

    def test_safe_import_disallowed_library(self):
        """
        Test that importing disallowed libraries raises ImportError.
        """
        with self.assertRaises(ImportError):
            safe_import('os')

        with self.assertRaises(ImportError):
            safe_import('sys')

    @patch('basis_vm.security.safe_import.os.path.isfile', return_value=True)
    @patch('basis_vm.security.safe_import.is_code_valid', return_value=True)
    @patch('basis_vm.security.safe_import.is_code_safe', return_value=True)
    def test_safe_import_interface_bns20(self, mock_is_code_safe, mock_is_code_valid, mock_isfile):
        """
        Test importing BNS20 interface module.
        """
        module = safe_import('IBNS20')
        self.assertIsNotNone(module)

    @patch('basis_vm.security.safe_import.os.path.isfile', return_value=True)
    @patch('basis_vm.security.safe_import.is_code_valid', return_value=True)
    @patch('basis_vm.security.safe_import.is_code_safe', return_value=True)
    def test_safe_import_interface_bns721(self, mock_is_code_safe, mock_is_code_valid, mock_isfile):
        """
        Test importing BNS721 interface module.
        """
        module = safe_import('IBNS721')
        self.assertIsNotNone(module)

    @patch('basis_vm.security.safe_import.os.path.isfile', return_value=True)
    @patch('basis_vm.security.safe_import.is_code_valid', return_value=True)
    @patch('basis_vm.security.safe_import.is_code_safe', return_value=True)
    def test_safe_import_interface_bns721_enumerable(self, mock_is_code_safe, mock_is_code_valid, mock_isfile):
        """
        Test importing BNS721Enumerable interface module.
        """
        module = safe_import('IBNS721Enumerable')
        self.assertIsNotNone(module)

if __name__ == '__main__':
    unittest.main()
