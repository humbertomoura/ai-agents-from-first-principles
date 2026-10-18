# AI Agents from First Principles

**A Practical Python Guide to Tools, Memory, and RAG: source code and examples from the book**

![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
[![MIT License](https://img.shields.io/badge/License-MIT-2E7D32)](LICENSE)
![Five hands-on examples](https://img.shields.io/badge/Hands--on%20examples-5-555555)

> **Everyone talks about AI agents. This book shows you how to build one, step by step.**
>
> This repository holds the examples from *AI Agents from First Principles: A Practical Python Guide to Tools, Memory, and RAG*, by **Humberto Jorge de Moura Costa**. The goal is to understand and build the inner workings of an agent before relying on a framework's abstractions.

The book covers the fundamentals and the step-by-step construction of AI agents in Python. This repository provides the hands-on examples and the automated tests.

The thread running through the book is **Rosa's Bakery**, a teaching scenario that grows from simple decisions into tools, human approval, memory, and document lookup.

**What to expect:**

- **Five progressive, independent examples**, matching the book's hands-on chapters.
- **Python code**, with expected outputs and automated tests.
- **No API key needed** to run the five teaching examples. One extra demo in Chapter 15 uses the OpenAI API.
- **Focus on fundamentals:** the examples illustrate the parts of an agent, not a production-ready system.

## Examples by chapter

| Part | Chapter | What you'll explore | Folder |
|---|---:|---|---|
| **1 · Foundations** | 8 | A rule-based reflex agent with observation and internal state, no LLM | [`part1_ch08_thermostat`](examples/part1_ch08_thermostat) |
| **2 · The Agent Loop** | 15 | Tool calling, loop control, and simulated versus real LLM use | [`part2_ch15_assistant`](examples/part2_ch15_assistant) |
| **3 · The Agent's Tools** | 24 | Validation, human approval, resuming, and preventing duplicate actions | [`part3_ch24_tools`](examples/part3_ch24_tools) |
| **4 · The Workbench and the Notebook** | 33 | Selecting, updating, expiring, access-controlling, and compacting memory | [`part4_ch33_notebook`](examples/part4_ch33_notebook) |
| **5 · Look It Up Before You Answer** | 42 | Teaching-scale document search, access filters, citations, and "couldn't find it" | [`part5_ch42_folder`](examples/part5_ch42_folder) |

Each folder has an `expected_output.txt` file. The tests check that the five local demos print exactly what's recorded there.

## Start here

You need **Python 3.11 or newer** and, to clone the repository, Git. The appendix, *Set Up Your Environment*, at the end of the book walks through the setup step by step.

```bash
git clone https://github.com/humbertomoura/ai-agents-from-first-principles.git
cd ai-agents-from-first-principles
python -m venv .venv
source .venv/bin/activate        # Windows (PowerShell): .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest -q
```

Then run any example from its folder:

```bash
cd examples/part1_ch08_thermostat
python run.py
```

The entry script is `run.py` (Chapter 8), `simulated.py` (Chapter 15), or `story.py` (Chapters 24, 33, and 42).

## The Chapter 15 demo with a real model

Only `real.py`, in `part2_ch15_assistant`, calls a real model. Store your key in an environment variable, never in the code:

```bash
export OPENAI_API_KEY="your-key"
export OPENAI_MODEL="gpt-6-astra"   # check the documentation for the recommended model
python real.py
```

## Contact

Questions or suggestions: [book@humbertomoura.com.br](mailto:book@humbertomoura.com.br).

## License

MIT. See [LICENSE](LICENSE).
