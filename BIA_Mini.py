import pandas as pd
import re

def calculate_advanced_score_and_level(row):
    score = 0
    is_high_priority = False
    
    # 1. Process Status (Core Criticality - up to 40 points)
    status = str(row.get('Process Status', '')).strip().lower()
    if status == 'critical': 
        score += 40
        is_high_priority = True  # Straight critical need
    elif status == 'operational': 
        score += 20
    
    # 2. RTO Factor (Recovery Speed - up to 40 points)
    rto_val = 999 
    try:
        rto_str = str(row.get('Process RTO', '')).lower()
        numbers = re.findall(r'\d+', rto_str)
        if numbers: 
            val = int(numbers[0])
            if 'week' in rto_str: rto_val = val * 24 * 7
            elif 'day' in rto_str: rto_val = val * 24
            elif 'month' in rto_str: rto_val = val * 24 * 30
            else: rto_val = val
    except Exception:
        pass
    
    if rto_val <= 4: 
        score += 40
        is_high_priority = True  # Straight critical need if RTO <= 4
    elif rto_val <= 24: score += 25
    elif rto_val <= 72: score += 10
    
    # 3. SPOF Factor (Vulnerability - up to 20 points)
    if str(row.get('SPOF', '')).strip().lower() == 'yes': score += 20
    
    # 4. Time-Critical Factor (Peak Periods/Deadlines - up to 15 points)
    tc = str(row.get('Time-Critical', '')).strip().lower()
    if tc not in ['nan', 'none', '', 'no', 'n/a', 'false']:
        score += 15
        # High priority if time critical is less than a day (hourly, immediately, daily)
        if any(word in tc for word in ['hour', 'minute', 'daily', 'day', 'immediate']):
            is_high_priority = True
            
    # 5. Dependency Factor (Complexity - up to 20 points capped)
    dep_count = 0
    all_deps_text = ""
    for dep_type in ['Internal Process Dependency', 'External Process Dependency']:
        deps = row.get(dep_type)
        if pd.notna(deps) and str(deps).strip() != '' and str(deps).strip().lower() != 'none':
            all_deps_text += " " + str(deps).lower()
            dep_count += len(str(deps).split(','))
            
    score += min(dep_count * 5, 20)  # 5 points per dependency, maxed at 20
    
    # Check if dependencies include finance
    if 'finance' in all_deps_text:
        is_high_priority = True
        
    # Define Level based on conditions
    if is_high_priority or score > 120:
        level = 'High'
    elif score >= 60:
        level = 'Medium'
    else:
        level = 'Low'
        
    return pd.Series([score, level], index=['Score', 'Level'])

# Load the data (skipping the first 3 rows of headers)
df = pd.read_excel('BIA_-_2026.xlsx', header=3)

# Extract relevant columns
cols = ['Process', 'Process RTO', 'Process Status', 'SPOF', 'Internal Process Dependency', 'External Process Dependency', 'Time-Critical']
df_subset = df[cols].copy().dropna(subset=['Process'])

# Apply scoring and categorization
df_subset[['Score', 'Level']] = df_subset.apply(calculate_advanced_score_and_level, axis=1)

# Rank the processes
df_subset = df_subset.sort_values(by='Score', ascending=False).reset_index(drop=True)
df_subset['Rank'] = df_subset.index + 1

# Final Output display
for _, row in df_subset.iterrows():
    print(f"Process {row['Process']}: Rank {row['Rank']}, {row['Level']} (Score: {row['Score']})")