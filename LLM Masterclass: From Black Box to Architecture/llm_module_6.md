# LLM Masterclass: From Black Box to Architecture  
## Module 6 — GPT-2 as a Reference Architecture

**Module Goal:** Understand GPT-2 as the "first modern stack" that established the transformer-based LLM blueprint. Learn key architectural parameters (model size, context window, training cost), how these have evolved, and why GPT-2's design remains relevant for reasoning about modern LLMs. Build intuition for scaling implications and cost-performance trade-offs.

---

## 1. GPT-2: The First Modern Stack

### 1.1 What Made GPT-2 "Modern"? 

GPT-2 (2019) was revolutionary not because it was the first neural language model, but because it demonstrated that a **pure transformer-based architecture** trained on large, diverse internet-scale data (WebText corpus, ~45GB of text) could generate coherent, long-form text without task-specific training. Before GPT-2, most NLP systems were task-specific: you'd build separate models for translation, summarization, question-answering, etc. GPT-2 showed that a single, general-purpose model trained with a simple next-token prediction objective could flexibly adapt to many tasks through prompting alone—what we now call **in-context learning**. The architecture was deceptively simple: stacked transformer layers with self-attention, feed-forward networks, layer normalization, and residual connections. What distinguished GPT-2 was the **scale**: 1.5 billion parameters (at the time, enormous) trained on 40 GB of high-quality, diverse web text with modern optimization techniques (Adam optimizer, mixed precision). The combination of scale, data quality, and architectural simplicity proved powerful: GPT-2 could write coherent paragraphs, generate code, answer questions, and perform translations with minimal or no task-specific training.

**Key idea:** GPT-2 established the blueprint: simple architecture + large scale + diverse data = surprising generality.

---

### 1.2 Why GPT-2 Still Matters 

Even though GPT-2 (the small 124M-parameter version) is tiny by modern standards, it remains a critical reference point for understanding LLM scaling and design. The scaling laws derived from GPT-2's training (and subsequent models like GPT-3) revealed that performance improves **predictably** with scale, following power-law relationships: adding more parameters, more training data, or more compute roughly follows the same trajectory. These scaling laws are not specific to GPT-2; they generalize across architectures and datasets, making them valuable for predicting the behavior of new models. Understanding GPT-2's architecture and training also demystifies modern LLMs: they are not fundamentally different algorithms; they are larger, better-trained instances of the same blueprint. Additionally, GPT-2 is small and efficient enough to run locally or on modest hardware, making it ideal for education and experimentation. Finally, many open-source models (Llama, Mistral, etc.) follow the GPT-2 blueprint, so understanding GPT-2 gives you a foundation for understanding the ecosystem.

**Key idea:** GPT-2 is the Rosetta Stone for understanding scaling laws and modern LLM design.

---

## 2. Architectural Parameters & Implications

### 2.1 Model Size (Parameter Count) 

The "size" of an LLM is typically measured in the number of trainable parameters, usually reported in billions. GPT-2 came in several sizes: 124M (small), 355M (medium), 774M (large), and 1.5B (XL) parameters. Each additional parameter allows the model to learn more nuanced patterns from training data, but with diminishing returns: going from 124M to 355M provides substantial improvements, but going from 774M to 1.5B provides proportionally smaller gains. Larger models generally have better capabilities, but they also require more compute to train (proportional to parameters × tokens seen) and more memory and latency to run. A rough heuristic: **memory required ≈ 4 bytes per parameter** (for 32-bit floats; smaller for quantization). So a 7B parameter model requires ~28 GB of memory for weights alone, plus additional memory for intermediate computations. The relationship between model size and capability follows a smooth power law: doubling parameters roughly improves perplexity (a measure of model performance) by ~10%, but the exact relationship depends on training data size and compute budget.

**Key idea:** Model size enables expressiveness but comes with computational costs; scaling is predictable but not free.

---

### 2.2 Context Window (Sequence Length) 

GPT-2 was trained with a context window of **1024 tokens**—the maximum number of previous tokens the model can "see" when predicting the next token. This context window has direct implications for what tasks the model can tackle: if you have a document longer than 1024 tokens, the model can only process the last 1024, potentially missing context from earlier sections. Modern LLMs have dramatically increased context windows: GPT-4 supports up to 128K tokens, and some specialized models support 1M+ tokens. Longer context windows enable new capabilities: the model can summarize entire books, engage in longer conversations without forgetting early context, and process more complex reasoning chains. However, longer context windows have costs: the self-attention mechanism in transformers scales quadratically with sequence length (more precisely, O(n²) memory and computation where n is sequence length). A 1024-token context requires manageable computation, but a 128K-token context requires sophisticated optimizations (sparse attention, flash attention, etc.) to be practical. For practitioners, context window is a critical parameter: if your task requires reasoning over long documents, you need a longer context window, which may push you toward newer, more expensive models.

**Key idea:** Context window limits what the model can "see"; longer windows enable more complex tasks but require optimization.

---

### 2.3 Training Data & Diversity 

GPT-2 was trained on the **WebText** dataset: a curated collection of 45GB of high-quality text from web pages shared on Reddit (filtered for quality via upvotes). This was a deliberate choice to ensure data diversity: Reddit includes everything from technical discussions to creative writing, code, explanations, advice, and more. The diversity of training data is crucial for generalization: a model trained only on scientific papers will fail at creative writing, and vice versa. Modern LLMs expand on this principle: they train on mixtures of web text, books, code repositories, academic papers, and domain-specific datasets, carefully weighted to balance breadth and depth. The quality of training data also matters enormously: 45GB of high-quality Reddit text leads to better performance than 450GB of low-quality web scraps. This observation has led to the practice of **data curation**: investing significant engineering effort into filtering, deduplicating, and cleaning training data. For practitioners using pre-trained models, this means that a model trained on high-quality, diverse data will generalize better to your specific task than one trained on narrow data, even if the narrower model is larger.

**Key idea:** Training data quality and diversity are first-class concerns; they determine generalization and prevent mode collapse.

---

## 3. Training Cost & Scaling Implications

### 3.1 Compute Cost (FLOPs & GPU Hours)

The training cost of an LLM is typically measured in **FLOPs** (floating-point operations) or **GPU-hours**. A rough estimate is: **FLOPs ≈ 6 × parameters × tokens seen**. For GPT-2 (1.5B parameters, trained on ~40GB of text ≈ 10B tokens), this yields roughly 6 × 1.5B × 10B ≈ 90 trillion FLOPs. On a modern GPU (e.g., V100, which does ~100 trillion FLOPs/second), this could be done in ~900 seconds ≈ 15 minutes. However, real training involves overhead, parallelization across many GPUs (with communication costs), and longer training durations to tune hyperparameters and evaluate checkpoints. Empirically, GPT-2 (1.5B) took roughly 1-2 weeks on a modest cluster of GPUs in 2019. Modern LLMs are vastly larger: GPT-3 (175B parameters) required an estimated **3,600 petaFLOPs** (million times larger than GPT-2), costing millions of dollars. This exponential growth in training cost has become a critical limitation: not everyone can afford to train models from scratch. This has driven the industry toward **transfer learning** (fine-tuning pre-trained models) and **prompt engineering** (using existing models creatively without retraining).

**Key idea:** Training cost scales with model size and data; large models require massive compute budgets, limiting who can train from scratch.

---

### 3.2 Scaling Laws & Chinchilla Scaling 

Scaling laws describe the empirical relationship between model size, data size, compute, and performance. Early observations from GPT-2 and GPT-3 suggested that performance improved smoothly with scale, following power laws. The **Chinchilla scaling law** (DeepMind, 2022) showed that the "optimal" training approach balances model size and data size: you should not train a huge model on a small dataset, nor a tiny model on huge data. Instead, the **compute budget should be split roughly equally between model size and data size**: if you have a budget for 1 trillion FLOPs, you should allocate roughly equal resources to making the model larger and to seeing more training data. This insight has influenced modern LLM design: models like Llama and others are trained with more data and shorter training runs, rather than the older approach of huge models trained for a very long time. For practitioners, Chinchilla scaling implies: **given a fixed compute budget, you can get better performance by training a somewhat smaller model on more diverse data, rather than a huge model on limited data**. This is good news for accessibility: you don't always need the biggest model.

**Key idea:** Optimal scaling balances model size and data; Chinchilla law enables efficient training without requiring maximal size.

---

## 4. How GPT-2 Architecture Influenced Modern LLMs

### 4.1 The Transformer Block

GPT-2's core building block is the **transformer layer**, which combines self-attention and feed-forward networks. The self-attention mechanism allows each token to attend to (learn dependencies on) all previous tokens in the sequence, with learned attention weights that indicate which tokens are most relevant for predicting the current position. This is powerful because the model can learn to focus on contextually important tokens: when predicting the next word after "The cat sat on the ___," attention can focus on "cat" to predict "mat" or "sat" to predict "down." The feed-forward network applies learned nonlinear transformations to each position independently, adding expressiveness. Stacking many transformer layers (GPT-2-XL has 48 layers) builds up hierarchical representations: early layers learn low-level syntax and common phrases, middle layers learn semantic relationships, and later layers learn task-specific patterns. Modern LLMs (GPT-4, Llama, etc.) still use this core structure, though with optimizations and variations (e.g., flash attention, group query attention). The elegance of the transformer design is that it scales predictably: you can stack more layers, increase hidden dimensions, and expect performance to improve in a controllable way.

**Key idea:** The transformer layer is the basic currency; stacking them scales intelligently without surprises.

---

### 4.2 Why Alternatives Haven't Replaced Transformers 

Since GPT-2, researchers have explored alternatives to transformer architecture: recurrent networks (RNNs, LSTMs), convolutional networks (CNNs), state-space models (S4, Mamba), and hybrid approaches. Some of these have advantages (e.g., linear attention, better long-range modeling, or lower inference cost), but none have definitively displaced transformers at scale. The reasons are partly technical (transformers parallelize well on modern hardware, attention is intuitive and debuggable) and partly economic (the infrastructure for training and serving transformers is mature and optimized). Additionally, transformers have shown that they scale very smoothly and predictably; the scaling laws hold across wide ranges of model size and data. There's also a "rich get richer" effect: since most compute and research focuses on transformers, they get better optimizations and tooling, which makes them more attractive to use. For practitioners, this stability means: **the transformer + scaling law blueprint is likely here to stay**, at least in the near term. This makes it safe to build systems around transformer-based models; you're not betting on an architecture that might become obsolete.

**Key idea:** Transformers dominate not because they're perfect, but because they scale predictably and the ecosystem is mature.

---

## 5. From GPT-2 to Modern LLMs: Evolution

### 5.1 Scaling Trajectory 

The progression from GPT-2 to modern LLMs shows how scale, data, and optimization have evolved. GPT-2 (2019): 1.5B parameters, 40GB training data, ~2 weeks training. GPT-3 (2020): 175B parameters, 570GB training data, months of training on massive clusters. Llama (2023): 65B parameters, 1.4T tokens (~2TB data), highly optimized training. Each generation brought architectural improvements (better normalization, improved optimization, better data curation), but the core blueprint remained: stack transformer layers, train on diverse data, scale up. One critical observation: models didn't keep growing unbounded. Instead, the focus shifted to **efficient scaling**: getting more capability per parameter and per compute unit. This led to techniques like **quantization** (using lower precision), **distillation** (training smaller models to mimic larger ones), and **mixture-of-experts** (specialized subnetworks for different tasks). The trajectory suggests that future LLMs will be more efficient and specialized, not just uniformly larger.

**Key idea:** Evolution is not just bigger; it's smarter scaling via better data, better optimization, and specialized architectures.

---

### 5.2 What Stayed the Same 

Despite massive growth in parameter count and training data, several core aspects of the GPT-2 design have remained stable. **Next-token prediction** is still the fundamental objective; even though modern models use variants like contrastive learning or reinforcement learning, next-token prediction remains central. **Transformer architecture** still dominates; variations exist, but the core structure persists. **Prompting and in-context learning** are still the primary ways to adapt models; few-shot prompting (showing examples) remains more practical than full fine-tuning for many tasks. **Tokenization** based on byte-pair encoding or variants still dominates; no fundamentally new tokenization scheme has replaced it. The **scaling laws** that governed GPT-2 still hold; performance improves predictably with scale. This stability is important: it means that insights from GPT-2 papers and research transfer directly to modern models. If you understand GPT-2, you understand the core of any modern transformer-based LLM; the differences are in scale, optimization, and post-training techniques, not fundamental architecture.

**Key idea:** The "GPT-2 blueprint" is so robust that it's survived multiple generations of scaling and remains the foundation of modern LLMs.

---

## 6. Practical Labs (Parameter & Cost Intuition)

Labs here focus on building intuition for model sizing, context, and cost trade-offs.

---

### Lab 1: Parameter Count & Memory Requirements

**Goal:** Understand the relationship between parameters, memory, and cost.

#### 6.1 Lab 1 — Code

```python
"""
Lab 1: Parameter Count & Memory Requirements

Estimate:
- Memory needed to store model weights
- Approximate training time
- Inference cost per token
"""

# Model configurations (inspired by real models)
models = {
    "GPT-2 Small": {"params": 0.124e9, "layers": 12, "hidden_dim": 768},
    "GPT-2 Medium": {"params": 0.355e9, "layers": 24, "hidden_dim": 1024},
    "GPT-2 Large": {"params": 0.774e9, "layers": 36, "hidden_dim": 1280},
    "GPT-2 XL": {"params": 1.5e9, "layers": 48, "hidden_dim": 1600},
    "GPT-3 Small": {"params": 125e9, "layers": 96, "hidden_dim": 12288},
    "GPT-3": {"params": 175e9, "layers": 96, "hidden_dim": 12288},
    "Llama-7B": {"params": 7e9, "layers": 32, "hidden_dim": 4096},
    "Llama-70B": {"params": 70e9, "layers": 80, "hidden_dim": 8192},
}

print("=" * 100)
print("MODEL SIZE & MEMORY ESTIMATES")
print("=" * 100)

for model_name, config in models.items():
    params = config["params"]
    
    # Memory estimates (rough)
    weight_memory_gb = (params * 4) / 1e9  # 4 bytes per parameter (float32)
    weight_memory_bf16_gb = (params * 2) / 1e9  # 2 bytes per parameter (bfloat16)
    
    # Training memory (weights + gradients + optimizer states)
    # Rough: 4x the weight memory
    training_memory_gb = weight_memory_gb * 4
    
    # Inference memory (weights + KV cache for context)
    # Rough: weight_memory + (2 * context_size * hidden_dim * layers * 2 bytes)
    # Simplified: weight_memory + 10% overhead for KV cache
    kv_cache_gb = weight_memory_gb * 0.1
    inference_memory_gb = weight_memory_gb + kv_cache_gb
    
    # Approximate training cost (FLOPs = 6 × params × tokens)
    tokens_seen = 300e9  # 300B tokens (typical for modern models)
    flops = 6 * params * tokens_seen
    tflops_per_gpu = 312  # V100: ~312 TFLOP/s (approximate)
    training_seconds = flops / (tflops_per_gpu * 1e12)
    training_hours = training_seconds / 3600
    training_days = training_hours / 24
    
    print(f"\n{model_name:20} ({params/1e9:7.1f}B params)")
    print(f"  Weight Memory (FP32):       {weight_memory_gb:7.1f} GB")
    print(f"  Weight Memory (BF16):       {weight_memory_bf16_gb:7.1f} GB")
    print(f"  Inference Memory (total):   {inference_memory_gb:7.1f} GB")
    print(f"  Training Memory (estimate): {training_memory_gb:7.1f} GB")
    print(f"  Training Time (300B tokens):{training_days:7.1f} days on 1 V100")
```

#### 6.2 Lab 1 — What You Should Observe

- **Memory scales linearly with parameters** (roughly 4 bytes per param for FP32).
- **Inference memory is dominated by weights**, not KV cache (unless context is very long).
- **Training memory is much larger** due to gradients and optimizer states.
- **Training time scales with parameter count**; larger models take much longer (or need more GPUs).

**Reflection prompts:**

1. Why would you want to use BFloat16 instead of FP32?
2. If you had 80GB of GPU memory, what's the largest model you could run?
3. How does this relate to the cost of running models in production?

---

### Lab 2: Context Window & Attention Cost

**Goal:** Understand how context window size affects computation.

#### 7.1 Lab 2 — Code

```python
"""
Lab 2: Context Window & Attention Cost

Show that:
- Self-attention scales quadratically with context length
- Longer context = more compute and memory
"""

import numpy as np

def attention_cost_flops(sequence_length, hidden_dim, num_heads, num_layers):
    """
    Rough estimate of FLOPs for self-attention.
    Attention cost per layer: ~2 × sequence_length² × hidden_dim
    """
    attention_flops_per_layer = 2 * sequence_length**2 * hidden_dim
    total_flops = attention_flops_per_layer * num_layers
    return total_flops

def attention_memory_gb(sequence_length, hidden_dim, num_layers):
    """
    Memory for attention matrices (QK^T) and values.
    Roughly: 2 × sequence_length² × num_heads × (hidden_dim / num_heads) × 2 bytes per layer
    Simplified: ~sequence_length² × 2 bytes per layer
    """
    qk_memory = sequence_length**2 * num_layers * 2 / 1e9
    return qk_memory

# Test different context windows
print("=" * 80)
print("CONTEXT WINDOW & ATTENTION COST")
print("=" * 80)

hidden_dim = 768
num_layers = 12
num_heads = 12

context_lengths = [512, 1024, 2048, 4096, 8192, 16384]

print(f"\nModel: {hidden_dim} hidden dim, {num_layers} layers, {num_heads} heads")
print(f"\n{'Context':>10} | {'Attention FLOPs':>15} | {'Attention Memory (GB)':>20} | {'Multiplier':>10}")
print("-" * 70)

baseline_flops = attention_cost_flops(1024, hidden_dim, num_heads, num_layers)

for ctx_len in context_lengths:
    flops = attention_cost_flops(ctx_len, hidden_dim, num_heads, num_layers)
    mem_gb = attention_memory_gb(ctx_len, hidden_dim, num_layers)
    multiplier = flops / baseline_flops
    
    print(f"{ctx_len:>10} | {flops/1e9:>15.1f}B | {mem_gb:>20.2f} | {multiplier:>10.1f}x")

print("\n" + "=" * 80)
print("KEY INSIGHT: Attention cost grows quadratically with context!")
print("Doubling context = 4x more compute and memory for attention.")
print("=" * 80)
```

#### 7.2 Lab 2 — What You Should Observe

- Attention FLOPs and memory scale with **context_length²**.
- Doubling context → 4x more attention cost.
- At 16K tokens, attention becomes the dominant cost.
- This is why longer context windows require optimization (sparse attention, flash attention).

**Reflection prompts:**

1. Why is attention cost quadratic while feed-forward cost is linear?
2. How would you handle a 1M-token context efficiently?
3. What trade-offs would you accept to support longer contexts?

---

### Lab 3: Training Data & Scaling Laws

**Goal:** Illustrate scaling laws and how to estimate model performance.

#### 8.1 Lab 3 — Code

```python
"""
Lab 3: Scaling Laws & Model Performance

Demonstrate:
- Performance improves with scale (parameters and data)
- Power-law relationship
- Estimation of new model performance
"""

import numpy as np
import math

def chinchilla_scaling_law(compute_budget):
    """
    Simplified Chinchilla scaling law.
    Optimal: allocate compute equally to model size and data.
    Empirically: params ≈ compute_budget / (6 * tokens_per_param)
    Tokens ≈ compute_budget / (6 * params)
    Optimal ratio: tokens ≈ 20 * params (roughly)
    """
    # Optimal split: params and data roughly balanced
    params_optimal = compute_budget / (6 * 20)  # Simplified
    tokens_optimal = compute_budget / (6 * params_optimal)
    return params_optimal, tokens_optimal

def performance_estimate(params, tokens_seen):
    """
    Rough power-law estimate of model loss (perplexity surrogate).
    Loss ≈ A / (params^alpha) + B / (tokens^beta)
    Simplified: Loss ≈ 10 / (params^0.07) + 10 / (tokens^0.16)
    Lower loss = better model.
    """
    loss_params = 10 / (params**0.07)
    loss_tokens = 10 / ((tokens_seen / 1e9)**0.16)
    total_loss = loss_params + loss_tokens
    return total_loss

# Test different compute budgets
print("=" * 100)
print("SCALING LAWS: Optimal Model Size & Data for Given Compute Budget")
print("=" * 100)

compute_budgets = [
    (1e18, "1 ExaFLOP"),
    (10e18, "10 ExaFLOP"),
    (100e18, "100 ExaFLOP"),
    (1000e18, "1 ZettaFLOP (1000 ExaFLOP)"),
]

for budget, label in compute_budgets:
    params, tokens = chinchilla_scaling_law(budget)
    loss = performance_estimate(params, tokens)
    
    print(f"\n{label}")
    print(f"  Compute Budget: {budget:.1e} FLOPs")
    print(f"  Optimal Params: {params/1e9:.1f}B")
    print(f"  Optimal Tokens: {tokens/1e9:.1f}B ({tokens/1e12:.1f}T)")
    print(f"  Est. Loss: {loss:.3f}")

print("\n" + "=" * 100)
print("COMPARISON: Allocating compute differently")
print("=" * 100)

budget = 1e20  # 100 ExaFLOP (very large)

configs = [
    ("Optimal (Chinchilla)", chinchilla_scaling_law(budget)),
    ("Large model, less data", (budget / (6 * 5), budget / (6 * (budget / (6 * 5))))),  # 5x more params
    ("Small model, more data", (budget / (6 * 40), budget / (6 * (budget / (6 * 40))))),  # 2x less params
]

print(f"\nCompute budget: {budget:.1e} FLOPs\n")
print(f"{'Config':20} | {'Params (B)':>12} | {'Tokens (B)':>12} | {'Est. Loss':>10}")
print("-" * 70)

for label, (params, tokens) in configs:
    loss = performance_estimate(params, tokens)
    print(f"{label:20} | {params/1e9:>12.1f} | {tokens/1e9:>12.1f} | {loss:>10.3f}")

print("\n" + "=" * 100)
print("KEY INSIGHT: Balanced scaling (Chinchilla) gives better loss than extreme configs!")
print("=" * 100)
```

#### 8.2 Lab 3 — What You Should Observe

- Optimal scaling balances parameters and tokens.
- Allocating too much to parameters (with limited data) is wasteful.
- Allocating too much to data (with tiny model) also wastes compute.
- The Chinchilla law provides a principled way to allocate a compute budget.

**Reflection prompts:**

1. Why does the performance scale as a power law (not exponentially)?
2. If your compute budget doubled, how would you allocate it?
3. How does this relate to your decision to fine-tune vs. pre-train?

---

## 7. Module 6 Summary & Strategic Takeaways

| Concept | Why It Matters | Practical Implication |
|---------|----------------|----------------------|
| **GPT-2 Blueprint** | Simple, scalable, enduring design | Modern LLMs follow this architecture; understanding GPT-2 explains them all |
| **Scaling Laws** | Performance improves predictably with scale | You can forecast model capability given compute budget |
| **Chinchilla Scaling** | Optimal allocation of compute | Balance parameters and data; don't maximize one dimension |
| **Context Window** | Limited to what model can "see" | Longer context requires optimization; affects cost |
| **Training Cost** | Scales with parameters × tokens | Large models require massive budgets; access is unequal |
| **Transformer Stability** | Architecture persists across scales | Safe to build long-term systems on transformer-based models |

---

## 8. Evolution Timeline

| Model | Year | Params | Context | Key Insight |
|-------|------|--------|---------|------------|
| GPT-2 | 2019 | 1.5B | 1K | Blueprint established; simple = powerful |
| GPT-3 | 2020 | 175B | 2K | Scale alone improves generalization dramatically |
| PaLM | 2022 | 540B | 2K | Chain-of-thought emerges at scale |
| Llama | 2023 | 70B | 2K | Chinchilla-optimal scaling; open weight |
| GPT-4 | 2023 | ? (100s B) | 128K | Multimodal; emergent reasoning; post-training dominates |

---

## 9. From Theory to Practice

### For Practitioners:
- If you have a fixed compute budget: use Chinchilla law to allocate between parameters and data.
- If you need long-context capabilities: expect to pay in compute; use sparse attention or newer architectures.
- If you need specific behavior: fine-tune on smaller, high-quality data rather than pre-training from scratch.
- If you need cutting-edge performance: expect to use the largest models available; scaling still works.

### For Researchers:
- Scaling laws remain predictable; you can forecast future model capabilities.
- Beyond scale, post-training and alignment become increasingly important (Module 8 and beyond).
- The transformer + next-token prediction pipeline is robust; innovation often comes from training techniques, not architecture.
