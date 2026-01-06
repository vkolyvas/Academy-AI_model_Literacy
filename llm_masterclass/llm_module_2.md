# LLM Masterclass: From Black Box to Architecture  
## Module 2 — Pre-Training: Internet as Raw Material

**Timestamps**: 00:01:00 – 00:07:47  

**Module Goal:** Build an intuitive, architecture-ready mental model of how the internet becomes training data, how that data is filtered, what "scale" really means, and why pre-training is best understood as **lossy compression of the internet**. Labs are deliberately **simpler and lighter** than Module 1: mostly small scripts and conceptual hands-on, no heavy frameworks.

---

## 1. What Happens in Pre-Training?

### 1.1 Internet as Raw Material (5+ sentences)

Pre-training starts with a massive corpus of text scraped from the internet: web pages, books, code, forums, documentation, and more. Conceptually, you can imagine starting with "everything text-like that is publicly reachable" and then progressively filtering it down into something usable for training a neural network. This raw material is extremely heterogeneous: high-quality research papers and official docs coexist with spam, duplicates, hate speech, SEO garbage, and nonsense. The role of the data pipeline is to **clean, filter, deduplicate, and structure** this chaos into a large but somewhat coherent training set. During pre-training, the model repeatedly sees small chunks of this text and learns to predict the next token; it never "reads" the whole internet in a human way, but instead samples batches of it millions or billions of times. Over time, this process distills statistical patterns about language, facts, styles, and reasoning templates into the model's parameters.

**Key idea:** The model does not store documents; it optimizes a function (the neural network) so that its outputs match the patterns in this data as closely as possible, under a next-token prediction objective.

---

### 1.2 Downloading and Filtering the Internet (5+ sentences)

If you naively train on "all text found online," you inherit every flaw of the public internet: bias, toxicity, redundancy, and low-quality content. Modern LLM pipelines therefore apply several stages of filtering: language detection, deduplication (removing near-identical copies of the same content), heuristic quality filters, classifier-based quality scoring, and domain whitelists/blacklists. Deduplication is essential because many web pages are mirrored, quoted, or scraped multiple times, and repeatedly training on near-identical text can cause overfitting and reduce diversity. Quality filtering matters because the model's behavior is heavily influenced by its training distribution: too much low-quality or toxic content will show up later as biases, harmful completions, or incoherent behavior. The end result is not a pristine dataset, but a **biased, curated slice of the internet** that is "good enough" to learn useful linguistic and world-knowledge patterns.

**Key idea:** Data curation is as important as model architecture—garbage in, garbage out scales with billions of parameters.

---

## 2. Scale, Diversity, and Quality of Data

### 2.1 Scale (5+ sentences)

Scale in LLMs refers both to **data size** (number of tokens) and **model size** (number of parameters). Empirically, performance improves predictably as you increase data and parameters together, following scaling laws: more tokens and more parameters yield lower loss and better downstream capabilities, up to a point. At small scales, the model underfits; it hasn't seen enough data to capture the complexity of language. At very large scales, if you keep growing the model without sufficient fresh data, you hit diminishing returns and eventually over-training on the same patterns. There is thus an approximate "sweet spot" where model size, data size, and compute budget are balanced. For practitioners, the implication is that **you can't fix a small dataset just by making the model huge**; data scale and diversity are first-class citizens in capability planning.

**Key idea:** Scale is not just bigger models; it's the coordinated scaling of data, parameters, and compute.

---

### 2.2 Diversity (5+ sentences)

Diversity means the training data spans many domains, writing styles, languages, and formats. A model trained mostly on programming code will be excellent at coding tasks but weak at creative writing or legal reasoning, while one trained mostly on informal web text might struggle with precise technical language. Diversity is crucial for **generalization**: the ability to perform well on tasks and domains that were not explicitly represented during training, but are related by underlying patterns. However, diversity without quality control can backfire: including too many noisy or adversarial sources can confuse the model, reinforce undesirable behaviors, or dilute its signal on high-value domains. In practice, data engineers often craft mixtures: some portion of high-quality books and curated corpora, some from filtered web sources, some from code, some from domain-specific datasets.

**Key idea:** Diversity is a tool to broaden capabilities, but it must be balanced against quality and alignment goals.

---

### 2.3 Quality (5+ sentences)

Quality is multidimensional: grammatical correctness, factual accuracy, absence of spam, clarity, and usefulness. High-quality data leads to models that produce more coherent, accurate, and helpful outputs, while low-quality data increases hallucinations, incoherence, and toxic or biased completions. Quality is often enforced with a combination of **heuristics** (e.g., minimum length, no excessive repetition), **learned filters** (models that classify text as good/bad), and **source selection** (e.g., giving more weight to respected corpora). For example, a line of random tokens or keyword-stuffed SEO content looks very different from a well-written article; training on too much of the former skews the model toward poor language habits. Practically, every percentage point of quality improvement at scale matters: small filter tweaks on trillions of tokens have system-level impact.

**Key idea:** A model is only as "smart" as the signal-to-noise ratio of the data it was trained on.

---

## 3. FineWeb as an Illustrative Dataset

### 3.1 What is FineWeb? (5+ sentences)

FineWeb (as an illustrative example) is a curated web-scale dataset that emphasizes high-quality, deduplicated, and filtered text. Instead of simply scraping everything, FineWeb applies rules and classifiers to remove boilerplate, spam, and low-quality pages, and to deduplicate near-identical content. It aims to produce a web dataset that is both large and clean, suitable for training or pre-training large language models. You can think of it as "common crawl, but scrubbed and refined," where significant engineering effort has gone into preserving useful text and discarding the worst noise. In many public LLM research projects, datasets in this spirit are used to show how better curation improves downstream benchmarks without changing model architecture.

**Key idea:** FineWeb-like datasets illustrate how **data engineering alone** can move model quality significantly.

---

### 3.2 Why Use FineWeb-like Datasets? (5+ sentences)

Training on raw, unfiltered web crawl is computationally expensive and yields poor behavior, because a large fraction of tokens contribute little to learning useful patterns. FineWeb-style datasets increase the **effective quality per token**, meaning each token is more likely to teach the model something valuable. This is especially important under compute constraints: given a fixed budget, you want every training step to move the model meaningfully closer to your desired behavior. Additionally, such datasets are easier to analyze and monitor for biases and policy violations, since they were built with explicit filtering stages. For practitioners, the message is that **investing in better data beats simply throwing more GPUs at the problem**.

**Key idea:** Curated datasets are a force multiplier for training efficiency and model behavior.

---

## 4. Pre-Training as Lossy Compression of the Internet

### 4.1 Compression Mental Model (5+ sentences)

A powerful mental model is to view pre-training as **compressing the internet into the weights of a neural network**. Instead of storing documents verbatim, the model learns a function that can approximate which token sequences are likely, given a history of tokens, based on patterns it has seen during training. Like any compression, this process is **lossy**: many rare details, exact phrasings, and specific facts are not preserved precisely. What remains is a kind of "statistical sketch" of language and knowledge, which allows the model to generate plausible continuations but not to reliably retrieve exact ground-truth facts. This explains why the model can write in the style of a famous author without reproducing any single book exactly—it has captured stylistic patterns and common phrases, not an indexed copy of the corpus. It also explains why hallucinations are inevitable: when the model lacks a precise memory of some fact, it still produces the **most statistically plausible completion**, even if it's wrong.

**Key idea:** Pre-training trades exactness for generality—excellent for generation, unreliable for precise retrieval.

---

### 4.2 Implications for Practice (5+ sentences)

Understanding pre-training as lossy compression immediately leads to architecture choices. For **factual or compliance-critical tasks**, you should not rely on the pre-trained model alone; instead, augment it with retrieval from trusted sources (RAG), structured knowledge bases, or tools that can fetch and verify facts. For **creative, summarization, or transformation tasks**, the compressed representation of the internet is a strength, enabling flexible recombination of patterns. This view also explains why **fine-tuning** or **instruction-tuning** can be so effective with relatively small datasets: you are nudging the model's compressed representation toward your desired behavior in key regions of its function space. Finally, it clarifies why you cannot "train out" every hallucination purely via pre-training; the objective function itself (next-token prediction) encourages plausible completions, not necessarily truthful ones.

**Key idea:** Use pre-trained models as **pattern engines**, not as authorities; design systems that correct for their lossy nature.

---

## 5. Practical Labs (Simplified)

Labs in this module are intentionally **easy and lightweight**: small Python scripts, no LangChain, and simple local reasoning about datasets. They're designed so you can run and tweak them quickly.

---

### Lab 1: Simulating a Tiny "Internet" and a Filter

**Goal:** Build intuition for "raw web" vs "filtered dataset" using a toy corpus.

#### 5.1 Lab 1 — Code

```python
"""
Lab 1: Tiny Internet → Filtered Corpus

Simulate:
- A small "raw web" of documents
- Simple filters (quality + deduplication)
- The idea that pre-training sees the FILTERED version
"""

from collections import Counter

# Step 1: Define a tiny "raw internet"
raw_documents = [
    "How to cook perfect pasta in 10 minutes.",
    "BUY CHEAP PILLS!!! CLICK HERE CLICK HERE CLICK HERE",
    "Neural networks are function approximators that learn from data.",
    "Neural networks are function approximators that learn from data.",  # duplicate
    "Visit my site!!! Visit my site!!! Visit my site!!!",
    "An introduction to large language models and transformers.",
    "LOREM IPSUM LOREM IPSUM LOREM IPSUM",
    "Python is a popular programming language for data science and AI.",
]

print("=" * 60)
print("RAW DOCUMENTS")
print("=" * 60)
for i, doc in enumerate(raw_documents, start=1):
    print(f"{i}. {doc}")

# Step 2: Simple quality filter (toy heuristic)
def is_high_quality(doc: str) -> bool:
    doc_lower = doc.lower()
    # Toy rules:
    if "click here" in doc_lower:
        return False
    if "buy cheap" in doc_lower:
        return False
    if "visit my site" in doc_lower:
        return False
    if "lorem ipsum" in doc_lower:
        return False
    # Very short documents could be considered low quality
    if len(doc.split()) < 5:
        return False
    return True

filtered_docs = [d for d in raw_documents if is_high_quality(d)]

print("\n" + "=" * 60)
print("AFTER QUALITY FILTER")
print("=" * 60)
for i, doc in enumerate(filtered_docs, start=1):
    print(f"{i}. {doc}")

# Step 3: Deduplication
unique_docs = list(dict.fromkeys(filtered_docs))  # preserves order, removes duplicates

print("\n" + "=" * 60)
print("AFTER DEDUPLICATION")
print("=" * 60)
for i, doc in enumerate(unique_docs, start=1):
    print(f"{i}. {doc}")

print("\n" + "=" * 60)
print("STATS")
print("=" * 60)
print(f"Raw documents:        {len(raw_documents)}")
print(f"After quality filter: {len(filtered_docs)}")
print(f"After deduplication:  {len(unique_docs)}")
```

#### 5.2 Lab 1 — What You Should Observe

- Some documents are removed as "spammy" or low-quality.
- Exact duplicates are removed by deduplication.
- The resulting dataset is smaller, but of higher average quality.
- This mimics, at toy scale, what happens in real pre-training pipelines.

**Reflection prompts:**

1. How would changing the filter rules change the model's eventual behavior?
2. What happens if you remove too aggressively (e.g., filter out most technical content)?
3. How could you add a simple **domain whitelist** (e.g., only keep docs that contain "neural", "python", "language models")?

---

### Lab 2: Tokens as "Raw Material Units"

**Goal:** Understand that training data is measured in tokens, not characters or "pages", and get a feel for tokenization.

We won't implement a full tokenizer here; instead, we'll use a rough approximation: split on whitespace and punctuation, and observe counts. The point is conceptual, not exact.

#### 6.1 Lab 2 — Code

```python
"""
Lab 2: Rough Token Counting

Approximate how many "tokens" are in a tiny corpus and see
how scale quickly grows when you imagine millions of documents.
"""

import re

documents = [
    "Neural networks are function approximators that learn from data.",
    "An introduction to large language models and transformers.",
    "Python is a popular programming language for data science and AI.",
]

def rough_tokenize(text: str):
    # Very rough: split on non-alphanumeric
    tokens = re.split(r"[^A-Za-z0-9]+", text)
    tokens = [t for t in tokens if t]  # remove empty
    return tokens

print("=" * 60)
print("DOCUMENTS & ROUGH TOKENS")
print("=" * 60)

total_tokens = 0
for i, doc in enumerate(documents, start=1):
    tokens = rough_tokenize(doc)
    total_tokens += len(tokens)
    print(f"\nDoc {i}: {doc}")
    print(f"Tokens ({len(tokens)}): {tokens}")

print("\n" + "=" * 60)
print("TOTAL TOKENS")
print("=" * 60)
print(f"Total tokens in this tiny corpus: {total_tokens}")

# Now scale up conceptually
million_docs_tokens = total_tokens * 1_000_000
print(f"\nIf you had 1 million similar docs, rough tokens ≈ {million_docs_tokens:,}")
```

#### 6.2 Lab 2 — What You Should Observe

- Even a tiny corpus produces dozens of tokens.
- Scaling to millions of documents quickly leads to **billions** of tokens.
- This is why **token count** is a primary unit for training cost and data scale.

**Reflection prompts:**

1. If each training step uses, say, 2,048 tokens, how many steps would you need to see the corpus once?
2. How does this help you reason about cost when fine-tuning vs. pre-training?
3. How might subword tokenization (BPE) change these counts?

---

### Lab 3: Lossy Compression Analogy with Strings

**Goal:** Experience the idea of lossy vs lossless "compression" in a toy way to anchor the pre-training analogy.

We'll "compress" strings by only keeping some information (e.g., first letters of words), then "decompress" by reconstructing plausible sentences—not necessarily the originals.

#### 7.1 Lab 3 — Code

```python
"""
Lab 3: Toy Lossy Compression

- "Compress" sentences into a simple sketch (first letters of each word)
- "Decompress" by reconstructing plausible sentences from the sketch
This mirrors how LLMs reconstruct plausible text from compressed patterns.
"""

import random

sentences = [
    "Neural networks learn patterns from data.",
    "Large language models compress the internet.",
    "Pre-training is a form of lossy compression.",
    "High-quality data improves model behavior.",
]

def compress(sentence: str):
    words = sentence.split()
    # "Compression": keep first letter of each word
    return [w[0].lower() for w in words]

def decompress(sketch):
    # "Decompression": make up a plausible sentence with same number of words
    vocab = {
        "n": ["neural", "new", "novel"],
        "l": ["large", "language", "learning"],
        "m": ["models", "memory", "methods"],
        "c": ["compress", "compute", "capture"],
        "d": ["data", "details", "documents"],
        "p": ["pre-training", "patterns", "probabilities"],
        "h": ["high-quality", "huge", "hidden"],
        "i": ["internet", "information", "insights"],
    }
    words = []
    for letter in sketch:
        candidates = vocab.get(letter, [letter * 3])
        words.append(random.choice(candidates))
    return " ".join(words).capitalize() + "."

print("=" * 60)
print("ORIGINAL → COMPRESSED → DECOMPRESSED")
print("=" * 60)

for s in sentences:
    sketch = compress(s)
    recon = decompress(sketch)
    print(f"\nOriginal:     {s}")
    print(f"Compressed:   {sketch}")
    print(f"Reconstructed:{recon}")
```

#### 7.2 Lab 3 — What You Should Observe

- The reconstructed sentences are **plausible**, but they are not the originals.
- The "compression" preserves some structure (word count, some letters) but loses details.
- This is analogous to how a pre-trained model can generate text that "feels right" without reproducing the exact training samples.

**Reflection prompts:**

1. How does this analogy help you understand hallucinations?
2. If you wanted more faithful reconstruction, what extra information would you store?
3. How does this relate to **parameter count** and **data scale** in real models?

---

## 8. Module 2 Summary & Strategic Takeaways

- **Internet → Filtered Corpus:** Pre-training starts from messy web data but heavily filters and deduplicates it before training.  
- **Scale, Diversity, Quality:** All three dimensions shape what the model can do; they must be tuned together, not independently.  
- **FineWeb-like Datasets:** Carefully curated web corpora significantly improve efficiency and behavior, even without changing model architecture.  
- **Lossy Compression of the Internet:** Pre-training builds a statistical sketch of language and knowledge that is excellent for generation but unreliable for exact retrieval.  
- **Architectural Implication:** Treat pre-trained models as **pattern engines** and always consider retrieval, tools, and post-training when you need reliability, truthfulness, or domain specificity.

---

## 9. Next Steps

Continue to Module 3 (Tokenization) to understand how text becomes the atomic units the model operates on.