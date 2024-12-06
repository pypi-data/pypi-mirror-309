import unittest
from decimal import Decimal
from bson.decimal128 import Decimal128
from basis_vm.utils.serialization import serialize_state, deserialize_state

class TestSerialization(unittest.TestCase):
    """
    Test cases for the serialization and deserialization functions.
    """

    def test_serialize_state_with_dict(self):
        """
        Test serializing a dictionary with various types.
        """
        state = {
            'int': 123,
            'float': 123.456,
            'decimal': Decimal('123.456'),
            'nested': {
                'int': 789,
                'float': 789.012,
                'decimal': Decimal('789.012')
            }
        }
        serialized = serialize_state(state)
        self.assertIsInstance(serialized['int'], dict)
        self.assertIsInstance(serialized['float'], dict)
        self.assertIsInstance(serialized['decimal'], dict)
        self.assertIsInstance(serialized['nested']['int'], dict)
        self.assertIsInstance(serialized['nested']['float'], dict)
        self.assertIsInstance(serialized['nested']['decimal'], dict)

    def test_serialize_state_with_list(self):
        """
        Test serializing a list with various types.
        """
        state = [123, 123.456, Decimal('123.456'), [789, 789.012, Decimal('789.012')]]
        serialized = serialize_state(state)
        self.assertIsInstance(serialized[0], dict)
        self.assertIsInstance(serialized[1], dict)
        self.assertIsInstance(serialized[2], dict)
        self.assertIsInstance(serialized[3][0], dict)
        self.assertIsInstance(serialized[3][1], dict)
        self.assertIsInstance(serialized[3][2], dict)

    def test_deserialize_state_with_dict(self):
        """
        Test deserializing a dictionary with serialized values.
        """
        state = {
            'int': {'__type__': 'int', '__value__': '123'},
            'float': {'__type__': 'float', '__value__': '123.456'},
            'decimal': {'__type__': 'Decimal', '__value__': '123.456'},
            'nested': {
                'int': {'__type__': 'int', '__value__': '789'},
                'float': {'__type__': 'float', '__value__': '789.012'},
                'decimal': {'__type__': 'Decimal', '__value__': '789.012'}
            }
        }
        deserialized = deserialize_state(state)
        self.assertIsInstance(deserialized['int'], int)
        self.assertIsInstance(deserialized['float'], float)
        self.assertIsInstance(deserialized['decimal'], Decimal)
        self.assertIsInstance(deserialized['nested']['int'], int)
        self.assertIsInstance(deserialized['nested']['float'], float)
        self.assertIsInstance(deserialized['nested']['decimal'], Decimal)

    def test_deserialize_state_with_list(self):
        """
        Test deserializing a list with serialized values.
        """
        state = [
            {'__type__': 'int', '__value__': '123'},
            {'__type__': 'float', '__value__': '123.456'},
            {'__type__': 'Decimal', '__value__': '123.456'},
            [
                {'__type__': 'int', '__value__': '789'},
                {'__type__': 'float', '__value__': '789.012'},
                {'__type__': 'Decimal', '__value__': '789.012'}
            ]
        ]
        deserialized = deserialize_state(state)
        self.assertIsInstance(deserialized[0], int)
        self.assertIsInstance(deserialized[1], float)
        self.assertIsInstance(deserialized[2], Decimal)
        self.assertIsInstance(deserialized[3][0], int)
        self.assertIsInstance(deserialized[3][1], float)
        self.assertIsInstance(deserialized[3][2], Decimal)

    def test_serialize_and_deserialize_state(self):
        """
        Test serializing and then deserializing a state to ensure the original state is restored.
        """
        state = {
            'int': 123,
            'float': 123.456,
            'decimal': Decimal('123.456'),
            'nested': [789, 789.012, Decimal('789.012')]
        }
        serialized = serialize_state(state)
        deserialized = deserialize_state(serialized)
        self.assertEqual(deserialized, state)

    def test_serialize_state_with_mixed_types(self):
        """
        Test serializing a dictionary with mixed types.
        """
        state = {
            'int': 123,
            'float': 123.456,
            'string': 'test',
            'bool': True,
            'none': None,
            'decimal': Decimal('123.456'),
            'nested': {
                'int': 789,
                'float': 789.012,
                'string': 'nested_test',
                'bool': False,
                'none': None,
                'decimal': Decimal('789.012')
            }
        }
        serialized = serialize_state(state)
        self.assertIsInstance(serialized['int'], dict)
        self.assertIsInstance(serialized['float'], dict)
        self.assertEqual(serialized['string'], 'test')
        self.assertEqual(serialized['bool'], True)
        self.assertEqual(serialized['none'], None)
        self.assertIsInstance(serialized['decimal'], dict)
        self.assertIsInstance(serialized['nested']['int'], dict)
        self.assertIsInstance(serialized['nested']['float'], dict)
        self.assertEqual(serialized['nested']['string'], 'nested_test')
        self.assertEqual(serialized['nested']['bool'], False)
        self.assertEqual(serialized['nested']['none'], None)
        self.assertIsInstance(serialized['nested']['decimal'], dict)

    def test_deserialize_state_with_mixed_types(self):
        """
        Test deserializing a dictionary with mixed types.
        """
        state = {
            'int': {'__type__': 'int', '__value__': '123'},
            'float': {'__type__': 'float', '__value__': '123.456'},
            'string': 'test',
            'bool': True,
            'none': None,
            'nested': {
                'int': {'__type__': 'int', '__value__': '789'},
                'float': {'__type__': 'float', '__value__': '789.012'},
                'string': 'nested_test',
                'bool': False,
                'none': None
            }
        }
        deserialized = deserialize_state(state)
        self.assertIsInstance(deserialized['int'], int)
        self.assertIsInstance(deserialized['float'], float)
        self.assertEqual(deserialized['string'], 'test')
        self.assertEqual(deserialized['bool'], True)
        self.assertEqual(deserialized['none'], None)
        self.assertIsInstance(deserialized['nested']['int'], int)
        self.assertIsInstance(deserialized['nested']['float'], float)
        self.assertEqual(deserialized['nested']['string'], 'nested_test')
        self.assertEqual(deserialized['nested']['bool'], False)
        self.assertEqual(deserialized['nested']['none'], None)

    def test_serialize_state_with_empty_dict(self):
        """
        Test serializing an empty dictionary.
        """
        state = {}
        serialized = serialize_state(state)
        self.assertEqual(serialized, {})

    def test_deserialize_state_with_empty_dict(self):
        """
        Test deserializing an empty dictionary.
        """
        state = {}
        deserialized = deserialize_state(state)
        self.assertEqual(deserialized, {})

    def test_serialize_state_with_empty_list(self):
        """
        Test serializing an empty list.
        """
        state = []
        serialized = serialize_state(state)
        self.assertEqual(serialized, [])

    def test_deserialize_state_with_empty_list(self):
        """
        Test deserializing an empty list.
        """
        state = []
        deserialized = deserialize_state(state)
        self.assertEqual(deserialized, [])

    def test_serialize_state_with_non_serializable_type(self):
        """
        Test serializing a state with a non-serializable type.
        """
        state = {'set': {1, 2, 3}}
        serialized = serialize_state(state)
        self.assertEqual(serialized, {'set': {1, 2, 3}})

    def test_deserialize_state_with_non_serializable_type(self):
        """
        Test deserializing a state with a non-serializable type.
        """
        state = {'set': {1, 2, 3}}
        deserialized = deserialize_state(state)
        self.assertEqual(deserialized, {'set': {1, 2, 3}})

    def test_serialize_state_with_nested_empty_dict(self):
        """
        Test serializing a state with nested empty dictionary.
        """
        state = {'nested': {}}
        serialized = serialize_state(state)
        self.assertEqual(serialized, {'nested': {}})

    def test_deserialize_state_with_nested_empty_dict(self):
        """
        Test deserializing a state with nested empty dictionary.
        """
        state = {'nested': {}}
        deserialized = deserialize_state(state)
        self.assertEqual(deserialized, {'nested': {}})

    def test_serialize_state_with_nested_empty_list(self):
        """
        Test serializing a state with nested empty list.
        """
        state = {'nested': []}
        serialized = serialize_state(state)
        self.assertEqual(serialized, {'nested': []})

    def test_deserialize_state_with_nested_empty_list(self):
        """
        Test deserializing a state with nested empty list.
        """
        state = {'nested': []}
        deserialized = deserialize_state(state)
        self.assertEqual(deserialized, {'nested': []})

if __name__ == '__main__':
    unittest.main()