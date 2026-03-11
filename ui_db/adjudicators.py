from .utilities import execute_read_one, execute_read_all

def get_adjudicator(adjudicator_id):
    return execute_read_one("SELECT * FROM adjudicators WHERE id = ?", (adjudicator_id,))

def get_adjudicators_by_round(round_id):
    query = """
        SELECT a.*, p.name, p.id AS person_id
        FROM adjudicators a
        LEFT JOIN people p ON a.people_id = p.id
        WHERE a.round_id = ? 
        ORDER BY a.letter
    """
    return execute_read_all(query, (round_id,))

def get_adjudicators_by_person(person_id):
    query = """
        SELECT * FROM adjudicators WHERE person_id = ?
    """
    return execute_read_all(query, (person_id,))

def get_round_judges_map(round_id):
    # Get dictionary mapping letters to person names
    rows = execute_read_all("""
        SELECT a.letter, p.name 
        FROM adjudicators a
        JOIN people p ON a.people_id = p.id
        WHERE a.round_id = ?
        ORDER BY a.letter
    """, (round_id,))
    return {row['letter']: row['name'] for row in rows}