import json
from itemadapter import ItemAdapter
from sqlite3 import dbapi2 as sqlite


class UserWriterPipeline:
    def __init__(self):
        self.connection = sqlite.connect('./database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users ' \
                            '(id INTEGER PRIMARY KEY, user_name VARCHAR(80), repos_link VARCHAR(80), email VARCHAR(80), name VARCHAR(80))')

    def process_item(self, item, spider):
        if item.class_name() != 'UserItem':
            return item

        self.cursor.execute("SELECT * FROM users where user_name=?", [item['user_name']])
        result = self.cursor.fetchone()
        if result:
            self.cursor.execute(
                "UPDATE users SET repos_link=?, email=?, name=? WHERE user_name =?",
                [item['repos_link'],
                item['email'],
                item['name'],
                item['user_name']]
            )
        else:
            self.cursor.execute(
                "INSERT INTO users (user_name, repos_link, email, name) VALUES (?, ?, ?, ?)",
                [item['user_name'],
                 item['repos_link'],
                 item['email'],
                 item['name']]
            )

        self.connection.commit()
        return item


class RepoWriterPipeline:
    def __init__(self):
        self.connection = sqlite.connect('./database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS repos ' \
                            '(id INTEGER PRIMARY KEY, user_name VARCHAR(80), repo_link VARCHAR(80), has_readme INTEGER, is_readme_empty INTEGER, last_checked TEXT)')

    def process_item(self, item, spider):
        if item.class_name() != 'RepoItem':
            return item
        self.cursor.execute("SELECT * FROM repos where repo_link=?", [item['repo_link']])
        result = self.cursor.fetchone()
        if result:
            self.cursor.execute(
                "UPDATE repos SET has_readme=?, is_readme_empty=?, last_checked=? WHERE repo_link =?",
                [item['has_readme'],
                 item['is_readme_empty'],
                 item['last_checked'],
                 item['repo_link']]
            )
        else:
            self.cursor.execute(
                "INSERT INTO repos (user_name, repo_link, has_readme, is_readme_empty, last_checked) VALUES (?, ?, ?, ?, ?)",
                [item['user_name'],
                 item['repo_link'],
                 item['has_readme'],
                 item['is_readme_empty'],
                 item['last_checked']]
            )

        self.connection.commit()
        return item
