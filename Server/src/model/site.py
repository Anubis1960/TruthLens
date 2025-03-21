class Site:
    def __init__(self, domain: str, articles: list[dict], stats: dict):
        self.domain = domain
        self.articles = articles
        self.stats = stats

    def to_dict(self):
        return {
            'domain': self.domain,
            'articles': self.articles,
            'stats': self.stats,
        }

    @staticmethod
    def from_dict(data: dict) -> "Site":
        return Site(data['domain'], data['articles'], data.get('stats', {}))
