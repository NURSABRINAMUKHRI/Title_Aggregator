import requests
from bs4 import BeautifulSoup
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

# Scrape The Verge
def scrape_the_verge():
    url = "https://www.theverge.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for item in soup.find_all("a", class_="group-hover:shadow-underline-franklin"):
        # Extract article title and link
        title = item.text.strip()
        link = f"https://www.theverge.com{item['href']}"  # Full URL

        # Extract date from the URL if it contains it (e.g., /2025/1/20/)
        try:
            date_str = item['href'].split("/")[1:4]  # Extract year, month, day
            article_date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
        except (IndexError, ValueError):
            # Skip articles without valid dates
            continue

        # Filter articles from Jan 1, 2022, onwards
        if article_date >= datetime(2022, 1, 1):
            articles.append({"title": title, "link": link, "date": article_date})

    # Sort articles anti-chronologically (latest first)
    articles.sort(key=lambda x: x["date"], reverse=True)

    return articles


@app.route("/")
def index():
    articles = scrape_the_verge()
    return render_template("index.html", articles=articles)

if __name__ == "__main__":
    app.run(debug=True)
