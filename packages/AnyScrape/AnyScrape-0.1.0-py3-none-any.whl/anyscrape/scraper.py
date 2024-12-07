import requests
from bs4 import BeautifulSoup

class AnyScrape:
    @staticmethod
    def scrape(url, target='headlines'):
        """Scrape basic information from a webpage.

        Args:
            url (str): The URL to scrape.
            target (str): What to scrape. Options: 'headlines', 'links', 'images'.

        Returns:
            list: Extracted content.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            if target == 'headlines':
                return [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3'])]
            elif target == 'links':
                return [a['href'] for a in soup.find_all('a', href=True)]
            elif target == 'images':
                return [img['src'] for img in soup.find_all('img', src=True)]
            else:
                raise ValueError(f"Unsupported target: {target}")
        except Exception as e:
            return [f"Error: {e}"]
