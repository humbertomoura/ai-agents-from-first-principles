<div align="center">
  <a href="https://www.amazon.com/dp/B0HNJ65Q5S">
  <img src="assets/cover-ai-agents.jpg" alt="Cover of the book AI Agents from First Principles: A Practical Python Guide to Tools, Memory, and RAG" width="235">
  </a>

# AI Agents from First Principles

**Build an AI agent in plain Python. No frameworks, no magic, about 700 lines of code.**

[![Tests](https://github.com/humbertomoura/ai-agents-from-first-principles/actions/workflows/tests.yml/badge.svg)](https://github.com/humbertomoura/ai-agents-from-first-principles/actions/workflows/tests.yml)
![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
[![MIT License](https://img.shields.io/badge/License-MIT-2E7D32)](LICENSE)
![No API key needed](https://img.shields.io/badge/API%20key-not%20needed-555555)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/humbertomoura/ai-agents-from-first-principles/blob/main/quickstart.ipynb)

[**Kindle**](https://www.amazon.com/dp/B0HNJ65Q5S) · [**Paperback**](https://www.amazon.com/dp/B0HNJGRL9S) · [🇧🇷 Edição em português](https://github.com/humbertomoura/agentes-ia-livro)

</div>

---

Everyone talks about AI agents. Few people can explain what happens inside one.

This repository is the companion code for the book *AI Agents from First Principles*. It builds an agent piece by piece, the way you would build it if LangChain, LangGraph, and CrewAI didn't exist: the decision loop, tools that need human approval, memory that doesn't leak customer data, and document search that cites its sources.

Once you've built the parts yourself, every framework becomes easier to learn and much easier to debug.

## See it in 10 seconds

An assistant for **Rosa's Bakery** takes a cake order. It has to wait for Rosa's approval before recording it, and when the request is retried it must not create a second order:

```text
$ python examples/part3_ch24_tools/story.py
[1] p1 check_calendar: {'openings': 3}
[2] p2 record_order: NEEDS_APPROVAL
    >> Rosa approved p2
[2] p2 record_order: {'number': 'ORD-001'}
[2] p3 record_order: {'number': 'ORD-001'} (repeated)
state: SUCCESS
answer: Order ORD-001 confirmed!
```

No double cake, no double charge. That idempotency check takes only a few lines of Python, and Chapter 24 explains every one of them.

## Run it now

**In your browser, nothing to install:** click [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/humbertomoura/ai-agents-from-first-principles/blob/main/quickstart.ipynb)

**On your machine** (Python 3.11+):

```bash
git clone https://github.com/humbertomoura/ai-agents-from-first-principles.git
cd ai-agents-from-first-principles
python -m venv .venv
source .venv/bin/activate        # Windows (PowerShell): .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -q              # 32 tests, no network, no API key
```

Then run any example from the repository root:

```bash
python examples/part1_ch08_thermostat/run.py
python examples/part2_ch15_assistant/simulated.py
python examples/part3_ch24_tools/story.py
python examples/part4_ch33_notebook/story.py
python examples/part5_ch42_folder/story.py
```

None of these five commands calls an external model or needs an API key.

## What you'll build

| Part | Chapter | What you'll build | Folder |
|---|---:|---|---|
| **1 · Foundations** | 8 | A reflex agent with observation and internal state, no LLM | [`part1_ch08_thermostat`](examples/part1_ch08_thermostat) |
| **2 · The Agent Loop** | 15 | Tool calling, loop control, budgets, and simulated vs. real LLM | [`part2_ch15_assistant`](examples/part2_ch15_assistant) |
| **3 · The Agent's Tools** | 24 | Validation, human approval, resuming, and duplicate-proof actions | [`part3_ch24_tools`](examples/part3_ch24_tools) |
| **4 · The Workbench and the Notebook** | 33 | Memory that is selected, updated, expired, access-controlled, and compacted | [`part4_ch33_notebook`](examples/part4_ch33_notebook) |
| **5 · Look It Up Before You Answer** | 42 | Document search with access filters, citations, and an honest "couldn't find it" | [`part5_ch42_folder`](examples/part5_ch42_folder) |

Each folder has an `expected_output.txt`, and the tests check that every demo prints exactly that. `tests/test_contracts.py` checks the promises the chapters make: validation before action, terminal states, approval bound to the exact proposal, idempotent retries, memory updates, and the role of retrieved data.

## Why no frameworks?

Frameworks change fast. In the last year alone, the major agent libraries shipped breaking 1.0 releases and replaced whole APIs. The ideas underneath them did not change: a loop that observes, decides, and acts, surrounded by a system that checks, limits, remembers, searches, and records.

This code teaches those ideas with nothing but Python and, for one optional demo, the OpenAI SDK. There is very little here that can break.

## Who this is for

- **Developers** who use agent frameworks and want to know what they hide.
- **Students** who want a gentle, hands-on path from "what is an agent?" to working code.
- **Managers and tech leads** who need to make decisions about agents. Part I of the book has almost no code.

## Get the book

The code works on its own, but the book explains *why* each line is there, what would break in production, and when you shouldn't use an agent at all.

<table>
<tr>
<td width="140"><a href="https://www.amazon.com/dp/B0HNJ65Q5S"><img src="assets/cover-ai-agents.jpg" width="120" alt="Book cover"></a></td>
<td>

**AI Agents from First Principles: A Practical Python Guide to Tools, Memory, and RAG**
271 pages · 5 parts · 17 diagrams · 5 hands-on projects

**Kindle:** [US](https://www.amazon.com/dp/B0HNJ65Q5S) · [UK](https://www.amazon.co.uk/dp/B0HNJ65Q5S) · [CA](https://www.amazon.ca/dp/B0HNJ65Q5S) · [AU](https://www.amazon.com.au/dp/B0HNJ65Q5S) · [DE](https://www.amazon.de/dp/B0HNJ65Q5S) · [FR](https://www.amazon.fr/dp/B0HNJ65Q5S) · [ES](https://www.amazon.es/dp/B0HNJ65Q5S) · [IT](https://www.amazon.it/dp/B0HNJ65Q5S) · [NL](https://www.amazon.nl/dp/B0HNJ65Q5S) · [JP](https://www.amazon.co.jp/dp/B0HNJ65Q5S) · [BR](https://www.amazon.com.br/dp/B0HNJ65Q5S) · [MX](https://www.amazon.com.mx/dp/B0HNJ65Q5S)

**Paperback:** [US](https://www.amazon.com/dp/B0HNJGRL9S) · [UK](https://www.amazon.co.uk/dp/B0HNJGRL9S) · [CA](https://www.amazon.ca/dp/B0HNJGRL9S) · [AU](https://www.amazon.com.au/dp/B0HNJGRL9S) · [DE](https://www.amazon.de/dp/B0HNJGRL9S) · [FR](https://www.amazon.fr/dp/B0HNJGRL9S) · [ES](https://www.amazon.es/dp/B0HNJGRL9S) · [IT](https://www.amazon.it/dp/B0HNJGRL9S) · [NL](https://www.amazon.nl/dp/B0HNJGRL9S) · [JP](https://www.amazon.co.jp/dp/B0HNJGRL9S)

Already read it? An honest review on Amazon helps other readers find the book.

</td>
</tr>
</table>

## The Chapter 15 demo with a real model

Only `real.py`, in `part2_ch15_assistant`, calls a real model. Store your key in an environment variable, never in the code. From the repository root:

```bash
export OPENAI_API_KEY="your-key"
export OPENAI_MODEL="gpt-6-astra"   # any model on your account that supports tool calls
python examples/part2_ch15_assistant/real.py
```

API use is billed. Before running it, set a low spending alert **and**, where available, a hard spend limit for the project: an alert alone does not stop requests.

## Edition and versions

The code that matches the first edition of the book is tagged [`v1.0-book`](https://github.com/humbertomoura/ai-agents-from-first-principles/releases/tag/v1.0-book). Later changes on `main` may differ from the printed listings. The examples are tested on every push with Python 3.11, 3.12, and 3.13 (see the [CI workflow](.github/workflows/tests.yml)), and the optional demo was tested with `openai` 3.35.1.

## What the examples are (and aren't)

Each example is an independent teaching demonstration of one building block. They deliberately simplify: for instance, the Chapter 24 intention key treats "same customer, product, and day" as one order, and the Chapter 42 check only confirms that cited labels exist, not that the answer is supported. Each chapter explains its own limits under "What's missing for production."

## About the author

**Humberto Jorge de Moura Costa, PhD** is a professor and researcher at the Federal Institute of Rio Grande do Sul (IFRS), Brazil, where he leads the Software Factory lab and teaches AI to developers. He is an IEEE Senior Member, holds a PhD in Applied Computing, and builds AI systems for healthcare.

## Questions, bugs, ideas

Found a problem? [Open an issue](https://github.com/humbertomoura/ai-agents-from-first-principles/issues) with the chapter, the file, your Python version, and what you saw. You can also write to [book@humbertomoura.com.br](mailto:book@humbertomoura.com.br).

**If this repository helped you understand agents, please give it a ⭐. It helps other people find it.**

## License

The **source code** is available under the [MIT License](LICENSE). The **text, figures, and other editorial content of the book** are not covered by this license; all rights reserved.
