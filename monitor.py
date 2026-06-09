import requests
import json
import os
import smtplib
from email.mime.text import MIMEText

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

    url = "https://civiweb-api-prd.azurewebsites.net/api/Offers/search"

    payload = {
        "activitySectorId": [],
        "companiesSizes": [],
        "countriesIds": ["DE", "AT"],
        "enterprisesIds": [0],
        "geographicZones": ["5"],
        "limit": 500,
        "missionsDurations": [],
        "missionsTypesIds": [],
        "porteEnv": ["0"],
        "query": None,
        "skip": 0,
        "specializationsIds": [],
        "studiesLevelId": [],
        "teletravail": ["0"]
    }

    headers = {
        "Content-Type": "application/json",
        "Origin": "https://mon-vie-via.businessfrance.fr"
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    try:
        data = response.json()
        print(json.dumps(data["result"][0], indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Erreur JSON : {e}")
        return []

    offers = []

    for offer in data["result"]:

        offers.append({
            "id": offer["id"],
            "title": offer.get("missionTitle", ""),
            "company": offer.get("organizationName", "")
        })
    print(f"Nombre d'offres récupérées : {len(offers)}")
    return offers


def main():

    previous = load_previous()

    current = get_offers()
    if not previous:
        print("Premier lancement : initialisation de la base")
        save_current(current)
        return

    previous_ids = {o["id"] for o in previous}

    new_offers = [
        o for o in current
        if o["id"] not in previous_ids
    ]

    if new_offers:

        body = ""

        for offer in new_offers:
            body += (
                f"Entreprise : {offer['company']}\n"
                f"Mission : {offer['title']}\n"
                f"ID : {offer['id']}\n\n"
            )

        send_email(
            "Nouvelle offre VIE Allemagne/Autriche",
            body
        )

    if new_offers:
        print(f"Nouvelles offres détectées : {len(new_offers)}")

    for offer in new_offers:
        print(
            f"{offer['company']} - "
            f"{offer['title']} "
            f"(ID {offer['id']})"
        )
    save_current(current)


if __name__ == "__main__":
    main()
