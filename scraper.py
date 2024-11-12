import requests
import sys
from time import sleep

# Define the retry count and delay between retries
RETRY_COUNT = 3
RETRY_DELAY = 5  # seconds

# List of Chinese e-commerce websites to scrape
URLS = [
    "https://www.temu.com/search?q={item}",
    "https://www.shein.com/search/{item}-c-1673.html",
    "https://www.aliexpress.com/wholesale?SearchText={item}",
    "https://www.jd.com/search?keyword={item}",
    "https://www.taobao.com/search?q={item}",
    "https://www.pinduoduo.com/search/{item}",
]

def fetch_item_data(url, item):
    """Fetches data from a URL and handles request exceptions."""
    for attempt in range(RETRY_COUNT):
        try:
            # Format the URL with the item
            formatted_url = url.format(item=item)
            print(f"Attempting to fetch data from {formatted_url}")
            
            # Send GET request to the formatted URL
            response = requests.get(formatted_url)
            response.raise_for_status()  # Will raise HTTPError for bad status codes
            
            # Assuming the website returns JSON, you can adjust this as needed for HTML scraping
            return response.text  # You can process the HTML further if needed
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}/{RETRY_COUNT} failed: {e}")
            if attempt < RETRY_COUNT - 1:
                sleep(RETRY_DELAY)  # Wait before retrying
            else:
                print(f"Failed to fetch data from {formatted_url} after {RETRY_COUNT} attempts.")
                raise  # Reraise the error if retries are exhausted

def main():
    if len(sys.argv) != 2:
        print("Error: Please provide the item name as a command-line argument.")
        sys.exit(1)

    item = sys.argv[1]  # Get the item name from the command line arguments
    
    all_results = {}
    
    # Loop through all URLs and fetch data
    for url in URLS:
        try:
            print(f"Searching for '{item}' on {url}")
            results = fetch_item_data(url, item)
            all_results[url] = results
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
    
    # Output all the results fetched
    print("\nAll search results:")
    for url, results in all_results.items():
        print(f"Results from {url}: {results}")

if __name__ == "__main__":
    main()
