from flask_restful import reqparse
from flasgger import swag_from
from flask import send_file

from ..common.base_controller import AdminResource
from src.services import RecordService

class AdminRecordListResource(AdminResource):
    def get(self):
        record_service = RecordService()

        return record_service.get_all_record()
