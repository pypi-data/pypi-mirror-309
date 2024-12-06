import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from hexaa_business_scraper import scrape_data

if __name__ == "__main__":
    search_term = "cafes in Paris"
    total_results = 5
    data = scrape_data(search_term, total=total_results)
    print(data)
