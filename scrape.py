import requests
from bs4 import BeautifulSoup
import json
import os

target_urls = [
    "https://iitk.ac.in/ccn/services/network/how-to-use-ssl-vpn",
    "https://iitk.ac.in/ccn/services/network/direct-no-proxy-internet",
    "https://iitk.ac.in/ccn/services/network/cisco-webex",
    "https://iitk.ac.in/ccn/services/network/wlan",
    "https://iitk.ac.in/ccn/services/network/dhcp",
]

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
    # Ensure that a folder named 'data' exists; create it if it doesn't
    os.makedirs('data', exist_ok=True)  # Make sure output folder exists if not make one

    # Loop through each URL in the list 'target_urls'
    for url in target_urls:
        try:
            print(f"Scraping: {url}")  # Inform which URL is being scraped

            # Call a function to extract data from the page at this URL
            page_info = extract_page_data(url)

            # Generate a safe filename from the last part of the URL
            # Strip trailing '/', take the last part of the URL, replace '-' with '_', and add .json extension
            filename = url.rstrip('/').split('/')[-1].replace('-', '_') + ".json"
            path = os.path.join("data", filename)  # Full path to save the JSON file

            # Open the file for writing and save the scraped data as JSON
            with open(path, "w", encoding="utf-8") as f:
                json.dump(page_info, f, ensure_ascii=False, indent=4)  # Save with indentation and UTF-8 characters

            print(f"Saved: {path}")  # Confirm the file was saved

        except Exception as e:
            # If something goes wrong while scraping or saving, print an error message
            print(f"Failed to scrape {url}: {e}")

    print("✅ All pages scraped.")  # Final message after the loop is done


if __name__ == '__main__':
    main()
