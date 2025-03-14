class SiteDTO:
	def __init__(self, id: str, domain: str, articles: list[dict], stats: dict):
		self.id = id
		self.domain = domain
		self.articles = articles
		self.stats = stats

	def to_dict(self):
		return {
			'id': self.id,
			'domain': self.domain,
			'articles': self.articles,
			'stats': self.stats,
		}

	@staticmethod
	def from_dict(data: dict):
		return SiteDTO(data['id'], data['domain'], data['articles'], data['stats'])