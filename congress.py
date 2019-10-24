from bs4 import BeautifulSoup
import requests
import re
from typing import Dict, Set
import random
url = "https://www.house.gov/representatives"
text = requests.get(url).text
soup = BeautifulSoup(text, 'html5lib')


all_urls = [a['href'] for a in soup('a') if a.has_attr('href')]
print(f"total number of urls before cleaning: {len(all_urls)}")

regex = r"^https?://.*\.house\.gov/?$"

assert re.match(regex, "http://paris.house.gov")
assert re.match(regex, "https://paris.house.gov")
assert re.match(regex, "http://joel.house.gov/")
assert re.match(regex, "https://joel.house.gov/")
assert not re.match(regex, "joel.house.gov")
assert not re.match(regex, "http://joel.house.com")
assert not re.match (regex, "https://joel.house.gov/biography")


good_urls = [url for url in all_urls if re.match(regex, url)]
# print(len(good_urls))
good_urls = list(set(good_urls))
print(f"Number of urls after cleaning: {len(good_urls)}")
# print(good_urls[:5])


html = requests.get('https://jayapal.house.gov').text
soup = BeautifulSoup(html, 'html5lib')
links = {a['href'] for a in soup('a') if 'press releases' in a.text.lower()}
# print(links) # {'/media/press-releases'}

good_urls = random.sample(good_urls,10)
print(f"Randomly picked {len(good_urls)} urls")


press_releases: Dict[str, Set[str]] = {}
for house_urls in good_urls:
    html = requests.get(house_urls).text
    soup = BeautifulSoup(html, 'html5lib')
    pr_links = {a['href'] for a in soup('a') if 'press releases' in a.text.lower()}
    print(f"{house_urls}: {pr_links}")
    press_releases[house_urls] = pr_links



def paragraph_mentions(text: str, keyword: str) -> bool:
    soup = BeautifulSoup(text, 'html5lib')
    paragraphs = [p.get_text() for p in soup('p')]
    return any(keyword.lower() in paragraph.lower() for paragraph in paragraphs)

text = """<body><h1>Facebook</h1><p>Twitter</p>"""
assert paragraph_mentions(text, "twitter")
assert not paragraph_mentions(text, "facebook")

print("Chose a word for start scraping")
word = input("Type one word: ")
assert len(word.split()) == 1, "Chose only one word"
word.lower()

def look_for_info(word: str)-> str:
    for house_url, pr_links in press_releases.items():
        for pr_link in pr_links:
            url = f"{house_url}/{pr_link}"
            text = requests.get(url).text

            if paragraph_mentions(text, word):
                print(f"****{house_url}**** mentions the word {word} at least once at {pr_link}")
                break
look_for_info(word)
