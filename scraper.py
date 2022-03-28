# Top repositories of GitHub Topics Scraping

import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd
import os

topics_url = 'https://github.com/topics'
response = req.get(topics_url)
page_contents = response.text
# print('status', response.status_code)

# download and create an ofline copy of the page
# with open('web_page.html', 'w') as w:
#     w.write(response.text)

doc = bs(page_contents, 'html.parser')

topic_title = doc.find_all('p', {'class': 'Link--primary'})
titles = []
for title in topic_title:
    titles.append(title.text.strip())
# print('titles', len(titles))

topic_description = doc.find_all('p', {'class': 'f5'})
descriptions = []
for desc in topic_description:
    descriptions.append(desc.text.strip())
# print('descriptions', len(descriptions))

topic_url = doc.find_all('a', {'class': 'flex-column'})
base_url = 'https://github.com'
links = []
for link in topic_url:
    links.append(base_url + link.get('href'))
# print('links', len(links))

topics_dict = {
    'Title': titles, 'Description': descriptions, 'URL': links
}
# print(topics_dict)
df = pd.DataFrame(topics_dict)
# print(df)
df.to_csv('/home/farazsoomro/Scraper/github_topics.csv')

####################################### Scrapping each topic page #######################################

path = '/home/farazsoomro/Scraper'
os.chdir(path)
os.makedirs('Topic Repos', exist_ok=True)

for topic_page_url in links:
    page_response = req.get(topic_page_url)
    doc = bs(page_response.text, 'html.parser')

    title = doc.find_all('h1', {'class': 'h1'})
    # print(title)
    repo_user_tags = doc.find_all('a', {'data-ga-click': 'Explore, go to repository owner, location:explore feed'})
    username = []
    for user in repo_user_tags:
        username.append(user.text.strip())
    # print(len(username))
    
    user_profile = []
    for profile in repo_user_tags:
        user_profile.append(base_url + profile.get('href'))
    # print(len(user_profile))

    repo_tags = doc.find_all('a', {'class': 'text-bold wb-break-word'})
    user_repo_url = []
    for repo in repo_tags:
        user_repo_url.append(base_url + repo.get('href'))
    # print(len(repo_tags))

    repo_stars = doc.find_all('span', {'id': 'repo-stars-counter-star'})
    user_repo_stars = []
    for stars in repo_stars:
        user_repo_stars.append(stars.text + ' Stars')
    # print(len(repo_stars))

    repo_info_dict = {
        'Username': username, 'User Profile': user_profile, 'User Repo URL': user_repo_url, 'Repo Stars': user_repo_stars
    }

    topic_repos_df = pd.DataFrame(repo_info_dict, index=None)
    # print(len(repo_info_dict))
    topic_repos_df = pd.DataFrame(repo_info_dict, index=None)
    for fname in title:
        topic_repos_df.to_csv('Topic Repos/{}.csv'.format(fname.text.strip()))