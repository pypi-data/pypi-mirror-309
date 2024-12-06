from decimal import Decimal
from bson.decimal128 import Decimal128

def serialize_state(state):
    """
    Recursively serializes the given state. Converts integers, floats, and Decimals to Decimal128.

    Args:
        state (any): The state to serialize. Can be a dictionary, list, int, float, Decimal, or other types.

    Returns:
        any: The serialized state with integers, floats, and Decimals converted to Decimal128.
    """
    if isinstance(state, dict):
        return {k: serialize_state(v) for k, v in state.items()}
    elif isinstance(state, list):
        return [serialize_state(v) for v in state]
    elif isinstance(state, bool):
        # Booleans are not supported by Decimal128, so
        return state
    elif isinstance(state, int):
        return {'__type__': 'int', '__value__': str(state)}
    elif isinstance(state, float):
        return {'__type__': 'float', '__value__': repr(state)}
    elif isinstance(state, Decimal):
        return {'__type__': 'Decimal', '__value__': str(state)}
    else:
        return state

def deserialize_state(state):
    """
    Recursively deserializes the given state. Converts Decimal128 back to int or float as appropriate.

    Args:
        state (any): The state to deserialize. Can be a dictionary, list, or Decimal128.

    Returns:
        any: The deserialized state with Decimal128 converted back to int or float.
    """
    if isinstance(state, dict):
        if '__type__' in state and '__value__' in state:
            t = state['__type__']
            v = state['__value__']
            if t == 'int':
                return int(v)
            elif t == 'float':
                return float(v)
            elif t == 'Decimal':
                return Decimal(v)
            else:
                return state  # Unknown type, return as is
        else:
            return {k: deserialize_state(v) for k, v in state.items()}
    elif isinstance(state, list):
        return [deserialize_state(v) for v in state]
    else:
        return state