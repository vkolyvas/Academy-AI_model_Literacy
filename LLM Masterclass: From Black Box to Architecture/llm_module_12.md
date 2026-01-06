# LLM Masterclass: From Black Box to Architecture  
## Module 12 — Jagged Intelligence & Failure Modes

**Module Goal:** Understand that LLM capabilities are **non-monotonic**: models can be superhuman at complex reasoning but fail spectacularly at simple tasks. Learn to recognize failure modes, understand why they occur, and design systems that work around them.

---

## 1. The Jagged Capability Curve

### 1.1 Non-Monotonic Intelligence

LLMs don't improve uniformly across tasks with scale. A larger model might excel at reasoning, coding, and creative writing, yet fail at: counting letters in a word, recognizing simple patterns not in training data, or adhering to strict format requirements. This creates a **jagged capability curve**: performance peaks sharply in some domains (expertise from training data), drops suddenly in others (out-of-distribution), then peaks again elsewhere. For example, GPT-4 can write a novel but might fail at "Count the number of 'r's in 'strawberry'." A 7B parameter model might beat a 70B model on a specific domain if the 7B was specialized on that domain during training. This non-monotonicity violates intuitions about intelligence: bigger should be better, but it's not universally true. The jaggedness occurs because model performance is determined entirely by what patterns exist in training data and whether the model learned them. Simple tasks like counting aren't well-represented in natural language training data (few texts describe character-by-character counting), while complex reasoning tasks appear throughout training data. As a result, complex tasks benefit from scale while simple tasks don't.

**Key idea:** Bigger models aren't universally smarter; they're smarter at tasks represented in training data.

---

### 1.2 Understanding Jaggeredness

Jaggeredness is not a flaw; it's a consequence of the training objective. The model is trained on next-token prediction, which emphasizes learning patterns in natural language text. Tasks that appear naturally in text (reasoning, writing, explanation) are learned well. Tasks that don't (exact counting, precise formatting, out-of-distribution logic) are learned poorly. Additionally, different models (trained on different data or with different post-training) have different jaggeredness patterns. A model trained on large amounts of code excels at programming but might be weaker at poetry. A model trained on diverse data is more generalist but weaker in any single domain. For practitioners, jaggeredness means: **test your model thoroughly on your specific tasks**. Don't assume strong performance on one task predicts performance on others. Design systems that acknowledge jaggeredness: use tools for tasks where the model is jagged (e.g., external calculator for math), and rely on the model for tasks where it's strong. Finally, recognize that jaggeredness is a feature of LLMs that won't be eliminated by just scaling; it's fundamental to how language models work.

**Key idea:** Jaggeredness is inevitable; design systems that work around it rather than expecting fixes through scaling alone.

---

## 2. Common Failure Modes

### 2.1 Failure Mode Categories

Several failure modes are consistent across LLMs. **Counting & enumeration**: Models struggle to count characters, items in a list, or occurrences of a substring. They know what counting is conceptually but can't execute it reliably. **Format adherence**: Asking for output in a specific format often fails; the model generates the right content but in the wrong structure. **Negation & logic**: "Tell me everything except X" often fails; the model forgets the negation. **Precise math**: Arithmetic beyond the training distribution fails; models can't reliably compute 847 + 389 but can generate an explanation of how to do it. **Long-range dependencies**: In very long documents, the model loses track of earlier context or contradicts itself. **Hallucination under pressure**: When asked a question it doesn't know, the model generates confident lies rather than admitting uncertainty. **Self-correction**: Models often don't catch their own errors, even when errors are obvious. **Following complex constraints**: Multi-condition constraints (if A then do X, if B do Y, if A and B...) confuse the model. Understanding these failure modes helps you design around them: use tools for math, verifiers for format, external state for long-range, clarifying prompts for complex constraints.

**Key idea:** Failure modes are predictable; learn them and design mitigation accordingly.

---

### 2.2 Why Failure Modes Occur

Failure modes occur for multiple reasons. First, **training data gap**: If a task doesn't appear in training data, the model hasn't learned it. Counting characters appears rarely; thus, models are weak at it. Second, **objective mismatch**: The training objective (next-token prediction) doesn't incentivize correctness on tasks like formatting; it incentivizes plausibility. Third, **token constraint**: Some tasks require more tokens than is allocated; counting items in a large list requires many tokens of attention. Fourth, **architectural limitation**: The transformer attention mechanism is better at semantic reasoning than symbolic counting or exact matching. Fifth, **learned shortcuts**: The model sometimes learns shortcuts that work most of the time but fail on edge cases. For example, it learns "numbers in sequence" and thus gets 847+389 wrong because it learned an approximation that works for smaller numbers. Understanding these root causes helps you choose the right mitigation: external tools for capabilities the model lacks, prompts that better align with the training objective, or simply avoiding the task for the model and delegating it entirely.

**Key idea:** Failure modes have root causes; understanding them guides mitigation choice.

---

## 3. Identifying & Working Around Failures

### 3.1 Testing & Diagnosis 

To identify failure modes in your use case, systematic testing is essential. First, **create test cases** covering normal cases, edge cases, and adversarial cases. For example, if using the model for customer support, test straightforward questions, complex queries, contradictory instructions, and out-of-domain questions. Second, **measure performance**: Don't just try a few examples; test on 100+ cases and measure success rate, error types, and patterns. Third, **analyze failures**: When the model fails, diagnose why. Is it a knowledge gap? A formatting mistake? A reasoning error? Different failure types require different solutions. Fourth, **segment by difficulty**: Separate easy, medium, and hard tasks; identify the threshold where performance drops. Fifth, **compare with baselines**: Test multiple models and versions; understand how performance varies. Documentation of failure modes is as important as documentation of capabilities. Build a failure mode registry: "On queries about pricing, the model hallucinates 40% of the time" helps you know when to trigger external systems or human review.

**Key idea:** Systematic testing reveals failure modes; documentation prevents repeating mistakes.

---

### 3.2 Mitigation Strategies 

For each failure mode, multiple mitigation strategies exist. **Redesign the prompt**: Sometimes clearer instructions or different framing shifts the model toward a better behavior. **Use external tools**: Calculators, formatters, retrieval systems, and verification tools can handle tasks the model can't. **Decompose the task**: Break complex tasks into simpler subtasks; the model might succeed on each part. **Add verification**: Ask the model to check its own work or use another system to verify outputs. **Escalate to humans**: For high-stakes or ambiguous cases, route to human review. **Accept limitations**: Sometimes the best strategy is to simply not use the model for that task. **Fine-tune or retrieval**: If a task is critical, invest in fine-tuning the model on that task or using retrieval to ground outputs. The best strategy depends on the stakes (how bad is failure?), frequency (how often does this occur?), and cost (what's the mitigation cost?). In production, effective systems layer multiple strategies: prompting first, then tools, then verification, then escalation.

**Key idea:** Mitigation is layered; no single strategy solves all failures.

---

## 4. Practical Labs (Failure Mode Discovery)

---

### Lab 1: Identifying Failure Modes Through Testing

**Goal:** Simulate systematic testing to discover failure mode patterns.

#### 4.1 Lab 1 — Code

```python
"""
Lab 1: Failure Mode Discovery Through Testing

Simulate testing a model on various task types and identifying patterns.
"""

def simulate_model_performance(task_category, task_difficulty):
    """Simulate model performance across task categories and difficulties."""
    
    performance_matrix = {
        "counting": {
            "easy": 0.95,      # Count items in a list
            "medium": 0.70,    # Count letters in a word
            "hard": 0.20,      # Count occurrences of a substring
        },
        "math": {
            "easy": 0.90,      # Simple arithmetic
            "medium": 0.60,    # Multi-digit arithmetic
            "hard": 0.10,      # Out-of-distribution numbers
        },
        "reasoning": {
            "easy": 0.85,
            "medium": 0.80,
            "hard": 0.70,
        },
        "writing": {
            "easy": 0.90,
            "medium": 0.88,
            "hard": 0.85,
        },
        "format": {
            "easy": 0.95,      # Simple format
            "medium": 0.60,    # Complex format with multiple constraints
            "hard": 0.20,      # Strict format with edge cases
        },
    }
    
    return performance_matrix.get(task_category, {}).get(task_difficulty, 0.5)

print("=" * 80)
print("FAILURE MODE DISCOVERY: Testing Across Task Categories")
print("=" * 80)

categories = ["counting", "math", "reasoning", "writing", "format"]
difficulties = ["easy", "medium", "hard"]

print(f"\n{'Task Category':15} | {'Easy':>8} | {'Medium':>8} | {'Hard':>8} | {'Failure Mode?':15}")
print("-" * 65)

failure_modes = []

for category in categories:
    easy = simulate_model_performance(category, "easy")
    medium = simulate_model_performance(category, "medium")
    hard = simulate_model_performance(category, "hard")
    
    print(f"{category:15} | {easy*100:>7.0f}% | {medium*100:>7.0f}% | {hard*100:>7.0f}% |", end=" ")
    
    # Detect failure pattern
    if hard < 0.5 and easy > 0.8:
        print("Jagged ⚠️")
        failure_modes.append(f"{category}: Sharp drop at hard difficulty")
    elif medium < 0.5:
        print("Weak 🔴")
        failure_modes.append(f"{category}: Consistently weak")
    else:
        print("OK ✓")

print("\n" + "=" * 80)
print("IDENTIFIED FAILURE MODES:")
print("=" * 80)

for mode in failure_modes:
    print(f"- {mode}")

print("\n" + "=" * 80)
print("MITIGATION RECOMMENDATIONS:")
print("=" * 80)

for mode in failure_modes:
    if "counting" in mode:
        print("→ Counting: Use external tool (Python len/count)")
    elif "math" in mode:
        print("→ Math: Integrate calculator API")
    elif "format" in mode:
        print("→ Format: Use structured output parsing or template")
```

#### 4.2 Lab 1 — What You Should Observe

- Counting is weak; math is weak; format is jagged (strong on easy, weak on hard)
- Reasoning and writing are relatively strong across difficulties
- Jagged pattern: strong on trained tasks, weak on edge cases

---

### Lab 2: Mitigation Strategy Selection

**Goal:** Given a failure mode, choose appropriate mitigation.

#### 5.1 Lab 2 — Code

```python
"""
Lab 2: Choosing Mitigation Strategies for Failure Modes

Map failure modes to mitigation strategies based on stakes and cost.
"""

failure_modes_and_mitigations = {
    "counting_letters": {
        "failure_rate": 0.80,
        "mitigations": {
            "Redesign prompt": {"cost": "low", "effectiveness": "low"},
            "External tool": {"cost": "low", "effectiveness": "high"},
            "Decompose task": {"cost": "medium", "effectiveness": "medium"},
            "Accept limitation": {"cost": "none", "effectiveness": "none"},
        },
        "best": "External tool",
    },
    "arithmetic_large_numbers": {
        "failure_rate": 0.90,
        "mitigations": {
            "Redesign prompt": {"cost": "low", "effectiveness": "low"},
            "Calculator API": {"cost": "low", "effectiveness": "high"},
            "Fine-tune on math": {"cost": "high", "effectiveness": "high"},
        },
        "best": "Calculator API",
    },
    "format_adherence": {
        "failure_rate": 0.40,
        "mitigations": {
            "Clearer prompt": {"cost": "low", "effectiveness": "medium"},
            "Structured output": {"cost": "medium", "effectiveness": "high"},
            "Human verification": {"cost": "high", "effectiveness": "high"},
        },
        "best": "Clearer prompt first, then structured output if needed",
    },
}

print("=" * 80)
print("MITIGATION STRATEGY SELECTION")
print("=" * 80)

for failure_mode, details in failure_modes_and_mitigations.items():
    print(f"\n{failure_mode.upper()} (Failure Rate: {details['failure_rate']*100:.0f}%)")
    print(f"Recommended: {details['best']}")
    print(f"Options:")
    for strategy, attributes in details['mitigations'].items():
        print(f"  - {strategy}: Cost={attributes['cost']}, Effectiveness={attributes['effectiveness']}")
```

---

## 5. Module 12 Summary

| Insight | Implication |
|---------|------------|
| **Non-monotonic capability** | Don't assume bigger = better on all tasks |
| **Jaggeredness is fundamental** | Work around it; don't expect fixes from scale alone |
| **Failure modes are predictable** | Test systematically; document failure patterns |
| **Root causes matter** | Different failures require different mitigations |
| **Layered defense** | Combine prompting, tools, verification, escalation |

