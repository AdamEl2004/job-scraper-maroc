import requests
from bs4 import BeautifulSoup
import time
import random

BASE_URL = "https://www.rekrute.com"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

INCLUDE_KEYWORDS = [
    "data", "python", " ia ", " bi ", " ml ",
    "machine learning", "deep learning", "business intelligence",
    "data scientist", "data analyst", "data engineer",
    "power bi", "tableau", "sql", "nlp", "analytique"
]

EXCLUDE_KEYWORDS = [
    "stagiaire", "stage", "intern", "commercial", "call center"
]


def is_data_related(text):
    text = text.lower()
    if any(ex in text for ex in EXCLUDE_KEYWORDS):
        return False
    return any(kw in text for kw in INCLUDE_KEYWORDS)


def extract_li_value(ul_tag, keyword):
    if not ul_tag:
        return ""
    for li in ul_tag.find_all("li"):
        li_text = li.get_text(separator=" ", strip=True)
        if keyword.lower() in li_text.lower():
            idx = li_text.lower().find(keyword.lower())
            value = li_text[idx + len(keyword):].strip(" :")
            return value
    return ""


def parse_offer(li_tag):
    title_tag = li_tag.find("a", class_="titreJob")
    if not title_tag:
        return None

    full_title = title_tag.get_text(strip=True)
    url = BASE_URL + title_tag["href"]

    if "|" in full_title:
        parts = full_title.split("|")
        title = parts[0].strip()
        location = parts[1].strip().replace("(Maroc)", "").strip()
    else:
        title = full_title.strip()
        location = ""

    if not is_data_related(title):
        return None

    company = ""
    img_tag = li_tag.find("img", class_="photo")
    if img_tag:
        company = img_tag.get("alt", "").strip()

    description = ""
    info_divs = li_tag.find_all("div", class_="info")
    for div in info_divs:
        span = div.find("span")
        if span:
            description = span.get_text(strip=True)
            break

    date_posted = ""
    date_em = li_tag.find("em", class_="date")
    if date_em:
        spans = date_em.find_all("span")
        if spans:
            date_posted = spans[0].get_text(strip=True)

    ul_tag = li_tag.find("ul")
    contract_type = extract_li_value(ul_tag, "Type de contrat proposé")
    experience = extract_li_value(ul_tag, "Expérience requise")
    sector = extract_li_value(ul_tag, "Secteur d'activité")

    if "-" in contract_type:
        contract_type = contract_type.split("-")[0].strip()

    return {
        "title": title,
        "company": company,
        "location": location,
        "contract_type": contract_type,
        "experience": experience,
        "description": description,
        "skills": sector,
        "source": "rekrute",
        "url": url,
        "date_posted": date_posted,
    }


def scrape_rekrute(max_pages=5):
    all_offers = []

    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}/offres.html?p={page}&s=1&o=1&keyword=data&st=d"
        print(f"📄 Page {page} : {url}")

        try:
            response = requests.get(url, headers=HEADERS, timeout=15)

            if response.status_code != 200:
                print(f"⚠️  HTTP {response.status_code} — arrêt.")
                break

            soup = BeautifulSoup(response.text, "html.parser")
            blocks = soup.find_all("li", class_="post-id")

            if not blocks:
                print(f"ℹ️  Plus d'offres à la page {page}.")
                break

            count = 0
            for block in blocks:
                offer = parse_offer(block)
                if offer:
                    all_offers.append(offer)
                    count += 1

            print(f"   ✅ {count} offres Data/BI trouvées")
            time.sleep(random.uniform(1.5, 3.0))

        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur réseau : {e}")
            break

    print(f"\n🎯 Total : {len(all_offers)} offres")
    return all_offers