from scrapy import Item, Field


class UserItem(Item):
    def class_name(self):
        return type(self).__name__

    user_name = Field(serializer=str)
    repos_link = Field(serializer=str)
    email = Field(serializer=str)
    name = Field(serializer=str)
    pass


class RepoItem(Item):
    def class_name(self):
        return type(self).__name__

    user_name = Field(serializer=str)
    repo_link = Field(serializer=str)
    has_readme = Field(serializer=bool)
    is_readme_empty = Field(serializer=bool)
    last_checked = Field(serializer=str)
    pass
