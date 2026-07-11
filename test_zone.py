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

    # Lance la recherche

    page.locator("button.valid_search").click()
    
    print("Recherche lancée")
    
    page.wait_for_load_state("networkidle")
    
    page.wait_for_timeout(5000)
    
    print("Recherche terminée")

    print(page.url)

    previous_ids = {o["id"] for o in previous}

    while True:
    
        offres = page.locator("div.figure_container")
    
        stop = False
    
        for i in range(offres.count()):
    
            offre = offres.nth(i)
    
            href = offre.locator("a.postuler").get_attribute("href")
            offer_id = int(href.split("/")[-1])
    
            if offer_id in previous_ids:
                stop = True
                break
    
            # Sinon on extrait toutes les infos de la carte
            title = offre.locator("h2.mission-title").inner_text()
            company = offre.locator("h3.organization-name").inner_text()
            location = offre.locator("h2.location").inner_text()
    
            print(offer_id, title)
    
        if stop:
            break
    
        # Cliquer sur "Voir plus d'offres"

    page.screenshot(path="test.png")

    browser.close()
