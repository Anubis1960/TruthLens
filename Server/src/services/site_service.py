import json
from ..model.site import Site
from ..dto.site_dto import SiteDTO
from ..util.scrape import *
from ..util.news.news_detect import *
from firebase_admin import db

#
#	Path for sites
#
DB_REF = 'fake-news/websites'
REF = db.reference(DB_REF)

#
#	CRUD operations
#
def validate_link(url: str) -> dict[str, str] | None:
	print(f'Service -> received link:{url}')

	try:
		# fetch link domain
		domain = extract_domain(url)
		print(f'Extracted domain -> {domain}')

		# fetch link text and title
		text = extract_text(get_soup(url))
		title = extract_title(get_soup(url))
		print(title)
		predicted_text = predict(title, text)
		print(f'Predicted text -> {predicted_text}')

		# fetch db data based on domain
		fetched_data = REF.order_by_child('domain').equal_to(domain).get()

		if fetched_data:
			print('Data exists')
			# data exists
			return None


		else:
			print('Data doesn\'t exist')
			# no data
			return None

	except Exception as e:
		return {'error': str(e)}