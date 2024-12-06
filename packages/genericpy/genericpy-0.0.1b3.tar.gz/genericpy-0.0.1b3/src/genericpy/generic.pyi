from typing import Optional, Union, Tuple, Any
class generic:
    __type__: Optional[type]
    __types__: Optional[tuple[type, ...]]
    @staticmethod
    def receive(obj: Union[type, Any, None] = None) -> Union[type, Tuple[type, ...], Any, None]: ...
def receive(obj: Union[type, Any, None] = None) -> Union[type, Tuple[type, ...], Any, None]: ...