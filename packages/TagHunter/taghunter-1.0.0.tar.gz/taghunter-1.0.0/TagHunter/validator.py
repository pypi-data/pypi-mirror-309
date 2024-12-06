import pandas as pd
from bs4 import BeautifulSoup
import re

def fill_patterns_found(df):
    '''This function fill_patterns_found analyzes the text content of <p> tags in a DataFrame column 
    P_HTML_Content to identify patterns using regular expressions (e.g., numeric lists, parenthetical numbers/letters, Roman numerals, alphabetic markers).'''
    patterns = {
        'Numeric': r'^\s*(\d+)\.(?!\d)',          # Matches "1.", "2.", "3."
        'Parenthetical Numbers': r'\(\d+\)',  # Matches "(1)", "(2)", "(3)"
        'Parenthetical Letters': r'\([a-zA-Z]\)',  # Matches "(a)", "(b)", "(A)", "(B)"
        'Roman Numerals': r'[IVXLCDM]+\.',  # Matches Roman numerals like "I.", "II.", "III."
        'Alphabetic': r'\b([a-zA-Z])\.'  # Matches "a.", "b.", etc.
    }
    for index, row in df.iterrows():
        html_content = row['P_HTML_Content']
        soup = BeautifulSoup(html_content, 'html.parser')
        p = soup.find('p')
        if p:
            p_text = p.get_text(strip=True)
            matches = {key: re.findall(pattern, p_text) for key, pattern in patterns.items()}
            # Combine matches for all found patterns dynamically
            patterns_found = {key: match_list for key, match_list in matches.items() if match_list}
            patterns_found = patterns_found if patterns_found else None
            df.at[index, 'Patterns_Found'] = patterns_found
    return df

# This function is Validate pattern is it valid or not
def validate_patterns(patterns):
    # Handle empty or non-string patterns
    if not patterns or pd.isna(patterns):
        return False  # No patterns found, invalid

    # Convert patterns (dictionary or list) to string if necessary
    if not isinstance(patterns, str):
        patterns = str(patterns)

    # Extract patterns
    numeric_list = re.findall(r'^\s*(\d+)\.(?!\d)', patterns)  # Matches "1.", "2.", etc.
    roman_numerals = re.findall(r'([IVXLCDM]+)\.', patterns)  # Matches "I.", "II.", etc.
    parenthetical_numbers = re.findall(r'\((\d+)\)', patterns)  # Matches "(1)", "(2)", etc.
    parenthetical_letters = re.findall(r'\(([a-zA-Z])\)', patterns)  # Matches "(a)", "(b)", etc.
    alphabetic_with_dot = re.findall(r'\b([a-zA-Z])\.', patterns)  # Matches "a.", "b.", etc.

    # Check for valid continuous sequences
    def is_sequential(lst, transform=lambda x: int(x)):
        if len(lst) < 2:  # Require at least two items to form a sequence
            return False
        try:
            lst = list(map(transform, lst))  # Transform each item in the list
            if any(x > 20 for x in lst):  # Exclude sequences with numbers greater than 20
                return False
            return all(lst[i] == lst[i - 1] + 1 for i in range(1, len(lst)))
        except ValueError:
            return False

    # Validate Roman numerals
    def roman_to_int(roman):
        roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        num = 0
        prev_value = 0
        for char in reversed(roman):
            value = roman_map[char]
            if value < prev_value:
                num -= value
            else:
                num += value
            prev_value = value
        return num

    # Check each pattern type for validity
    is_numeric_valid = is_sequential(numeric_list, transform=int) if numeric_list else False
    is_roman_valid = is_sequential(roman_numerals, transform=roman_to_int) if roman_numerals else False
    is_parenthetical_numbers_valid = is_sequential(parenthetical_numbers, transform=int) if parenthetical_numbers else False
    is_parenthetical_letters_valid = is_sequential(parenthetical_letters, transform=ord) if parenthetical_letters else False
    is_alphabetic_with_dot_valid = is_sequential(alphabetic_with_dot, transform=ord) if alphabetic_with_dot else False

    # Return True if any sequence is valid
    return (
        is_numeric_valid
        or is_roman_valid
        or is_parenthetical_numbers_valid
        or is_parenthetical_letters_valid
        or is_alphabetic_with_dot_valid
    )
    