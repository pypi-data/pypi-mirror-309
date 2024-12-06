import Kratos
from typing import overload

@overload
def GetRegisteredName(arg0: Kratos.Element) -> str: ...
@overload
def GetRegisteredName(arg0: Kratos.Condition) -> str: ...
