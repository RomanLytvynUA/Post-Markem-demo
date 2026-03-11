import ui_db
from collections import defaultdict

def translate_dance(dance):
    dances = {
        'C': 'Cha-cha-cha',
        'S': 'Samba',
        'R': 'Rumba',
        'P': 'Paso Doble',
        'J': 'Jive',

        'W': 'Slow Waltz',
        'T': 'Tango',
        'VW': 'Viennese Waltz',
        'F': 'Slow Foxtrot',
        'Q': 'Quickstep'
    }

    return dances.get(dance, dance)

def format_analysis_display_data(raw_data, competitors, adjudicators):
    alignment, bias, voting_blocs = raw_data
    
    return (
        get_alignment_display_data(alignment, adjudicators),
        get_bias_display_data(bias, adjudicators, competitors),
        get_voting_blocs_display_data(voting_blocs, adjudicators)
    )

def get_score_status(score):
    if score is None: 
        return 'status-ghost'
        
    # --- THE ELITE & HIGH ALIGNMENT ZONES ---
    elif score >= 0.90: return 'status-elite'           # 0.90 to 1.00 (Suspiciously perfect)
    elif score >= 0.80: return 'status-excellent'       # 0.80 to 0.89 (Very high consensus)
    elif score >= 0.70: return 'status-great'           # 0.70 to 0.79 (Strong consensus)
    
    # --- THE HEALTHY BASELINE (Where honest experts live) ---
    elif score >= 0.60: return 'status-good'            # 0.60 to 0.69 (Healthy standard deviation)
    elif score >= 0.50: return 'status-average'         # 0.50 to 0.59 (Moderate deviation)
    elif score >= 0.40: return 'status-fair'            # 0.40 to 0.49 (Noticeable deviation)
    
    # --- THE WARNING ZONES ---
    elif score >= 0.30: return 'status-below-average'   # 0.30 to 0.39 (High deviation)
    elif score >= 0.20: return 'status-poor'            # 0.20 to 0.29 (Weak consensus)
    elif score >= 0.10: return 'status-very-poor'       # 0.10 to 0.19 (Borderline random)
    
    # --- THE RANDOM & INVERTED ZONES ---
    elif score >= 0.00: return 'status-bad'             # 0.00 to 0.09 (Purely random marking)
    elif score >= -0.20: return 'status-terrible'       # -0.01 to -0.19 (Slightly inverted)
    elif score >= -0.50: return 'status-critical'       # -0.20 to -0.49 (Actively inverted)
    else: return 'status-rogue'                         # < -0.50 (Completely opposite to panel)


def get_score_comment(score):
    if score is None: 
        return 'No sufficient data. The algorithm requires more rounds to render a verdict.'
        
    # --- THE ELITE & HIGH ALIGNMENT ZONES ---
    elif score >= 0.90: 
        return 'Extremly high alignment. Marks are nearly identical to the panel.'    
    elif score >= 0.80: 
        return 'Excellent alignment. Highly consistent with the panel consensus while maintaining slight independence.'
    elif score >= 0.70: 
        return 'Great alignment. Strong reputation and highly predictable judging patterns.'
        
    # --- THE HEALTHY BASELINE ---
    elif score >= 0.60: 
        return 'Good baseline. A perfectly healthy balance of panel consensus and independent expert evaluation.'        
    elif score >= 0.50: 
        return 'Average baseline. Standard panel alignment with moderate, acceptable deviations in placement.'      
    elif score >= 0.40: 
        return 'Fair alignment. Noticeable deviation from the final panel results, leaning heavily on personal criteria.'
        
    # --- THE WARNING ZONES ---
    elif score >= 0.30: 
        return 'Below average. Frequently disagrees with the panel. Marks often conflict with standard industry placements.'
    elif score >= 0.20: 
        return 'Poor alignment. Weak consensus. Struggles to match the visual standard set by the rest of the adjudicators.'
    elif score >= 0.10: 
        return 'Very poor. Highly irregular judging patterns. Marks are bordering on statistical randomness.'
        
    # --- THE RANDOM & INVERTED ZONES ---
    elif score >= 0.00: 
        return 'Bad reputation. Marks exhibit zero mathematical correlation to the panel. Essentially random guessing.'
    elif score >= -0.20: 
        return 'Terrible alignment. Slightly inverted. Tends to mark the panel favorites slightly lower than average.'
    elif score >= -0.50: 
        return 'Critical variance. Actively inverted. Consistently penalizes the couples the rest of the panel rewards.'
    else: 
        return 'Rogue judge. Completely opposite to the panel. Marks the best couples last, and the worst couples first.'

def get_alignment_display_data(alignment_data, adjudicators):
    alignment_data.index.name = 'letter'

    df = alignment_data.reset_index().round(2)
    name_map = {adj['letter']: adj for adj in adjudicators}
    records = df.to_dict(orient='records')


    final_data = []
    for row in records:
        processed_row = {
            'letter': row['letter'],
            'name': name_map.get(row['letter'], {}).get("name", f"Judge {row['letter']}"),
            'people_id': name_map.get(row['letter'], {}).get('people_id', ""),
            'overall': {
                'val': row.get('overall_accuracy'),
                'status': get_score_status(row.get('overall_accuracy'))
            },
            'dances': {}
        }
        
        for key, value in row.items():
            if key not in ['letter', 'overall_accuracy']:
                processed_row['dances'][key] = {
                    'val': value,
                    'status': get_score_status(value)
                }
        
        final_data.append(processed_row)

    return final_data

def get_competitors_map(competitors):
    """Normalize the parser's output to the competitors map"""
    data = competitors
    for comp in data:
        comp['p1_name'] = comp['dancers'][0]['name']if len(comp['dancers']) > 0 else 'Unknown dancer'
        comp['p2_name'] = comp['dancers'][1]['name'] if len(comp['dancers']) > 1 else ""
    return data

def get_bias_display_data(bias_data, adjudicators, competitors, threshold=2):
    comp_map = {str(c['number']): c for c in competitors}
    adj_map = {a['letter']: a['name'] for a in adjudicators}

    system_cols = ['judge', 'couple', 'overall_bias']
    dance_cols = [col for col in bias_data.columns if col not in system_cols]
    
    # group reports by judge
    grouped_reports = defaultdict(list)

    for _, row in bias_data.iterrows():
        val = row['overall_bias']
        couple_num = str(int(row['couple']))
        judge_letter = row['judge']
        
        if abs(val) < threshold:
            status = "neutral"
        else:
            status = "favoritism" if val > 0 else "opposition"
        
        dances = []
        for d in dance_cols:
            d_val = int(row[d])
            prefix = "+" if d_val > 0 else ""
            dances.append(f"{d}: {prefix}{d_val}")
        
        dancers = comp_map.get(couple_num, [{'name': 'Unknown'}, {'name': 'Unknown'}])
        judge_display = f"{judge_letter} {adj_map.get(judge_letter, 'Unknown')}"
        
        grouped_reports[judge_display].append({
            "overall": f"{'+' if val > 0 else ''}{val}",
            "name1": dancers['p1_name'],
            "name2": dancers['p2_name'],
            "p1_id": dancers.get("p1_id", ""),
            "p2_id": dancers.get("p2_id", ""),
            "number": couple_num,
            "type": status,
            "details": " / ".join(dances)
        })

    return dict(grouped_reports)

def get_voting_blocs_display_data(blocs_data, adjudicators):
    adj_map = {a['letter']: a for a in adjudicators}

    data = [
        {
            "name": f"Bloc #{i+1}",
            "judges": [
                {"letter": adj, "name": adj_map.get(adj, {}).get("name", "Unknown"), "p_id": adj_map.get(adj, {}).get("person_id", "")}
                for adj in bloc
            ]
        }
        for i, bloc in enumerate(blocs_data)
    
    ]
    
    return data

def get_alignment_score_data(score, r=None):
    if not score:
        return {
            'score': f'-',
            'status': get_score_status(None),
            'comment': get_score_comment(None),
        }
    
    formated_score = score
    if r == 'int': formated_score = int(score*100)
    else: formated_score = round(score*100, r)
    return {
            'score': f'{formated_score}%',
            'status': get_score_status(score),
            'comment': get_score_comment(score),
        }

def get_analytics_data(round_id=None):
    data = ui_db.rounds.get_analytics_cache(round_id) if round_id else None
   
    return data