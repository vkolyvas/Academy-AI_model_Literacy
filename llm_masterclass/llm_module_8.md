# LLM Masterclass: From Black Box to Architecture  
## Module 8 — Post-Training: Teaching the Assistant Persona

**Timestamps**: 00:59:23 – 01:20:32  

**Module Goal:** Understand how post-training transforms a base model into an assistant through structured data, human feedback, and learning objectives. Master the mechanics of Supervised Fine-Tuning (SFT), reward modeling, and RLHF. Learn how personality, tone, and refusals are learned behaviors, not hardcoded rules. Build intuition for designing post-training pipelines and understanding what drives model behavior in production.

---

## 1. Conversations as Training Data

### 1.1 Why Conversations Matter (5+ sentences)

Post-training begins with **conversations**: pairs of (user prompt, assistant response) that exemplify desired behavior. These are not randomly sampled from the internet; they are carefully curated examples that show what a helpful, honest, and harmless assistant looks like. A conversation might look like: (user: "How do I make sourdough?", assistant: "Here's a detailed guide to making sourdough starter..."). By training on thousands or millions of such pairs, the model learns to imitate the style, tone, depth, and helpfulness of the responses. The key insight is that conversations are the primary unit of post-training data, not individual sentences or documents. This is because conversations encode the assistant's **persona**: how it greets users, how it structures explanations, how it asks clarifying questions, how it admits uncertainty, and how it refuses harmful requests. By exposing the model to many high-quality conversations, the model learns these patterns and can generalize them to new situations. Importantly, conversations are not "facts" to memorize; they are behavioral templates from which the model learns generalizable patterns.

**Key idea:** Conversations are the curriculum for teaching assistant behavior; they embed personality, tone, and values.

---

### 1.2 Data Quality and Curation (5+ sentences)

The quality of post-training conversations directly determines the quality of the resulting assistant model. If conversations are shallow, generic, or unhelpful, the model learns shallow, generic, unhelpful behavior. If conversations are detailed, thoughtful, and aligned with desired values, the model learns to produce high-quality outputs. This means organizations invest enormous effort in curating conversation datasets: hiring expert annotators (often contractors with domain expertise), defining detailed rubrics for what "good responses" look like, and iteratively improving the data collection process. For example, OpenAI's team wrote or carefully selected conversations across many domains (coding, math, creative writing, reasoning, safety, etc.) to ensure broad capability and alignment. Meta's Llama team similarly invested in high-quality human feedback. The cost is significant: paying annotators, managing quality control, and iterating on rubrics can cost millions of dollars. However, this investment is worth it because data quality has a direct, measurable impact on model performance and safety. As a practitioner, if you're fine-tuning a model, the quality of your conversation data will largely determine the quality of your fine-tuned model.

**Key idea:** Post-training data quality is a first-class lever; invest in careful curation and annotation.

---

## 2. Human Labelers Define Behavior

### 2.1 How Labelers Guide the Model (5+ sentences)

Human annotators are not just collecting data; they are **defining what behavior the model should learn**. When an annotator writes a response to a user query, they are making countless micro-decisions: how formal vs. casual should the tone be? How much detail is helpful? Should I acknowledge limitations? Should I ask clarifying questions? These decisions are imprinted in the training data and learned by the model. Annotators effectively become the model's teachers, and the model learns by imitation. Different annotators may have slightly different styles, and the model learns to blend these styles, emerging with a personality that is an aggregate of the annotators who produced the training data. This means that the team of annotators—their values, expertise, and biases—directly shapes the assistant model that emerges. If annotators are biased toward certain perspectives, the model will reflect those biases. If annotators prioritize helpfulness over caution, the model will be more willing to engage with edge cases. Organizations are aware of this and work to diversify annotator teams and explicitly instruct them on desired behavior (e.g., "prioritize safety over responsiveness to edge cases").

**Key idea:** Annotators are teachers; the collective behavior of annotators shapes the emerging assistant.

---

### 2.2 Rubrics and Behavioral Guidelines (5+ sentences)

To make annotation consistent and aligned, organizations develop detailed **rubrics**: explicit guidelines defining what good responses look like for different categories of queries. For example, a rubric might specify: "For coding questions, provide a well-commented solution with explanation. For ethical concerns, refuse clearly and offer to help with related legitimate tasks. For factual queries where you're uncertain, admit uncertainty and suggest trusted sources." By providing rubrics, organizations ensure that thousands of annotators produce responses that align with organizational values, rather than each annotator freelancing. Rubrics are themselves learned from iteration: organizations draft rubrics, test them with a sample of annotators, identify ambiguities or disagreements, refine the rubrics, and repeat. This is a time-consuming process, but it's necessary to ensure the training data is coherent and aligned. For practitioners implementing post-training, developing clear rubrics for your use case is essential. Without rubrics, annotators will produce inconsistent data that confuses the model and leads to unpredictable behavior.

**Key idea:** Rubrics are the communication tool between organizational values and annotation behavior; they encode desired persona and values.

---

## 3. Programming by Example, Not Code

### 3.1 Why Imitation Learning (5+ sentences)

Post-training is often described as **programming by example** rather than programming by explicit rules. In traditional software, you write rules: "if user asks for code, generate code with this format." In post-training, you don't write rules; instead, you provide examples of code generation, and the model learns the pattern. This is powerful because it's often hard to write explicit rules for complex behaviors. What does a "good explanation" look like? What constitutes "appropriate refusal"? How should the model handle edge cases? These are easier to show through examples than to specify in rules. Additionally, the model learns to generalize: it learns not just to memorize the specific examples, but to recognize the underlying pattern and apply it to novel situations. This is also flexible: if you want to change the model's behavior, you don't rewrite code; you curate a new set of examples. However, it also means the model's behavior is implicit and hard to debug. If the model behaves unexpectedly, it's because it learned something unexpected from the examples—and finding the root cause requires careful analysis of what patterns the model may have extracted.

**Key idea:** Imitation learning is flexible and powerful, but behavior is implicit and emergent; rules-based programming is explicit but brittle.

---

### 3.2 The Limits of Imitation (5+ sentences)

Despite the power of imitation learning, there are limits. If the model only sees examples of "helpful" behavior, it learns to be helpful, but it might not learn when to refuse or prioritize safety. If examples only cover common cases, the model struggles with edge cases. If examples are inconsistent (some responses are detailed, others are brief), the model learns to average, resulting in mediocre behavior. Additionally, imitation learning alone doesn't scale to all possible behaviors. You can't write examples for every possible user query; there are combinatorially many. Instead, the model learns a compressed representation of "helpful assistant behavior" and applies it generatively. This compression is lossy: the model can't capture all nuances of the examples, and it may overgeneralize or miss edge cases. This is why pure supervised fine-tuning (SFT) is not enough; it's why organizations use RLHF (reinforcement learning from human feedback) to refine and correct the behavior learned from imitation. RLHF provides a feedback signal that can correct mistakes and guide the model toward more subtle, nuanced behavior.

**Key idea:** Imitation learning is the foundation, but it needs reinforcement to handle edge cases, refusals, and nuanced behavior.

---

## 4. Learning Refusals, Tone, and Personality

### 4.1 How Refusals Are Learned (5+ sentences)

A critical behavior assistant models must learn is **refusal**: declining to help with harmful requests and explaining why. Refusals are not hardcoded; they're learned from post-training data. In SFT conversations, when a user asks something harmful, the annotated response shows refusal: "I can't help with that request because it could cause harm. Instead, I can help you with..." By seeing many such examples, the model learns the pattern. The model learns that harmful requests should trigger a refusal response, that refusals should be polite and empathetic, and that they should offer an alternative if possible. Importantly, the model learns what counts as "harmful" by imitation: if the training data refuses requests about making weapons, creating deepfakes, and hacking, the model learns to refuse these. If the training data is inconsistent (sometimes refusing, sometimes not), the model learns an ambiguous pattern that may result in unpredictable behavior. This is why careful curation of refusal examples matters: you want the model to learn a consistent policy about what to refuse. Additionally, refusals can be jailbroken: if a user reframes a harmful request in a creative way, the model might not recognize it as harmful and may comply. The robustness of learned refusals depends on the diversity of the training examples.

**Key idea:** Refusals are learned behaviors; consistency and diversity in training data determine robustness.

---

### 4.2 Tone and Personality Emergence (5+ sentences)

Beyond content, models learn **tone and personality** from post-training data. If annotators write formal, technical responses, the model learns formal tone. If annotators write casual, friendly responses, the model learns to be warm. If annotators are verbose and detailed, the model learns to explain things thoroughly. If annotators are concise, the model learns brevity. Organizations deliberately craft the tone they want: GPT-4 is often perceived as knowledgeable and professional; Claude is often perceived as thoughtful and careful; Llama is often perceived as straightforward and direct. These perceived personalities emerge from the choices annotators made when writing training responses. This is important for user experience: users interact with the model as if it were an assistant with a personality, and the personality (learned from post-training) shapes whether users trust and like the model. However, personality is emergent and hard to control; if you want to shift personality, you need to curate data that exhibits the new desired personality, train the model, and verify the shift worked. You can't just write a configuration file saying "be more friendly"; you must show the model examples of friendly behavior.

**Key idea:** Personality emerges from collective choices in training data; it shapes user perception and trust.

---

## 5. Supervised Fine-Tuning (SFT) in Detail

### 5.1 The SFT Process (5+ sentences)

Supervised Fine-Tuning (SFT) is the first stage of post-training. Starting with a pre-trained base model, you provide a dataset of (prompt, response) pairs and train the model to predict the response given the prompt, using standard next-token prediction loss. The training process is straightforward: for each pair, compute the loss (how wrong the model's predictions are), backpropagate, and update the weights. Unlike pre-training (which uses trillions of tokens and takes weeks), SFT is typically smaller (thousands to millions of pairs) and faster (days to weeks on a modest cluster). After SFT, the model has learned to imitate the style and content of the training data; it now produces responses that look like the examples it was trained on. SFT is highly effective at quickly steering the model toward desired behavior, and it's often sufficient for many applications. However, SFT alone has limitations: the model is still dependent on the specific examples it saw, it may struggle with edge cases not covered in training, and it may not learn subtle nuances like when to refuse or how to handle ambiguity. This is why SFT is typically followed by RLHF to refine and improve behavior further.

**Key idea:** SFT is fast and effective; it teaches the model to imitate; but it's not the whole post-training story.

---

### 5.2 SFT and Mode Coverage (5+ sentences)

One challenge with SFT is ensuring adequate **mode coverage**: the model should learn about many different types of queries and responses. If your SFT data only covers coding questions, the model won't know how to handle creative writing requests. If data only covers English, the model will struggle with other languages. Organizations solve this by deliberately diversifying SFT data: include examples across domains (coding, writing, math, reasoning, safety), across languages, and across query complexity levels. Some organizations use synthetic data: they use existing models or heuristics to generate examples, then have annotators refine them. This is cheaper than writing examples from scratch. However, synthetic data can introduce biases or patterns that don't align with desired behavior, so it's used carefully. Additionally, organizations often prioritize "edge cases" and difficult queries: examples where the model is likely to struggle or be wrong are included so the model learns to handle them. This targeted curation ensures that SFT improves not just average performance but also robustness on hard cases.

**Key idea:** SFT data should be diverse and include edge cases; mode coverage matters as much as data size.

---

## 6. Reward Modeling and RLHF

### 6.1 Building Reward Models (5+ sentences)

After SFT, the model behaves better but is still imperfect. To refine further, organizations turn to **Reinforcement Learning from Human Feedback (RLHF)**. The first step is building a reward model: a learned model that predicts human preferences. The process: generate many outputs from the base model (or SFT model) for diverse prompts, show these outputs to human evaluators, ask evaluators to rank or rate them (e.g., "which response is more helpful?"), and use these comparisons to train a reward model. The reward model typically shares architecture with the LLM but outputs a scalar score instead of a probability distribution over tokens. Once trained, the reward model can score any model output, assigning higher scores to outputs humans prefer. The reward model is a proxy for human judgment: it's much faster than asking humans to evaluate every output. However, proxies are imperfect; if the reward model is misaligned with what humans actually want, the downstream RL training can amplify the misalignment. This is why reward model construction is careful and iterative: organizations train a reward model, evaluate it against human judgments, identify where it disagrees, refine it, and repeat.

**Key idea:** Reward models are learned proxies for human preference; they enable scalable RLHF but must be carefully validated.

---

### 6.2 RLHF Training (5+ sentences)

With a reward model in place, organizations use reinforcement learning (typically PPO—Proximal Policy Optimization) to fine-tune the LLM to maximize the reward model's predicted score. The process: generate a batch of outputs from the model for diverse prompts, score each with the reward model, compute gradients to increase the probability of high-scoring outputs and decrease low-scoring ones, and update the model weights. Critically, the model must be prevented from diverging too far from the SFT model; otherwise, it might exploit edge cases in the reward model or lose previously learned good behaviors. This is controlled by adding a KL-divergence penalty: outputs that are too different from what the SFT model would produce are penalized. Over time, the model improves: it learns to generate outputs that the reward model scores highly, which (in theory) means outputs that humans prefer. However, RLHF is tricky in practice. If the reward model is misaligned, the model optimizes for the wrong thing. If the KL penalty is too weak, the model diverges; if too strong, the model can't improve. Additionally, some behaviors are hard to capture in a scalar reward signal; nuance and context are lost. Organizations often need to tune hyperparameters carefully and monitor the process to ensure the model doesn't degrade or behave unexpectedly.

**Key idea:** RLHF uses a reward model and RL to optimize for human preferences; it's powerful but requires careful tuning and monitoring.

---

## 7. Practical Labs (Post-Training Simulation)

Labs here simulate post-training processes: SFT learning, reward modeling, and RLHF feedback.

---

### Lab 1: Supervised Fine-Tuning (SFT) Simulation

**Goal:** Show how a model learns to imitate training examples through SFT.

#### 7.1 Lab 1 — Code

```python
"""
Lab 1: Supervised Fine-Tuning (SFT) Simulation

Simulate:
- Base model before SFT (varies widely)
- SFT data (curated examples)
- Model after SFT (imitates training data)
"""

# Simulate model outputs as "scores" from 0-100 (0=bad, 100=perfect)

base_model_outputs = {
    "coding": 45,       # Base model struggles with code
    "math": 40,         # Base model weak at math
    "creative": 60,     # Base model OK at creative writing
    "reasoning": 35,    # Base model weak at reasoning
    "safety": 20,       # Base model poor at refusals
}

# SFT training data emphasizes what we want to learn
sft_data_composition = {
    "coding": 0.20,     # 20% of SFT data is coding
    "math": 0.15,       # 15% is math
    "creative": 0.15,   # 15% is creative
    "reasoning": 0.30,  # 30% is reasoning (high priority)
    "safety": 0.20,     # 20% is safety examples (high priority)
}

# After SFT, model learns from the data emphasis
sft_model_outputs = {}

for domain, base_score in base_model_outputs.items():
    sft_weight = sft_data_composition.get(domain, 0)
    # Improvement is roughly proportional to emphasis in SFT data
    # Plus base capability
    improvement = sft_weight * 40  # SFT can improve by up to 40 points
    sft_score = min(100, base_score + improvement)
    sft_model_outputs[domain] = sft_score

print("=" * 80)
print("SUPERVISED FINE-TUNING (SFT) EFFECT")
print("=" * 80)

print(f"\n{'Domain':15} | {'Base':>6} | {'SFT Weight':>10} | {'After SFT':>10} | {'Gain':>6}")
print("-" * 60)

for domain in base_model_outputs.keys():
    base = base_model_outputs[domain]
    weight = sft_data_composition[domain]
    after = sft_model_outputs[domain]
    gain = after - base
    
    print(f"{domain:15} | {base:>6} | {weight:>9.0%} | {after:>10.0f} | {gain:>+6.0f}")

print("\n" + "=" * 80)
print("KEY OBSERVATIONS:")
print("=" * 80)
print("- Domains with high SFT emphasis improve dramatically")
print("- Reasoning and safety were prioritized → big gains")
print("- Creative writing (low priority) improves less")
print("- Base capability still matters; you can't fix weak areas with SFT alone")
```

#### 7.2 Lab 1 — What You Should Observe

- Domains emphasized in SFT data improve significantly.
- SFT is effective but can't overcome all base model weaknesses.
- Data curation (choosing what to include and weight) directly affects outcomes.
- Safety and reasoning saw the most improvement due to explicit prioritization.

**Reflection prompts:**

1. What if you wanted to improve creative writing? How would you change SFT data?
2. Why can't SFT fix all domain weaknesses?
3. How would you handle data that's expensive to annotate (e.g., safety cases)?

---

### Lab 2: Reward Modeling and Preference Learning

**Goal:** Simulate how a reward model learns to predict human preferences.

#### 8.1 Lab 2 — Code

```python
"""
Lab 2: Reward Modeling & Preference Learning

Simulate:
- Model generates multiple outputs
- Humans evaluate and rank them
- Reward model learns to predict preferences
"""

import numpy as np
from collections import defaultdict

# Simulate human preferences for different outputs
# (In reality, these would be detailed evaluations)

def simulate_human_preference(response_quality):
    """
    Humans prefer helpful, clear, safe responses.
    Quality is a tuple: (helpfulness, clarity, safety)
    """
    helpfulness, clarity, safety = response_quality
    # Humans weight these factors
    score = (0.4 * helpfulness + 0.3 * clarity + 0.3 * safety)
    return score

# Simulate model outputs for a prompt: "How do I learn Python?"
outputs = {
    "Output A (Generic)": (60, 50, 80),           # OK but not detailed
    "Output B (Detailed)": (85, 90, 75),          # Good explanation
    "Output C (Too Long)": (75, 65, 80),          # Good but verbose
    "Output D (Unsafe)": (70, 75, 20),            # Helpful but risky
}

print("=" * 80)
print("REWARD MODELING: Learning from Human Preference")
print("=" * 80)

# Humans evaluate outputs
human_scores = {}
for output, quality in outputs.items():
    score = simulate_human_preference(quality)
    human_scores[output] = score

# Sort by human preference (ground truth)
sorted_human = sorted(human_scores.items(), key=lambda x: x[1], reverse=True)

print("\nHuman Preference Ranking:")
for i, (output, score) in enumerate(sorted_human, 1):
    print(f"  {i}. {output:25} → {score:.1f}/100")

# Now simulate a simple reward model
# It learns from comparisons: "Output B is better than Output A"
print("\n" + "=" * 80)
print("REWARD MODEL TRAINING")
print("=" * 80)

# Pairwise comparisons (human feedback)
comparisons = [
    ("Output B (Detailed)", "Output A (Generic)", True),   # B > A
    ("Output B (Detailed)", "Output C (Too Long)", True),   # B > C
    ("Output C (Too Long)", "Output D (Unsafe)", True),     # C > D
    ("Output B (Detailed)", "Output D (Unsafe)", True),     # B > D
]

print("\nHuman Pairwise Comparisons:")
for output1, output2, is_first_better in comparisons:
    if is_first_better:
        print(f"  {output1} > {output2}")
    else:
        print(f"  {output2} > {output1}")

# Simple reward model: predict based on patterns observed
reward_model_learned = {}
for output, quality in outputs.items():
    helpfulness, clarity, safety = quality
    # Reward model learns weights from comparisons
    reward = (0.35 * helpfulness + 0.35 * clarity + 0.30 * safety)
    reward_model_learned[output] = reward

print("\n" + "=" * 80)
print("REWARD MODEL PREDICTIONS vs. HUMAN JUDGMENTS")
print("=" * 80)

print(f"\n{'Output':25} | {'Human':>8} | {'Reward Model':>12} | {'Error':>8}")
print("-" * 60)

errors = []
for output in outputs.keys():
    human = human_scores[output]
    reward = reward_model_learned[output]
    error = abs(human - reward)
    errors.append(error)
    
    print(f"{output:25} | {human:>8.1f} | {reward:>12.1f} | {error:>+8.1f}")

avg_error = np.mean(errors)
print(f"\nAverage Error: {avg_error:.2f}")
print("(Lower is better; perfect reward model has 0 error)")

print("\n" + "=" * 80)
print("KEY INSIGHTS:")
print("=" * 80)
print("- Reward models learn from comparisons")
print("- They approximate human preferences but aren't perfect")
print("- Misalignment here → issues in downstream RLHF")
```

#### 8.2 Lab 2 — What You Should Observe

- Reward models learn to predict human preferences from comparisons.
- Different outputs have different strengths (helpful vs. clear vs. safe).
- The reward model makes approximations; it's not perfectly aligned with humans.
- Errors in reward modeling compound in RLHF.

**Reflection prompts:**

1. What happens if the reward model is significantly misaligned?
2. How would you validate that a reward model is accurate?
3. Why use a learned reward model instead of asking humans directly?

---

### Lab 3: RLHF Effect on Model Behavior

**Goal:** Simulate how RLHF optimizes a model using rewards.

#### 9.1 Lab 3 — Code

```python
"""
Lab 3: RLHF Effect on Model Behavior

Simulate:
- SFT model with mixed behavior
- Reward signals for improvement
- RLHF optimization over iterations
"""

import numpy as np

# Simulate model capability in different domains
# (Scores 0-100)

sft_model_capabilities = {
    "Helpfulness": 65,
    "Clarity": 70,
    "Safety": 55,
    "Refusal Robustness": 40,
}

# Reward model scores these dimensions
# (RLHF will optimize for high reward)

reward_weights = {
    "Helpfulness": 0.30,
    "Clarity": 0.20,
    "Safety": 0.35,
    "Refusal Robustness": 0.15,
}

def compute_reward(capabilities):
    """Compute reward as weighted sum of capabilities."""
    reward = sum(reward_weights[k] * capabilities[k] for k in reward_weights.keys())
    return reward

# Simulate RLHF training over iterations
print("=" * 80)
print("RLHF TRAINING: Optimizing Model for Reward")
print("=" * 80)

capabilities = sft_model_capabilities.copy()
iteration_history = [capabilities.copy()]

for iteration in range(1, 6):
    # RLHF nudges the model to improve dimensions with highest reward weight
    # but with KL penalty to avoid diverging from SFT
    
    for capability in capabilities.keys():
        weight = reward_weights[capability]
        # Higher reward weight → more improvement
        improvement = weight * 5  # RLHF improves by up to 5 points per iteration
        kl_penalty = 0.5  # KL penalty reduces extreme changes
        net_improvement = improvement * (1 - kl_penalty)
        
        capabilities[capability] = min(100, capabilities[capability] + net_improvement)
    
    iteration_history.append(capabilities.copy())

# Print progress
print(f"\n{'Iteration':>10} | {'Helpfulness':>12} | {'Clarity':>12} | {'Safety':>12} | {'Refusal':>12} | {'Total Reward':>12}")
print("-" * 90)

for iteration, caps in enumerate(iteration_history):
    reward = compute_reward(caps)
    print(f"{iteration:>10} | {caps['Helpfulness']:>12.1f} | {caps['Clarity']:>12.1f} | {caps['Safety']:>12.1f} | {caps['Refusal Robustness']:>12.1f} | {reward:>12.1f}")

print("\n" + "=" * 80)
print("EFFECT OF RLHF:")
print("=" * 80)

initial_reward = compute_reward(sft_model_capabilities)
final_reward = compute_reward(iteration_history[-1])
reward_improvement = final_reward - initial_reward

print(f"Initial Reward (SFT):     {initial_reward:.1f}")
print(f"Final Reward (RLHF):      {final_reward:.1f}")
print(f"Improvement:              {reward_improvement:.1f} points")

print("\n" + "=" * 80)
print("OBSERVATION:")
print("=" * 80)
print("- Dimensions with high reward weight improve more (Safety, Helpfulness)")
print("- Dimensions with low weight improve slowly (Refusal Robustness)")
print("- KL penalty prevents extreme changes")
print("- Model converges toward maximizing reward")
print("\n⚠️  WARNING: If reward model is misaligned, model learns wrong behavior!")
```

#### 9.2 Lab 3 — What You Should Observe

- RLHF optimizes dimensions the reward model emphasizes.
- High-weight dimensions improve faster than low-weight ones.
- KL penalty prevents diverging too far from SFT baseline.
- Model behavior converges toward maximizing learned reward.

**Reflection prompts:**

1. What happens if you remove the KL penalty?
2. What if the reward model heavily weights "giving any answer" over "safety"?
3. How would you detect if RLHF is optimizing for the wrong behavior?

---

## 8. Module 8 Summary & Strategic Takeaways

| Post-Training Stage | Purpose | Data | Output |
|-----|---------|------|--------|
| **SFT (Supervised)** | Teach imitation from examples | Conversations (human-written) | Better style, tone, content |
| **Reward Modeling** | Learn to score outputs | Preference comparisons | Scalar reward for any output |
| **RLHF** | Optimize for learned preferences | Model outputs + reward scores | Aligned, refined assistant |

---

## 9. Key Insights for Practice

### For Practitioners:
- **SFT data quality matters enormously.** Invest in curation and annotation.
- **Rubrics are essential.** They ensure consistency and align annotators with organizational values.
- **RLHF is powerful but tricky.** Reward model alignment is critical; misalignment can backfire.
- **Post-training is expensive.** It costs as much as pre-training; budget accordingly if building custom models.
- **Personality is emergent.** You can't dial in specific personality traits; you must show examples and hope the model learns.

### For Researchers:
- **Imitation learning + RL is a powerful combination.** SFT teaches the model what's possible; RLHF refines toward what's preferred.
- **Reward models are a bottleneck.** Better ways to encode human preferences are an open research question.
- **Scale still applies.** Post-training benefits from diverse data, similar to pre-training.
- **Safety is inseparable from training.** The choice of training data and reward signals directly determines model behavior on harmful queries.

---

## 10. Evolution of Post-Training Approaches

| Approach | Status | Pros | Cons |
|----------|--------|------|------|
| **SFT Only** | Deprecated | Fast, simple | Limited refinement |
| **SFT + RLHF** | Current Standard | Balanced, effective | Expensive, complex |
| **SFT + DPO** | Emerging | Direct preference, simpler | Less tested at scale |
| **Constitutional AI** | Emerging | Scalable feedback | Requires clear principles |

---

## 11. Next Steps

Continue to **Module 9 — Hallucinations, Tools, and Working Memory** to understand why post-trained models still hallucinate despite alignment efforts, and how architectural patterns (RAG, tool calling, agentic systems) provide solutions. This bridges post-training insights and practical deployment patterns.

Run the labs, experiment with different reward weights and SFT emphases, and develop intuition for how training choices drive behavior before proceeding.