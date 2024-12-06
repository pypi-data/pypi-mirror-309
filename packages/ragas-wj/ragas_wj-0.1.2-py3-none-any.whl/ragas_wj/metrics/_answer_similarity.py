from __future__ import annotations

import logging
import typing as t
from dataclasses import dataclass, field

import numpy as np

from ragas_wj.dataset_schema import SingleTurnSample
from ragas_wj.embeddings.base import HuggingfaceEmbeddings
from ragas_wj.metrics.base import (
    MetricType,
    MetricWithEmbeddings,
    MetricWithLLM,
    SingleTurnMetric,
)

if t.TYPE_CHECKING:
    from langchain_core.callbacks.base import Callbacks


logger = logging.getLogger(__name__)


@dataclass
class SemanticSimilarity(MetricWithLLM, MetricWithEmbeddings, SingleTurnMetric):
    """
    Scores the semantic similarity of ground truth with generated answer.
    cross encoder score is used to quantify semantic similarity.
    SAS paper: https://arxiv.org/pdf/2108.06130.pdf

    Attributes
    ----------
    name : str
    model_name:
        The model to be used for calculating semantic similarity
        Defaults open-ai-embeddings
        select cross-encoder model for best results
        https://huggingface.co/spaces/mteb/leaderboard
    threshold:
        The threshold if given used to map output to binary
        Default 0.5
    """

    name: str = "semantic_similarity"
    _required_columns: t.Dict[MetricType, t.Set[str]] = field(
        default_factory=lambda: {MetricType.SINGLE_TURN: {"reference", "response"}}
    )
    is_cross_encoder: bool = False
    threshold: t.Optional[float] = None

    def __post_init__(self):
        # only for cross encoder
        if isinstance(self.embeddings, HuggingfaceEmbeddings):
            self.is_cross_encoder = True if self.embeddings.is_cross_encoder else False
            self.embeddings.encode_kwargs = {
                **self.embeddings.encode_kwargs,
            }

    async def _single_turn_ascore(
        self, sample: SingleTurnSample, callbacks: Callbacks
    ) -> float:
        row = sample.to_dict()
        return await self._ascore(row, callbacks)

    async def _ascore(self, row: t.Dict, callbacks: Callbacks) -> float:
        assert self.embeddings is not None, "embeddings must be set"

        ground_truth = t.cast(str, row["reference"])
        answer = t.cast(str, row["response"])

        # Handle embeddings for empty strings
        ground_truth = ground_truth or " "
        answer = answer or " "

        if self.is_cross_encoder and isinstance(self.embeddings, HuggingfaceEmbeddings):
            raise NotImplementedError(
                "async score [ascore()] not implemented for HuggingFace embeddings"
            )
        else:
            
            # keywords = row.get('keywords',[])
            # # 计算关键词覆盖率
            # text_2_keywords = {word for word in keywords if word in answer}
            # text_1_keywords = {word for word in keywords if word in ground_truth}
            #
            # # 关键词命中情况
            # num_keywords_in_text2 = len(text_2_keywords)  # text2中的关键词数量
            # num_keywords_matched = len(text_1_keywords & text_2_keywords)  # text1中命中的关键词数量
            #
            # # 覆盖率
            # if num_keywords_in_text2 > 0:  # 避免除零
            #     num_keywords_matched = 3
            #     num_keywords_in_text2 = 2
            #     coverage_ratio = num_keywords_matched / num_keywords_in_text2
            # else:
            #     coverage_ratio = 1.0  # 如果text2没有定义关键词，保持相似度不变
            # #
            # # 嵌入生成
            # embedding_1 = np.array(await self.embeddings.embed_text(ground_truth))
            # embedding_2 = np.array(await self.embeddings.embed_text(answer))
            # 
            # # 归一化
            # norms_1 = np.linalg.norm(embedding_1, keepdims=True)
            # norms_2 = np.linalg.norm(embedding_2, keepdims=True)
            # 
            # embedding_1_normalized = embedding_1 / norms_1
            # embedding_2_normalized = embedding_2 / norms_2
            # 
            # # 计算基础余弦相似度
            # similarity = embedding_1_normalized @ embedding_2_normalized.T
            # base_score = similarity.flatten()
            # 
            # # 使用覆盖率调整得分
            # final_score = base_score * coverage_ratio
            # 
            # # print(f"基础相似度得分: {base_score} - {answer} - {coverage_ratio}")
            # print(f"base_score:{base_score}: final_score:{final_score}")
            # # assert isinstance(score, np.ndarray), "Expects ndarray"
            # # if self.threshold:
            # #     score = score >= self.threshold
            # #
            # # return score.tolist()[0]
            # return final_score
            # input()

            embedding_1 = np.array(await self.embeddings.embed_text(ground_truth))
            embedding_2 = np.array(await self.embeddings.embed_text(answer))
            # Normalization factors of the above embeddings
            norms_1 = np.linalg.norm(embedding_1, keepdims=True)
            norms_2 = np.linalg.norm(embedding_2, keepdims=True)
            embedding_1_normalized = embedding_1 / norms_1
            embedding_2_normalized = embedding_2 / norms_2
            similarity = embedding_1_normalized @ embedding_2_normalized.T
            score = similarity.flatten()

        assert isinstance(score, np.ndarray), "Expects ndarray"
        if self.threshold:
            score = score >= self.threshold

        return score.tolist()[0]


class AnswerSimilarity(SemanticSimilarity):
    name: str = "answer_similarity"

    async def _ascore(self, row: t.Dict, callbacks: Callbacks) -> float:
        return await super()._ascore(row, callbacks)


answer_similarity = AnswerSimilarity()
