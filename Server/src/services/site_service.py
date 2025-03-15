# import json
# from ..model.site import Site
# from ..dto.site_dto import SiteDTO
# from ..util.scrape import *
# from ..util.news.news_detect import *
# from firebase_admin import db

# #
# #	Path for sites
# #
# DB_REF = 'fake-news/websites'
# REF = db.reference(DB_REF)

# #
# #	CRUD operations
# #
# def validate_link(url: str) -> dict[str, str]:
#     print(f'Service -> received link:{url}')
#     try:
#         # Fetch link domain
#         domain = extract_domain(url)
#         print(f'Extracted domain -> {domain}')

#         # Fetch link text and title
#         soup = get_soup(url)
#         text = extract_text(soup)
#         title = extract_title(soup)
#         print(title)

#         # Predict category
#         predicted_text = predict(title, text)
#         print(f'Predicted text -> {predicted_text}')

#         # Return result as a dictionary
#         return {"domain": domain, "title": title, "text": text, "prediction": predicted_text}

#     except Exception as e:
#         # Log the error and return an error message
#         print(f"Error validating link: {e}")
#         return {"error": f"Failed to validate link: {str(e)}"}