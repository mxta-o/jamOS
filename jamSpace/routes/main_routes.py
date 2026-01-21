from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('pages/home.html')

@main_bp.route('/apps')
def apps():
    return render_template('pages/apps.html')

@main_bp.route('/about-me')
def about_me():
    return render_template('pages/about.html')

@main_bp.route('/roadmap')
def roadmap():
    return render_template('pages/roadmap.html')
