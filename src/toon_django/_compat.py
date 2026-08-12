import sys

if sys.version_info < (3, 11):
    from typing_extensions import NotRequired, Unpack
else:
    from typing import NotRequired, Unpack

if sys.version_info < (3, 12):
    from typing_extensions import override
else:
    from typing import override

__all__ = [
    "NotRequired",
    "Unpack",
    "override",
]
