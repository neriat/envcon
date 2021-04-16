import inspect
from typing import Any, Optional


def retrieve_name(variable: Any) -> Optional[str]:
    for frame_info in reversed(inspect.stack()):
        for name, value in frame_info.frame.f_locals.items():
            if value is variable:
                return name
    return None
