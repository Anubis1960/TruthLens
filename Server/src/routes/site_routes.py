# from http import HTTPStatus
# from flask import jsonify, request, Blueprint

# from ..services.site_service import *

# SITE_URL = '/api/sites'

# #
# #	BluePrint setup
# #
# site_bp = Blueprint('sites', __name__, url_prefix=SITE_URL)

# #
# #	Routes
# #
# @site_bp.route('', methods=['POST'])
# def verify_link() -> jsonify:
# 	data = request.get_json()

# 	# check data
# 	if data is None:
# 		return jsonify({'error': 'Bad data.'}), HTTPStatus.BAD_REQUEST

# 	# retrieve link from json
# 	url = data['link']

# 	if url is None:
# 		return jsonify({'error': 'No url'}), HTTPStatus.BAD_REQUEST

# 	# response
# 	response = validate_link(url)

# 	return jsonify(response), HTTPStatus.OK


