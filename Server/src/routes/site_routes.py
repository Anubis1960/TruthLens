from http import HTTPStatus
from flask import jsonify, request, Blueprint

from ..services.site_service import *

SITE_URL = '/api/sites'

#
#	BluePrint setup
#
site_bp = Blueprint('sites', __name__, url_prefix=SITE_URL)

#
#	Routes
#

# Article verify
@site_bp.route('/article-link', methods=['POST'])
def verify_link() -> jsonify:
	data = request.get_json()
	print(f'Received article request: {data}')

	try:
		# retrieve link from json
		url = data['link']
		print(f'Verifying link: {url}')

		# response
		response = validate_link(url)
		print(f'Verified link response: {response}')

		if 'error' in response:
			return jsonify({'error': response['error']}), HTTPStatus.BAD_REQUEST

		return jsonify(response), HTTPStatus.OK

	except Exception as e:
		return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@site_bp.route('/video-url', methods=['GET'])
def verify_video_url() -> jsonify:
	url = request.args.get('url')

	try:
		# response
		response = validate_video_link(url)

		if 'error' in response:
			return jsonify({'error': response['error']}), HTTPStatus.BAD_REQUEST

		return jsonify(response), HTTPStatus.OK

	except Exception as e:
		return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@site_bp.route("/image-url", methods=['GET'])
def verify_image_url() -> jsonify:
	url = request.args.get('url')

	try:
		# response
		response = validate_image_link(url)

		if 'error' in response:
			return jsonify({'error': response['error']}), HTTPStatus.BAD_REQUEST

		return jsonify(response), HTTPStatus.OK

	except Exception as e:
		return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST


@site_bp.route("/stats", methods=['GET'])
def get_stats() -> jsonify:
	try:
		# response
		response = get_site_stats()
		return jsonify(response), HTTPStatus.OK

	except Exception as e:
		return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@site_bp.route("/articles", methods=['GET'])
def get_articles() -> jsonify:
	try:
		data = request.get_json()

		if 'domain' not in data:
			return jsonify({'error': 'No domain provided'}), HTTPStatus.BAD_REQUEST

		res = get_articles_by_domain(data['domain'])

		if 'error' in res:
			return jsonify({'error': res['error']}), HTTPStatus.BAD_REQUEST

		return jsonify(res), HTTPStatus.OK

	except Exception as e:
		return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

@site_bp.route("/", methods=['GET'])
def get_all_sites() -> jsonify:
	try:
		# response
		response = get_all_sites()
		return jsonify(response), HTTPStatus.OK

	except Exception as e:
		return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST