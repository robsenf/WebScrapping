import requests
import bs4
from bs4 import BeautifulSoup

# Let's go to example.com first
result = requests.get("http://www.example.com")
print(result.text)  # or do something with the response


type(result)

soup = BeautifulSoup(result.text, "lxml")  # Create a BeautifulSoup object
res = requests.get("https://en.wikipedia.org/wiki/Grace_Hopper")
soup = bs4.BeautifulSoup(res.text, "lxml")
first_item = soup.select('.vector-toc-text')[1]
first_item.text
for item in soup.select('.vector-toc-text') : 
    print(item.text)
    

