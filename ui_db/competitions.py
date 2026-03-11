from .utilities import execute_read_one, execute_read_all

def get_competition(competition_id):
    return execute_read_one("SELECT * FROM competitions WHERE id = ?", (competition_id,))

def get_competition_by_name(name):
    return execute_read_one("SELECT * FROM competitions WHERE name = ?", (name,))

def list_competitions():
    query = """
        SELECT * FROM competitions 
        ORDER BY 
            substr(date, 7, 4) || substr(date, 4, 2) || substr(date, 1, 2) DESC, 
            name ASC
    """
    return execute_read_all(query)
