from abc import ABC

from scrapy.utils.project import get_project_settings
from scrapy.http import FormRequest
from giteaBot.items import UserItem
from giteaBot.items import RepoItem
import scrapy
import datetime

class ReadmeSpider(scrapy.Spider, ABC):
    name = "readme"
    settings = get_project_settings()
    base_url = settings.get('BASE_URL')
    login_url = base_url + '/user/login'
    users_url = base_url + '/explore/users'

    def start_requests(self):
        return [
            FormRequest(self.login_url, formdata={"user_name": self.settings.get('BOT_USER_NAME'),
                                                  "password": self.settings.get('BOT_PASSWORD')}, callback=self.go_to_users)]

    def go_to_users(self, response):
        if response.css('div.right.stackable.menu a.item svg.svg.octicon-sign-in').extract_first():
           self.logger.error('Cant log in to ' + self.base_url + '! Check credentials.')
        else:
            yield scrapy.Request(self.users_url, callback=self.process_users)

    def process_users(self, response):
        user_list = response.css('div.ui.user.list div.item')
        user_item = UserItem()

        for user in user_list:
            user_item['user_name'] = user.css('span.header a::text').extract_first()
            user_item['repos_link'] = self.base_url + user.css('span.header a::attr(href)').extract_first().lower()
            user_item['email'] = user.css('div.description a[rel="nofollow"]::text').extract_first().lower()
            user_item['name'] = user.css('span.header::text').extract_first().strip()

            yield user_item
            request = scrapy.Request(user_item['repos_link'], dont_filter=True, callback=self.process_repos)
            request.meta['item'] = user_item
            yield request

    def process_repos(self, response):
        repo_list = response.css('div.ui.repository.list div.item')

        for repo in repo_list:
            # if repo is forked one, ignore it
            if repo.css('svg.svg.octicon-repo-forked').extract_first():
                 continue
            repo_item = RepoItem()
            repo_item['user_name'] = response.css('span.username::text').extract_first().strip()
            repo_item['repo_link'] = self.base_url + repo.css('div.ui.header a::attr(href)').extract_first().strip()
            request = scrapy.Request(repo_item['repo_link'], dont_filter=True, callback=self.process_repo)
            request.meta['item'] = repo_item
            yield request

        pagination_buttons = response.css('div.page.buttons div.pagination.menu a.item.navigation:not(.disabled)')
        next_button = None

        for button in pagination_buttons:
            if button.css('i.icon.right.arrow'):
                next_button = button
                break

        # if pagination go to next page button is not disabled, make request to it
        if next_button is not None:
            yield scrapy.Request(self.base_url + next_button.css('::attr(href)').extract_first().strip(), callback=self.process_repos)

    def process_repo(self, response):
        file_list = response.css('table#repo-files-table tr td.name')
        has_readme = 0
        repo_item = response.meta['item']
        readme_link = None

        for file in file_list:
            if file.css('a::text').extract_first().strip().lower().find('readme') != -1:
                has_readme = 1
                readme_link = file.css('a::attr(href)').extract_first()
                break

        repo_item['has_readme'] = has_readme
        repo_item['last_checked'] = datetime.datetime.now()

        if has_readme and readme_link is not None:
            request = scrapy.Request(self.base_url + readme_link, dont_filter=True, callback=self.process_readme)
            request.meta['item'] = repo_item
            yield request
        else:
            repo_item['is_readme_empty'] = -1
            yield repo_item



    def process_readme(self, response):
        repo_item = response.meta['item']
        if response.css('div.file-info-entry').extract_first():
            repo_item['is_readme_empty'] = 0
        else:
            repo_item['is_readme_empty'] = 1
        yield repo_item

