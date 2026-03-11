from .utilities import execute_read_one, execute_read_all

def get_entry(entry_id):
    return execute_read_one("SELECT * FROM entries WHERE id = ?", (entry_id,))

def list_entries(category_id):
    return execute_read_all("SELECT * FROM entries WHERE category_id = ? ORDER BY number", (category_id,))

def get_round_entries(round_id):
    query = """
        SELECT 
            e.number, 
            e.place, 
            p1.name AS p1_name, 
            p2.name AS p2_name, 
            e.partner1_id AS p1_id, 
            e.partner2_id AS p2_id
        FROM entries e
        JOIN rounds r ON r.category_id = e.category_id
        JOIN people p1 ON e.partner1_id = p1.id
        LEFT JOIN people p2 ON e.partner2_id = p2.id
        WHERE r.id = ?
        ORDER BY e.number
    """
    return execute_read_all(query, (round_id,))

def get_entries_display_map(round_id):
    rows = get_round_entries(round_id)
    couples = {}
    for row in rows:
        p2 = f" & {row['p2_name']}" if row['p2_name'] else ""
        couples[row['number']] = f"{row['p1_name']}{p2}"
    return couples

def get_entries_by_person(person_id):
    query = """
        SELECT * FROM entries WHERE partner1_id = ? OR partner2_id = ?
    """
    return execute_read_all(query, (person_id,))
