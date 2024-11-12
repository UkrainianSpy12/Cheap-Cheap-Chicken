import requests
from bs4 import BeautifulSoup

def search_item(item):
    websites = [
        "https://www.aliexpress.com/wholesale?SearchText=",
        "https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=",
        "https://www.shein.com/SearchResults.asp?SearchKey=",
        "https://www.taobao.com/search?q=",
        "https://www.jd.com/search?keyword=",
        "https://www.pinduoduo.com/search?query=",
        "https://www.temu.com/search?q=",
        "https://www.1688.com/chanpin/?keywords=",
        "https://www.dhgate.com/wholesale?q=",
    ]

    results = []

    # Search each website
    for website in websites:
        url = website + item
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        if 'aliexpress' in website:
            products = soup.find_all('div', class_="product")  # Update with actual class on Aliexpress
        elif 'alibaba' in website:
            products = soup.find_all('div', class_="item-content")  # Update with actual class on Alibaba
        elif 'shein' in website:
            products = soup.find_all('div', class_="product-item")  # Update with actual class on Shein

        for product in products:
            name = product.find('a', class_="product-name") or product.find('span', class_="product-name")  # Example
            price = product.find('span', class_="price") or product.find('span', class_="price-range")  # Example
            if name and price:
                results.append({
                    "name": name.get_text(strip=True),
                    "price": price.get_text(strip=True),
                    "link": website + item
                })
    
    return results

def generate_gpt_prompt(results):
    prompt = "Here are some options for the product you're looking for:\n\n"
    
    for idx, result in enumerate(results, start=1):
        prompt += f"Option {idx}: {result['name']} - Price: {result['price']}\nLink: {result['link']}\n\n"
    
    prompt += "Please summarize the options in a way that highlights the best deals, including any discounts or notable features."
    
    return prompt

# Main function to run the program
def main():
    # Ask the user for the name of the item
    item = input("Enter the name of the item you want to search for: ")

    # Collect results from websites
    results = search_item(item)

    # Generate a GPT-4 Mini prompt based on the collected data
    gpt_prompt = generate_gpt_prompt(results)

    # Print the GPT-4 Mini prompt (or save to a text file)
    print(gpt_prompt)

    # Optionally save it to a text file
    with open("gpt_prompt.txt", "w") as f:
        f.write(gpt_prompt)

if __name__ == "__main__":
    main()
