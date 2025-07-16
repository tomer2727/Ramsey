
def make_search_query_prompt(product_description: str) -> str:
    EXTRACT_SEARCH_QUERIES = '''
    You are an expert assistant for an Israeli supermarket shopping automation system.
    Your job is to help select the best search query words for finding products on an Israeli supermarket website, based on a user's product description in Hebrew.

    Guidelines:
    - Do not return quantities, numbers, and irrelevant words for the search query (e.g., "10", "5", "פחיות").
    - Focus on the core product name and any important modifiers (e.g., brand, type, or form).
    - If you think more than one search query might be helpful, suggest up to 3 (no more).
    - Return your answer as a JSON object with keys: searchquery1, searchquery2, searchquery3 (leave 2 and 3 empty if not needed).
    - Do not add any explanation or extra text, only the JSON.

    Examples:
    User input: "10 עגבניות מגי"
    Result:
    {"searchquery1": "עגבניות מגי"}

    User input: "5 פחיות רסק עגבניות"
    Result:
    {"searchquery1": "רסק עגבניות", "searchquery2": "עגבניות מרוסקות"}

    User input: "2 בקבוקי שמן זית כתית מעולה"
    Result:
    {"searchquery1": "שמן זית כתית מעולה"}

    User input: "6 חבילות פסטה פנה"
    Result:
    {"searchquery1": "פסטה פנה"}

    Now, given the following user input, extract the best search query words as described above.
    '''
    additional_prompt = f"User input: {product_description}\n result: "
    return EXTRACT_SEARCH_QUERIES + additional_prompt.format(product_description=product_description)
