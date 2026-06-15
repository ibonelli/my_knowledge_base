# AI_New_Links

## Question

This document has an structure, but it evolved very organically. So I'm wondering if there is a better possible structure and if I should separate it in different documents.

## Answer

----

This is a **good document in terms of content density**, but structurally it shows **classic “organic growth” symptoms**:

*   multiple mental models mixed together (learning notes, reference links, commentary, and research backlog),
*   inconsistent depth (some sections are definitions, others are deep architecture notes),
*   temporal mixing (foundational concepts mixed with very recent research),
*   and unclear *intended audience* (you-now, future-you, teammates, or onboarding readers?).

I’ll be direct and critical, per your preference.

***

## Executive verdict (straight answer)

✅ **Yes, there is a better structure.**  
✅ **Yes, you should split this into multiple documents.**  
❌ **Keeping this as one file will actively reduce its usefulness over time.**

Right now this is **three different documents wearing the trench coat of one markdown file**.

***

## The core structural problem

This document mixes **four incompatible purposes**:

1.  **Conceptual learning notes**  
    (e.g. “What is Generative AI”, Words vs Tokens, LLM parameters)

2.  **Technology landscape tracking**  
    (models, frameworks, MCP servers, Chinese LLMs, image generators)

3.  **Research paper bookmarking**  
    (arXiv links, Stanford, Apple, Meta, OpenAI papers)

4.  **Personal commentary + synthesis**  
    (“what I learned”, lessons, interpretations, opinions)

Each of these **wants a different structure, cadence, and evolution path**.

Trying to keep them together means:

*   navigation degrades,
*   updates become risky,
*   and future reuse (sharing, onboarding, presenting) becomes hard.

***

## What “good” should look like (target state)

You want **clear axes**:

*   **Why does this exist?**
*   **How will I use it later?**
*   **What changes often vs rarely?**
*   **What is reference vs reasoning?**

Once you answer those, the structure naturally emerges.

***

## Recommended split: 4-document system

### 📘 1. `AI_Fundamentals.md` (slow-changing, teaching-oriented)

**Purpose:**  
Canonical reference for core concepts. This is the document you *don’t want to rewrite every 3 months*.

**Belongs here:**

*   What is Generative AI (IEEE content, summarized in *your* words)
*   AI vs ML vs DL
*   LLM basics
*   Words vs Tokens
*   Parameters explanation
*   Transformers overview
*   Prompt Engineering (high-level, not tools)
*   Data Scientist vs AI Engineer (conceptual, not tool lists)

**What to remove from here:**

*   links to specific tools/models
*   2024/2025 trend videos
*   “this framework is better than X” opinions

**Why this matters:**  
This becomes reusable for:

*   onboarding others,
*   refreshing your own understanding,
*   grounding future decisions.

***

### 🧠 2. `AI_Systems_and_Architecture.md` (engineering-focused)

**Purpose:**  
“How modern AI systems are actually built.”

**Belongs here:**

*   RAG
*   CAG vs RAG
*   MCP servers (this is *architecture*, not “Links”)
*   Control logic (thinkFAST vs thinkSLOW)
*   Agents: Reason / Act / Observe
*   Memory systems
*   Vector databases
*   Tool calling
*   Spec-driven development
*   DSPy (concepts more than tutorials)

This section is currently scattered across:

*   “Building AI Agents”
*   “Model Context Protocol Servers”
*   random links under “Links”

📌 **Critique:**  
Your MCP section is strong, but buried in the document. It deserves its *own conceptual chapter*, not a subheading.

***

### 🧪 3. `AI_Research_and_Papers.md` (high-churn, chronological)

**Purpose:**  
A living lab notebook of *what’s new and why it matters*.

**Structure recommendation:**

```markdown
## 2025
### Apple – The Illusion of Thinking
- What the paper claims
- Why it matters
- My skepticism / concerns

### Meta – Large Concept Models
- What problem this tries to solve
- Why token-level modeling may plateau
```

**Belongs here:**

*   arXiv papers
*   Meta / Apple / Anthropic research
*   Biology of LLM papers
*   FAN, No-Prop, Jamba, DARWIN-Gödel Machine
*   “AI 2027” material (clearly marked as speculative)

❌ **Do not** mix these with fundamentals.
Temporal content should be **versioned, dated, and arguable**.

***

### 🔗 4. `AI_Landscape_and_Tools.md` (catalog, not thinking)

**Purpose:**  
Index of relevant tools, models, and ecosystems.

**Belongs here:**

*   Chinese LLMs and companies
*   Ollama models
*   Image generation tools (Flux, Fooocus, ComfyUI)
*   MCP servers lists
*   Coding agents (Cline, Aider, Gemini Coder)
*   Framework comparisons (LangGraph vs CrewAI)

⚠️ Minimal prose. This is a **map**, not an essay.

***

## What to remove or rethink

### 🔥 Kill these anti-patterns

1.  **“Links” as a bucket section**
    *   It destroys information scent.
    *   Everything should live *by purpose*, not by source.

2.  **Raw copy-paste of full articles**
    *   Replace with:
        *   1-paragraph summary
        *   why it was added
        *   what question it answers

3.  **Unbounded lists**
    *   Papers ≠ tutorials ≠ opinion pieces
    *   If a section exceeds \~2 screens, it should be split

***

## Optional (but powerful): add metadata

At the top of each document:

```markdown
Purpose:
Audience:
Update Frequency:
Last Reviewed:
```

Example:

> **Purpose:** Track and evaluate AI systems architecture patterns  
> **Audience:** Solution Architects / Senior Engineers  
> **Update Frequency:** Monthly  
> **Last Reviewed:** 2026-01-15

This pays off long-term.

***

## One important challenge for you

Right now this file assumes **you will remember why something mattered**.

You won’t.

Future-you needs:

*   *why this link exists*
*   *what question it answered*
*   *what you still disagree with*

If you don’t capture that, this becomes a graveyard of impressive but unused links.

***

## Suggested next step (concrete)

1.  Create a new folder:
        /AI/
          AI_Fundamentals.md
          AI_Systems_and_Architecture.md
          AI_Research_and_Papers.md
          AI_Landscape_and_Tools.md

2.  Move content **without rewriting** first (structural refactor only).

3.  On a second pass, **compress and synthesize**.

----

## My Conclusion

I need to re-think my approach of saving links in the way I do. It is becoming increasingly difficult to find things.
I could use a new DB approach that allows me to save the information in a tagged way. So link, conections, etc.
Could be a case application for AI assited development. Could use a local database, run on my server, etc.

Steps:
1. Try to describe a bit more what I'm trying to achieve (started with TXT, moved to Zim Wiki, and now I'm with MD)
2. Describe the use cases, functionality, architecture, etc.
3. Look for solutions that might be good enough for what I'm trying to accomplish
4. Decide how to continue...
