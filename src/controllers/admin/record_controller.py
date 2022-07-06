from flask_restful import reqparse
from flasgger import swag_from
from flask import send_file
import werkzeug

from ..common.base_controller import AdminResource
from src.services import RecordService

class AdminRecordListResource(AdminResource):
    def get(self):
        record_service = RecordService()

        return record_service.get_all_record()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('record_file', type=werkzeug.datastructures.FileStorage, required=True, location='files')
        parser.add_argument('user_id', type=str, required=True)
        args = parser.parse_args()
        record_service = RecordService()

        return record_service.upload_record(user_id=args['user_id'], record_file=args['record_file'])


class AdminRecordResource(AdminResource):
    def get(self, record_id):
        """Get full transcript of record

        Args:
            record_id (str): id of record

        Returns:
            full_transcript(json)
        """
        record_service = RecordService()

        return record_service.get_full_transcript_by_record_id(record_id=record_id)

    def delete(self, record_id):
        record_service = RecordService()

        return record_service.delete_record(record_id=record_id)
