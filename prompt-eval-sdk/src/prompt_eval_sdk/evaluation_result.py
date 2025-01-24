import json

class EvaluationResult:
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            relevance=data.get("relevance", 0.0),
            coherence=data.get("coherence", 0.0),
            similarity=data.get("similarity", 0.0)
        )
    
    def __init__(self, relevance: float, coherence: float, similarity: float):
        self.relevance = relevance
        self.coherence = coherence
        self.similarity = similarity

    def __str__(self):
        return f"Relevance: {self.relevance}, Coherence: {self.coherence}, Similarity: {self.similarity}"

    def to_dict(self):
        return {
            "relevance": self.relevance,
            "coherence": self.coherence,
            "similarity": self.similarity
        }