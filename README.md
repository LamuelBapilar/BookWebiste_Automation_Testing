# Testing-Robot

UI test automation project built with **Robot Framework**, **Python**, and **Selenium**, targeting [the-internet.herokuapp.com](https://the-internet.herokuapp.com) as the system under test.

This project demonstrates automated UI testing with a modular, maintainable project structure suitable for scaling into a larger test suite.

---

## Tech Stack

- **Robot Framework** — keyword-driven test automation framework
- **Python** — scripting language / custom library support
- **Selenium** (via SeleniumLibrary) — browser automation engine
- **webdriver-manager** — automatically manages browser driver binaries

---

## Project Structure

```
Testing-Robot/
├── tests/               # .robot test suites
│   └── sample_test.robot
├── resources/           # reusable keywords, page objects
├── libraries/           # custom Python libraries
├── results/             # test run output (log.html, report.html, output.xml)
├── venv/                # Python virtual environment (not committed)
├── requirements.txt     # pinned Python dependencies
├── .gitignore
└── README.md
```

- **tests/** — the actual `.robot` test case files, organized by feature/page
- **resources/** — shared keywords and locators, following the Page Object Model pattern
- **libraries/** — custom Python-based Robot Framework libraries for functionality beyond built-in keywords
- **results/** — generated automatically when tests run; gitignored

---

## Prerequisites

- [Python 3.8+](https://www.python.org/downloads/) installed and available on PATH
- Google Chrome, Microsoft Edge, or Firefox installed (whichever browser you plan to run tests against)
- Git (to clone the repository)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repository-url>
cd Testing-Robot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows (PowerShell):**
```powershell
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal prompt once activated.

> **Windows PowerShell note:** if activation fails with a script execution error, run this once (as your user, not admin):
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Verify installation

```bash
robot --version
```

You should see output similar to `Robot Framework 7.4.2 (Python 3.14.4 on win32)`.

---

## Running the Tests

Run all tests in the `tests/` folder, with results saved to `results/`:

```bash
robot --outputdir results tests/
```

Run a single test file:

```bash
robot --outputdir results tests/sample_test.robot
```

Run tests by tag (once tags are added to test cases):

```bash
robot --outputdir results --include smoke tests/
```

---

## Viewing Test Results

After a run, open the generated report in your browser:

- `results/report.html` — high-level pass/fail summary
- `results/log.html` — detailed step-by-step execution log, useful for debugging failures
- `results/output.xml` — raw machine-readable results

---

## VS Code Setup (Recommended)

1. Install the **RobotCode** extension (by Daniel Biehl) from the VS Code Marketplace
2. Install the **Python** extension (by Microsoft), if not already installed
3. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) → **Python: Select Interpreter** → choose the interpreter inside `.\venv\Scripts\python.exe` (labeled "Workspace")

---

## Notes

- Browser driver binaries are managed automatically via `webdriver-manager` — no manual driver downloads needed.
- The `venv/` folder and `results/` folder are excluded from version control via `.gitignore`; only `requirements.txt` is committed so dependencies can be reproduced elsewhere.