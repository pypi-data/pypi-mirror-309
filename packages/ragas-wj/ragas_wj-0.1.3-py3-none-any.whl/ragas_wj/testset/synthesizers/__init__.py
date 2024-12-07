import typing as t

from ragas_wj.llms import BaseRagasLLM
from ragas_wj.testset.synthesizers.multi_hop import (
    MultiHopAbstractQuerySynthesizer,
    MultiHopSpecificQuerySynthesizer,
)
from ragas_wj.testset.synthesizers.single_hop.specific import (
    SingleHopSpecificQuerySynthesizer,
)

from .base import BaseSynthesizer

QueryDistribution = t.List[t.Tuple[BaseSynthesizer, float]]


def default_query_distribution(llm: BaseRagasLLM) -> QueryDistribution:
    return [
        (SingleHopSpecificQuerySynthesizer(llm=llm), 0.5),
        (MultiHopAbstractQuerySynthesizer(llm=llm), 0.25),
        (MultiHopSpecificQuerySynthesizer(llm=llm), 0.25),
    ]


__all__ = [
    "BaseSynthesizer",
    "default_query_distribution",
]
