import os
import unittest
from prompt_eval_sdk.evaluation import Evaluation

class TestEvaluation(unittest.TestCase):
    def setUp(self):
        # Set up model configuration using environment variables
        self.model_config = {
            "azure_endpoint": os.environ.get("AZURE_OPENAI_ENDPOINT"),
            "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
            "azure_deployment": os.environ.get("AZURE_OPENAI_DEPLOYMENT"),
        }
        self.evaluation = Evaluation(self.model_config)

    def test_evaluate_relevance(self):
        query = "What is the capital of Japan?"
        response = "The capital of Japan is Tokyo."
        result = self.evaluation.evaluate_relevance(query, response)
        self.assertIsInstance(result, dict)
        # Add more assertions based on expected result structure

    def test_evaluate_coherance(self):
        query = "What is the capital of Japan?"
        response = "The capital of Japan is Tokyo."
        result = self.evaluation.evaluate_coherance(query, response)
        self.assertIsInstance(result, dict)
        # Add more assertions based on expected result structure

    def test_evaluate_similarity(self):
        query = "What is the capital of Japan?"
        response = "The capital of Japan is Tokyo."
        ground_truth = "Tokyo is the capital of Japan."
        result = self.evaluation.evaluate_similarity(query, response, ground_truth)
        self.assertIsInstance(result, dict)
        # Add more assertions based on expected result structure

if __name__ == '__main__':
    unittest.main()