from lxml import html
import requests
from pygithub3 import Github
import os
import re

# Your github credentials
gh_password = os.environ['GH_PASSWORD']
gh_username = os.environ['GH_USERNAME']

gh_organization = 'TwilioDevEd'
gh = Github(login=gh_username, password=gh_password)

base_path = 'https://www.twilio.com'

page = requests.get('https://www.twilio.com/docs/tutorials')
tree = html.fromstring(page.content)

a_tags = tree.xpath('//div[@class="block-page_group"]/div/ul/li/a')
tutorials = map((lambda x: x.get('href')), a_tags)

for tutorial in tutorials:
  if ("masked-numbers" in tutorial) or ("workflow-automation" in tutorial):
    print "skipped" + tutorial
    continue
  if not base_path in tutorial:
    tutorial_url =  "{}{}".format(base_path, tutorial)
  else:
    tutorial_url = tutorial

  tutorial_page = requests.get(tutorial_url)
  tutorial_tree = html.fromstring(tutorial_page.content)

  repo_url = tutorial_tree.xpath('/html/body/div[4]/div/div/div[1]/div/span[2]/a[2]')[0].get('href')

  repo_search = re.search('https://github.com/TwilioDevEd/(.+)/tree/master', repo_url)
  repo_name = repo_search.group(1)

  repo = gh.repos.get(user=gh_organization, repo=repo_name)

  print "\n-----------**********--------------"
  print 'Tutorial url: ' + tutorial_url
  print 'Repo Homepage: ' + repo.homepage
  print 'Repo Url: ' + repo_url
  print 'Repo Name: ' + repo_name

  if repo.homepage == None or repo.homepage == '' or repo.homepage != tutorial_url:
    gh.repos.update(dict(homepage=tutorial_url, name=repo_name), user=gh_organization, repo=repo_name)
    print 'Changed from : ' + str(repo.homepage) + ' to: ' + tutorial_url
