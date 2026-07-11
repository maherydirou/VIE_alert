from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.on(
        "request",
        lambda request: print(request.method, request.url)
    )

    page.goto(
        "https://mon-vie-via.businessfrance.fr/offres",
        wait_until="networkidle"
    )

    print(
        page.evaluate("""
    Object.keys(window)
    """)
    )

    print(
        page.evaluate("""
    typeof window.__NUXT__
    """)
    )

    print(
        page.evaluate("""
    window.__NUXT__.config
    """)
    )

    page.wait_for_timeout(5000)

    browser.close()
