import requests
import json
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, time
from zoneinfo import ZoneInfo

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

COUNTRIES = [
    "DE", #Allemagne
    "AT", #Autriche
    "CH" #Suisse
]


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
        "countriesIds": COUNTRIES,
        "limit": 500
    }

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://mon-vie-via.businessfrance.fr",
        "Referer": "https://mon-vie-via.businessfrance.fr/",
        "User-Agent": "Mozilla/5.0"
        #"Content-Type": "application/json",
       # "Origin": "https://mon-vie-via.businessfrance.fr"
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
    except Exception as e:
        print(f"Erreur JSON : {e}")
        return []

    offers = []

    for offer in data["result"]:

        publication_date = ""
        
        if offer.get("startBroadcastDate"):
            publication_date = datetime.fromisoformat(
                offer["startBroadcastDate"].replace("Z", "+00:00")
            ).strftime("%d/%m/%Y")
            
        offers.append({
            "id": offer["id"],
            "reference": offer.get("reference", ""),
            "title": offer.get("missionTitle", ""),
            "company": offer.get("organizationName", ""),
            "city": offer.get("cityName", ""),
            "country": offer.get("countryName", ""),
            "publication_date": publication_date,
            "duration_months": offer.get("missionDuration", ""),
            "mission_profile": offer.get("missionProfile", ""),
            "indemnity": offer.get("indemnite", ""),
            "contact_name": offer.get("contactName", ""),
            "contact_email": offer.get("contactEmail", ""),
            "url": f"https://mon-vie-via.businessfrance.fr/offres/{offer['id']}"
        })
        
    print(f"Nombre d'offres récupérées : {len(offers)}")
    return offers

def get_today_offers(offers):
    today = datetime.now().strftime("%d/%m/%Y")
    return [
        offer for offer in offers
        if offer.get("publication_date") == today
    ]

def main():

    previous = load_previous()

    current = get_offers()
    today_offers = get_today_offers(current)
    now = datetime.now(ZoneInfo("Europe/Paris")).time()

    if time(18,00) <= now <= time(18,30) :
        recap = ""

        for offer in today_offers:
            recap += (
                "=========================\n"
                f"MISSION : {offer['title']}\n\n"
            
                f"ENTREPRISE : {offer['company']}\n"
            
                f"LOCALISATION : {offer['city']} ({offer['country']})\n"
            
                f"DATE DE PUBLICATION : {offer['publication_date']}\n"
            
                f"DURÉE : {offer['duration_months']} mois\n"
            
                f"INDEMNITÉ : {offer['indemnity']} €\n"
            
                f"RÉFÉRENCE : {offer['reference']}\n\n"
            
                "PROFIL RECHERCHÉ\n"
                "----------------\n"
                f"{offer['mission_profile']}\n\n"
            
                "CONTACT\n"
                "-------\n"
                f"{offer['contact_name']}\n"
                f"{offer['contact_email']}\n\n"
            
                "LIEN DE L'OFFRE\n"
                "--------------\n"
                f"{offer['url']}\n"
            
                "===========================\n\n"
            )
            
        send_email(
            "Récapitulatif offres VIE Allemagne/Autriche/Suisse",
            recap
        )
        
    
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
                "=========================\n"
                f"MISSION : {offer['title']}\n\n"
            
                f"ENTREPRISE : {offer['company']}\n"
            
                f"LOCALISATION : {offer['city']} ({offer['country']})\n"
            
                f"DATE DE PUBLICATION : {offer['publication_date']}\n"
            
                f"DURÉE : {offer['duration_months']} mois\n"
            
                f"INDEMNITÉ : {offer['indemnity']} €\n"
            
                f"RÉFÉRENCE : {offer['reference']}\n\n"
            
                "PROFIL RECHERCHÉ\n"
                "----------------\n"
                f"{offer['mission_profile']}\n\n"
            
                "CONTACT\n"
                "-------\n"
                f"{offer['contact_name']}\n"
                f"{offer['contact_email']}\n\n"
            
                "LIEN DE L'OFFRE\n"
                "--------------\n"
                f"{offer['url']}\n"
            
                "===========================\n\n"
            )

        send_email(
            "Nouvelle offre VIE Allemagne/Autriche/Suisse",
            body
        )

    save_current(current)


if __name__ == "__main__":
    main()
