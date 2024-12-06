import requests
from collections import deque
from bs4 import BeautifulSoup

TARGET = 'Neon_Genesis_Evangelion'
QUICKPATHS = [['Asia', 'Japan', 'Anime'], ['East_Asia', 'Japan', 'Anime']]

class eva:
    def __init__(self):
        self.path = []
        self.depth = -1
        self.checked = 0
        self.EndIsExact = False
        self.start = None
        self.end = None

    def fetch_content(self, title):
        try:
            url = f'https://en.wikipedia.org/wiki/{title.replace(" ", "_")}'
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.text
            else:
                return ""
        except requests.RequestException:
            return ""

    def fetch_links(self, title):
        try:
            url = f'https://en.wikipedia.org/wiki/{title.replace(" ", "_")}'
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                return []
            soup = BeautifulSoup(response.text, 'html.parser')
            return [link['href'].split("/wiki/")[-1] for link in soup.find_all("a", href=True)]
        except requests.RequestException:
            return []

    def check_for_direct_evangelion_link(self, title):
        return TARGET.lower() in self.fetch_content(title).lower()

    def search(self, start_article):
        visited = set()
        queue = deque([(start_article, 0, [start_article])])
        self.checked = 0
        self.EndIsExact = False
        self.end = None
        self.start = start_article
        self.path = [start_article]

        for quickpath in QUICKPATHS:
            if start_article in quickpath:
                index = quickpath.index(start_article)
                self.path = quickpath[:index+1]  
                break  

        while queue:
            current_article, depth, path = queue.popleft()
            if current_article in visited:
                continue
            visited.add(current_article)

            if self.check_for_direct_evangelion_link(current_article):  
                self.depth = depth + 1
                self.path = path + ['Neon_Genesis_Evangelion']
                self.EndIsExact = True
                self.end = "Neon_Genesis_Evangelion"
                return  

            links = self.fetch_links(current_article)
            quickpath_links = []
            for link in links:
                
                for quickpath in QUICKPATHS:
                    if link in quickpath and link not in visited:
                        quickpath_links.append(link)
                        break  

            if quickpath_links:
                for link in quickpath_links:
                    self.checked += 1
                    queue.append((link, depth + 1, path + [link]))
            else:
                for link in links:
                    if link not in visited:
                        self.checked += 1
                        queue.append((link, depth + 1, path + [link]))

        self.depth = -1
        self.path = []
        self.end = None
