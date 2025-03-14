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
@site_bp.route('', methods=['POST'])
def verify_site() -> jsonify:
	site_data = request.get_json()
	print(site_data)

	try:
		domain = site_data['domain']
		articles = site_data['articles']
		stats = site_data['stats']

		# response
		response = create_site(domain, articles, stats)
		print(f'Response: {response}')

		if 'error' in response:
			return jsonify(response), HTTPStatus.BAD_REQUEST

		return jsonify(response), HTTPStatus.CREATED

	except Exception as e:
		return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST

