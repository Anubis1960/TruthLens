from http import HTTPStatus
from flask import request, Blueprint
from ..services.upload_service import *

UPLOAD_URL = '/api/upload'

upload_bp = Blueprint('upload', __name__, url_prefix=UPLOAD_URL)

@upload_bp.route('/image', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return {'error': 'No files sent'}, HTTPStatus.BAD_REQUEST

    files = request.files.getlist('files')  

    for file in files:
        res = verify_img_file(file)
        if 'error' in res:
            return res, HTTPStatus.BAD_REQUEST

        return res, HTTPStatus.OK

    return {'message': 'Files uploaded successfully!'}, HTTPStatus.OK
