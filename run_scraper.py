from scraper.rekrute import scrape_rekrute
from scraper.emploima import scrape_emploima
from database.db_handler import save_offers, count_offers

if __name__ == "__main__":
    print("🚀 Démarrage du scraping...\n")

    print("── Rekrute ──")
    offers_rekrute = scrape_rekrute(max_pages=5)
    save_offers(offers_rekrute)

    print("\n── Emploi.ma ──")
    offers_emploi = scrape_emploima(max_pages=5)
    save_offers(offers_emploi)

    print(f"\n📊 Total dans la base : {count_offers()} offres")