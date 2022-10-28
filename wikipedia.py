from bs4 import BeautifulSoup
import requests
import re


def get_inputs():
    while True:
        n = int(input("Enter number between 1-20: "))
        if 20 >= n >= 1:
            break
        else:
            print("Entered number is out of range. Please try again.")
    url = input("Enter Wikipedia Link: ")
    print(get_links(n, url))


def get_links(n, url):
    valid_urls = []
    for i in range(n):
        try:
            r = requests.get(url, timeout=3)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser')
            title = soup.find('h1', {'class': 'firstHeading'})
            for link in soup.find_all('a'):
                url = link.get('href', '')
                if url not in valid_urls and is_valid(url):
                    valid_urls.append(url)

        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
    return valid_urls


def is_valid(url):
    if url:
        if url.startswith('/wiki/'):
            if not re.compile('/\w+:').search(url):
                return True

    return False


get_inputs()
