from flask_restful import reqparse
from flask_restful import Resource
import werkzeug
# from flasgger import swag_from

from ..common.base_controller import BaseResource
from src.services import RecordService
from src.utils.check_connection import *

class RecordListResource(BaseResource):
    def get(self):
        return check_connection()

    def post(self, user_data):
        """Upload record

        Args:
            user_data (dict): contain user_id get by token

        Returns:
            Status Upload
        """
        parser = reqparse.RequestParser()
        parser.add_argument('record_file', type=werkzeug.datastructures.FileStorage, required=True, location='files')
        args = parser.parse_args()
        record_service = RecordService()

        return record_service.upload_record(user_id=user_data['user_id'], record_file=args['record_file'])

class RecordProcessingResource(BaseResource):
    # def get(self):
    #     return check_connection()
    def get(self, user_data):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument('task_id', type=str, required=True, location='args')
        args = parser.parse_args()
        record_service = RecordService()

        return record_service.get_processing_info(task_id=args['task_id'])


    def post(self, user_data):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument('record_id', type=str, required=True)
        args = parser.parse_args()
        record_service = RecordService()

        return record_service.request_processing(user_id=user_data['user_id'], record_id=args['record_id'])

class RecordTranscriptResource(BaseResource):
    def get(self, user_data):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument('record_id', type=str, required=True, location='args')
        args = parser.parse_args()
        record_service = RecordService()

        return record_service.get_full_transcript(user_id=user_data['user_id'], record_id=args['record_id'])
