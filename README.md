# Gen-AI

A workspace for Generative-AI experiments — LangChain agents, prompt engineering, and LLM-assisted tooling.

The first project here is **Ice Breaker** — an agent that takes a person's name and returns a short, structured profile summary built from their LinkedIn page.

---

## Projects

### `ice_breaker/`

Given a full name, the agent:

1. Uses a **ReAct LangChain agent** powered by **Google Gemini 1.5 Flash** to look up the person's LinkedIn URL via **Tavily** search.
2. Calls **Scrapin.io** to enrich the profile (or a mocked gist payload for offline testing).
3. Pipes the profile into a prompt template and parses the response with a Pydantic output parser into a structured `Summary { summary, facts[] }`.

#### Pipeline at a glance

```
name ──> [ReAct agent + Tavily] ──> LinkedIn URL
              │
              ▼
       [Scrapin.io API] ──> profile JSON
              │
              ▼
       [PromptTemplate + Gemini]
              │
              ▼
       [PydanticOutputParser] ──> { summary, facts: [..] }
```

#### Stack

- **LangChain** — `langchain`, `langchain-core`, `langchain-google-genai`, `langchain-tavily`
- **LLM** — Google Gemini 1.5 Flash via `ChatGoogleGenerativeAI`
- **Search** — Tavily (`langchain-tavily`)
- **Scraping** — Scrapin.io (LinkedIn profile enrichment API)
- **Output parsing** — Pydantic v2 (`PydanticOutputParser`)
- **Config** — `python-dotenv`, `pipenv`

#### Project layout

```
ice_breaker/
├── iceBreaker.py             # Entry point — wires the chain end-to-end
├── output_parsers.py         # Pydantic `Summary` model + parser
├── agents/
│   └── linkedin_lookup_agent.py   # ReAct agent that finds a LinkedIn URL from a name
├── third_parties/
│   └── linkedin.py           # Scrapin.io profile scrape (with mock mode)
├── tools/
│   └── tools.py              # Tavily search wrapper used as an agent tool
└── Pipfile / Pipfile.lock    # Pipenv environment
```

#### Setup

```bash
cd ice_breaker
pipenv install
pipenv shell
```

Create a `.env` file in `ice_breaker/` with:

```dotenv
GEMINI_API_KEY=...
TAVILY_API_KEY=...
SCRAPIN_API_KEY=...
```

#### Run

```bash
python iceBreaker.py
```

By default `iceBreaker.py` calls `ice_break_with("Thilak Reddy United States")` — change the name in `__main__` to point at someone else.

---

## Roadmap

- More LangChain-based agents (RAG over local docs, structured-output chains, multi-tool agents).
- Notebook walk-throughs of prompt-engineering patterns I use at work (NL → SQL, schema injection, few-shot scaffolds).

---

*Author — [Jashwanth Reddy Earla](https://github.com/JashwanthReddyE)*
