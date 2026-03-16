from tools.search_tool import search_phd_programs
from tools.scraper_tool import scrape_page, filter_links
from agents.extractor_agent import extract_phd_info
from agents.planner_agent import validate_and_rank_results
from utils.country_detector import detect_country
from urllib.parse import urlparse
from tqdm import tqdm



def is_university_domain(url):

    domain = urlparse(url).netloc.lower()

    allowed_domains = [
        ".edu",
        ".ac.uk",
        ".edu.au",
        ".ac.in",
        ".de",
        ".nl",
        ".se",
        ".fi",
        ".no",
        ".dk"
    ]

    return any(domain.endswith(d) for d in allowed_domains)

def score_result(result, query):

    score = 0

    text = (result.get("title","") + " " + result.get("content","")).lower()
    query = query.lower()

    keywords = [
        "phd",
        "doctoral",
        "graduate",
        "program",
        "admission",
        "apply",
        "funding",
        "scholarship"
    ]

    for k in keywords:
        if k in text:
            score += 2

    for word in query.split():
        if word in text:
            score += 3

    return score

def research_phd_programs(query):

    search_results = search_phd_programs(query)

    search_results = sorted(
    search_results,
    key=lambda r: score_result(r, query),
    reverse=True
)

    structured_results = []
    seen_urls = set()

    for result in tqdm(search_results[:20], desc="Processing pages"):

        url = result["url"]

        if not is_university_domain(url):
            print("Skipping non-university site:", url)
            continue

        try:
            print(f"\n Scraping: {url}")

            page_text, links = scrape_page(url)
            

            if not page_text:
                print("No content extracted")
                continue
            
            if len(page_text) < 500:
                print("Page too small - skipping")
                continue
            links = filter_links(links)

            # Combine Tavily summary + scraped content
            tavily_summary = result.get("content", "")
            combined_text = (tavily_summary + "\n\n" + page_text)[:15000]

            # MULTI-PAGE SCRAPING STARTS HERE
            for link in links[:5]:

                print("Following link:", link)

                sub_text, _ = scrape_page(link)

                if sub_text:
                    combined_text += "\n\n" + sub_text

            phd_info = extract_phd_info(combined_text)

            # fallback: try to detect university from URL
            if phd_info.get("university") == "Not found":
                domain = urlparse(url).netloc.lower()
                domain = domain.replace("www.", "")

                parts = domain.split(".")

                # detect university domain
                if "ac" in parts:
                    uni_index = parts.index("ac") - 1
                    university = parts[uni_index]
                elif "edu" in parts:
                    uni_index = parts.index("edu") - 1
                    university = parts[uni_index]
                else:
                    university = parts[0]

                phd_info["university"] = university.capitalize()

                print("University inferred from domain:", phd_info["university"])
            
            # detect country
            if phd_info.get("country") == "Not found":
                phd_info["country"] = detect_country(url, combined_text)

            # skip duplicate URLs instead of universities
            if url in seen_urls:
                print("Duplicate URL skipped")
                continue

            if phd_info.get("application_link") == "Not found":
                phd_info["application_link"] = url

            seen_urls.add(url)

            phd_info["source_url"] = url

            structured_results.append(phd_info)

        except Exception as e:
            print("Error processing:", url, e)

    structured_results = validate_and_rank_results(structured_results, query)

    print(f"\n Total valid universities found: {len(structured_results)}")

    return structured_results