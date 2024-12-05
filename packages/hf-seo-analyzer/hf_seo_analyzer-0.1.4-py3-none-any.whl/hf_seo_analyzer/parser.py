import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import yaml
from datetime import datetime
from urllib.parse import urlparse
import os
from collections import Counter
import re

def fetch_url_to_markdown(url, file_path=None, default_author="unknown", keyword_limit=10):
    """
    Fetch the content and metadata of a URL and save it to a Markdown file with YAML frontmatter.
    Only includes main content, excluding headers, footers, and comments.

    :param url: The URL of the post to fetch.
    :param file_path: Optional custom path to save the Markdown file. Defaults to slug-based name in the current directory.
    :param default_author: Default author if none is found in the post.
    :param keyword_limit: Maximum number of suggested keywords.
    """
    # Fetch the URL
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch URL: {url} (status code: {response.status_code})")

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract metadata
    title = soup.find("title").text.strip() if soup.find("title") else "Untitled"
    description = soup.find("meta", attrs={"name": "description"})
    description = description["content"].strip() if description else ""
    h1_headings = " ".join([h.get_text(strip=True) for h in soup.find_all("h1")])
    h2_headings = " ".join([h.get_text(strip=True) for h in soup.find_all("h2")])
    h3_headings = " ".join([h.get_text(strip=True) for h in soup.find_all("h3")])
    h4_headings = " ".join([h.get_text(strip=True) for h in soup.find_all("h4")])

    # Extract main content
    main_content = extract_main_content(soup)

    # Combine text sources for keyword suggestion
    text_sources = {
        "content": main_content,
        "title": title,
        "description": description,
        "h1": h1_headings,
        "h2": h2_headings,
        "h3": h3_headings,
        "h4": h4_headings,
    }

    keywords = suggest_keywords(text_sources, keyword_limit)

    # Prepare additional metadata
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    domain = urlparse(url).netloc
    image = soup.find("meta", attrs={"property": "og:image"})
    image = image["content"].strip() if image else "https://learn-anything.vn/images/default-image.png"

    # Extract the slug from the URL and use it as the file name
    slug = url.rstrip("/").split("/")[-1]

    # Use the slug for the file path if none is provided
    if not file_path:
        file_path = os.path.join(os.getcwd(), f"{slug}.md")

    metadata = {
        "title": title,
        "author": [default_author],
        "date": date,
        "description": description,
        "domain": domain,
        "image": image,
        "keywords": keywords,
        "slug": slug,
    }

    # Convert main content to Markdown
    markdown_content = f"---\n{yaml.dump(metadata, allow_unicode=True)}---\n\n{main_content}"

    # Save to Markdown file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"✨ Markdown file saved to: {file_path}")

def extract_main_content(soup):
    """
    Extract the main content of a page, excluding headers, footers, and comments.

    :param soup: BeautifulSoup object of the HTML page.
    :return: Main content as Markdown.
    """
    # Try to locate the <article> or <main> tag, which usually contains the main content
    main_content_tag = soup.find("article") or soup.find("main")

    if main_content_tag:
        # Remove irrelevant elements within the main content
        for unwanted in main_content_tag.find_all(["header", "footer", "aside", "nav", "form"]):
            unwanted.decompose()

        return md(str(main_content_tag))

    # If no <article> or <main> tag, use the <body> content as a fallback
    body_content = soup.find("body")
    if body_content:
        # Remove irrelevant elements within the body
        for unwanted in body_content.find_all(["header", "footer", "aside", "nav", "form", "script", "style"]):
            unwanted.decompose()

        return md(str(body_content))

    return "No content available."

def suggest_keywords(text_sources, limit=10, min_words=2, max_words=5):
    """
    Suggest keywords based on high-frequency n-grams and validate their presence in key SEO areas (title, description, headings).

    :param text_sources: Dictionary of text sources (e.g., content, title, description, h1, h2, h3, h4).
    :param limit: Maximum number of keywords to suggest.
    :param min_words: Minimum number of words in a keyword phrase.
    :param max_words: Maximum number of words in a keyword phrase.
    :return: A list of prioritized accented keywords.
    """
    # Extract individual sources
    content = text_sources.get("content", "").lower()
    title = text_sources.get("title", "").lower()
    description = text_sources.get("description", "").lower()
    headings = " ".join([text_sources.get(f"h{i}", "") for i in range(1, 5)]).lower()

    # Extract n-grams from content
    content_ngrams = extract_ngrams(content, min_words=min_words, max_words=max_words)

    # Count frequency in content
    ngram_counts = Counter(content_ngrams)

    # Match n-grams across SEO areas
    matched_keywords = {}
    for keyword, freq in ngram_counts.items():
        keyword_positions = []

        # Check presence in title, description, and headings
        if keyword in title:
            keyword_positions.append("title")
        if keyword in description:
            keyword_positions.append("description")
        if keyword in headings:
            keyword_positions.append("headings")

        # Consider only keywords appearing in at least 2 positions
        if len(keyword_positions) >= 2:
            matched_keywords[keyword] = {
                "positions": keyword_positions,
                "frequency": freq,
            }

    # Sort by the number of positions matched, then by frequency
    sorted_keywords = sorted(
        matched_keywords.items(),
        key=lambda x: (len(x[1]["positions"]), x[1]["frequency"]),
        reverse=True,
    )

    # Return the top `limit` keywords
    return [keyword for keyword, _ in sorted_keywords[:limit]]

def extract_ngrams(text, min_words=2, max_words=5):
    """
    Extract n-grams (phrases with a variable number of words) from text.

    :param text: Original text.
    :param min_words: Minimum number of words in a keyword phrase.
    :param max_words: Maximum number of words in a keyword phrase.
    :return: List of n-grams.
    """
    # Tokenize text into words
    words = re.findall(r'\b\w{3,}\b', text)

    # Define stopwords (both English and Vietnamese)
    stopwords = set([
        # English stopwords
        "the", "and", "for", "with", "that", "this", "from", "are", "was", "you", "your",
        "have", "has", "will", "not", "but", "all", "about",
        # Vietnamese stopwords
        "và", "là", "của", "có", "cho", "trong", "một", "những", "được", "với", "để", "không",
        "khi", "này", "ở", "cũng", "như", "thì", "đã", "rằng", "đó", "nhưng", "điều", "hơn"
    ])

    # Filter out stopwords
    filtered_words = [word for word in words if word not in stopwords]

    # Generate n-grams for all lengths between min_words and max_words
    ngrams = []
    for n in range(min_words, max_words + 1):
        ngrams.extend(
            " ".join(filtered_words[i:i + n])
            for i in range(len(filtered_words) - (n - 1))
        )
    return ngrams