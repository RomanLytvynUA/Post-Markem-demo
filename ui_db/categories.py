from .utilities import execute_read_one, execute_read_all

def get_category(category_id):
    return execute_read_one("SELECT * FROM categories WHERE id = ?", (category_id,))

def get_category_by_comp_and_name(competition_id, name):
    return execute_read_one("SELECT * FROM categories WHERE competition_id = ? AND name = ?", 
                            (competition_id, name))

def list_categories(competition_id):
    return execute_read_all("SELECT * FROM categories WHERE competition_id = ? ORDER BY name", 
                            (competition_id,))
