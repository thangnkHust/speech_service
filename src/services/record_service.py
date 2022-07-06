import json
import os
from flask import current_app, jsonify
from nanoid import generate
from celery import states

from src.daos import UserDAO, RecordDAO
from task.workers import speech_recognition, get_status
from src.utils.constants import *

class RecordService:
    def __init__(self) -> None:
        self.user_dao = UserDAO()
        self.record_dao = RecordDAO()


    def upload_record(self, user_id: int, record_file):
        user = self.user_dao.get_by_id(user_id)

        if not user:
            return {
                'message': 'User not fond!!!'
            }, 404

        folder_path = current_app.config['RECORD_FOLDER']
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        try:
            file_ext = os.path.splitext(record_file.filename)[1]
            filename_random = generate() + file_ext
            path_save = os.path.join(folder_path, filename_random)
            # save file to server
            record_file.save(path_save)
            # save to database
            record_id = self.record_dao.create_record(id=generate(), user=user, record_path=path_save)

            res = jsonify({
                'message': 'Upload record successfully!!!',
                'record_id': record_id
            })
            res.status_code = 201

            return res
        except Exception as e:
            # When exception => delete file
            os.remove(path_save)
            raise e


    def request_processing(self, user_id: int, record_id: str):
        record = self.record_dao.get_by_record_id(record_id=record_id, user_id=user_id)
        if not record:
            res = jsonify({
                'message': 'Record not found!!!'
            })
            res.status_code = 404
        else:
            task = get_status(task_id=record_id)

            if task.status == states.PENDING or task.status == states.FAILURE or task.status == states.REVOKED:
                speech_recognition.apply_async((record.record_path, user_id, record_id), task_id=record_id)
                self.record_dao.update_record(record_id=record_id, user_id=user_id, status=STARTED)

            res = jsonify({
                'task_id': task.id,
                'status': task.status
            })
            res.status_code = 202

        return res


    def get_processing_info(self, task_id: str):
        try:
            task = get_status(task_id=task_id)
            switcher = {
                states.PENDING: 'Đang chờ xử lý',
                states.STARTED: 'Đang xử lý',
                states.SUCCESS: 'Đã xử lý xong',
                states.FAILURE: 'Lỗi xử lý',
                states.REVOKED: 'Đã hủy xử lý'
            }
            res = jsonify({
                'status': task.status,
                'status_message': switcher[task.status]
            })
            res.status_code = 200
        except Exception as e:
            res = jsonify({'message': 'Internal server error!!!'})
            res.status_code = 500
            raise e
        finally:
            return res

    def get_full_transcript(self, user_id: int, record_id: str):
        record = self.record_dao.get_by_record_id(record_id=record_id, user_id=user_id)
        if not record:
            res = jsonify({
                'message': 'Record not found!!!'
            })
            res.status_code = 404
        if not record.result_path:
            return None, 200
        try:
            with open(record.result_path, 'r') as f:
                result_data = json.load(f)
            return result_data
        except Exception as e:
            raise e

    def get_all_record(self):
        records = self.record_dao.get_all()

        return [r.serialize() for r in records]

    def delete_record(self, record_id):
        record = self.record_dao.get_by_id(record_id=record_id)

        if not record:
            return {
                'message': 'Bad request!!!'
            }, 400

        if self.record_dao.delete_record(record=record):
            return {
                'message': 'Delete record successfully'
            }, 200

        return {
            'message': 'Server Internal Error!!!'
        }, 500

    def get_full_transcript_by_record_id(self, record_id: str) -> dict:
        record = self.record_dao.get_by_id(record_id=record_id)

        if not record:
            res = jsonify({
                'message': 'Record not found!!!'
            })
            res.status_code = 404
            return res

        if not record.result_path:
            return None, 200

        try:
            with open(record.result_path, 'r') as f:
                result_data = json.load(f)
            return result_data
        except Exception as e:
            raise e
