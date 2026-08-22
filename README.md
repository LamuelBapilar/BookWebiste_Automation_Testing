# Books Webiste Test Automation

Automated testing suite for [books.toscrape.com](https://books.toscrape.com), built with **Robot Framework**, **Selenium**, and a **Groq-powered AI spell-checker** for scraped book titles.

The suite scrapes book listings from the site, saves them to JSON, then runs a series of Robot Framework tests that validate data quality, verify the live UI, and use an AI model to catch misspelled titles.

## Features

- 🕸️ **Web scraping** — Selenium-based scraper (`BookScraper.py`) pulls title, price, and stock status across multiple pages.
- ✅ **Data-quality checks** — confirms every scraped book has all required fields populated.
- 🤖 **AI spelling validation** — sends scraped titles to Groq (`openai/gpt-oss-120b`) to flag genuine typos while ignoring invented names, brands, and stylized terms.
- 🌐 **Live UI checks** — opens the real site in a browser and verifies listings actually render.
- 🔁 **Cross-check** — confirms every scraped title can still be found by paging through the live site.

## Project Structure

```
BookWebiste_Automation_Testing/
├── libraries/
│   ├── AISpellingValidator.py   # Groq API wrapper for spelling checks
│   └── BookScraper.py           # Selenium scraper for books.toscrape.com
├── resources/                   # Shared Robot Framework resources
├── results/
│   └── books.json               # Scraped output (generated)
├── tests/
│   └── test_book.robot          # Main Robot Framework test suite
├── log.html                     # Robot Framework run log (generated)
├── output.xml                   # Robot Framework run output (generated)
├── report.html                  # Robot Framework run report (generated)
├── requirements.txt
├── .env                         # Your Groq API key (not committed)
└── README.md
```

## Prerequisites

- Python 3.9+
- Microsoft Edge + matching [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) on your `PATH`
- A [Groq API key](https://console.groq.com/keys) — free to generate, required to run the AI spelling check
- VS Code

## Setup

1. **Open a terminal**

   In VS Code, open the integrated terminal via `Terminal > New Terminal` (or `` Ctrl+` ``). Alternatively, open your system terminal (Command Prompt, PowerShell, or Terminal.app) and `cd` into the folder where you want the project to live.

2. **Clone the repo**
   ```bash
   git clone git@github.com:LamuelBapilar/BookWebiste_Automation_Testing.git
   cd BookWebiste_Automation_Testing
   ```

3. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Get a Groq API key**

   1. Go to [console.groq.com/keys](https://console.groq.com/keys)
   2. Sign up or log in (free)
   3. Click **Create API Key**, give it a name, and copy the generated key 
   
6. **Set up your Groq API key**

   Create a file named `.env` in the project root and add your key:
   ```
   GROQ_API_KEY=your_key_here
   ```
   This key is required for the AI spelling check test to run. `.env` is excluded from version control via `.gitignore`, so your key stays local to your machine.

## Running the Tests

Run the full suite:
```bash
robot tests/test_book.robot
```

This will:
1. Scrape up to `MAX_PAGES` (default: 3) pages from books.toscrape.com and save results to `results/books.json`.
2. Validate that scraped data is complete.
3. Run the AI spelling check against scraped titles.
4. Open a browser and verify the live site renders book listings.
5. Cross-check that scraped titles are findable on the live site.

Test results are written to `log.html`, `report.html`, and `output.xml`.

## Configuration

Key settings can be adjusted in `libraries/BookScraper.py`:

| Variable     | Description                          | Default                          |
|--------------|---------------------------------------|-----------------------------------|
| `URL`        | Target site to scrape                 | `https://books.toscrape.com/`     |
| `MAX_PAGES`  | Number of pages to scrape (max 50)    | `3`                                |
| `SAVE_FILE`  | Output path for scraped JSON          | `results/books.json`               |

And in `tests/test_book.robot`:

| Variable      | Description                | Default   |
|---------------|-----------------------------|-----------|
| `${BROWSER}`  | Browser used for Selenium   | `edge`    |
| `${SITE_URL}` | Site under test              | `https://books.toscrape.com` |

## Notes

- `MAX_PAGES` is capped at 3 by default to stay within Groq's free-tier rate limits and keep demo runs fast — increase it if you have a higher rate limit.
- `AISpellingValidator.py` reads the Groq key from the `GROQ_API_KEY` environment variable via `.env` 