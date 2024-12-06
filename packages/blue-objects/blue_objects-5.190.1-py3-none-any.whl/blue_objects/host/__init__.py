from typing import List

from abcli.host import signature as abcli_signature

from blue_objects import fullname
from blue_objects.host.functions import shell


def signature() -> List[str]:
    return [
        fullname(),
    ] + abcli_signature()
