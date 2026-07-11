from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(
        "https://mon-vie-via.businessfrance.fr/offres",
        wait_until="domcontentloaded"
    )

    print("Page chargée")

    response = page.wait_for_response(
        lambda r: "/api/Offers/search" in r.url,
        timeout=30000
    )

    print("Réponse reçue :", response.status)

    data = response.json()

    print("Nombre d'offres :", len(data["result"]))

    print("Première offre :")
    print(data["result"][0])

    browser.close()
