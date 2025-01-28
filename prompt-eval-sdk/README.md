# Prompt Evaluation SDK

## Overview

The Prompt Evaluation SDK is a Python library designed to facilitate the evaluation of AI prompts, specifically focusing on Azure OpenAI Services. This SDK provides tools to evaluate the relevance, coherence, and similarity of AI-generated responses.

## Features

- Evaluate the relevance of AI-generated responses to a given query.
- Assess the coherence of AI-generated responses.
- Measure the similarity between AI-generated responses and ground truth.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-username/prompt-eval-sdk.git
    cd prompt-eval-sdk
    ```

2. **Install dependencies**:
```
poetry install
```

3. **Build the package**:
```
poetry build
```

4. **Install the package**:
```
poetry install
```

## Usage

To evaluate AI prompts using the SDK:

```python
from prompt_eval_sdk.evaluation import Evaluation

evaluation = Evaluation()
relevance = evaluation.evaluate_relevance('your_query', 'your_response')
coherence = evaluation.evaluate_coherance('your_query', 'your_response')
similarity = evaluation.evaluate_similarity('your_query', 'your_response', 'your_ground_truth')