'''
Autor: Witten Yeh
Date: 2025-02-21 19:44:34
LastEditors: Witten Yeh
LastEditTime: 2025-02-21 20:23:20
Description: 
'''

import pandas as pd

def extract_code_and_name(file_path: str):
    """
    Read the "证券代码" (company Code) and "证券简称" (company Name) columns from an Excel file,
    and return two lists.
    
    Parameters:
        file_path (str): Path to the Excel file
    
    Returns:
        tuple: Two lists (list of company codes, list of company names)
    """
    
    try:
        # Read specified columns
        df = pd.read_excel(file_path, usecols=["证券代码", "证券简称"])
        
        # Convert the two columns to lists
        company_codes = df["证券代码"].tolist()  # Convert the "company Code" column to a list
        company_names = df["证券简称"].tolist()  # Convert the "company Name" column to a list
        
        return company_codes, company_names

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found. Please check the file path.")
    except ValueError as e:
        print(f"Error: An issue occurred while reading the file, possibly due to mismatched column names. Specific error: {e}")
    except Exception as e:
        print(f"Unknown error occurred: {e}")

# Example usage
if __name__ == "__main__":
    file_path = '../data/company_list.xlsx'  # Replace with your .xlsx file path
    company_codes, company_names = extract_code_and_name(file_path)
    
    if company_codes and company_names:
        print("List of company codes:", company_codes)
        print("List of company names:", company_names)
    