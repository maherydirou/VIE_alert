from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://mon-vie-via.businessfrance.fr/offres",
        wait_until="domcontentloaded"
    )

    page.wait_for_timeout(3000)

    # Ouvre le filtre Zone
    page.locator("span.multiselect__placeholder", has_text="Zone").click()

    page.wait_for_timeout(500)

    # Choisit Europe occidentale
    page.get_by_text("EUROPE OCCIDENTALE", exact=True).click()

    print("Zone sélectionnée")

    page.wait_for_timeout(10000)

    browser.close()
