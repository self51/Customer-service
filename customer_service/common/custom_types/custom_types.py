from typing import Any, NewType, TypeAlias

Args: TypeAlias = tuple[Any, ...]
Kwargs: TypeAlias = dict[str, Any]

UserID = NewType('UserID', int)
CustomerID = NewType('CustomerID', int)
WorkerID = NewType('WorkerID', int)
LocationID = NewType('LocationID', int)
