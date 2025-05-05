import requests
from bs4 import BeautifulSoup
import json

# List of IITK CCN network service URLs to scrape
target_urls = [
    "https://iitk.ac.in/ccn/services/network/how-to-use-ssl-vpn",
    "https://iitk.ac.in/ccn/services/network/direct-no-proxy-internet",
    "https://iitk.ac.in/ccn/services/network/cisco-webex",
    "https://iitk.ac.in/ccn/services/network/wlan",
    "https://iitk.ac.in/ccn/services/network/dhcp",
]

# Function to extract structured content from a page
def extract_page_data(url):
    response = requests.get(url)
    response.raise_for_status()  # ensure we stop on HTTP errors
    soup = BeautifulSoup(response.text, 'html.parser')

    page_data = {
        "url": url,
        "title": soup.title.string.strip() if soup.title else "",
        "headings": [],
        "paragraphs": [],
        "links": []
    }

    # Extract headings (h1-h6)
    for heading in soup.find_all([f"h{i}" for i in range(1, 7)]):
        text = heading.get_text(strip=True)
        if text:
            page_data["headings"].append({
                "Heading": heading.name,
                "text": text
            })

    # Extract paragraph text
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        if text:
            page_data["paragraphs"].append(text)

    # Extract all links (anchor tags)
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True)
        href = a['href']
        page_data["links"].append({
            "text": text,
            "href": href
        })

    return page_data


def main():
    all_data = []
    for url in target_urls:
        try:
            print(f"Scraping: {url}")
            page_info = extract_page_data(url)
            all_data.append(page_info)
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    # Save the collected data into a JSON file
    with open('network_services.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_data, json_file, ensure_ascii=False, indent=4)

    print("Data extraction complete. Saved to network_services.json")

if __name__ == '__main__':
    main()
