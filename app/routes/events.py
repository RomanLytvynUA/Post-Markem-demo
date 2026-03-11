from flask import render_template, request, Blueprint
import ui_db

events_bp = Blueprint('events_bp', __name__)

@events_bp.route('/')
def get_events():
    return render_template('/views/events.html', competitions=ui_db.list_competitions())

@events_bp.route('/get/<int:comp_id>')
def get_event_details(comp_id):
    categories = ui_db.list_categories(comp_id)
    return render_template("event_components/categories.html", comp_id=comp_id, data=[
        {**category, "rounds": ui_db.list_rounds(category["id"])} 
        for category in categories
    ])