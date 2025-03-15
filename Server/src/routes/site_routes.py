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
@site_bp.route('/video-link', methods=['POST'])
def verify_link() -> jsonify:
	data = request.get_json()
	print(data)

	try:
		# retrieve link from json
		url = data['link']

		# response
		response = validate_link(url)

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

