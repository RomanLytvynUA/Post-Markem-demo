from .utilities import execute_read_one, execute_read_all

def get_people():
    query = """
        WITH EntryCounts AS (
        SELECT person_id, SUM(cnt) as total_entries
        FROM (
            SELECT partner1_id AS person_id, COUNT(id) AS cnt 
            FROM entries 
            WHERE partner1_id IS NOT NULL
            GROUP BY partner1_id
            
            UNION ALL
            
            SELECT partner2_id AS person_id, COUNT(id) AS cnt 
            FROM entries 
            WHERE partner2_id IS NOT NULL
            GROUP BY partner2_id
        )
        GROUP BY person_id
        ),
        AdjudicatorCounts AS (
            SELECT people_id, COUNT(id) AS total_adjudications
            FROM adjudicators
            GROUP BY people_id
        )
        SELECT 
            p.*,
            COALESCE(e.total_entries, 0) AS entries,
            COALESCE(a.total_adjudications, 0) AS adjudicators
        FROM people p
        LEFT JOIN EntryCounts e ON p.id = e.person_id
        LEFT JOIN AdjudicatorCounts a ON p.id = a.people_id;
    """
    return execute_read_all(query)

def get_adjudicators_leaderboard():
    query = """
        SELECT
            p.*,
            COUNT(DISTINCT a.id) AS num_of_records,
            ROUND(AVG(ar.alignment), 4) AS score
        FROM people p
        JOIN adjudicators a 
            ON a.people_id = p.id
        JOIN alignment_records ar 
            ON ar.person_id = p.id
        GROUP BY p.id
        ORDER BY score DESC;
    """
    return execute_read_all(query)

def get_adjudication_records(person_id, score_formatter=None):
    query = """
        SELECT 
            comp.id AS comp_id, comp.date AS comp_date, comp.name AS comp_name,
            cat.id AS cat_id, cat.name AS cat_name,
            r.id AS round_id, r.type AS round_name,
            ROUND(ar.alignment, 4) AS round_score
        FROM competitions comp
        JOIN categories cat ON cat.competition_id = comp.id
        JOIN rounds r ON r.category_id = cat.id
        JOIN adjudicators a ON a.round_id = r.id
        LEFT JOIN alignment_records ar ON ar.round_id = r.id AND ar.person_id = a.people_id
        WHERE a.people_id = ?
    """
    rows = execute_read_all(query, (person_id,)) 
    
    # --- Step 1: Initial Grouping ---
    comps = {}
    for row in rows:
        cid, catid = row['comp_id'], row['cat_id']
        if cid not in comps:
            comps[cid] = {'name': row['comp_name'], 'date': row['comp_date'], 'categories': {}}
        if catid not in comps[cid]['categories']:
            comps[cid]['categories'][catid] = {'name': row['cat_name'], 'rounds': []}
            
        comps[cid]['categories'][catid]['rounds'].append({
            'id': row['round_id'], 'name': row['round_name'], 'score': row['round_score']
        })
        
    # --- Step 2: Processing with the Formatter ---
    final_output = []
    for comp_data in comps.values():
        processed_categories = []
        valid_cat_scores = []
        
        for cat_data in comp_data['categories'].values():
            round_scores = [r['score'] for r in cat_data['rounds'] if r['score'] is not None]
            
            cat_avg = sum(round_scores) / len(round_scores) if round_scores else None
            if cat_avg is not None: valid_cat_scores.append(cat_avg)

            processed_categories.append({
                'name': cat_data['name'],
                'score': round(cat_avg, 4) if cat_avg is not None else None,
                # Decorate Category if formatter exists
                'alignment_data': score_formatter(cat_avg) if score_formatter else None,
                'rounds': cat_data['rounds']
            })
            
        comp_avg = sum(valid_cat_scores) / len(valid_cat_scores) if valid_cat_scores else None
            
        final_output.append({
            'name': comp_data['name'],
            'date': comp_data['date'],
            'score': round(comp_avg, 4) if comp_avg is not None else None,
            # Decorate Competition if formatter exists
            'alignment_data': score_formatter(comp_avg) if score_formatter else None,
            'categories': processed_categories
        })
        
    return final_output

def get_entry_records(person_id):
    query = """
        SELECT 
            comp.id AS comp_id, comp.date AS comp_date, comp.name AS comp_name,
            cat.id AS cat_id, cat.name AS cat_name, 
            MIN(r.id) AS round_id
        FROM competitions comp
        JOIN categories cat ON cat.competition_id = comp.id
        JOIN entries e ON e.category_id = cat.id
        JOIN rounds r ON r.category_id = cat.id
        WHERE e.partner1_id = ? OR e.partner2_id = ?
        GROUP BY comp.id, comp.date, comp.name, cat.id, cat.name
    """
    rows = execute_read_all(query, (person_id, person_id)) 
    
    comps = {}
    for row in rows:
        comp_id = row['comp_id']
        if comp_id not in comps:
            comps[comp_id] = {'name': row['comp_name'], 'date': row['comp_date'], 'categories': []}
        comps[comp_id]['categories'].append({'name': row['cat_name'], 'round_id': row['round_id']})
        
    return list(comps.values())

def get_person(person_id):
    query = """
        SELECT 
            p.*,
            (SELECT COUNT(id) FROM alignment_records WHERE person_id = p.id) AS num_of_records,
            COALESCE((SELECT ROUND(AVG(alignment), 4) FROM alignment_records WHERE person_id = p.id), 0) AS score
        FROM people p
        WHERE p.id = ?
    """
    return execute_read_one(query, (person_id,))

def get_person_by_name(name):
    return execute_read_one("SELECT * FROM people WHERE name = ?", (name,))

def list_people():
    return execute_read_all("SELECT * FROM people ORDER BY name")