from typing import Dict, Union, Sequence

# Custom Typing
Scalar = Union[str, bool, int, float]
AttrDict = Dict[str, Union[str, bool, int, float, Sequence[Scalar]]]

# Custom Naming
log_event_name_key = 'log.event.name'