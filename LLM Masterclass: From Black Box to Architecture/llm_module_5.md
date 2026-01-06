# LLM Masterclass: From Black Box to Architecture  
## Module 5 — Inference: Why Outputs Are Unstable

**Module Goal:** Understand why identical prompts yield different outputs, how sampling introduces stochasticity, why the model "remixes" rather than retrieves, and how temperature and sampling strategies control output variability. Build mental models for production inference decisions.

---

## 1. Inference as Repeated Probabilistic Sampling

### 1.1 The Iterative Generation Process

Inference in an LLM is not a single forward pass that produces text; it is an **iterative, probabilistic sampling process** repeated hundreds or thousands of times. The process begins with your prompt (tokenized), which is fed through the network to produce a probability distribution over the next token. Rather than deterministically selecting the highest-probability token, the model **samples** a token from this distribution—a random draw weighted by the probabilities. That sampled token is appended to the sequence, the updated sequence is fed back through the network, and the process repeats. Each iteration produces a fresh probability distribution, which is again sampled, continuing until a stopping condition is met (e.g., end-of-sequence token, max length reached). Since each sampling step introduces randomness, two runs of the same prompt will produce different trajectories through the probability space, resulting in different outputs. This is the fundamental reason why temperature, top-k sampling, and other hyperparameters exist: they control the degree of randomness injected at each sampling step.

**Key idea:** Generation is a **Markov chain**: each token is sampled from the model's output distribution, conditioned on all previous tokens.

---

### 1.2 Why Sampling Matters 

If the model always selected the single highest-probability token (greedy decoding), all outputs would be deterministic and identical for a given prompt. While determinism might seem desirable, it would lead to boring, repetitive text, since the highest-probability continuations are often predictable patterns. Sampling introduces **diversity**: the model can explore different continuations, each plausible under the learned distribution. This is especially important for creative tasks (storytelling, brainstorming, code generation) where diverse outputs are valuable. However, sampling also introduces **noise**: if you ask the model a factual question and run it twice, you might get two different answers due to sampling variation. The trade-off between diversity (sampling) and consistency (greedy decoding) is controlled by temperature: lower temperatures favor high-probability tokens (more deterministic), while higher temperatures make the distribution flatter (more sampling diversity). For production systems, this choice is critical: should you optimize for consistency or creativity? The answer depends on your use case.

**Key idea:** Sampling is a feature, not a bug; it enables diversity but sacrifices determinism.

---

## 2. Stochasticity: Flipping Coins at Each Step

### 2.1 The Role of Randomness 

At each step of inference, the model makes a probabilistic choice: "which token comes next?" The model outputs a distribution, and you sample from it—this is a **biased coin flip**. If the highest-probability token has probability 0.7 and the second-highest has 0.2, each sample has a 70% chance of picking the highest-probability token and a 20% chance of the second-highest. The inherent randomness means you can never guarantee an exact output; you can only specify a probability distribution over outputs. This randomness compounds: if the first token is sampled randomly, it influences the distribution for the second token, which is also sampled randomly, and so on. By the time you've generated 100 tokens, you've made 100 independent probabilistic choices, each of which is influenced by previous choices, resulting in an exponentially large space of possible outputs. Two runs of the same prompt will almost certainly produce different sequences of sampled tokens, leading to divergent trajectories. For practitioners, this means that **identical prompts cannot guarantee identical outputs** (without fully deterministic settings like temperature=0 and no randomness).

**Key idea:** Generation is a stochastic process; outputs are samples from a learned distribution, not deterministic computations.

---

### 2.2 Implications for Production Systems 

In production, you must decide: do you want deterministic outputs (for reproducibility, testing, compliance) or diverse outputs (for creative tasks, user experience)? If you require determinism, you can set temperature to 0, which makes the model greedily select the highest-probability token at each step, eliminating randomness (though at the cost of repetitive outputs). If you want diversity, you use higher temperatures or nucleus sampling, accepting that outputs will vary between runs. However, there's a hidden cost: higher sampling temperatures can increase the probability of hallucinations or factual errors, because lower-probability tokens (which might be incorrect continuations) become more likely to be sampled. Additionally, monitoring and testing become harder when outputs are non-deterministic; you must test across many samples and check for consistency in aggregated behavior, not individual outputs. Some systems mitigate this by using temperature=0 for high-stakes tasks (facts, code, compliance) and higher temperatures for user-facing creative content.

**Key idea:** Temperature is a knob you control; choose it based on whether your use case prioritizes consistency or diversity.

---

## 3. Why Identical Prompts Yield Different Answers

### 3.1 The Stochastic Cascade 

Given a fixed prompt and a model with temperature > 0, each run produces a fresh sequence of probabilistic samples. The first token is sampled from the output distribution for your prompt; each possible first token leads to a different distribution for the second token, which is again sampled. If the first token differs between two runs, the second token's distribution will likely differ, diverging further. This **cascade of probabilistic choices** means that two runs can diverge significantly even if the early tokens are identical. Mathematically, the space of possible outputs grows exponentially with sequence length: if each position has ~50,000 possible tokens and the model samples from a distribution (not deterministically picking the max), the number of possible trajectories through token space is astronomically large. In practice, most of these paths are low-probability and won't be sampled frequently, but many high-probability paths exist, each producing valid-looking outputs that the model learned during training. This is why you can ask a model the same question multiple times and get different (sometimes contradictory) answers—not because the model is "confused," but because it's correctly sampling from a learned distribution with multiple plausible continuations.

**Key idea:** Identical prompts diverge due to stochastic sampling at each step; the output distribution is often multimodal (multiple plausible answers).

---

### 3.2 When Different Is a Problem

In some contexts, output variance is desirable (creative writing, brainstorming, hypothesis generation). In others, it's a critical failure mode: a medical AI should not give different diagnoses for identical patient records, and a code-generation tool should not produce subtly different logic between runs. For such use cases, you have several options. First, use deterministic decoding (temperature=0), accepting the cost of more repetitive outputs. Second, augment the model with **retrieval** or **tools** that ground outputs in consistent, external sources, reducing reliance on the model's probabilistic sampling. Third, **verify and rank** multiple samples: generate multiple outputs and use heuristics or secondary models to select the best one. Fourth, implement **output caching or memoization**: if the same prompt appears again, return the cached output rather than resampling. In production systems serving high-stakes decisions, a combination of these strategies is common.

**Key idea:** Variance in outputs is inherent; manage it through temperature control, augmentation, verification, or caching.

---

## 4. Models Remix Rather Than Retrieve

### 4.1 Generation as Probabilistic Remixing

A critical insight is that LLMs **generate text by remixing learned patterns**, not by retrieving stored facts or memorized passages. When you ask the model a question, it doesn't look up an answer in a database; it generates tokens that are statistically likely given the learned patterns. If the model was trained on a text saying "Paris is the capital of France," it learned associations between tokens in that sentence, not a factual entry "Paris: capital of France." When asked "What is the capital of France?", the model generates tokens that statistically fit the pattern it learned, which typically results in "Paris." But the model could just as plausibly generate "The most beautiful city in the world is Paris, and yes, it is indeed the capital of France," or other plausible continuations, depending on what patterns it emphasizes. This remixing is powerful for generation and synthesis: the model can combine patterns creatively (e.g., write a poem about neural networks in the style of Shakespeare). However, it's problematic for retrieval: if you ask the model to cite a source or quote a specific passage, it will generate plausible-sounding text that may be entirely fabricated, because it has no mechanism to "remember" or retrieve the original text—only to approximate it via statistical patterns.

**Key idea:** Generation is remixing; retrieval requires external systems (RAG, vector databases, knowledge bases).

---

### 4.2 Why This Matters for Architecture 

Understanding this distinction leads directly to architectural decisions. For **generative tasks** (summarization, creative writing, code generation), the remixing nature of LLMs is a strength: the model learns to combine patterns in novel ways, producing outputs that are flexible and contextual. For **retrieval and fact-checking**, remixing is a critical weakness: the model will produce hallucinations with high confidence because from its perspective, generating plausible text is indistinguishable from retrieving true text. To mitigate this, you adopt a **RAG (Retrieval-Augmented Generation)** architecture: retrieve relevant documents or data from a trusted source, inject them into the prompt, and let the model generate outputs grounded in that retrieved context. This shifts the burden from "model must remember facts" to "retrieval system must provide facts," playing to each component's strengths. Alternatively, you can use **tool calling**: the model generates a call to an external function (e.g., a database query or API), the tool returns data, and the model incorporates it into its response. Both patterns acknowledge that the model remixes patterns; they just ensure the "remix palette" includes verified facts.

**Key idea:** Remixing ≠ retrieval; use external systems when facts matter.

---

## 5. Practical Labs (Sampling Behavior)

Labs here are **intentionally simple**: small Python scripts exploring sampling, temperature effects, and output variability.

---

### Lab 1: Understanding Temperature & Sampling

**Goal:** Observe how temperature controls the "spread" of a probability distribution.

#### 5.1 Lab 1 — Code

```python
"""
Lab 1: Temperature Effects on Sampling

Demonstrate:
- Temperature = 1.0: unchanged probabilities (baseline)
- Temperature < 1.0: sharper distribution (favor high-prob tokens)
- Temperature > 1.0: flatter distribution (increase diversity)
"""

import numpy as np

def apply_temperature(logits, temperature):
    """Apply temperature scaling to logits and convert to probabilities."""
    scaled_logits = logits / temperature
    probs = np.exp(scaled_logits) / np.sum(np.exp(scaled_logits))
    return probs

# Toy logits (output before softmax) for a 5-token vocabulary
logits = np.array([2.0, 1.0, 0.5, -0.5, -2.0])
vocab = ["Paris", "Lyon", "France", "city", "unknown"]

temperatures = [0.1, 0.5, 1.0, 2.0, 5.0]

print("=" * 70)
print("TEMPERATURE EFFECTS ON PROBABILITY DISTRIBUTION")
print("=" * 70)

for temp in temperatures:
    probs = apply_temperature(logits, temperature=temp)
    print(f"\nTemperature = {temp}:")
    for token, prob in zip(vocab, probs):
        bar = "█" * int(prob * 40)
        print(f"  {token:10} {prob:.4f}  {bar}")

print("\n" + "=" * 70)
print("OBSERVATIONS:")
print("=" * 70)
print("Temperature 0.1:  Sharp spike at highest-prob token (deterministic)")
print("Temperature 1.0:  Original distribution (baseline)")
print("Temperature 5.0:  Flattened distribution (high diversity)")
```

#### 5.2 Lab 1 — What You Should Observe

- **Low temperature (0.1):** Probabilities become extreme; highest-prob token dominates.
- **Temperature 1.0:** Original logit distribution (no change).
- **High temperature (5.0):** Distribution flattens; all tokens become equally likely.

**Reflection prompts:**

1. Why is temperature=0 not the same as just picking the max? (Hint: softmax.)
2. What happens if you sample from the distribution at temperature=0.1 vs. 5.0?
3. In production, would you use high or low temperature for factual QA?

---

### Lab 2: Simulating Multi-Run Variance with Sampling

**Goal:** Show that identical prompts with sampling > 0 produce different outputs.

#### 6.1 Lab 2 — Code

```python
"""
Lab 2: Multi-Run Variance via Stochastic Sampling

Simulate:
- Multiple "runs" of the same prompt
- Sample from learned distributions at each step
- Show output divergence
"""

import numpy as np
import random

# Toy "learned" distributions for a simple sequence
# Each dict maps "context" to a distribution over next tokens
distributions = {
    "start": {"The": 0.5, "A": 0.3, "One": 0.2},
    "The": {"capital": 0.6, "model": 0.2, "answer": 0.2},
    "A": {"network": 0.5, "model": 0.3, "system": 0.2},
    "capital": {"of": 0.9, "is": 0.1},
    "of": {"France": 0.7, "Spain": 0.2, "Italy": 0.1},
    "is": {"Paris": 0.8, "Lyon": 0.2},
}

def sample_next_token(context, dist_map):
    """Sample next token from distribution given context."""
    if context not in dist_map:
        return None
    dist = dist_map[context]
    tokens = list(dist.keys())
    probs = list(dist.values())
    return np.random.choice(tokens, p=probs)

def generate_sequence(max_length=4, dist_map=distributions):
    """Generate a sequence by sampling tokens."""
    sequence = ["start"]
    for _ in range(max_length):
        last_token = sequence[-1]
        next_token = sample_next_token(last_token, dist_map)
        if next_token is None:
            break
        sequence.append(next_token)
    return " ".join(sequence[1:])  # Remove "start" marker

print("=" * 70)
print("MULTI-RUN STOCHASTIC SAMPLING")
print("=" * 70)
print("\nRunning the same 'prompt' 10 times with stochastic sampling:\n")

outputs = []
for run in range(10):
    output = generate_sequence()
    outputs.append(output)
    print(f"Run {run+1:2d}: {output}")

print("\n" + "=" * 70)
print("ANALYSIS")
print("=" * 70)

from collections import Counter
output_counts = Counter(outputs)
print(f"Unique outputs: {len(output_counts)}")
print(f"Most common: {output_counts.most_common(3)}")

print("\nKey insight: Same prompt, different outputs due to sampling.")
print("This is WHY identical prompts yield different answers in production!")
```

#### 6.2 Lab 2 — What You Should Observe

- Multiple runs of the same "prompt" produce different outputs.
- Some outputs appear more frequently (higher probability paths).
- The output distribution is stochastic but not uniform.

**Reflection prompts:**

1. How would you reduce output variance in this system?
2. What if you set all temperatures to 0 (greedy decoding)?
3. How does this explain hallucinations in production systems?

---

### Lab 3: Temperature & Output Variability Trade-off

**Goal:** Show empirically how temperature controls the trade-off between consistency and diversity.

#### 7.1 Lab 3 — Code

```python
"""
Lab 3: Temperature Trade-off: Consistency vs. Diversity

Simulate multiple samples at different temperatures
and measure variability in outputs.
"""

import numpy as np
from collections import Counter

def sample_with_temperature(probs, temperature, num_samples=100):
    """Sample tokens multiple times with given temperature."""
    # Apply temperature to convert probs to logits, then back to probs
    # (Approximation: use log probs as "logits")
    log_probs = np.log(probs + 1e-9)
    scaled_logits = log_probs / temperature
    scaled_probs = np.exp(scaled_logits) / np.sum(np.exp(scaled_logits))
    
    vocab = ["Paris", "Lyon", "France", "city", "London"]
    samples = np.random.choice(vocab, size=num_samples, p=scaled_probs)
    return samples

# Base probability distribution (from a mock model output)
base_probs = np.array([0.6, 0.2, 0.1, 0.05, 0.05])
vocab = ["Paris", "Lyon", "France", "city", "London"]

temperatures = [0.1, 0.5, 1.0, 2.0]

print("=" * 70)
print("TEMPERATURE EFFECT ON OUTPUT CONSISTENCY")
print("=" * 70)

for temp in temperatures:
    samples = sample_with_temperature(base_probs, temperature=temp, num_samples=100)
    counts = Counter(samples)
    unique_count = len(counts)
    most_common_count = counts.most_common(1)[0][1]
    
    print(f"\nTemperature {temp}:")
    print(f"  Unique outputs in 100 samples: {unique_count}")
    print(f"  Most common token appears: {most_common_count}% of the time")
    print(f"  Distribution:")
    for token in vocab:
        count = counts.get(token, 0)
        bar = "█" * int(count / 5)
        print(f"    {token:10} {count:3d}  {bar}")

print("\n" + "=" * 70)
print("CONSISTENCY vs. DIVERSITY TRADE-OFF")
print("=" * 70)
print("Low temperature (0.1):   Highly consistent (same answer ~90% of time)")
print("Medium temperature (1.0): Balanced")
print("High temperature (2.0):  Diverse (many different answers)")
```

#### 7.2 Lab 3 — What You Should Observe

- **Temperature 0.1:** Most samples are identical; high consistency, low diversity.
- **Temperature 1.0:** Moderate variance; mix of consistency and diversity.
- **Temperature 2.0:** High variance; many different outputs, lower consistency.

**Reflection prompts:**

1. For a customer support chatbot answering FAQs, which temperature would you use? Why?
2. For a creative brainstorming tool, which temperature?
3. How does this relate to production cost (more sampling = more compute)?

---

## 6. Common Sampling Strategies

### 6.1 Greedy Decoding (Temperature = 0)

**Definition:** Always select the highest-probability token; no randomness.

**Pros:**
- Fully deterministic; identical outputs for identical prompts.
- Efficient; no need for multiple samples or ranking.
- Predictable for testing and compliance.

**Cons:**
- Repetitive, boring outputs; often devolves into cycles.
- Lower quality; model avoids exploring alternative paths.

**When to use:** High-stakes, factual tasks; reproducible testing; deterministic behavior required.

---

### 6.2 Nucleus (Top-p) Sampling

**Definition:** Sample from the smallest set of tokens whose cumulative probability ≥ p (e.g., p=0.9).

**Pros:**
- Removes "tail" of very low-probability tokens, reducing nonsense.
- More diverse than greedy, more controlled than full sampling.
- Often produces higher-quality text than temperature alone.

**Cons:**
- More complex to implement; adds hyperparameter (p).
- Still stochastic; identical prompts produce different outputs.

**When to use:** Balancing quality and diversity; text generation; when you want to avoid low-probability gibberish.

---

### 6.3 Top-k Sampling

**Definition:** Sample from the k highest-probability tokens only.

**Pros:**
- Simple; just limit the vocab to top k tokens.
- Prevents sampling from the long tail of low-probability tokens.

**Cons:**
- Fixed k may not adapt to different distributions (sometimes top 10 tokens cover 95% prob, sometimes only 90%).
- Less flexible than nucleus sampling.

**When to use:** Simple baseline when you want to avoid nonsense; when k is domain-specific.

---

## 7. Module 5 Summary & Strategic Takeaways

| Concept | Why It Matters | Practical Implication |
|---------|----------------|----------------------|
| **Iterative Sampling** | Each step is probabilistic, compounding variance | Outputs diverge; manage with temperature control |
| **Stochasticity** | Inherent randomness at each token; not a bug | Accept variance or use deterministic decoding |
| **Temperature Control** | Trades consistency for diversity | Low temp for facts, high temp for creativity |
| **Remixing vs. Retrieval** | Model generates plausible text, not exact facts | Use RAG for factual accuracy |
| **Multi-run Variance** | Same prompt → different outputs (temp > 0) | For critical systems, verify or cache outputs |

---

## 8. Architecture Decision Matrix

| Use Case | Temperature | Sampling Strategy | Why |
|----------|-------------|-------------------|-----|
| Factual QA | 0.0 | Greedy | Determinism + consistency required |
| Creative writing | 0.7–1.0 | Nucleus (p=0.9) | Diversity balanced with quality |
| Code generation | 0.2 | Top-k (k=40) | Avoid gibberish, some diversity |
| Brainstorming | 1.2–1.5 | Nucleus (p=0.95) | High diversity, plausible outputs |
| Production API | 0.3 | Greedy or cached | Speed + consistency for users |
| Research/exploration | 1.0–2.0 | Nucleus (p=0.95) | Maximum diversity for discovery |
