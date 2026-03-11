import json
import io
import pandas as pd
from .utilities import execute_read_one, execute_read_all

def get_round(round_id):
    return execute_read_one("SELECT * FROM rounds WHERE id = ?", (round_id,))

def get_round_by_category_and_type(category_id, round_type):
    return execute_read_one("SELECT * FROM rounds WHERE category_id = ? AND type = ?", (category_id, round_type))

def list_rounds(category_id):
    return execute_read_all("SELECT * FROM rounds WHERE category_id = ?", (category_id,))

# --- Marks Logic ---

def get_marks(round_id):
    """Fetches and parses the marks JSON into a dictionary of Pandas DataFrames."""
    row = execute_read_one("SELECT marks FROM rounds WHERE id = ?", (round_id,))
    
    if row and row['marks']:
        raw_json = json.loads(row['marks'])
        parsed_marks = {
            dance: pd.read_json(io.StringIO(df_json), orient='split') 
            for dance, df_json in raw_json.items()
        }
        return parsed_marks

    return None

# --- Cache Logic ---

def get_garbage_rounds():
    query = """
        SELECT DISTINCT
            r.id,
            r.type
        FROM 
            rounds r
        JOIN 
            alignment_records ar ON r.id = ar.round_id
        WHERE 
            ar.alignment IS NULL;
    """
    
    return execute_read_all(query)

def get_analytics_cache(round_id):
    """
    Assembles the JSON strings from the rounds table back into live Pandas DataFrames.
    Returns: (accuracy_df, bias_df, voting_blocs)
    """
    query = "SELECT alignment_cache, bias_cache, blocs_cache FROM rounds WHERE id = ?"
    row = execute_read_one(query, (round_id,))
    
    if row:
        def parse_df(json_str):
            if not json_str:
                return None
            
            return pd.read_json(io.StringIO(json_str), orient='split').round(2)
        
        accuracy_df = parse_df(row["alignment_cache"])
        bias_df = parse_df(row["bias_cache"])
        voting_blocs = json.loads(row["blocs_cache"]) if row["blocs_cache"] else []

        return accuracy_df, bias_df, voting_blocs
        
    return None, None, None
