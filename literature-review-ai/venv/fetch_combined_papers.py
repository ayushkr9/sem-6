import requests
import xml.etree.ElementTree as ET
import pandas as pd
from database import session, ResearchPaper
# --- arXiv API ---
def fetch_arxiv_papers(query, max_results=5):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    response = requests.get(url)
    if response.status_code != 200:
        print("❌ Failed to fetch papers from arXiv")
        return []

    root = ET.fromstring(response.text)
    papers = []
    
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        authors = [author.find("{http://www.w3.org/2005/Atom}name").text for author in entry.findall("{http://www.w3.org/2005/Atom}author")]
        link = entry.find("{http://www.w3.org/2005/Atom}id").text
        
        papers.append({
            "title": title,
            "summary": summary.strip(),
            "authors": authors,
            "source": "arXiv",
            "citations": "N/A",
            "doi": "N/A",
            "journal": "N/A",
            "publisher": "N/A",
            "url": link
        })

    return papers

# --- Semantic Scholar API ---
def fetch_semantic_scholar_papers(query, max_results=5):
    API_KEY = "91JejA8b7l6c5vlyXLqm145uPbcuKfXQ49pxbmem"  # Replace with your actual API key
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={max_results}&fields=title,authors,url,abstract,citationCount"

    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ Failed to fetch papers from Semantic Scholar")
        return []

    data = response.json()
    papers = []

    for paper in data.get("data", []):
        papers.append({
            "title": paper["title"],
            "summary": paper.get("abstract", "No abstract available"),
            "authors": [author["name"] for author in paper.get("authors", [])],
            "source": "Semantic Scholar",
            "citations": paper.get("citationCount", 0),
            "doi": "N/A",
            "journal": "N/A",
            "publisher": "N/A",
            "url": paper.get("url", "No URL available")
        })

    return papers

# --- CrossRef API ---
def fetch_crossref_papers(query, max_results=5):
    url = f"https://api.crossref.org/works?query={query}&rows={max_results}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("❌ Failed to fetch papers from CrossRef")
        return []

    data = response.json()
    papers = []

    for item in data.get("message", {}).get("items", []):
        papers.append({
            "title": item.get("title", ["No Title"])[0],
            "summary": "N/A",  # CrossRef doesn't provide abstracts
            "authors": [author["given"] + " " + author["family"] for author in item.get("author", [])] if "author" in item else [],
            "source": "CrossRef",
            "citations": "N/A",  # CrossRef doesn't provide citation counts
            "doi": item.get("DOI", "No DOI"),
            "journal": item.get("container-title", ["No Journal"])[0],
            "publisher": item.get("publisher", "Unknown"),
            "url": item.get("URL", "No URL")
        })

    return papers

# --- Combine Results ---
def fetch_all_papers(query, max_results=5):
    papers = []
    papers.extend(fetch_arxiv_papers(query, max_results))
    papers.extend(fetch_semantic_scholar_papers(query, max_results))
    papers.extend(fetch_crossref_papers(query, max_results))

    return papers

def save_to_db(papers):
    for paper in papers:
        existing_paper = session.query(ResearchPaper).filter_by(title=paper["title"]).first()
        if not existing_paper:
            new_paper = ResearchPaper(
                title=paper["title"],
                summary=paper["summary"],
                authors=", ".join(paper["authors"]),
                source=paper["source"],
                citations=str(paper["citations"]),
                doi=paper["doi"],
                journal=paper["journal"],
                publisher=paper["publisher"],
                url=paper["url"]
            )
            session.add(new_paper)
    
    session.commit()
    print("✅ Papers saved to the database!")

# Fetch and store papers
query = "natural language processing"
papers = fetch_all_papers(query)
save_to_db(papers)

