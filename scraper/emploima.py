import requests
from bs4 import BeautifulSoup
import time
import random

BASE_URL = "https://www.emploi.ma"

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


def extract_li_strong(ul_tag, keyword):
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
    h3 = li_tag.find("h3")
    if not h3:
        return None
    title_tag = h3.find("a")

    if not title_tag:
        return None

    full_title = title_tag.get_text(strip=True)
    url = BASE_URL + title_tag["href"]

    title = full_title.strip() 
    

    company_tag = li_tag.find("a", class_="card-job-company")
    company = company_tag.get_text(strip=True) if company_tag else ""

    desc_div = li_tag.find("div", class_="card-job-description")
    description = desc_div.find("p").get_text(strip=True) if desc_div else ""

    time_tag = li_tag.find("time")
    date_posted = time_tag["datetime"] if time_tag else ""

    ul_tag = li_tag.find("ul")
    contract_type = extract_li_strong(ul_tag, "Contrat proposé").strip().lstrip(":").strip()
    experience    = extract_li_strong(ul_tag, "Niveau d'expérience").strip().lstrip(":").strip()
    region        = extract_li_strong(ul_tag, "Région de").strip().lstrip(":").strip()
    skills        = extract_li_strong(ul_tag, "Compétences clés").strip().lstrip(":").strip()

    if not is_data_related(title) and not is_data_related(skills):
            return None

    if "-" in contract_type:
        contract_type = contract_type.split("-")[0].strip()

    return {
        "title": title,
        "company": company,
        "location": region,
        "contract_type": contract_type,
        "experience": experience,
        "description": description,
        "skills": skills,
        "source": "emploi.ma",
        "url": url,
        "date_posted": date_posted,
    }

def scrape_emploima(max_pages=5):
    all_offers = []
    seen_urls = set()

    SEARCH_KEYWORDS = [
    "data", "python", "business+intelligence", "machine+learning",
    "power+bi", "sql", "analytique", "reporting", "big+data","intelligence+artificielle",
    "data+scientist", "data+analyst"
    ]

    for keyword in SEARCH_KEYWORDS:
        for page in range(0, max_pages):
            url = f"{BASE_URL}/recherche-jobs-maroc/{keyword}?page={page}"
            print(f"📄 Page {page} : {url}")

            try:
                response = requests.get(url, headers=HEADERS, timeout=15)

                if response.status_code != 200:
                    print(f"⚠️  HTTP {response.status_code} — arrêt.")
                    break

                soup = BeautifulSoup(response.text, "html.parser")
                blocks = soup.find_all("div", class_="card-job-detail")

                if not blocks:
                    print(f"ℹ️  Plus d'offres à la page {page}.")
                    break

                count = 0
                for block in blocks:
                    offer = parse_offer(block)
                    if offer and offer["url"] not in seen_urls:
                        seen_urls.add(offer["url"])
                        all_offers.append(offer)
                        count += 1

                print(f"   ✅ {count} offres Data/BI trouvées")
                time.sleep(random.uniform(0.8, 1.5))

            except requests.exceptions.RequestException as e:
                print(f"❌ Erreur réseau : {e}")
                break

    print(f"\n🎯 Total : {len(all_offers)} offres")
    return all_offers