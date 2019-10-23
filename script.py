'''
Script for scraping data and updating DB

jobs dictionary should look like:
{
'/listing/1234': {
'name': 'job',
'url': '/listing/1234',
'employer': 'IRS',
'date_posted': '2018-11-27',
},
...
}
'''
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import os
import random
from dotenv import load_dotenv


load_dotenv()
jobs = {}
searches = [
    "software-engineer",
    "software-developer",
    "python"]
BACKEND_DOMAIN = os.environ.get('BACKEND_DOMAIN') or 'http://localhost:8000'
KSL_URL = 'https://jobs.ksl.com/search/keywords/'


def get_jobs(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}  # noqa: E501
    print(f'Fetching {url}...')
    data = requests.get(
        url, headers=headers, verify=False, timeout=20)
    soup = BeautifulSoup(data.text, 'html.parser')
    print('Done.')
    names = []
    urls = []
    employers = []
    dates = []

    # Get name and url from anchor tags.
    for title in soup.find_all('h2', {'class': 'job-title'}):
        anchor = title.find('a')
        names.append(anchor.text.strip())
        urls.append(anchor.get('href'))

    # Get employer names
    for employer in soup.find_all('span', {'class': 'company-name'}):
        employers.append(employer.text.strip())

    # Get posting dates
    for date in soup.find_all('span', {'class': 'posted-time'}):
        d = datetime.strptime(date.text.strip(), 'Posted %b %d, %Y')
        d = d.strftime('%Y-%m-%d')
        dates.append(d)

    # Test that array sizes match
    if len(names) == len(urls) and \
        len(urls) == len(employers) and \
        len(employers) == len(dates):
        for i in range(len(names)):
            job = {
                'name': names[i],
                'employer': employers[i],
                'url': urls[i],
                'date_posted': dates[i],
            }
            jobs[urls[i]] = job

    # Now, fint 'next' anchor and rerun.
    next_page = soup.find('a', {'class': 'next link'})

    data.close()
    time.sleep(random.randint(1, 15))

    if next_page is not None:
        get_jobs(next_page.get('href'))


def post_to_backend():
    login_path = '/api/auth/login/'
    post_path = '/api/jobs/update/'
    username = os.environ.get('USER')
    password = os.environ.get('PASSWORD')
    auth = {}
    resp = requests.post(BACKEND_DOMAIN + login_path, json={
        'username': username,
        'password': password})
    data = resp.json()
    if 'key' in data:
        auth['Authorization'] = f'Token {data["key"]}'
        resp.close()
        resp = requests.post(
            BACKEND_DOMAIN + post_path, headers=auth, json=jobs)
        print(resp.status_code)
        print(resp.json())
        print()


if __name__ == '__main__':
    print(time.strftime("Starting at %A, %d. %B %Y %I:%M:%S %p"))
    print('Scraping pages...')
    for search in searches:
        get_jobs(KSL_URL + search)
    print('Posting to backend...')
    post_to_backend()
    print()
