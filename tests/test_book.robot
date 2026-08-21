*** Settings ***
Documentation    Uses the custom BookScraper library to scrape book listings
...              from books.toscrape.com and export to JSON, plus Selenium
...              checks that verify the live site's UI matches expectations,
...              plus an AI check for misspelled book titles.
Library          ../libraries/BookScraper.py
Library          ../libraries/AISpellingValidator.py
Library          SeleniumLibrary
Library          OperatingSystem
Suite Setup      Scrape Books

*** Variables ***
${JSON_OUTPUT}    results/books.json
${BROWSER}        edge
${SITE_URL}       https://books.toscrape.com

*** Test Cases ***
Scrape Books Across Multiple Pages
    [Documentation]    Scrape site pages for book details and save results to a JSON file.
    Save To Json
    File Should Exist    ${JSON_OUTPUT}

Scraped Book Fields Should Not Be Empty
    [Documentation]    Data-quality check: every book must have all fields populated.
    ${books}=    Get Scraped Books
    FOR    ${book}    IN    @{books}
        Should Not Be Empty    ${book}[title]
        Should Not Be Empty    ${book}[price]
        Should Not Be Empty    ${book}[stock]
    END

AI Should Find No Misspelled Book Titles
    [Documentation]    Uses AI (Groq) to check scraped book titles for spelling errors.
    ${books}=    Get Scraped Books
    ${misspelled}=    Ai Check Titles For Misspellings    ${books}
    Log    AI flagged: ${misspelled}
    Ai Titles Should Have No Misspellings

Open Browser and Verify Book Listings Render
    [Documentation]    Selenium check: verifies the live site loads and
    ...                actually renders book listings in the browser.
    Open Browser    ${SITE_URL}    ${BROWSER}
    Title Should Be    All products | Books to Scrape - Sandbox
    ${count}=    Get Element Count    css=article.product_pod
    Should Be True    ${count} > 0    No book listings rendered on the page
    [Teardown]    Close Browser

Scraped Site if Books Exist
    [Documentation]    Cross-check: confirms every scraped book title
    ...                actually appears somewhere across the site's pages.
    ${books}=    Get Scraped Books
    Open Browser    ${SITE_URL}    ${BROWSER}

    FOR    ${book}    IN    @{books}
        ${found}=    Run Keyword And Return Status
        ...    Page Should Contain Element    xpath=//h3/a[@title="${book}[title]"]
        IF    not ${found}
            Click Element    css=li.next a
            Wait Until Element Is Visible    css=article.product_pod
            Page Should Contain Element    xpath=//h3/a[@title="${book}[title]"]
        END
    END

    [Teardown]    Close Browser