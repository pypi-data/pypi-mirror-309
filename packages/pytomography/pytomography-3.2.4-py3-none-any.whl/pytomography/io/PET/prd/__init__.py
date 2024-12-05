# This file was generated by the "yardl" tool. DO NOT EDIT.

# pyright: reportUnusedImport=false
from typing import Tuple as _Tuple
import re as _re
import numpy as _np

_MIN_NUMPY_VERSION = (1, 22, 0)

def _parse_version(version: str) -> _Tuple[int, ...]:
    try:
        return tuple(map(int, version.split(".")))
    except ValueError:
        # ignore any prerelease suffix
        version = _re.sub(r"[^0-9.]", "", version)
        return tuple(map(int, version.split(".")))

if _parse_version(_np.__version__) < _MIN_NUMPY_VERSION:
    raise ImportError(f"Your installed numpy version is {_np.__version__}, but version >= {'.'.join(str(i) for i in _MIN_NUMPY_VERSION)} is required.")

from .yardl_types import *
from .types import (
    CoincidenceEvent,
    Detector,
    ExamInformation,
    Header,
    Institution,
    ScannerInformation,
    Subject,
    TimeBlock,
    TimeFrameInformation,
    TimeInterval,
    get_dtype,
)
from .protocols import (
    PrdExperimentReaderBase,
    PrdExperimentWriterBase,
)
from .binary import (
    BinaryPrdExperimentReader,
    BinaryPrdExperimentWriter,
)
from .ndjson import (
    NDJsonPrdExperimentReader,
    NDJsonPrdExperimentWriter,
)
