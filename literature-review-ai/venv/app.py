from flask import Flask, render_template, request
from database import session, ResearchPaper
from sqlalchemy import desc

app = Flask(__name__)

# --- Search Papers with Pagination & Sorting ---
@app.route("/search", methods=["GET"])
def search_papers():
    query = request.args.get("query", "")
    page = request.args.get("page", 1, type=int)
    per_page = 5  # Number of results per page
    sort_by = request.args.get("sort", "relevance")  # Default sorting

    if not query:
        return render_template("index.html", papers=[], query=query)

    # Base query
    papers_query = session.query(ResearchPaper).filter(ResearchPaper.title.ilike(f"%{query}%"))

    # Sorting Logic
    if sort_by == "citations":
        papers_query = papers_query.order_by(desc(ResearchPaper.citations))  # Most cited first
    elif sort_by == "journal":
        papers_query = papers_query.order_by(ResearchPaper.journal)  # Alphabetical order
    elif sort_by == "year":
        papers_query = papers_query.order_by(desc(ResearchPaper.year))  # Newest first

    total_papers = papers_query.count()
    papers = papers_query.offset((page - 1) * per_page).limit(per_page).all()

    return render_template("index.html", papers=papers, query=query, page=page, total_papers=total_papers, per_page=per_page, sort_by=sort_by)

if __name__ == "__main__":
    app.run(debug=True)
