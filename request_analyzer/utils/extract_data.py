import re

def extract_data(text):
    # Try to match city name enclosed in double quotes
    match = re.search(r'"(.*?)"', text)
    if match:
        return match.group(1)
    else:
        # Try to match city name with double quote only at the end
        match = re.search(r'(.*?)"', text)
        if match:
            return match.group(1).strip()
        else:
            return "None"
