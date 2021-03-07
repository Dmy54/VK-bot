from flask import Flask, request, jsonify
from flask import render_template
import threading
from datetime import datetime
from services.service import *


application = Flask(__name__)


@application.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@application.route("/")
def hello():
    return render_template('index.html'), 200


# @application.route('/VkPosts')
# def get_post_info():
#     firstDate = request.args.get("firstDate")
#     secondDate = request.args.get("secondDate")
#     return jsonify(result=get_posts_data(datetime.date(datetime.strptime(firstDate, "%Y-%m-%d")),
#                                          datetime.date(datetime.strptime(secondDate, "%Y-%m-%d"))))



if __name__ == "__main__":
    thread = threading.Thread(target=check_messages)
    thread.start()
    application.run()