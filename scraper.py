import requests
from bs4 import BeautifulSoup
import time

def search_item(item):
    search_urls = [
        f"https://www.gearbest.com/search?keyword={item}",
        f"https://www.aliexpress.com/wholesale?SearchText={item}",
        f"https://www.jd.com/search?keyword={item}",
        f"https://www.taobao.com/search?q={item}",
        f"https://item.jd.com/search?keyword={item}"
    ]
    
    results = []
    
    for url in search_urls:
        try:
            print(f"Searching {url}...")
            response = requests.get(url, timeout=10)  # Set timeout for faster failure
            response.raise_for_status()  # Will raise an HTTPError if the status is 4xx/5xx
            soup = BeautifulSoup(response.text, 'html.parser')
            results.append(f"Results from {url}: {soup.title.string}")  # Just an example, change to real scraping logic
        except requests.exceptions.RequestException as e:
            print(f"Error with {url}: {e}")
            continue
    
    return results

def main():
    item = input("Enter item name: ")
    print(f"Searching for: {item}")
    results = search_item(item)
    if results:
        print("Search Results:")
        for result in results:
            print(result)
    else:
        print("No results found or failed to retrieve data.")

if __name__ == "__main__":
    main()
