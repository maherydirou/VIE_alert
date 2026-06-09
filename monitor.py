import requests
from bs4 import BeautifulSoup
import json
import os
import smtplib
from email.mime.text import MIMEText

URL = "https://mon-vie-via.businessfrance.fr/offres"

COUNTRIES = [
    "Allemagne",
    "Autriche"
]

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


def load_previous():
    if os.path.exists("offers.json"):
        with open("offers.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_current(data):
    with open("offers.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def send_email(subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(
            EMAIL_SENDER,
            EMAIL_RECEIVER,
            msg.as_string()
        )


def get_offers():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers)
    print(r.status_code)
    print(r.url)
    print(r.text[:1000])
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    offers = []

    cards = soup.find_all("a")

    for card in cards:

        text = card.get_text(" ", strip=True)

        upper = text.upper()

        if any(country in upper for country in COUNTRIES):

            href = card.get("href")

            if href:

                if href.startswith("/"):
                    href = "https://mon-vie-via.businessfrance.fr" + href

                offers.append({
                    "title": text[:200],
                    "url": href
                })

    unique = []
    seen = set()

    for offer in offers:
        if offer["url"] not in seen:
            unique.append(offer)
            seen.add(offer["url"])

    return unique


def main():

    previous = load_previous()

    current = get_offers()

    previous_urls = {o["url"] for o in previous}

    new_offers = [
        o for o in current
        if o["url"] not in previous_urls
    ]

    if new_offers:

        body = ""

        for offer in new_offers:
            body += (
                f"{offer['title']}\n"
                f"{offer['url']}\n\n"
            )

        send_email(
            "Nouvelle offre VIE Allemagne/Autriche",
            body
        )
    print(f"Nombre d'offres trouvées : {len(current)}")

    for offer in current[:10]:
        print(offer)
    
    save_current(current)


if __name__ == "__main__":
    main()
