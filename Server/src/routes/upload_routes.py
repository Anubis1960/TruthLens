from http import HTTPStatus
from flask import request, Blueprint
import cv2
import numpy as np
import io

UPLOAD_URL = '/api/upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

upload_bp = Blueprint('upload', __name__, url_prefix=UPLOAD_URL)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/image', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return {'error': 'Niciun fișier trimis!'}, HTTPStatus.BAD_REQUEST

    files = request.files.getlist('files')  

    for file in files:
        if file and allowed_file(file.filename):

            file_bytes = file.read()
            nparr = np.frombuffer(file_bytes, np.uint8)  
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  

            if image is not None:
        
                cv2.imshow(f"Imagine: {file.filename}", image)  
                cv2.waitKey(0)
                cv2.destroyAllWindows()  
            else:
                return {'error': f'Fișier invalid: {file.filename}'}, HTTPStatus.BAD_REQUEST
        else:
            return {'error': f'Fișier invalid: {file.filename}'}, HTTPStatus.BAD_REQUEST

    return {'message': '✅ Fișiere procesate!'}, HTTPStatus.OK
