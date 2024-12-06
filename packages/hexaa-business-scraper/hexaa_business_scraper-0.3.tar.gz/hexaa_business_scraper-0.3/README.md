# Hexaa Business Scraper

Hexaa Business Scraper is a Python library designed for scraping business information from Google Maps. With minimal setup, users can extract details like business names, addresses, websites, phone numbers, reviews, and more by simply importing the library and passing relevant parameters.

---

## Installation

Install the package using pip:

```bash
pip install hexaa-business-scraper
```

# Usage
After installation, you can import the library and use its main function to scrape business data.

# Example
```
from hexaa_business_scraper import scrape_data_cli

search_query = "restaurants in New York"  # Search term for businesses
total_results = 10  # Number of results to scrape

# Scrape and save results to a CSV file
scrape_data_cli(search_query, total_results)

```

# Parameters:
search_query = "restaurants in New York"  # Search term for businesses
total_results = 10  # Number of results to scrape

# Scrape and save results to a CSV file
scrape_businesses(search_query, total_results)
This example scrapes 10 businesses based on the search query and saves the results in a CSV file named result.csv.

# Parameters
The scrape_businesses function accepts the following parameters:

search_query (str): The search term to look for (e.g., "hotels in Paris").
total_results (int): The number of businesses to scrape. Default is 10.

# Output
The scraper saves the scraped data in a CSV file named result.csv with the following fields:

Business Name
Address
Website
Phone Number
Review Count
Average Rating
Business Type
Opening Hours
Notes
Make sure to have Playwright installed and set up properly.

For Playwright setup, run the following command after installing the library:

```
playwright install
```
# Happy Scraping! 🚀