from flask import render_template, Blueprint, abort
import ui_db
from .. import utilities as utl

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/display/<int:round_id>')
def get_round(round_id):
    round_data = ui_db.rounds.get_round(round_id)
    if not round_data:
        abort(404) 

    cat_id = round_data.get('category_id')
    category = ui_db.categories.get_category(cat_id)
    rounds = ui_db.rounds.list_rounds(cat_id)
    competition = ui_db.competitions.get_competition(category['competition_id'])

    competitors = ui_db.entries.get_round_entries(round_id)
    for comp in competitors:
        p2 = f" & {comp.get('p2_name')}" if comp.get('p2_name') else ""
        comp['name'] = f"{comp.get('p1_name')}{p2}"

    def safe_place_sort(comp):
        try:
            return int(str(comp.get('place', '999')).split()[0])
        except (ValueError, AttributeError):
            return 999
            
    competitors.sort(key=safe_place_sort)
 
    adjudicators = ui_db.adjudicators.get_adjudicators_by_round(round_id)

    raw_marks = ui_db.rounds.get_marks(round_id)
    marks = {}
    if raw_marks:
        for dance, df in raw_marks.items():
            translated_dance = utl.translate_dance(dance) 
            df.index = df.index.astype(int) 
            marks[translated_dance] = df.reset_index(names='number').to_dict('records')

    data_missing = False
    if not raw_marks or len(adjudicators) < 0 or len(competitors) < 0 :
        data_missing = True

    return render_template(
        '/views/round.html', 
        selected_round=round_id, 

        adjudicators=adjudicators, 
        competitors=competitors,
        marks=marks, 

        data_missing=data_missing,

        rounds=rounds, 
        round_data=round_data, 
        category=category,
        competition=competition
    )

@categories_bp.route("/analyse/<int:round_id>", methods=["GET"])
def get_round_analysis(round_id):
    adjudicators = ui_db.adjudicators.get_adjudicators_by_round(round_id)
    competitors = ui_db.entries.get_round_entries(round_id)

    analytics_data = utl.get_analytics_data(round_id)

    accuracy_table_data, bias_data, voting_blocs = utl.format_analysis_display_data(analytics_data, competitors, adjudicators)

    return render_template(
        'report_components/report.html',
        competitors=competitors,
        adjudicators=adjudicators,
        accuracy_table_data=accuracy_table_data,
        bias_data=bias_data,
        voting_blocs=voting_blocs,
        include_header=False)