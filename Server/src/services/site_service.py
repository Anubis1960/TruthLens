from ..util.database import db
from ..util.news.news_detect import NEWS_CLASS_MAPPING
from ..util.scrape import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "..", "temp")

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

SITES_COLLECTION = "sites"


def validate_link(url: str) -> dict:
    try:
        # Fetch link domain
        domain = extract_domain(url)

        # Fetch link text and title
        soup = get_soup(url)
        text = extract_text(soup)
        title = extract_title(soup)

        # Predict category
        predicted_text = predict_text(title, text)

        # Search domain in db
        domain_ref = db.collection(SITES_COLLECTION).document(domain).get()

        # Check domain existence
        if domain_ref.exists:
            site_data = domain_ref.to_dict()
            articles = site_data.get('articles', {})

            # check for duplicate link
            if url in articles:
                return {"verdict": predicted_text}

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
        return {"verdict": predicted_text}

    except Exception as e:
        # Log the error and return an error message
        print(f"Error validating link: {e}")
        return {"error": f"Failed to validate link: {str(e)}"}


def validate_video_link(link: str) -> dict:
    try:
        # Random generated file name
        file_name = os.urandom(8).hex()

        # Saving path
        out_path = os.path.join(TEMP_DIR, file_name)
        title = fetch_video_from_streaming_service(link, out_path)

        # Retrieve random captures
        total_frames = get_total_frames(out_path + ".mp4")
        frames = np.random.randint(0, total_frames, 5)

        prediction = analyze_frames(f"{out_path}.mp4", frames)
        if prediction[0] > 0.5:
            prediction = 'AI Generated'

        else:
            prediction = 'Real'

        text = transcript(link)
        verdict = predict_text(title, text)

        os.remove(f"{out_path}.mp4")

        print(verdict)
        return {"audio": verdict, "video": prediction}

    except Exception as e:
        # Log the error and return an error message
        print(f"Error validating video link: {e}")
        return {"error": f"Failed to validate video link: {str(e)}"}


def validate_image_link(link: str) -> dict:
    try:
        img = fetch_image(link)
        if img is None:
            return {"error": "Failed to fetch image."}

        prediction = predict_image(img)
        if prediction > 0.7:
            prediction = 'AI Generated'

        else:
            prediction = 'Real'

        return {"prediction": prediction}

    except Exception as e:
        # Log the error and return an error message
        print(f"Error validating image link: {e}")
        return {"error": f"Failed to validate image link: {str(e)}"}


def get_site_stats() -> list[dict]:
    try:
        # Fetch all sites
        sites = db.collection(SITES_COLLECTION).stream()

        # Extract 'stats' and 'domain' fields from each document
        site_stats = []
        for site in sites:
            site_data = site.to_dict()
            stats = site_data.get('stats')
            domain = site_data.get('domain')

            # Include only if both 'stats' and 'domain' are present
            if stats is not None and domain is not None:
                site_stats.append({'stats': stats, 'domain': domain})

        # Return the list of site stats
        return site_stats

    except Exception as e:
        # Log the error and return an empty list
        print(f"Error fetching site stats: {e}")
        return []


def get_articles_by_domain(domain: str) -> list:
    try:
        # Fetch the domain document
        domain_ref = db.collection(SITES_COLLECTION).document(domain).get()

        # Check if the domain document exists
        if domain_ref.exists:
            site_data = domain_ref.to_dict()
            articles = site_data.get('articles', {})

            # Convert the articles dictionary into a list of article data
            if isinstance(articles, dict):
                return list(articles.items())
            else:
                print(f"Unexpected format for 'articles' field in domain '{domain}'")
                return []

        # If the domain does not exist, return an empty list
        return []

    except Exception as e:
        # Log the error and return an error message
        print(f"Error fetching articles for domain '{domain}': {e}")
        return []


def get_all_domains() -> list:
    try:
        # Fetch all sites
        sites = list(db.collection(SITES_COLLECTION).stream())
        # Extract domain from each DocumentSnapshot
        domains = [site.id for site in sites]

        # Return the list of domains
        return domains

    except Exception as e:
        # Log the error and return an error message
        print(f"Error fetching all domains: {e}")
        return []


def get_all_sites() -> list[dict]:
    try:
        # Fetch all sites
        sites = list(db.collection(SITES_COLLECTION).stream())
        # Extract data from each DocumentSnapshot and convert to a list of dictionaries
        sites_data = [site.to_dict() for site in sites]

        # Return the list of site data
        return sites_data

    except Exception as e:
        # Log the error and return an error message
        print(f"Error fetching all sites: {e}")
        return []
