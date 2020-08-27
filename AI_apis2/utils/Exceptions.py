class PlatformAbilityError(Exception):
    def __init__(self, platform_title, ability_title):
        self.platform_title = platform_title
        self.ability_title = ability_title

    def __str__(self):
        return f"{self.platform_title}没有{self.ability_title}能力！"


class AssembleHeaderException(Exception):
    def __init__(self, requset_url):
        self.requset_url = requset_url

    def __str__(self):
        return f"invalid request url: {self.requset_url}"

