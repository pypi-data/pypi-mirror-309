from ragas_wj.dataset_schema import EvaluationDataset, MultiTurnSample, SingleTurnSample
from ragas_wj.evaluation import evaluate
from ragas_wj.run_config import RunConfig

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown version"


__all__ = [
    "evaluate",
    "RunConfig",
    "__version__",
    "SingleTurnSample",
    "MultiTurnSample",
    "EvaluationDataset",
]
