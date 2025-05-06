import requests
from bs4 import BeautifulSoup
import json
import os

# List of IITK CCN network service URLs to scrape
target_urls = [
    "https://iitk.ac.in/ccn/services/network/how-to-use-ssl-vpn",
    "https://iitk.ac.in/ccn/services/network/direct-no-proxy-internet",
    "https://iitk.ac.in/ccn/services/network/cisco-webex",
    "https://iitk.ac.in/ccn/services/network/wlan",
    "https://iitk.ac.in/ccn/services/network/dhcp",
]

# Function to extract structured content from the article body
def extract_page_data(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    page_data = {
        "url": url,
        "title": soup.title.string.strip() if soup.title else "",
        "headings": [],
        "paragraphs": [],
        "links": [],
        "tables": []
    }

    article_body = soup.find(itemprop="articleBody")
    if not article_body:
        article_body = soup.find('div', class_='article-body')

    if article_body:
        for heading in article_body.find_all([f"h{i}" for i in range(1, 7)]):
            text = heading.get_text(strip=True)
            if text:
                page_data["headings"].append({
                    "tag": heading.name,
                    "text": text
                })

        for p in article_body.find_all('p'):
            text = p.get_text(strip=True)
            if text:
                page_data["paragraphs"].append(text)

        for a in article_body.find_all('a', href=True):
            text = a.get_text(strip=True)
            href = a['href']
            page_data["links"].append({
                "text": text,
                "href": href
            })

        for table in article_body.find_all('table'):
            table_rows = []
            for tr in table.find_all('tr'):
                row = []
                for cell in tr.find_all(['td', 'th']):
                    # If the cell contains a link
                    a_tag = cell.find('a', href=True)
                    if a_tag:
                        cell_data = {
                            "text": cell.get_text(strip=True),
                            "link": a_tag['href'],
                            "link_text": a_tag.get_text(strip=True)
                        }
                    else:
                        cell_data = {"text": cell.get_text(strip=True)}
                    row.append(cell_data)
                if row:
                    table_rows.append(row)
            if table_rows:
                page_data["tables"].append(table_rows)

    return page_data

#Gpt
def main():
    os.makedirs('data', exist_ok=True)  # Make sure output folder exists if not make one

    for url in target_urls:
        try:
            print(f"Scraping: {url}")
            page_info = extract_page_data(url)

            # Create a valid filename from the URL path
            filename = url.rstrip('/').split('/')[-1].replace('-', '_') + ".json"
            path = os.path.join("data", filename)

            # Save to individual JSON file
            with open(path, "w", encoding="utf-8") as f:
                json.dump(page_info, f, ensure_ascii=False, indent=4)

            print(f"Saved: {path}")

        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    print("✅ All pages scraped.")

if __name__ == '__main__':
    main()
