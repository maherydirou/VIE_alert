from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    response_json = None

    def intercept(response):
        global response_json

        if "/api/Offers/search" in response.url:

            print("API trouvée :", response.url)

            try:
                data = response.json()

                print("Nombre d'offres :", len(data["result"]))

                print(data["result"][0])

            except Exception as e:
                print(e)

    page.on("response", intercept)

    page.goto(
        "https://mon-vie-via.businessfrance.fr/offres",
        wait_until="networkidle"
    )

    browser.close()
