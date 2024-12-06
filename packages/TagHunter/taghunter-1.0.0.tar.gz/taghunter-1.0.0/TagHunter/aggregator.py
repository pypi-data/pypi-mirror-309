import pandas as pd
from bs4 import BeautifulSoup
import re

def aggregated_df(df):
    df = pd.DataFrame(df)
    # Step 1: Sort DataFrame by Slide Number
    df = df.sort_values(by='Slide Number')
    
    # Step 2: Define custom aggregation functions
    def patterns_found_agg(x):
        patterns = [p for p in x if p is not None]
        return patterns if patterns else None
    
    def count_is_issue_breaks(x):
        issues = x.eq('Yes').astype(int).diff().fillna(0)
        return issues.eq(-1).sum()  # Count breaks (transition from 1 to 0)
    
    def count_is_issue_yes_continuity(x):
        issues = x.eq('Yes').astype(int)
        if issues.all():  # All values are 'Yes'
            return 1
        elif (issues.diff().fillna(0) == -1).any():  # "Yes" breaks and continues
            return 2
        else:  # Other cases
            return 0
    
    def count_p_class(x):
        count = x.notnull().sum()
        return count if count > 0 else None
    
    # Step 3: Group by Slide Number and Aggregate Data
    aggregated_data = df.groupby('Slide Number').agg({
        'P_ID': lambda x: list(x),  # Combine all P_IDs into a list
        'Patterns_Found': patterns_found_agg,  # Handle empty lists as None
        'Is_Issue': [
            count_is_issue_yes_continuity,  # Check if 'Yes' is continuous
            count_is_issue_breaks          # Count breaks in 'Yes'
        ],
        'P_Class': count_p_class,  # Replace 0 with None
        'P_Text_Content': lambda x: ' '.join(x),  # Combine P_Text_Content into a single string
        'P_HTML_Content': lambda x: ' '.join(x)  # Combine P_HTML_Content into a single string
    }).reset_index()
    
    # Step 4: Flatten Is_Issue Columns
    aggregated_data.columns = [
        'Slide Number',
        'Combined_P_ID',
        'Combined_Patterns_Found',
        'Is_Issue_Yes_Continuity',
        'Is_Issue_Breaks',
        'Count_P_Class',
        'Combined_P_Text_Content',
        'Combined_P_HTML_Content'
    ]
    
    # Step 5: Adjust Column Names for Clarity
    aggregated_data.rename(columns={
        'Is_Issue_Yes_Continuity': 'Is_Issue_Yes',
        'Is_Issue_Breaks': 'Count_Is_Issue_Breaks'
    }, inplace=True)
    
    return aggregated_data
