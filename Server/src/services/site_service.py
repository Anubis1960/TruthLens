import json
from ..model.site import Site
from ..dto.site_dto import SiteDTO
from firebase_admin import db

#
#	Path for sites
#
DB_REF = 'fake-news/websites'
REF = db.reference(DB_REF)

#
#	CRUD operations
#
# def create_site(data: Site) -> dict:
# 	print(f'SERVICE -> create_site: {data}')
# 	try:
# 		# Check if the domain already exists
# 		# existing_sites = REF.order_by_child('domain').equal_to(data.domain).get()
# 		#
# 		# if existing_sites:
# 		# 	# Update existing site's articles list and stats
# 		# 	site_id, existing_data = next(iter(existing_sites.items()))  # Get first match
# 		#
# 		# 	updated_articles = existing_data.get('articles', []) + data.articles  # Append new articles
# 		#
# 		# 	# Retrieve and update stats
# 		# 	updated_stats = existing_data.get('stats',
# 		# 									  {"missinformation": 0, "goodinformation": 0, "neutral": 0, "unknown": 0})
# 		#
# 		# 	# Iterate through new articles to update stats
# 		# 	for article in data.articles:
# 		# 		for url, category in article.items():  # {"www.example.com": "missinformation"}
# 		# 			if category in updated_stats:
# 		# 				updated_stats[category] += 1  # Increase count
# 		#
# 		# 	# Update in DB
# 		# 	REF.child(site_id).update({
# 		# 		'articles': updated_articles,
# 		# 		'stats': updated_stats
# 		# 	})
# 		#
# 		# 	return SiteDTO(site_id, data.domain, updated_articles, updated_stats).to_dict()
# 		#
# 		# else:
# 		# If no site exists, initialize stats
# 		# default_stats = {"missinformation": 0, "goodinformation": 0, "neutral": 0, "unknown": 0}
# 		#
# 		# # Count occurrences in the initial request
# 		# for article in data.articles:
# 		# 	for url, category in article.items():
# 		# 		if category in default_stats:
# 		# 			default_stats[category] += 1  # Increase count
# 		#
# 		# # Create new entry
# 		# data.stats = default_stats
# 		default_stats = {"missinformation": 0, "goodinformation": 0, "neutral": 0, "unknown": 0}
#
# 		# Convert articles list to a dictionary where URL is the key
# 		articles_dict = {list(article.keys())[0]: list(article.values())[0] for article in data.articles}
#
# 		# Count occurrences in the initial request
# 		for article in data.articles:
# 			for url, category in article.items():
# 				if category in default_stats:
# 					default_stats[category] += 1  # Increase count
#
# 		data_dict = {
# 			"domain": data.domain,
# 			"articles": articles_dict,  # Articles are now a dictionary with URL as the key
# 			"stats": default_stats,
# 		}
#
# 		print("Before saving:", data_dict)
#
# 		site_ref = REF.push(data_dict)  # Save to Firebase
# 		print("After saving")
#
# 		return SiteDTO(site_ref.key, data.domain, data.articles, default_stats).to_dict()
#
#
# 	except Exception as e:
# 		return {'error': str(e)}

def create_site(domain: str, articles: list(dict)) -> dict:

	try:
		# fetch domain
		existing_sites = REF.order_by_child('domain').equal_to(domain).get()

		# check if exists
		if existing_sites:
			print("TODO")
		else:
			print("TODO")

	except Exception as e:
		print(f"Error saving site: {str(e)}")
		return {'error': str(e)}
