import json
from ..model.site import Site
from ..dto.site_dto import SiteDTO
from ..util.scrape import *
from ..util.news.news_detect import *
from ..util.database import db
from ..util.news.news_detect import NEWS_CLASS_MAPPING

#
#	Path for sites
#
SITES_COLLECTION = "sites"

#
#	Article Validation
#
def validate_link(url: str) -> dict:
	try:
		# Fetch link domain
		domain = extract_domain(url)

		# Fetch link text and title
		soup = get_soup(url)
		text = extract_text(soup)
		title = extract_title(soup)

		# Predict category
		predicted_text = predict(title, text)

		# Search domain in db
		domain_ref = db.collection(SITES_COLLECTION).document(domain).get()
		print(domain_ref)

		# Check domain existence
		if domain_ref.exists:
			site_data = domain_ref.to_dict()
			articles = site_data.get('articles', {})

			# check for duplicate link
			if url in articles:
				return {"error": "Duplicate link."}

			stats = site_data.get('stats', {key: 0 for key in NEWS_CLASS_MAPPING.keys()})

		else:
			articles = {}
			stats = {key: 0 for key in NEWS_CLASS_MAPPING.keys()}

		# Update articles and stats
		articles[url] = predicted_text
		stats[predicted_text] = stats.get(predicted_text, 0) + 1

		# Prepare the data to be saved in the database
		site_data = {
			'domain': domain,
			'articles': articles,
			'stats': stats
		}

		# Save or update the domain in the database
		db.collection(SITES_COLLECTION).document(domain).set(site_data)

		# Return result as a dictionary
		return SiteDTO(domain, site_data['domain'], site_data['articles'], site_data['stats']).to_dict()

	except Exception as e:
		# Log the error and return an error message
		print(f"Error validating link: {e}")
		return {"error": f"Failed to validate link: {str(e)}"}