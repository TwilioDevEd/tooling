from lxml import html
import requests

page = requests.get('https://www.twilio.com/docs/tutorials')
tree = html.fromstring(page.content)
page_group_tags = tree.xpath('//div[@class="page-group"]')

for page_group_tag in page_group_tags:
    title = page_group_tag.xpath('h2/a/text()')
    languages = page_group_tag.xpath('ul/li/a/text()')

    print
    print title[0].strip()
    for language in languages:
        print "%s" % language.strip()
