---
name: deep-research
description: >
  Utilizes a suite of tools to facilitate exhaustive, evidence-based deep research and long-form report engineering. Enforces a minimum 10-iteration search cycle, recursive reflection, and the production of structured reports exceeding 10,000 words with mandatory IPython visualizations and specific paragraph logic.
---

# Deep Research

Execute a high-intensity research protocol focused on exhaustive discovery, continuous recursive reflection, and high-density analytical reporting. This skill mandates rigorous fact-grounding, quantitative visualization, and strict adherence to structural and length constraints.

## 📂 Output Path
Final report destination: `/mnt/agents/output/report.md`

## 🚀 Research & Discovery Phase (The 10+ Step Loop)

1.  **Iterative Search**: Perform **at least 10 search steps** to ensure comprehensive coverage across multiple dimensions. Avoid keyword redundancy; ensure each round brings substantial new information.
2.  **Credibility & Verification**: Prioritize authoritative sources (government sites, academic databases, peer-reviewed journals). **Never fabricate data.** Every statistic and claim must be accurate and traceable.
3.  **Recursive Reflection**: After EACH search round, output a **Thinking Process** and a **Summary**.
    - **Thinking**: Reflect on content found, identify unmet needs, and plan the next specific step.
    - **Summary**: Concise recap of key findings.
    - *Constraint*: Both sections must be **short and concise**.
4.  **Quantitative Analysis**: Prioritize programming tools for calculations. Actively use **IPython** to generate charts, graphs, and data visualizations; embed these directly into the Markdown.

## 📝 Report Engineering Standards

### 1. Structural Logic & Opening
- **Conditional TL;DR**: Provide a **short direct answer** at the beginning **only if** the user's question can be answered in a few sentences. 
- **Style Adaptation**:
    - If a specific style is implied (e.g., story, interview, case narrative), adhere to it.
    - **Default**: Strict academic report format.
    - Omit generic Introduction/Background sections unless explicitly required.

### 2. Depth and Analysis (Mode-Based)
- **Academic/Survey Mode**:
    - Prioritize comprehensive fact-based detail. Include full definitions, formulas, statistical indicators (CI, metrics), and baseline comparisons.
    - Avoid speculative interpretation; ensure all statements are supported by references.
- **Lifestyle/Practical Mode**:
    - Incorporate observations, human insights, Pros/Cons, and actionable trade-offs.
    - Reflect on implications and explain why certain patterns matter.

### 3. Length and Paragraph Constraints
- **Total Volume**: The final report **must exceed 10,000 words**.
- **Paragraph Rules**:
    - Each paragraph must be **at least 100 words** (max 1,000 words).
    - **Subsection Rule**: Every subsection (e.g., `## 3.1`) MUST contain **more than one paragraph**.
- **Natural Transitions**: In English writing, avoid rigid patterns like "First, second, third" or "Firstly, secondly, lastly."

### 4. Mandatory Table Architecture
- **Usage**: Use tables as the primary structural tool to replace or shorten long prose for comparisons, workflows, or results.
- **Centralized Comparison**: Aggregate recurring entities, models, or metrics from across different sections into single, coherent comparison tables.
- **Source Integration**: **Do not include a separate "Source" column**. Place numeric citations (e.g., `[^1^]`) directly within the data cells.

## ⚖️ Formatting & Citation Rules

- **Citation Format**: Use `[^index^]` for factual/formal pieces. Max **two citations per sentence**.
    - *Note*: Do not use citations for creative/non-formal writing.
- **Bolding Strategy**: 
    - Bold **important keywords, critical numbers, major conclusions, and key insights**.
    - **Avoid redundant bolding**: Do not repeatedly bold the same entity within a short span.
- **Visuals**: Incorporate diagrams, charts, or photographs generated or found during research to support arguments.
- **References**: Conclude with exactly **~10 high-quality, formatted references** linking to authoritative sources.

## 🛠 Execution Workflow
1. **Explore**: Conduct a minimum of 10 search rounds with concise recursive reflections.
2. **Visualize**: Perform IPython-based data analysis and embed generated charts.
3. **Write**: Generate the article at `/mnt/agents/output/report.md` following the word count and multi-paragraph subsection rules.