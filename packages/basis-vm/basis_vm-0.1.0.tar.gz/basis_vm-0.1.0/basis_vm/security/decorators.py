def read_only(func):
    """
    Decorator to mark functions as read-only (do not modify the state).
    """
    func.read_only = True
    return func

def owner_only(func):
    """
    Decorator to mark functions that can only be called by the contract owner.
    """
    func.owner_only = True
    return func