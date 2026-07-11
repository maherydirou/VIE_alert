from playwright.sync_api import sync_playwright

responses = []

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    def handle_response(response):
        if "/api/Offers/search" in response.url:
            print("API détectée :", response.url)
            responses.append(response)

    page.on("response", handle_response)

    page.goto(
        "https://mon-vie-via.businessfrance.fr/offres",
        wait_until="networkidle"
    )

    # On laisse le temps au JavaScript de finir ses appels
    page.wait_for_timeout(5000)

    print("Nombre de réponses API :", len(responses))

    if responses:
        data = responses[-1].json()

        print("Nombre d'offres :", len(data["result"]))
        print("Première offre :")
        print(data["result"][0])

    browser.close()
