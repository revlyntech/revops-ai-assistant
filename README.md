# RevOps Central — Mini AI Sales Assistant

RevOps Central is a lightweight AI-powered sales assistant that helps go-to-market teams qualify inbound leads, score them against a custom Ideal Customer Profile (ICP), and generate personalized outreach in seconds. Just paste a company website and the agent will scrape it, summarize the business, evaluate fit, and draft a cold email ready to send.

## Overview

Manual lead research is slow and inconsistent. Sales reps often spend hours studying a prospect's website, guessing industry fit, and writing outreach from scratch. This project automates that workflow end-to-end using a single web interface backed by a small AI agent.

Given a company URL and a custom ICP definition, the agent will:

1. Scrape the company website for relevant business context.
2. Generate a structured company summary (industry, size, location, revenue range).
3. Score the company against the ICP criteria you define.
4. Draft a personalized B2B cold email referencing the company's actual positioning.
5. Export the full analysis as a downloadable PDF report.

## Features

- **Website Enrichment** — Scrapes title, meta description, and visible content from any public company website.
- **AI-Generated Summary** — Uses an LLM to produce a clean two-sentence overview, industry classification, and firmographic estimates.
- **Custom ICP Scoring** — Configure target industries, staff size range, locations, and revenue range. Each lead is scored out of 100 and labeled as Yes, Maybe, or No fit.
- **Personalized Outreach** — Generates a short, professional cold email tailored to the prospect's value proposition.
- **PDF Export** — One-click export of the full analysis report for sharing or CRM upload.
- **Fallback Logic** — If the LLM call fails, the system falls back to a rule-based summary so the user always gets a usable result.

## Tech Stack

- **Frontend:** Streamlit
- **LLM Provider:** Groq (Llama 3.3 70B Versatile)
- **Web Scraping:** Requests, BeautifulSoup
- **PDF Generation:** FPDF
- **Language:** Python 3.10+

## Project Structure

```
.
├── streamlit_app.py      # Streamlit UI and PDF export
├── app.py                # Main agent orchestrator
├── enrichment.py         # Website scraping logic
├── summary.py            # LLM prompt and summary generation
├── icp.py                # ICP scoring rules
├── llm.py                # Groq API wrapper
├── requirements.txt      # Python dependencies
└── README.md
```

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/revops-central.git
cd revops-central
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

You can get a free API key from https://console.groq.com.

## Running the App

Start the Streamlit server from the project root:

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`.

## How to Use

1. Enter a company website URL in the sidebar (for example, `https://www.remitap.com/`).
2. Define your ICP criteria:
   - Select one or more target industries (or add a custom one).
   - Set the minimum and maximum staff size.
   - Select target locations (or add a custom region).
   - Set the minimum and maximum revenue range in millions of dollars.
3. Click **Analyze Lead**.
4. Review the generated company insights, ICP score, and outreach email.
5. Click **Export Report to PDF** to download the full analysis.

## How ICP Scoring Works

Each lead is evaluated against four criteria, with 25 points awarded for every match:

| Criterion | Points |
|-----------|--------|
| Industry match | 25 |
| Staff size within range | 25 |
| Location match | 25 |
| Revenue within range | 25 |

Final classification:

- **Yes** — Score of 75 or higher
- **Maybe** — Score between 50 and 74
- **No** — Score below 50

## Limitations

- Scraping is limited to publicly accessible HTML content. Sites that rely heavily on JavaScript rendering may return limited data.
- Firmographic estimates (size, revenue) are inferred by the LLM and should be verified before any sales decision.
- The agent currently processes one lead at a time. Batch processing is not yet supported.

## Roadmap

- Bulk lead upload via CSV.
- CRM integration (HubSpot, Salesforce).
- LinkedIn enrichment for contact discovery.
- Multi-language outreach email support.
- Slack and email notification on high-fit leads.

