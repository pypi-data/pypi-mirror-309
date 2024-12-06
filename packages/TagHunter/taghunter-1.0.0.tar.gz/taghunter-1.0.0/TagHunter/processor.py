from .extractor import process_html_folder_to_dataframe
from .validator import fill_patterns_found, validate_patterns
from .updater import extract_p_class, update_p_class, update_is_issue, update_and_save_issues_with_symbol_check
from .aggregator import aggregated_df

def process(html_folder_path, file_extension):
    df = process_html_folder_to_dataframe(html_folder_path,file_extension)
    df['Slide Number'] = df['Slide Number'].str.replace(' .txt', '', regex=False)
    df = fill_patterns_found(df) 
    # Update the 'Patterns_Found' column based on the validation
    df['Patterns_Found'] = df['Patterns_Found'].apply(lambda x: x if validate_patterns(x) else None)
    df = extract_p_class(df)
    df = update_p_class(df)
    df = update_is_issue(df)
    df = update_and_save_issues_with_symbol_check(df)
    df = df[
        (df['Patterns_Found'].notnull()) |  # Patterns_Found is not None
        (df['Is_Issue'].notnull()) |        # Is_Issue is not None
        (df['P_Class'] == 'dpg--annotations_markup--paragraph')
    ]
    df=aggregated_df(df)
    filtered_df = df[['Slide Number', 'Combined_P_Text_Content', 'Combined_P_HTML_Content']]
    return filtered_df