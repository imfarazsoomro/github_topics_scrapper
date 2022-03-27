# Top repositories of GitHub Topics Scraping

import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd
import os

topics_url = 'https://github.com/topics'
response = req.get(topics_url)
page_contents = response.text
# print('status', response.status_code)

#with open('web_page.html', 'w') as w:
#    w.write(response.text)

doc = bs(page_contents, 'html.parser')

topic_title = doc.find_all('p', {'class': 'Link--primary'})
titles = []
for title in topic_title:
    titles.append(title.text.strip())
# print('titles', len(titles), titles)

topic_description = doc.find_all('p', {'class': 'f5'})
descriptions = []
for desc in topic_description:
    descriptions.append(desc.text.strip())
# print('descriptions', len(descriptions) ,descriptions)

topic_url = doc.find_all('a', {'class': 'flex-column'})
base_url = 'https://github.com'
links = []
for link in topic_url:
    links.append(base_url + link.get('href'))
# print('links', len(links),  links)

topics_dict = {
    'Title': titles, 'Description': descriptions, 'URL': links
}
# print(topics_dict)
df = pd.DataFrame(topics_dict)
# print(df)
df.to_csv('github_topics.csv')

####################################### Scrapping each topic page #######################################

# topic_page_url = 'https://github.com/topics/algorithm'
for link in links:
    topic_page_url = link
    topic_page_response = req.get(topic_page_url)
    # print('status', topic_page_response.status_code)

    doc = bs(topic_page_response.text, 'html.parser')

    topic = doc.find_all('h1', {'class': 'h1'})

    users = doc.find_all('a', {'data-ga-click': 'Explore, go to repository owner, location:explore feed'})

    name = users[0]
    print(name)

    username = []
    for user in users:
        username.append(user.text.strip())
    print('username', len(username))

    user_profile = []
    for profile in users:
        user_profile.append(base_url + profile.get('href'))
    # print('user_profile', len(user_profile))

    repository = doc.find_all('a', {'class': 'text-bold wb-break-word'})
    # print(len(repository))

    user_git_repo = []
    for repo in repository:
        user_git_repo.append(base_url + repo.get('href'))
    # print('user_git_repo',len(user_git_repo))

    repo_stars = doc.find_all('span', {'id': 'repo-stars-counter-star'})
    user_repo_stars = []
    for stars in repo_stars:
        user_repo_stars.append(stars.text + ' Stars')
    # print('user_repo_stars',len(user_repo_stars))

    topic_repos_dict = {
        'Username': username, 'User Profile': user_profile, 'Git Repo': user_git_repo, 'Repo Stars': user_repo_stars
    }

    topic_df = pd.DataFrame(topic_repos_dict, index=None)
    print(topic_df)

    # path = os.makedirs('data', exist_ok=True)
    # topic_df.to_csv('path/{}.csv'.format('topic_repo'))
