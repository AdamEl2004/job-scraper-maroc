from scraper.rekrute import scrape_rekrute
from database.db_handler import save_offers, count_offers

if __name__ == "__main__":
    print("🚀 Démarrage du scraping...\n")
    offers = scrape_rekrute(max_pages=10)
    save_offers(offers)
    print(f"\n📊 Total dans la base : {count_offers()} offres")
