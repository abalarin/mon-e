from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user

from MonE import db

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.app_errorhandler(403)
@main.app_errorhandler(404)
@main.app_errorhandler(405)
@main.app_errorhandler(500)
def error_404(error):
    return render_template('errors/404.html', e=error)
