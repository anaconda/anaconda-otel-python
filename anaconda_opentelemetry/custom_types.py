from typing import Dict, Union, Sequence
# Limited Dict for attributes in OTel

Scalar = Union[str, bool, int, float]
AttrDict = Dict[str, Union[str, bool, int, float, Sequence[Scalar]]]