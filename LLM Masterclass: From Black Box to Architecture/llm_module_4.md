# LLM Masterclass: From Black Box to Architecture  
## Module 4 — Neural Network I/O & Internals (Conceptual)

**Module Goal:** Understand how tokens flow through a neural network, what the model actually computes at each layer, and why it's fundamentally a **function approximator** with no explicit rules, no symbolic logic engine, and no access to external knowledge. Build mental models that explain why the model can't "think" the way humans do, yet still produces coherent output.

---

## 1. Neural Networks as Function Approximators

### 1.1 What is a Neural Network?

At its core, a neural network is a **learnable function** that maps inputs to outputs through a series of mathematical operations. Unlike traditional programming where you write explicit rules ("if X, then do Y"), a neural network learns to approximate an unknown function by adjusting millions or billions of internal parameters based on training data. The network is composed of layers: each layer applies a linear transformation (matrix multiplication) followed by a nonlinearity (e.g., ReLU, GELU), and stacking many such layers creates a complex, nonlinear function that can approximate highly intricate mappings. During training, you feed the network examples (input, desired output) and use backpropagation to adjust the parameters to minimize error on those examples. The hope is that the function learned from training data **generalizes** to new data it hasn't seen before. In the case of LLMs, the function being approximated is "given a sequence of tokens, predict the next token," and the network learns this through exposure to billions of token sequences.

**Key idea:** The model is not storing rules or facts; it is learning a function that compresses patterns from training data into its weights.

---

### 1.2 Why Function Approximation Matters

Understanding LLMs as function approximators immediately clarifies why they have both superhuman and subhuman capabilities. The function the model learns is biased toward whatever patterns are most frequent and prominent in training data; if the training data contains a lot of logical reasoning examples, the model learns to produce reasoning-like text, but it doesn't actually "reason" in a symbolic sense. The approximation is also fundamentally **lossy**: the model cannot store or retrieve exact information; it only learns statistical patterns. This explains why you can ask a model about world knowledge and it produces plausible-sounding answers, even when those answers are hallucinated. Critically, there is no "understanding" in the human sense—there is no internal representation of meaning or consciousness, only learned associations between token sequences. Yet because language itself encodes so much human knowledge and reasoning, a sufficiently large model trained on enough text can approximate intelligent behavior.

**Key idea:** Intelligence emerges from pattern matching at scale, not from symbolic reasoning or true comprehension.

---

## 2. Inputs and Outputs are Token Probabilities

### 2.1 The Network's I/O Contract 

The input to an LLM is a **sequence of token IDs**: integers that represent the tokens produced by the tokenizer. For example, the text "Hello world" might be tokenized as \([15496, 995]\), and these integers are fed into the network. The output of the network is a **probability distribution over the next token**: a vector of length equal to the vocabulary size (often 50,000–100,000+), where each entry represents the model's estimated probability that a particular token comes next. To generate an actual response, you sample from this distribution (or take the highest-probability token, depending on the sampling strategy). So the fundamental I/O contract is: **[token IDs] → network → [probability distribution]**. This is repeated iteratively: you sample a token from the output distribution, append it to the input sequence, feed the new sequence back into the network, and repeat until you've generated enough tokens or hit an end-of-sequence marker. This explains why the model cannot be queried for "exact" information; it can only produce probabilistic continuations.

**Key idea:** The model does not retrieve or generate text directly; it outputs probabilities, and those probabilities are sampled to produce text.

---

### 2.2 What the Probability Distribution Encodes 

The output probability distribution is the network's estimate of "which tokens are likely to come next, given the input sequence?" This estimate is learned from training data: during pre-training, the model saw millions of text continuations and learned to predict which tokens typically follow certain contexts. High-probability tokens are those that commonly follow the given prefix in the training corpus; low-probability tokens are rare or never appear in that context. Importantly, this is a **statistical encoding**, not a symbolic one: there is no explicit list of "valid continuations" or "rules"; the model has simply learned to associate certain input contexts with certain output distributions. A token can have high probability even if it's factually wrong, as long as it's a plausible linguistic continuation. For example, given "The capital of France is," the model assigns high probability to "Paris," but it could plausibly assign high probability to "Lyon" or even "beautiful" if those appeared often enough in training data. This probabilistic I/O contract explains why the model hallucinates, why it can be confidently wrong, and why identical inputs with different sampling parameters yield different outputs.

**Key idea:** Probabilities encode learned statistical patterns, not truth or correctness.

---

## 3. No Symbols, No Rules, No Logic Engine

### 3.1 Why There Are No Explicit Rules 

Traditional symbolic AI systems (e.g., expert systems, constraint solvers) encode knowledge as explicit rules: "if disease symptoms include fever and cough, then consider pneumonia." Neural networks, by contrast, encode knowledge implicitly in their weights, with no human-interpretable rules. When you train an LLM on medical text, it does not extract a set of diagnostic rules; instead, it learns associations between token patterns in ways that are not amenable to explicit articulation. You cannot open the model and read out "if X then Y"; the model's computation is a black box in which billions of parameters interact nonlinearly. This is both a strength (the model can learn subtle, complex patterns that would be hard to express as rules) and a weakness (you cannot debug by inspecting rules, and the model's behavior can be surprising or non-obvious). Consequently, you cannot fix model errors by adding rules; the only way to steer behavior is through training, fine-tuning, or prompt engineering, all of which exploit the learned patterns without modifying any explicit rules.

**Key idea:** What you perceive as the model "knowing" or "reasoning" is actually learned statistical associations, not symbolic processing.

---

### 3.2 Why There's No Logic Engine

LLMs do not execute logic in the way computers run code: they don't maintain variables, perform explicit loops, or apply formal inference rules. Instead, they transform token sequences through layers of learned functions. If a task requires logical reasoning (e.g., "A is taller than B, B is taller than C, therefore A is taller than C"), the model doesn't solve it by executing a logic program; rather, it has learned from training data patterns that suggest such conclusions, and it outputs a token that completes the pattern. This "learned reasoning" can work well for reasoning tasks that are well-represented in training data, but it breaks down on novel logical structures, out-of-distribution reasoning, or tasks requiring adherence to strict rules. For instance, the model might fail at "If today is Tuesday, what was yesterday?" if the specific phrasing or context is unusual, because it doesn't have a logic engine that could reliably compute the answer; it depends on having seen similar phrasings during training. This is why **chain-of-thought prompting** helps: it encourages the model to generate intermediate reasoning steps, which shifts the task from pure logical inference (which the model can't do natively) to pattern matching on reasoning trajectories (which it's learned).

**Key idea:** The model is a pattern matcher, not a computer; logical reasoning is emergent behavior, not a primitive.

---

## 4. How the Network Actually Computes

### 4.1 The Layer-by-Layer Pipeline 

A modern LLM's internal computation unfolds in layers, each of which transforms the token representations. Starting with the input tokens (as IDs), the first step is **embedding**: each token ID is converted to a high-dimensional vector (e.g., 768 or 4096 dimensions) that represents learned semantic properties. Next, the network passes these vectors through many **transformer layers**, each of which applies attention (allowing tokens to "see" and influence each other based on learned similarity) and feed-forward networks (which apply learned nonlinear transformations). Each layer outputs a refined representation of the input tokens, and successive layers build on these representations. After all layers, the final layer applies an operation that maps the representations back to the original vocabulary size, producing logits (un-normalized scores) for each possible next token. These logits are converted to probabilities via softmax, and the final output is a probability distribution. Importantly, the entire computation is **differentiable**, meaning the network can compute gradients and be trained via backpropagation. During inference (after training), the network simply applies these learned transformations forward, without updating its weights.

**Key idea:** The network is a learnable pipeline that transforms tokens into higher-level representations, then back to token probabilities.

---

### 4.2 Why Layers Matter 

Each layer in an LLM specializes in learning certain patterns, though this specialization is not rigid or human-interpretable. Early layers tend to learn low-level linguistic patterns (word order, common phrases, syntax), while middle layers capture semantic relationships, and later layers focus on task-specific or reasoning-like patterns. Stacking more layers gives the model more "capacity" to learn complex mappings, but also increases computational cost and can require more training data to avoid overfitting. The depth (number of layers) and width (hidden dimension size) are critical design choices that trade off model expressiveness, training cost, and inference latency. For practitioners, understanding that the model is a layered pipeline is useful for techniques like **pruning** (removing less important layers or neurons), **distillation** (training a smaller model to mimic a larger one), or **layer-wise analysis** (inspecting what different layers learn). It also explains why fine-tuning only the last few layers can be effective: you're leveraging the learned representations from earlier layers and only adjusting the final, task-specific transformations.

**Key idea:** Depth enables expressiveness; understanding the layered structure is useful for optimization and debugging.

---

## 5. What the Model Cannot Do (Natively)

### 5.1 No Access to External Data 

The model's knowledge is entirely determined by its training data and the patterns it learned during training; it has no access to the internet, databases, or real-time information. When you ask the model a question about current events or specific facts not well-represented in training data, it must generate plausible continuations based solely on what it learned, which often results in hallucinations. Unlike a search engine that retrieves relevant documents, or a database system that executes queries against stored data, the model cannot say "let me look that up"; it can only produce statistically plausible text. This is a fundamental architectural constraint: the model's weights are frozen after training, and inference is purely feed-forward computation with no mechanism for fetching new information. Consequently, if you need factual accuracy, you must **augment** the model with retrieval (RAG), API calls, or knowledge bases, keeping in mind that the model will integrate this external information through its learned language patterns, not through symbolic data retrieval.

**Key idea:** The model is a static pattern engine; it cannot learn or fetch information during inference.

---

### 5.2 No Internal State Across Conversations 

Each time you send a new message to the model, the entire conversation history is re-processed from scratch; the model doesn't maintain an internal state or memory across messages. While the conversation context is provided as input (allowing the model to produce contextually appropriate responses), the model doesn't "remember" your earlier messages in any persistent sense—it only processes the sequence you feed it. This is why the model can be inconsistent across a long conversation: early facts or constraints can be "forgotten" if they're not relevant to the next token prediction. If you need persistent memory or state across interactions, you must implement this externally (e.g., by storing summaries, facts, or tags in a database). Some advanced techniques like **prompt caching** or **retrieval** can mitigate this, but the fundamental limitation remains: the model is a stateless function that processes sequences, not a system with persistent knowledge or memory.

**Key idea:** The model is stateless; long-term memory or knowledge must be maintained externally.

---

## 6. Practical Labs (Conceptual & Lightweight)

Labs here emphasize **understanding the pipeline**, not implementing a full transformer. We'll use toy computations to make the I/O contract and layer concept concrete.

---

### Lab 1: Token IDs → Probability Distribution (Toy Pipeline)

**Goal:** Simulate a minimal neural network that takes token IDs and outputs probability distributions.

#### 6.1 Lab 1 — Code

```python
"""
Lab 1: Toy Neural Network Pipeline

Simulate:
- Input: token IDs
- Simple embedding layer
- Simple feed-forward layers
- Output: probability distribution over next token
"""

import numpy as np

# Tiny vocabulary
vocab = ["hello", "world", "is", "beautiful", "end"]
vocab_size = len(vocab)

# Pretend we have a "trained" network with fixed weights
# (In reality, these would be learned via backpropagation)

class TinyNetwork:
    def __init__(self, vocab_size, embedding_dim=4):
        # Random but fixed "learned" weights
        np.random.seed(42)
        self.embedding_matrix = np.random.randn(vocab_size, embedding_dim)
        self.hidden_layer = np.random.randn(embedding_dim, 2)
        self.output_layer = np.random.randn(2, vocab_size)
    
    def forward(self, token_ids):
        # Step 1: Embed tokens
        embeddings = [self.embedding_matrix[tid] for tid in token_ids]
        # Average embeddings (toy simplification of sequence processing)
        avg_embedding = np.mean(embeddings, axis=0)
        
        # Step 2: Feed-forward layer
        hidden = np.tanh(avg_embedding @ self.hidden_layer)
        
        # Step 3: Output logits
        logits = hidden @ self.output_layer
        
        # Step 4: Softmax to probabilities
        probs = np.exp(logits) / np.sum(np.exp(logits))
        return probs

# Initialize network
net = TinyNetwork(vocab_size=vocab_size)

# Test inputs
test_sequences = [
    [0, 1],  # "hello world"
    [0],     # "hello"
    [2, 3],  # "is beautiful"
]

print("=" * 60)
print("TOY NETWORK: Token IDs → Probability Distribution")
print("=" * 60)

for token_ids in test_sequences:
    token_names = [vocab[tid] for tid in token_ids]
    probs = net.forward(token_ids)
    
    print(f"\nInput tokens: {token_names} (IDs: {token_ids})")
    print("Output probabilities for next token:")
    for token, prob in zip(vocab, probs):
        bar = "█" * int(prob * 30)
        print(f"  {token:12} {prob:.3f}  {bar}")
```

#### 6.2 Lab 1 — What You Should Observe

- Different token sequences produce different probability distributions.
- The probabilities are learned associations (our toy network learned random patterns).
- The fundamental I/O contract holds: tokens in, probabilities out.
- This toy network is vastly simpler than a real LLM, but the structure is the same.

**Reflection prompts:**

1. How would changing the embedding dimension affect the model's expressiveness?
2. What would happen if you added more layers to the network?
3. How does softmax ensure the output sums to 1 (is a valid probability distribution)?

---

### Lab 2: Why the Model Cannot Access External Data (Conceptual)

**Goal:** Illustrate the architectural constraint: weights are fixed, no mechanism to fetch data.

#### 7.1 Lab 2 — Code

```python
"""
Lab 2: No External Data Access (Conceptual)

Show that:
- Model weights are frozen after training
- No mechanism to fetch or query external data
- Hallucinations occur when model must extrapolate
"""

# Simulate a pre-trained model's knowledge
trained_facts = {
    "capital_france": "Paris",
    "capital_spain": "Madrid",
    "capital_italy": "Rome",
    # Note: missing some facts
}

def model_answer_question(question: str):
    """
    Toy model that can only answer questions it "learned" during training.
    (In reality, the model uses learned patterns, not a lookup table,
    but the principle is the same: limited to training knowledge.)
    """
    # Try to match the question to learned facts
    if "capital" in question and "France" in question:
        return trained_facts.get("capital_france", "Unknown")
    elif "capital" in question and "Spain" in question:
        return trained_facts.get("capital_spain", "Unknown")
    elif "capital" in question and "Italy" in question:
        return trained_facts.get("capital_italy", "Unknown")
    else:
        # Question not in training data; model hallucinates
        return "I'm not sure, but it might be something interesting!"

print("=" * 60)
print("MODEL KNOWLEDGE: Fixed at Training Time")
print("=" * 60)

questions = [
    "What is the capital of France?",
    "What is the capital of Spain?",
    "What is the capital of Germany?",  # NOT in training
    "What is the current president of France?",  # Not in training
]

for q in questions:
    answer = model_answer_question(q)
    in_training = any(f in trained_facts for f in trained_facts)
    print(f"\nQ: {q}")
    print(f"A: {answer}")
    print("   (Accurate)" if answer not in ["Unknown", "I'm not sure, but it might be something interesting!"] else "   (Hallucinated/Uncertain)")

print("\n" + "=" * 60)
print("Key Insight:")
print("=" * 60)
print("- Model can only 'know' what was in training data")
print("- No mechanism to fetch new data during inference")
print("- Questions outside training distribution → hallucinations")
print("- Solution: Augment with RAG, APIs, or external tools")
```

#### 7.2 Lab 2 — What You Should Observe

- Questions covered by training knowledge are answered accurately.
- Questions outside the training distribution result in hallucinations.
- The model has no way to "look things up" or query external sources.
- This is why RAG (Retrieval-Augmented Generation) is necessary for factual accuracy.

**Reflection prompts:**

1. How would you modify the architecture to allow access to external data?
2. What is RAG, and how does it solve this problem?
3. Why can't the model just "know" everything if it's trained on the internet?

---

### Lab 3: Layer Depth and Expressive Power (Conceptual)

**Goal:** Understand intuitively how stacking layers increases a network's ability to learn complex patterns.

#### 8.1 Lab 3 — Code

```python
"""
Lab 3: Layer Depth and Expressive Power

Show that:
- Shallow networks can only learn simple patterns
- Deeper networks can learn more complex patterns
- Trade-off: depth vs. training cost and data requirements
"""

import numpy as np

def shallow_network(x):
    """1-layer network: can only learn linear separability"""
    return x * 2 + 1

def medium_network(x):
    """2-layer network: can learn some nonlinear patterns"""
    hidden = np.tanh(x * 3)
    return hidden * 2 + 1

def deep_network(x):
    """3-layer network: can learn more complex patterns"""
    h1 = np.tanh(x * 3)
    h2 = np.tanh(h1 * 2 - 1)
    return np.tanh(h2 * 2) * 2 + 1

# Test pattern: can the network learn XOR-like behavior?
test_inputs = np.linspace(-1, 1, 11)

print("=" * 60)
print("LAYER DEPTH & EXPRESSIVE POWER")
print("=" * 60)

networks = [
    ("Shallow (1 layer)", shallow_network),
    ("Medium (2 layers)", medium_network),
    ("Deep (3 layers)", deep_network),
]

for name, net_func in networks:
    print(f"\n{name}:")
    for x in test_inputs:
        output = net_func(x)
        bar = "█" * int((output + 3) * 3)  # normalize for display
        print(f"  x={x:5.2f} → {output:6.3f}  {bar}")

print("\n" + "=" * 60)
print("Observations:")
print("=" * 60)
print("- Shallow: nearly linear output (limited expressiveness)")
print("- Medium: some nonlinearity (moderate expressiveness)")
print("- Deep: complex, nonlinear patterns (high expressiveness)")
print("\nTrade-off: deeper networks need more data and compute to train!")
```

#### 8.2 Lab 3 — What You Should Observe

- Shallow networks produce smooth, nearly linear transformations.
- Deeper networks produce more complex, nonlinear outputs.
- Depth enables the model to learn more sophisticated patterns.
- The trade-off is computational cost and data requirements.

**Reflection prompts:**

1. How deep are modern LLMs (hint: 32–80+ layers)? Why so deep?
2. What happens if you train a very deep network on very little data?
3. How does model size (depth + width) affect inference latency?

---

## 7. Module 4 Summary & Strategic Takeaways

- **Neural Network as Function Approximator:** The model learns a function from training data; it has no explicit rules or logic engine.
- **Probabilistic I/O:** Input is tokens; output is a probability distribution over the next token.
- **Stateless & Layered:** The model processes sequences without internal state; computation flows through learned layers.
- **No External Access:** The model's knowledge is fixed at training time; it cannot fetch data, access the internet, or maintain memory.
- **Learned Patterns, Not Rules:** What appears as reasoning or knowledge is actually statistical pattern matching; the model has no symbolic representations.
- **Architectural Constraints Are Fundamental:** Hallucinations, inconsistency, and failure modes are not bugs—they're inherent to how the architecture works. Design systems accordingly.

---

## 8. Practical Implications for Architecture

| Challenge | Why It Happens | Architectural Response |
|-----------|----------------|----------------------|
| Hallucinations | Model outputs plausible but false tokens | Use RAG, external verification, confidence scores |
| Inconsistency in long contexts | No persistent state; early context "forgotten" | Summarization, retrieval, explicit memory |
| Incorrect reasoning | No logic engine; only learned pattern matching | Chain-of-thought, tool calling, agentic frameworks |
| Outdated knowledge | Training data is static | Integrate real-time retrieval, vector stores, knowledge graphs |
| Cost scaling | Inference cost per token; context window large | Optimize prompts, use caching, compress context |
