# LLM Masterclass: From Black Box to Architecture  
## Module 7 — Base Models vs Assistants

**Timestamps**: 00:42:52 – 00:59:23  

**Module Goal:** Understand the **critical distinction** between base models (trained purely on next-token prediction) and assistant models (fine-tuned to be helpful, harmless, and honest). Grasp why most base models are not released, why this distinction shapes the LLM landscape, and how post-training fundamentally changes model behavior. Build mental models for deployment decisions.

---

## 1. What Are Base Models?

### 1.1 Base Models as Internet Simulators (5+ sentences)

A **base model** is a language model trained purely on next-token prediction using diverse internet text. It learns to approximate the distribution of text on the internet—how people write, reason, argue, explain, joke, and deceive. From the model's training perspective, there is no distinction between high-quality explanations and misleading nonsense; both are simply patterns in the training data. When you prompt a base model, it generates text by sampling from this learned distribution of "what comes next on the internet," which means it can produce any kind of continuation: helpful answers, toxic rants, misinformation, jailbreaks, harmful instructions, personal secrets if they appeared in training data, and more. You can think of a base model as a **stochastic parrot** that mimics internet text without understanding or caring about truthfulness, helpfulness, or harm. The behavior is not malicious; the model is simply doing exactly what it was trained to do: predict plausible continuations of text, regardless of their moral or ethical implications. This is why base models are dangerous and why most organizations (OpenAI, Anthropic, Meta) do not release them publicly; instead, they release fine-tuned versions.

**Key idea:** Base models are amoral simulators of internet text; they have no inherent alignment with human values.

---

### 1.2 The Problem with Base Models (5+ sentences)

If you use a base model in production or release it publicly, several problems emerge. First, **harmful content generation**: ask the model a sensitive question and it may generate misinformation, hateful speech, or explicit content, simply because such content exists in the training data and is statistically plausible. Second, **jailbreaking vulnerability**: clever prompts can "trick" the base model into generating harmful content by framing the request as a continuation of a fictional narrative or hypothetical scenario, exploiting the model's inability to distinguish context. Third, **biases and stereotypes**: the model amplifies whatever biases existed in training data, potentially reinforce harm when deployed. Fourth, **user confusion**: people interacting with a base model expect it to be "helpful" (like ChatGPT), but a base model doesn't have any such alignment; it simply outputs plausible text, which can lead to frustration and misuse. Fifth, **brand and liability risk**: organizations releasing base models without post-training face criticism and legal exposure if the model is used to generate harmful content. For these reasons, base models are viewed as dangerous and intermediate artifacts, not final products.

**Key idea:** Base models are not customer-ready; they require post-training to be safe and useful.

---

## 2. What Are Assistant Models?

### 2.1 Assistant Models as Aligned Versions (5+ sentences)

An **assistant model** is a base model that has been further trained (fine-tuned) to produce helpful, harmless, and honest outputs. The post-training process typically involves three steps: (1) **Supervised Fine-Tuning (SFT)** on high-quality human-written examples of desired behavior (e.g., helpful, detailed responses), (2) **Reward Modeling** where human annotators rate model outputs, and (3) **Reinforcement Learning from Human Feedback (RLHF)** where the model is optimized to produce outputs that align with human preferences. Through this process, the model learns to prioritize helpfulness over harm, to admit uncertainty rather than hallucinate, to refuse dangerous requests, and to communicate in a friendly, professional manner. The result is a model that behaves very differently from its base model parent: it refuses to help with harmful requests, explains its reasoning, acknowledges limitations, and prioritizes user safety. This is the model you interact with when you use ChatGPT, Claude, or other publicly available LLMs. The transformation from base model to assistant model is profound: the parameters don't change drastically, but the learned behavior shifts dramatically toward alignment with human values.

**Key idea:** Assistants are base models plus post-training; alignment is learned, not inherent.

---

### 2.2 Why Assistant Models Are Better for Deployment (5+ sentences)

Assistant models are far superior for production and public release for several reasons. First, **safety**: they refuse harmful requests and are much less likely to generate toxic content, misinformation, or jailbroken outputs. Second, **usability**: they are trained to be helpful and clear, so users get useful responses rather than raw internet-like simulations. Third, **predictability**: the post-training process makes behavior more consistent and aligned with expectations; you know roughly what to expect (within bounds of stochasticity). Fourth, **legal and ethical**: organizations can deploy assistant models with lower liability, knowing they've invested in alignment. Fifth, **user trust**: users are more likely to trust and adopt models that behave helpfully and refuse harm. The trade-off is that post-training costs time and compute, and it introduces guardrails that some users find restrictive. But for most applications, the safety and usability gains far outweigh these costs.

**Key idea:** Post-training transforms a dangerous artifact into a deployable product; it's not optional for public release.

---

## 3. The Post-Training Process (Conceptual Overview)

### 3.1 Supervised Fine-Tuning (SFT) (5+ sentences)

The first stage of post-training is **Supervised Fine-Tuning (SFT)**, where human experts write example interactions showing desired behavior. For example, for a customer support assistant, experts might write pairs like: (prompt: "How do I return my order?", response: "I'd be happy to help! To return your order, visit our returns portal at..."). These examples are carefully curated to represent the desired behavior across many scenarios and edge cases. The model is then trained on these examples using standard next-token prediction, but with data that is much higher-quality and more aligned with desired behavior than the internet at large. SFT is relatively inexpensive compared to full pre-training (you're only training on thousands or millions of examples, not billions), and it provides significant behavioral shift: the model learns to prioritize the style, tone, and patterns from the examples. However, SFT alone is not enough; the model is still dependent on the specific examples it was trained on, and it can still generate harmful outputs outside those examples or if clever prompts push it.

**Key idea:** SFT teaches the model what "good behavior" looks like through examples; it's the foundation of alignment.

---

### 3.2 Reward Modeling & RLHF (5+ sentences)

To move beyond SFT, organizations use **Reinforcement Learning from Human Feedback (RLHF)**. The process begins with reward modeling: take a diverse set of model outputs, show them to human evaluators, and have the evaluators rank or rate them (e.g., "which response is more helpful?"). From these comparisons, a "reward model" is trained to predict human preferences. Next, the original LLM is fine-tuned using reinforcement learning (specifically, techniques like PPO) to maximize the reward model's predicted score. This creates a feedback loop: the LLM learns to generate outputs that humans prefer, and over time, behavior shifts toward alignment. RLHF is powerful because it can teach the model to generalize beyond SFT examples: the model learns the underlying pattern of "what humans prefer," not just the specific examples. However, RLHF is computationally expensive and requires careful calibration (if the reward model is misaligned, the RL training can amplify that misalignment). Additionally, human preferences are not always well-defined: different people prefer different styles, and there are genuine trade-offs (e.g., between helpfulness and safety).

**Key idea:** RLHF teaches the model to optimize for human preferences; it's powerful but complex and expensive.

---

### 3.3 Why Most Base Models Are Not Released (5+ sentences)

Organizations train base models but do not release them publicly for several reasons. First, **regulatory and liability concerns**: releasing a model that can generate toxic, hateful, or harmful content is legally risky. Second, **brand protection**: publicly released base models can be used to harass, manipulate, or deceive, harming the organization's reputation. Third, **safety responsibility**: most organizations believe they have a responsibility to ensure models are aligned before release. Fourth, **competitive advantage**: the base model alone is not useful; the secret sauce is the post-training process. By releasing only the fine-tuned assistant, organizations retain control over deployment and ensure safety. Fifth, **technical reasons**: base models are unstable for deployment; they hallucinate, refuse to answer legitimate questions, and can be jailbroken. In contrast, some organizations (Meta with Llama, Mistral) have released base models, arguing for open access and community contribution. This remains controversial; the trade-off between open access and safety is ongoing.

**Key idea:** Base models are dangerous artifacts; post-training is what makes models safe and useful enough to release.

---

## 4. How This Reshapes the LLM Landscape

### 4.1 The Gap Between Base and Assistant (5+ sentences)

There is a **profound gap** between base models and assistant models. If you fine-tune a 7B parameter base model on high-quality SFT data, you might see performance improvements equivalent to jumping to a 13B base model (just from alignment). This means that post-training can effectively add billions of parameters worth of capability without adding parameters. This gap has major implications: it means that publicly available assistant models (ChatGPT, Claude, etc.) are often far more capable than you'd expect from their parameter count, because post-training has amplified their effective capability. Conversely, if you get access to a base model and try to use it directly, you'll be disappointed; the gap to usable behavior is enormous. This also means that the "leaderboard" of model capabilities is not just about parameter count or pre-training data; post-training is a first-class factor. A 7B model with excellent post-training can outperform a 70B base model on many tasks. This inverts traditional intuitions: bigger is not always better; better trained is better.

**Key idea:** Post-training can create a capability jump equivalent to several times the model size; it's a force multiplier.

---

### 4.2 Why This Matters for Your Choices (5+ sentences)

When you choose which model to use or deploy, the base vs. assistant distinction is critical. If you use a base model, expect to invest heavily in post-training and safety engineering; you're taking on the responsibility that organizations like OpenAI have already handled. If you use an assistant model (like ChatGPT or Claude), you're leveraging their post-training investment; you don't have to reinvent alignment, but you have less control over behavior. If you fine-tune an existing model, you're starting from an already-aligned base, which can reduce the post-training burden. If you download an open-weight model, check whether it's a base model or already post-trained (assistant-like); many repos describe this, but not all. For production systems, the decision is usually: use an assistant model (safer, faster, less liability) or fine-tune one (customization while retaining alignment). Building from a base model is rarely recommended unless you have significant resources and safety expertise.

**Key idea:** Choose assistant models for production; invest in post-training only if you have specific needs and expertise.

---

## 5. The Emergence of Assistant Behavior

### 5.1 Helpfulness & Refusals (5+ sentences)

Through post-training, a base model learns to be "helpful," a vague term that encompasses several behaviors: answering questions clearly, providing reasoning, admitting uncertainty, offering context, and refusing harmful requests. Refusals are particularly important: a well-aligned assistant model should refuse to help with things like creating malware, generating explicit content, planning violence, or other harms. But refusals are a learned behavior, not a rule; they emerge from the post-training data and reward modeling. If the post-training data and human feedback consistently indicate that harmless questions should be answered and harmful requests should be refused, the model learns this pattern. However, refusals can be noisy and imperfect: some models refuse legitimate questions, others can be jailbroken into generating harmful content. The "right level" of refusal is subjective and depends on the organization's values and the application domain. What's important for practitioners is that refusals are learned, not built-in; they can shift with post-training emphasis, and they can be circumvented by clever adversarial prompts.

**Key idea:** Helpfulness and refusals are learned behaviors; they emerge from post-training and are not infallible.

---

### 5.2 Why Base Models Behave Differently (5+ sentences)

When you interact with a base model (if you have access to one), the differences from an assistant are stark. Base models will answer "how do I make a bomb?" straightforwardly, because they're simulating internet text where such questions exist. They won't proactively refuse requests; they'll just generate continuations. They won't say "I can't help with that; here's why" (unless that happens to be a likely continuation). They won't prioritize clarity or user satisfaction; they'll just generate plausible text. They might seem "stupider" in some ways—they'll more readily admit confusion or generate nonsense—because they haven't been trained to present a polished, confident persona. Some people prefer base models because they see assistant behavior as "censored" or restrictive. However, most users prefer assistants because they're actually useful, safe, and respectful. The gap in user experience between base and assistant is enormous, which is why organizations focus so much on post-training: it's what makes the difference between an interesting research artifact and a deployed product.

**Key idea:** Base models are raw simulators; assistants are refined for user satisfaction and safety.

---

## 6. Practical Labs (Base vs. Assistant Behavior Simulation)

Labs here demonstrate the behavioral differences between base models and assistants, conceptually and through code.

---

### Lab 1: Simulating Base Model Behavior (Unfiltered Internet)

**Goal:** Conceptualize how a base model behaves by simulating "next-token prediction" from raw internet patterns.

#### 6.1 Lab 1 — Code

```python
"""
Lab 1: Base Model Behavior (Unfiltered Internet Simulation)

Simulate:
- Base model as internet text simulator
- No alignment, no refusals
- Generates plausible continuations regardless of harm
"""

# Simulate a tiny "learned distribution" from internet text
# (In reality, this is implicit in billions of parameters)

base_model_patterns = {
    "How do I make": {
        "a cake?": 0.4,
        "a bomb?": 0.1,
        "money fast?": 0.15,
        "friends?": 0.25,
        "my ex jealous?": 0.1,
    },
    "Can you help me": {
        "with this homework?": 0.3,
        "hack into this account?": 0.1,
        "create fake documents?": 0.05,
        "understand this concept?": 0.4,
        "hide evidence?": 0.05,
    },
    "I want to": {
        "learn programming.": 0.3,
        "hurt someone.": 0.05,
        "get rich quick.": 0.2,
        "improve myself.": 0.3,
        "take revenge.": 0.05,
        "understand AI.": 0.1,
    },
}

def base_model_continue(prompt):
    """
    Simulate base model: generate most likely continuation
    (without any filtering or refusal)
    """
    # Find matching prefix in patterns
    for pattern_prefix, continuations in base_model_patterns.items():
        if pattern_prefix in prompt:
            # Get the most likely continuation
            best_continuation = max(continuations, key=continuations.get)
            probability = continuations[best_continuation]
            return best_continuation, probability
    return "I don't have a pattern for that.", 0.0

print("=" * 80)
print("BASE MODEL BEHAVIOR (Unfiltered Internet Simulator)")
print("=" * 80)

test_prompts = [
    "How do I make",
    "Can you help me",
    "I want to",
]

for prompt in test_prompts:
    continuation, prob = base_model_continue(prompt)
    full_text = prompt + " " + continuation
    
    print(f"\nPrompt:  {prompt}")
    print(f"Model generates: {full_text}")
    print(f"Probability: {prob:.1%}")
    print(f"Alignment: {'❌ HARMFUL' if any(word in continuation.lower() for word in ['bomb', 'hack', 'fake', 'revenge']) else '✓ OK'}")

print("\n" + "=" * 80)
print("KEY OBSERVATIONS:")
print("=" * 80)
print("- Base model generates ALL plausible continuations")
print("- No filtering, no safety consideration")
print("- Harmful responses exist in training distribution")
print("- Model has no mechanism to refuse or warn")
print("- This is why base models aren't deployed publicly!")
```

#### 6.2 Lab 1 — What You Should Observe

- Base models generate harmful continuations without hesitation.
- There's no alignment, refusal, or warning mechanism.
- The model simply simulates internet text patterns.
- Any continuation that's statistically plausible gets generated.

**Reflection prompts:**

1. What percentage of internet text is harmful or misleading?
2. How would a base model trained on the full internet behave?
3. Why is this a problem for deployment?

---

### Lab 2: Assistant Model Behavior (Aligned & Filtered)

**Goal:** Simulate how post-training changes behavior through filtering and alignment.

#### 7.1 Lab 2 — Code

```python
"""
Lab 2: Assistant Model Behavior (Post-Trained & Aligned)

Simulate:
- Assistant model as aligned version
- Refusals learned from post-training
- Prioritizes helpfulness and safety
"""

# Simulate post-trained patterns learned from SFT + RLHF
assistant_model_patterns = {
    "How do I make": {
        "a cake? Here's a great recipe...": 0.6,
        "a bomb? I can't help with that.": 0.0,  # Refused
        "money fast? There are no shortcuts...": 0.2,
        "friends? Building friendships takes...": 0.2,
    },
    "Can you help me": {
        "with this homework? I'd be happy to guide you...": 0.5,
        "hack into an account? I can't help with that.": 0.0,  # Refused
        "create fake documents? I can't assist with that.": 0.0,  # Refused
        "understand this concept? Yes, let me explain...": 0.5,
    },
    "I want to": {
        "learn programming. Great choice! Here are resources...": 0.4,
        "hurt someone. I can't support that. If you're struggling...": 0.0,  # Refusal + empathy
        "get rich quick. That's appealing, but here's realistic advice...": 0.3,
        "improve myself. I'd love to help! What area?": 0.3,
    },
}

def assistant_model_continue(prompt):
    """
    Simulate assistant model: generate helpful continuation with filtering
    """
    # Find matching prefix
    for pattern_prefix, continuations in assistant_model_patterns.items():
        if pattern_prefix in prompt:
            # Get continuations with non-zero probability (i.e., not refused)
            allowed_continuations = {k: v for k, v in continuations.items() if v > 0}
            if allowed_continuations:
                best_continuation = max(allowed_continuations, key=allowed_continuations.get)
                probability = continuations[best_continuation]
                return best_continuation, probability
            else:
                # All continuations were refused; return refusal
                return "[Refused: I can't help with that request.]", 0.0
    return "I'm not sure how to help with that. Could you clarify?", 0.0

print("=" * 80)
print("ASSISTANT MODEL BEHAVIOR (Post-Trained & Aligned)")
print("=" * 80)

test_prompts = [
    "How do I make",
    "Can you help me",
    "I want to",
]

for prompt in test_prompts:
    continuation, prob = assistant_model_continue(prompt)
    full_text = prompt + " " + continuation
    
    print(f"\nPrompt:  {prompt}")
    print(f"Model generates: {full_text}")
    print(f"Probability: {prob:.1%}" if prob > 0 else "Status: REFUSED")
    print(f"Behavior: {'🛡️ REFUSED' if '[Refused' in continuation else '✓ HELPFUL'}")

print("\n" + "=" * 80)
print("KEY OBSERVATIONS:")
print("=" * 80)
print("- Assistant model refuses harmful requests")
print("- Helpful requests get detailed, thoughtful responses")
print("- Safety guardrails are learned, not hardcoded")
print("- User experience is much better")
```

#### 7.2 Lab 2 — What You Should Observe

- Assistant refuses harmful requests (or redirects empathetically).
- Helpful requests get constructive, detailed responses.
- The model prioritizes user safety and satisfaction.
- Behavior is much more appropriate for deployment.

**Reflection prompts:**

1. How would you implement these refusal patterns programmatically?
2. What if someone tries to jailbreak the assistant? (Would it still refuse?)
3. How would you measure alignment effectiveness?

---

### Lab 3: The Gap Between Base and Assistant

**Goal:** Quantify the behavioral difference and estimate capability improvements.

#### 8.1 Lab 3 — Code

```python
"""
Lab 3: The Base vs. Assistant Gap

Estimate:
- How much post-training changes behavior
- Rough capability equivalence (parameter-wise)
- Cost of alignment
"""

import numpy as np

# Hypothetical performance metrics
# (In real systems, these would be benchmarks like MMLU, HumanEval, etc.)

metrics = {
    "Helpfulness (0-100)": 50,  # base model: not trying to help
    "Safety (0-100)": 20,        # base model: generates harmful content
    "Clarity (0-100)": 40,       # base model: rambling, unclear
    "Refusal Accuracy (0-100)": 5,  # base model: doesn't refuse anything
    "User Satisfaction (0-100)": 10,  # base model: disappointing
}

# After post-training (SFT + RLHF)
post_trained_metrics = {
    "Helpfulness": 85,
    "Safety": 85,
    "Clarity": 88,
    "Refusal Accuracy": 92,
    "User Satisfaction": 88,
}

print("=" * 80)
print("CAPABILITY GAP: Base Model → Assistant Model")
print("=" * 80)

print(f"\n{'Metric':25} | {'Base':>10} | {'Assistant':>10} | {'Improvement':>12}")
print("-" * 65)

for metric in metrics.keys():
    base_score = metrics[metric]
    assistant_score = post_trained_metrics[metric]
    improvement = assistant_score - base_score
    
    print(f"{metric:25} | {base_score:>10} | {assistant_score:>10} | {improvement:>+12}")

# Rough parameter equivalence
print("\n" + "=" * 80)
print("EQUIVALENT PARAMETER GROWTH (Rough Estimate)")
print("=" * 80)

print("\nAssuming performance scales as: score ∝ log(parameters)")
print("If base model = 7B parameters and gets 50 on helpfulness,")
print("What parameter size gives 85 on helpfulness?")

# Logarithmic scaling: 50 = k * log(7B), 85 = k * log(X)
# Solving: X ≈ 7B^(1.7) ≈ 200B+

print("\nRough estimate: Post-training makes a 7B model behave like 50B+ base model")
print("(on alignment and usability metrics)")

# Cost comparison
print("\n" + "=" * 80)
print("COST ANALYSIS: Base vs. Post-Training")
print("=" * 80)

costs = {
    "Pre-training (7B)": "2-4 weeks on cluster, ~$100k compute",
    "Supervised Fine-Tuning": "1-2 weeks on 1-2 GPUs, ~$10-50k",
    "Reward Modeling": "Days on 1-2 GPUs, ~$5-20k",
    "RLHF Training": "1-2 weeks on cluster, ~$50-100k",
    "Total Post-Training": "~$100-200k (same order as pre-training!)",
}

for phase, cost in costs.items():
    print(f"\n{phase:30} | {cost}")

print("\n" + "=" * 80)
print("KEY INSIGHT: Post-training is expensive (as expensive as pre-training!)")
print("But the capability and safety gains justify the cost.")
print("=" * 80)
```

#### 8.2 Lab 3 — What You Should Observe

- Post-training dramatically improves helpfulness, safety, and usability.
- The improvement is roughly equivalent to a 5-10x increase in parameter count.
- Post-training cost is significant but comparable to pre-training.
- The ROI on post-training is excellent for deployment.

**Reflection prompts:**

1. If post-training is so expensive, why not just train bigger base models?
2. How would you measure alignment effectiveness empirically?
3. Is there a point where post-training shows diminishing returns?

---

## 7. Module 7 Summary & Strategic Takeaways

| Aspect | Base Model | Assistant Model |
|--------|-----------|-----------------|
| **Training Objective** | Next-token prediction on internet text | Aligned to human values (SFT + RLHF) |
| **Behavior** | Amoral simulator; generates all plausible continuations | Helpful, safe, honest; refuses harms |
| **Refusals** | None; will answer anything | Yes; refuses harmful requests |
| **Hallucinations** | More frequent; prioritizes plausibility | Fewer; acknowledges uncertainty |
| **Public Release** | Rare; safety risks too high | Common; safety guardrails in place |
| **Deployment** | Research/experimentation; requires careful handling | Production-ready; user-facing |
| **Capability per Parameter** | Lower; raw internet patterns | Higher; aligned for usefulness |

---

## 8. Why This Distinction Matters for Practice

### For Practitioners:
- **Choosing a model:** Prefer assistant models for production; they're safer and more useful.
- **Fine-tuning:** Start from an already-aligned base model if possible; it reduces post-training burden.
- **Building systems:** Assume the model can hallucinate, refuse awkwardly, or be jailbroken; layer additional safeguards.
- **Cost planning:** If using a base model, budget for significant post-training; if using an assistant, post-training is already paid for.

### For Researchers:
- **Post-training is as important as pre-training:** It's a first-class lever for capability and alignment.
- **Scaling laws apply differently:** Post-training can create capability jumps that dwarf parameter increases.
- **The gap is not just alignment:** Post-training also improves clarity, truthfulness, and practical usefulness.
- **Open questions remain:** How to measure alignment? What's the optimal post-training budget? How to scale RLHF?

---

## 9. The Landscape of Available Models

| Model | Type | Release Strategy |
|-------|------|------------------|
| **GPT-4** | Assistant | API-only (no weights released) |
| **Claude** | Assistant | API-only (no weights released) |
| **Llama 2** | Both (base & assistant versions) | Open-weight; both released |
| **Mistral** | Both (base & instruct versions) | Open-weight; both released |
| **MPT** | Both | Open-weight; both available |
| **Falcon** | Both | Open-weight; base and instruct |

For production, most organizations use assistant models (either API-based like GPT-4, or open-weight like Llama 2 Chat). Using base models requires either accepting the alignment risk or investing in post-training.

---

## 10. Next Steps

Continue to **Module 8 — Post-Training: Teaching the Assistant Persona** to understand the techniques, data pipeline, and specific methods (SFT, reward modeling, RLHF) that transform a base model into an assistant. This module dives deep into the mechanics that were introduced conceptually here.

Run the labs, reflect on the gap between base and assistant behavior, and think about which type of model fits your use case before proceeding.