from pygithub3 import Github
import grequests

filepath = 'https://raw.githubusercontent.com/%s/master/README.md'
test = lambda repo_name, content: repo_name in content

gh = Github()
repos = gh.repos.list_by_org('TwilioDevEd').all()
reqs = []
repo_by_url = {}

for repo in repos:
    file_url = filepath % repo.full_name
    reqs.append(grequests.get(file_url))
    repo_by_url[file_url] = repo

def exception_handler(request, exception):
    print "%s failed with %s" % (response.url, response.status_code)

responses = grequests.map(reqs, size=30, exception_handler=exception_handler)

for response in responses:
    if response.status_code is not 200:
        # print "%s failed with %s" % (response.url, response.status_code)
        continue
    if test('San Francisco', response.content):
        print "%s" % response.url
