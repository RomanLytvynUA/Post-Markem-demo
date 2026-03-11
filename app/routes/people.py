from flask import render_template, Blueprint
import ui_db
from .. import utilities as utl

people_bp = Blueprint('people', __name__)


@people_bp.route('/')
def get_people():
    data = ui_db.people.get_people()

    return render_template('/views/people.html', data=data)

@people_bp.route('/<int:p_id>')
def get_person(p_id):
    person = ui_db.people.get_person(p_id)

    adjudications = ui_db.people.get_adjudication_records(p_id, score_formatter=utl.get_alignment_score_data)
    entries = ui_db.people.get_entry_records(p_id)
    
    alignment_data = utl.get_alignment_score_data(person['score'], r=2)
    
    return render_template('/views/profile.html', 
                           person_data=person, 
                           adjudications=adjudications, 
                           entries=entries,
                           alignment_data=alignment_data)

@people_bp.route("/leaderboard")
def get_leaderboard():
    raw_data = ui_db.people.get_adjudicators_leaderboard()
    data = []
    for person in raw_data:
        if not person['score']:
            continue

        person["alignment_data"] = utl.get_alignment_score_data(person.get('score', 0), 'int')

        data.append(person)

    return render_template("/views/leaderboard.html", data=data)
