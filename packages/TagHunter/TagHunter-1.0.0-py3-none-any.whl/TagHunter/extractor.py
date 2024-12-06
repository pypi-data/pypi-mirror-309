import os
import pandas as pd
from bs4 import BeautifulSoup
def extract_p_tag_details(file_path):
    """ find all <p> tags from an HTML file that are not nested within <li> tags"""
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        p_tags = soup.find_all('p')
        data = []
        for p in p_tags:
            if not p.find_parent('li'):
                p_id = p.get('id', None)
                p_html_content = str(p)
                p_text_content = p.get_text(strip=True)
                p_class = ', '.join(p.get('class', [])) if p.get('class') else None
                patterns_found = None
                is_issue = None
                data.append([p_id, p_html_content, p_text_content, patterns_found, is_issue, p_class])
        return data
def process_html_folder_to_dataframe(html_folder_path, file_extension):
    """
    This function processes a folder of HTML files (with .txt extensions), extracts details of <p> tags 
    from each file using extract_p_tag_details function and organizes the data into a Pandas DataFrame. 
    Each row in the DataFrame includes the slide name and extracted <p> tag details
    """
    columns = ['Slide Number', 'P_ID', 'P_HTML_Content', 'P_Text_Content', 'Patterns_Found', 'Is_Issue', 'P_Class']
    all_data = []

    for slide_name in os.listdir(html_folder_path):
        if slide_name.endswith(str(file_extension)):
            file_path = os.path.join(html_folder_path, slide_name)
            p_details = extract_p_tag_details(file_path)
            for detail in p_details:
                all_data.append([slide_name] + detail)
    return pd.DataFrame(all_data, columns=columns)
