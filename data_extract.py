import requests
import webbrowser
from bs4 import BeautifulSoup

def search_crossref(query, max_results=5):
    base_url = 'https://api.crossref.org/works'
    params = {
        'query': query,
        'rows': max_results
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        results = response.json()

        papers = []
        doi_ = []
        if 'message' in results and 'items' in results['message']:
            for result in results['message']['items']:
                paper = {
                    'title': result.get('title', ['No title available'])[0],
                    'doi': result.get('DOI'),
                    'link': result['URL'],
                    'published': result.get('published-print', result.get('published-online', {})).get('date-parts', [[None]])[0][0]
                }
                papers.append(paper)
                doi_link = f"https://doi.org/{result.get('DOI')}"
                doi_.append(doi_link)
        else:
            print("No results found or unexpected response structure.")

        return papers, doi_
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Crossref: {e}")
        return [], []

def search_scholar(query, max_results=5):
    search_url = f'https://scholar.google.com/scholar?q={query}'
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        doi_ = []
        for idx, result in enumerate(soup.find_all('div', class_='gs_ri'), start=1):
            if idx > max_results:
                break
            link = result.find('a', href=True)
            if link and 'doi.org' in link['href']:
                doi_.append(link['href'])

        return doi_
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Google Scholar: {e}")
        return []

def open_link(url):
    webbrowser.open(url, new=2)  # new=2 opens the link in a new tab, if possible

def main():
    query = input("Enter your search query: ")
    papers_crossref, doi_crossref = search_crossref(query)
    doi_scholar = search_scholar(query)

    # Combine and deduplicate DOI links
    doi_ = list(set(doi_crossref + doi_scholar))

    if doi_:
        base = "https://sci-hub.se/"
        for doi_link in doi_:
            url = base + doi_link
            open_link(url)
        print("List of DOI links:", doi_)
    else:
        print("No DOI links found for the given query.")

if __name__ == "__main__":
    main()
