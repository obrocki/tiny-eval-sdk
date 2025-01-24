import os
from prompt_eval_sdk.evaluation_result import EvaluationResult

from azure.ai.evaluation import (
    RelevanceEvaluator,
    CoherenceEvaluator,
    SimilarityEvaluator,
)


class Evaluation:
    def __init__(self, model_config: dict = None):
        if model_config is None:
            model_config = {
                "azure_endpoint": os.environ.get("AZURE_OPENAI_ENDPOINT"),
                "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
                "azure_deployment": os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
            }
        self.model_config = model_config

    def evaluate_relevance(self, query: str, response: str) -> dict:
        relevance_evaluator = RelevanceEvaluator(self.model_config)
        result = relevance_evaluator(query=query, response=response)
        return result

    def evaluate_coherance(self, query: str, response: str) -> dict:
        coherence_evaluator = CoherenceEvaluator(self.model_config)
        result = coherence_evaluator(query=query, response=response)
        return result

    def evaluate_similarity(self, query: str, response: str, ground_truth: str) -> dict:
        similarity_evaluator = SimilarityEvaluator(self.model_config)
        result = similarity_evaluator(
            query=query, response=response, ground_truth=ground_truth
        )
        return result

    def evaluate_combined(
        self, query: str, response: str, ground_truth: str
    ) -> EvaluationResult:
        relevance_evaluator = RelevanceEvaluator(self.model_config)
        coherence_evaluator = CoherenceEvaluator(self.model_config)
        similarity_evaluator = SimilarityEvaluator(self.model_config)
        relevance = relevance_evaluator(query=query, response=response)
        coherence = coherence_evaluator(query=query, response=response)
        similarity = similarity_evaluator(
            query=query, response=response, ground_truth=ground_truth
        )
        return EvaluationResult(
            relevance["relevance"], coherence["coherence"], similarity["similarity"]
        )
