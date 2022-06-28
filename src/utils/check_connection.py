from flask import jsonify
def check_connection():
    res = jsonify({
        'message': 'Connect successfully'
    })
    res.status_code = 200

    return res
