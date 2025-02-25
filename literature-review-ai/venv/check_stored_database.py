from database import session, ResearchPaper

# Fetch all papers
papers = session.query(ResearchPaper).all()

for paper in papers:
    print(f"\n🔹 Title: {paper.title}")
    print(f"📌 Authors: {paper.authors}")
    print(f"📰 Journal: {paper.journal}")
    print(f"🔗 Read more: {paper.url}")
