import os
import sys
import logging
import unittest
import importlib

from unittest.mock import patch, MagicMock

class TestLoggingConfiguration(unittest.TestCase):
    def setUp(self):
        """
        Set up before each test by deleting the logging configuration module and resetting logging handlers.
        """
        if 'basis_vm.config.logging' in sys.modules:
            del sys.modules['basis_vm.config.logging']

        # Reset the _basis_vm_configured flag
        root_logger = logging.getLogger()
        if hasattr(root_logger, '_basis_vm_configured'):
            delattr(root_logger, '_basis_vm_configured')

        # Remove all handlers associated with the root logger
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
            handler.close()

        # Shutdown logging to close all file handlers
        logging.shutdown()
        
    def tearDown(self):
        """
        Clean up after each test by deleting the logging configuration module and resetting logging handlers.
        """
        if 'basis_vm.config.logging' in sys.modules:
            del sys.modules['basis_vm.config.logging']

        # Remove all handlers associated with the root logger object
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
            handler.close()

        # Reset the _basis_vm_configured flag
        if hasattr(root_logger, '_basis_vm_configured'):
            delattr(root_logger, '_basis_vm_configured')

        # Shutdown logging to close all file handlers
        logging.shutdown()

    def test_logging_setup(self):
        """
        Test that the logging configuration is set up correctly.
        """
        with patch('logging.FileHandler', autospec=True) as mock_FileHandler, \
             patch('logging.StreamHandler', autospec=True) as mock_StreamHandler, \
             patch('logging.basicConfig', autospec=True) as mock_basicConfig:

            mock_file_handler_instance = MagicMock()
            mock_stream_handler_instance = MagicMock()
            mock_FileHandler.return_value = mock_file_handler_instance
            mock_StreamHandler.return_value = mock_stream_handler_instance

            # Ensure the module is not imported before the patches
            if 'basis_vm.config.logging' in sys.modules:
                del sys.modules['basis_vm.config.logging']

            # Import the logging module to trigger the configuration
            import basis_vm.config.logging as logging_config

            expected_log_filename = os.path.abspath(os.path.join(os.path.dirname(logging_config.__file__), '../shared', "vm.log"))

            mock_FileHandler.assert_called_once_with(expected_log_filename)
            mock_StreamHandler.assert_called_once()

            mock_basicConfig.assert_called_once_with(
                level=logging.INFO,
                format='%(asctime)s [%(levelname)s] - %(message)s',
                handlers=[mock_file_handler_instance, mock_stream_handler_instance]
            )

    def test_logging_not_reconfigured_if_already_configured(self):
        """
        Test that the logging configuration is not reconfigured if already set up.
        """
        with patch('logging.basicConfig', autospec=True) as mock_basicConfig:

            # Ensure the module is not imported before the patches
            if 'basis_vm.config.logging' in sys.modules:
                del sys.modules['basis_vm.config.logging']

            # First import to configure logging
            import basis_vm.config.logging

            # Second import should not reconfigure logging
            importlib.reload(sys.modules['basis_vm.config.logging'])

            # Assert that basicConfig was called only once
            mock_basicConfig.assert_called_once()

    def test_logging_handlers_order(self):
        """
        Test that the handlers are passed to basicConfig in the correct order.
        """
        with patch('logging.FileHandler', autospec=True) as mock_FileHandler, \
             patch('logging.StreamHandler', autospec=True) as mock_StreamHandler, \
             patch('logging.basicConfig', autospec=True) as mock_basicConfig:

            mock_file_handler_instance = MagicMock()
            mock_stream_handler_instance = MagicMock()
            mock_FileHandler.return_value = mock_file_handler_instance
            mock_StreamHandler.return_value = mock_stream_handler_instance

            # Ensure the module is not imported before the patches
            if 'basis_vm.config.logging' in sys.modules:
                del sys.modules['basis_vm.config.logging']

            import basis_vm.config.logging

            mock_basicConfig.assert_called_once_with(
                level=logging.INFO,
                format='%(asctime)s [%(levelname)s] - %(message)s',
                handlers=[mock_file_handler_instance, mock_stream_handler_instance]
            )

    def test_logging_file_handler_failure(self):
        """
        Test that an exception in FileHandler creation is handled gracefully.
        """
        # Ensure the module is not imported before the patches
        if 'basis_vm.config.logging' in sys.modules:
            del sys.modules['basis_vm.config.logging']

        # Restart the logging configuration
        root_logger = logging.getLogger()
        if hasattr(root_logger, '_basis_vm_configured'):
            delattr(root_logger, '_basis_vm_configured')

        # Remove all handlers associated with the root logger object
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
            handler.close()

        # Apply patches to simulate a failure in FileHandler creation
        with patch('logging.FileHandler', side_effect=Exception("Failed to create FileHandler")), \
             patch('logging.StreamHandler', autospec=True), \
             patch('logging.basicConfig', autospec=True):

            with self.assertRaises(Exception) as context:
                import basis_vm.config.logging

            self.assertIn("Failed to create FileHandler", str(context.exception))

    def test_logging_multiple_imports_only_configured_once(self):
        """
        Test that logging.basicConfig is called only once even if the logging module is imported multiple times.
        """
        with patch('logging.basicConfig', autospec=True) as mock_basicConfig:

            # Ensure the module is not imported before the patches
            if 'basis_vm.config.logging' in sys.modules:
                del sys.modules['basis_vm.config.logging']

            import basis_vm.config.logging
            importlib.reload(sys.modules['basis_vm.config.logging'])
            importlib.reload(sys.modules['basis_vm.config.logging'])

            # Assert that basicConfig was called only once
            mock_basicConfig.assert_called_once()

if __name__ == '__main__':
    unittest.main()
