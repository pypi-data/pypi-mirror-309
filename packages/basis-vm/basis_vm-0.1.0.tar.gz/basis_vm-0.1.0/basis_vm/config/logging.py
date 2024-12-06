import os
import logging

root_logger = logging.getLogger()

if not getattr(root_logger, '_basis_vm_configured', False):
    # Log file name
    log_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared', "vm.log"))

    # Create handlers
    file_handler = logging.FileHandler(log_filename)
    stream_handler = logging.StreamHandler()

    # Configure the logging level to catch all messages from INFO onwards
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] - %(message)s',
                        handlers=[file_handler, stream_handler])

    root_logger._basis_vm_configured = True

logger = logging.getLogger(__name__)
