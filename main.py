from agents.researcher_agent import research_phd_programs as run_research
from utils.pdf_generator import generate_pdf

def main():

    print("\n===== AI PhD Research Agent =====\n")

    query = input("Enter your PhD search query: ")

    print("\nSearching universities...\n")

    results = run_research(query)

    if not results:
        print("No results found.")
        return

    print(f"Found {len(results)} results")

    pdf_path = generate_pdf(results)

    print(f"\nReport generated: {pdf_path}")


if __name__ == "__main__":
    main()