import unittest
from basis_vm.security.decorators import read_only, owner_only

class TestDecorators(unittest.TestCase):
    def test_read_only_decorator(self):
        """
        Test that the read_only decorator sets the attribute correctly.
        """
        @read_only
        def sample_function():
            pass

        self.assertTrue(hasattr(sample_function, 'read_only'))
        self.assertTrue(sample_function.read_only)

    def test_owner_only_decorator(self):
        """
        Test that the owner_only decorator sets the attribute correctly.
        """
        @owner_only
        def sample_function():
            pass

        self.assertTrue(hasattr(sample_function, 'owner_only'))
        self.assertTrue(sample_function.owner_only)

if __name__ == '__main__':
    unittest.main()
