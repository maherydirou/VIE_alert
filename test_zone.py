from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page(viewport={"width": 1600, "height": 1200})

    page.goto(
        "https://mon-vie-via.businessfrance.fr/offres",
        wait_until="networkidle"
    )

    print(page.title())

    # -------------------------
    # Zone
    # -------------------------

    page.locator(
        "span.multiselect__placeholder",
        has_text="Zone"
    ).click()

    page.locator(
        "li.multiselect__element"
    ).filter(
        has_text="EUROPE OCCIDENTALE"
    ).click()

    print("Zone OK")

    # -------------------------
    # Pays
    # -------------------------

    page.locator(
        "span.multiselect__placeholder",
        has_text="Pays"
    ).click()

    page.locator(
        "li.multiselect__element"
    ).filter(
        has_text="ALLEMAGNE"
    ).click()

    page.locator(
        "li.multiselect__element"
    ).filter(
        has_text="AUTRICHE"
    ).click()

    page.locator(
        "li.multiselect__element"
    ).filter(
        has_text="SUISSE"
    ).click()

    print("Pays OK")

    page.screenshot(path="test.png")

    browser.close()
