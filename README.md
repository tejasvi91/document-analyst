# 📄 Document Analyst

> **Chat with any PDF using GPT-4o. Upload. Ask. Understand.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://document-analyst-tsbtjrwprxkozt3oxafrcg.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![OpenAI](https://img.shields.io/badge/GPT--4o-OpenAI-412991?style=for-the-badge&logo=openai)](https://openai.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)

---

## 🚀 Live Demo

👉 **[document-analyst-tsbtjrwprxkozt3oxafrcg.streamlit.app](https://document-analyst-tsbtjrwprxkozt3oxafrcg.streamlit.app)**

Upload any PDF and start asking questions — no sign-up required.

---

## What it does

Most PDFs are painful to work with. Merged table cells, embedded images, multi-column layouts, and dense formatting make manual analysis slow and error-prone.

**Document Analyst** solves this. Upload any PDF and chat with it in plain English. The app extracts all content — text, tables, and images — then uses GPT-4o to answer your questions with precision.

---

## Features

- **Instant document summary** — get a concise overview the moment you upload
- **Natural language Q&A** — ask anything about the document in plain English
- **Table extraction** — handles merged cells and complex grids that break other tools
- **Image extraction** — detects embedded figures, charts, stamps, and signatures
- **Multi-turn chat** — follow-up questions with full conversation memory
- **Large document support** — automatic chunking for documents that exceed the context window
- **Real-time answers** — responses appear as GPT-4o generates them

---

## Use cases

| Industry | Example |
|---|---|
| Finance | "What was the total revenue in Q3?" |
| Legal | "Summarise the key obligations in this contract" |
| HR | "What are this candidate's top skills?" |
| Research | "What methodology did this paper use?" |
| Banking | "List all transactions above €1,000" |

---

## How it works

```
PDF upload → Text + Table + Image extraction → GPT-4o analysis → Streamed answer
```

Three extraction engines run in parallel:

- **PyMuPDF** — reconstructs reading order from raw character coordinates
- **pdfplumber** — detects cell boundaries and resolves merged table cells
- **PyMuPDF image decoder** — extracts embedded XObjects as PNG/JPEG bytes

Extracted content is assembled into an optimised context payload and sent to GPT-4o via the OpenAI API. For large documents exceeding the context window, the app automatically chunks the text and merges responses.

---

## Tech stack

| Tool | Purpose |
|---|---|
| `Streamlit` | Web UI with session state management |
| `OpenAI GPT-4o` | Document understanding and Q&A |
| `PyMuPDF (fitz)` | Text and image extraction |
| `pdfplumber` | Table parsing with merged cell support |
| `python-dotenv` | Secure local API key management |

---

## Project structure

```
document-analyst/
├── app.py              # Streamlit UI — upload, chat, results
├── extractor.py        # PDF parsing — text, tables, images
├── analyst.py          # GPT-4o integration — prompts, context, Q&A
├── requirements.txt    # Python dependencies
├── packages.txt        # System dependencies for deployment
└── .streamlit/
    └── secrets.toml    # API keys (local only, never committed)
```

---

## Getting started locally

**1. Clone the repo**
```bash
git clone https://github.com/tejasvi91/document-analyst
cd document-analyst
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your OpenAI API key**

Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk-your-key-here"
```

**5. Run the app**
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Deploying to Streamlit Cloud

1. Push your code to GitHub (without secrets)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add `OPENAI_API_KEY` in Advanced Settings → Secrets
5. Deploy — live in ~2 minutes

---

## Security

- API keys are stored in `.streamlit/secrets.toml` locally and in Streamlit Cloud secrets — never committed to GitHub
- `.env` and `secrets.toml` are listed in `.gitignore`
- Uploaded files are processed in memory and never persisted to disk

---

## Built by

**Tejasvi M N** — Data Engineer & AI Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com)
[![GitHub](https://img.shields.io/badge/GitHub-tejasvi91-181717?style=flat&logo=github)](https://github.com/tejasvi91)

---

> Built as part of an AI portfolio project series demonstrating applied AI development,
> PDF processing pipelines, and production Python deployment.
