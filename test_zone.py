from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page(
        viewport={"width": 1600, "height": 1200}
    )

    page.goto(
        "https://mon-vie-via.businessfrance.fr/offres",
        wait_until="domcontentloaded"
    )

    page.wait_for_timeout(3000)

    print(page.title())

    # Ouvre le filtre Zone
    page.locator(
        "span.multiselect__placeholder",
        has_text="Zone"
    ).click()

    page.wait_for_timeout(1000)

    # Sélectionne Europe occidentale
    page.locator("span.multiselect__option span", has_text="EUROPE OCCIDENTALE").click()
    
    page.screenshot(path="zone.png")
    print("Capture réalisée")
    
    print("Zone sélectionnée")

    page.wait_for_timeout(3000)

    browser.close()
