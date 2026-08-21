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
BookWebsite_Automation_Testing/
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
└── README.md
```

## Prerequisites

- Python 3.9+
- Microsoft Edge + matching [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) on your `PATH`
- A [Groq API key](https://console.groq.com/keys) (Temporary API already included for demo, expires at Sept 20, 2026)

## Setup

1. **Clone the repo**
   ```bash
   git clone <repo-url>
   cd BookWebsite_Automation_Testing
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

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
- For Demo purposes, Temporary Groq API Key (Expires at Sept 20, 2026) is already integrated in AISpellingValidator.py so no need to provide your own key. 
