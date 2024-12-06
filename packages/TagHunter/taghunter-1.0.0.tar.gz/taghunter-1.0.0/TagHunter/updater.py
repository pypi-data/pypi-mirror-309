import pandas as pd
from bs4 import BeautifulSoup
import re
def extract_p_class(df):
    # Iterate through the DataFrame and extract the class names
    def get_class_name(html_content):
        try:
            # Parse the HTML content
            soup = BeautifulSoup(html_content, 'html.parser')
            p = soup.find('p')  # Find the <p> tag
            if p and p.get('class'):  # Check if <p> tag and its class exist
                return ', '.join(p.get('class'))  # Join multiple classes if present
            else:
                return None  # Fill None if class doesn't exist
        except Exception as e:
            return None  # Handle any parsing errors and return None

    # Apply the logic to the DataFrame
    df['P_Class'] = df['P_HTML_Content'].apply(get_class_name)
    return df

def update_p_class(df, valid_class="dpg--annotations_markup--paragraph"):
    # Check if the 'P_Class' column exists in the DataFrame
    if 'P_Class' not in df.columns:
        raise ValueError("The DataFrame does not have a 'P_Class' column.")
    # Update the P_Class column
    df['P_Class'] = df['P_Class'].apply(lambda x: x if x == valid_class else None)
    return df

def update_is_issue(df):
    # Check if required columns exist
    if 'P_Text_Content' not in df.columns or 'Is_Issue' not in df.columns:
        raise ValueError("The DataFrame does not have the required columns: 'P_Text_Content' and 'Is_Issue'.")

    # Regex patterns to detect issues with additional constraints
    patterns = [
        r'^\s*(\d+)\.(?!\d)',       # Numeric followed by dot, not decimal
        r'^\s*\(\d+\)',             # Matches "(1)", "(2)", "(3)"
        r'^\s*\([a-zA-Z]\)',        # Matches "(a)", "(b)", "(A)", "(B)"
        r'^\s*(I{1,3}\.)'           # Roman numerals followed by dot (e.g., "I.")
    ]
    # Function to check if a text matches any of the patterns with constraints
    def check_issue(text):
        if re.match(r'^\s*(\d+)\.(?!\d)', text):
            # Extract the number and apply the limit condition
            number = int(re.match(r'^\s*(\d+)\.', text).group(1))
            if number > 50:  # Exclude numbers greater than 50
                return None
        # Check other patterns
        if any(re.match(pattern, text) for pattern in patterns):
            # Exclude decimal or negative numbers
            if re.match(r'^\s*-?\d+\.\d+', text):  # Exclude decimal or negative numbers
                return None
            return "Yes"
        return None
    df['Is_Issue'] = df['P_Text_Content'].apply(check_issue)
    return df

def update_and_save_issues_with_symbol_check(df):
    # Check if required columns exist
    required_columns = ['P_Text_Content', 'Is_Issue', 'Patterns_Found', 'P_Class']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"The DataFrame does not have the required column: '{col}'.")

    # Regex patterns to detect issues with additional constraints
    patterns = [
        r'^\s*(\d+)\.(?!\d)',       # Numeric followed by dot, not decimal
        r'^\s*\(\d+\)',             # Matches "(1)", "(2)", "(3)"
        r'^\s*\([a-zA-Z]\)',        # Matches "(a)", "(b)", "(A)", "(B)"
        r'^\s*(I{1,3}\.)'           # Roman numerals followed by dot (e.g., "I.")
    ]

    # Function to check if a text matches any of the patterns or starts with special symbols
    def check_issue(text):
        # Check if text starts with special symbols like '■'
        if re.match(r'^\s*[■●♦]', text):
            return "Yes"

        # Check numeric patterns with constraints
        if re.match(r'^\s*(\d+)\.(?!\d)', text):
            # Extract the number and apply the limit condition
            number = int(re.match(r'^\s*(\d+)\.', text).group(1))
            if number > 20:
                return None

        # Check other patterns
        if any(re.match(pattern, text) for pattern in patterns):
            # Exclude decimal or negative numbers
            if re.match(r'^\s*-?\d+\.\d+', text):  # Exclude decimal or negative numbers
                return None
            return "Yes"
        return None

    # Apply the logic to the 'Is_Issue' column
    df['Is_Issue'] = df['P_Text_Content'].apply(check_issue)
    return df