import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def extract_links(soup, base_url):

    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("mailto:") or href.startswith("tel:"):
            continue
        full_url = urljoin(base_url, href)
        links.append(full_url)

    return list(set(links))

def filter_links(links):

    good_keywords = [
        "phd",
        "graduate",
        "program",
        "admission",
        "apply",
        "application",
        "funding",
        "scholarship",
        "financial",
        "requirements"
    ]

    bad_keywords = [
        "privacy",
        "policy",
        "cookie",
        "faculty",
        "staff",
        "people",
        "news",
        "event",
        "calendar",
        "directory",
        "login",
        "contact"
    ]

    filtered = []


    for link in links:

        link_lower = link.lower()

        if link_lower.endswith(".pdf"):
            continue

        # skip bad links
        if any(bad in link_lower for bad in bad_keywords):
            continue

        # keep good links
        if any(good in link_lower for good in good_keywords):
            filtered.append(link)

    # remove duplicates and limit to 3 pages
    return list(set(filtered))[:3]

def scrape_page(url):

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            return "", []

        soup = BeautifulSoup(response.text, "lxml")

        for script in soup(["script", "style", "noscript"]):
            script.extract()

        elements = soup.find_all(["p", "li", "td", "span", "h1", "h2", "h3"])

        text = " ".join(e.get_text(" ", strip=True) for e in elements)

        text = " ".join(text.split())

        links = extract_links(soup, url)

        return text[:12000], links

    except Exception as e:

        print("Scraping error:", e)

        return "", []