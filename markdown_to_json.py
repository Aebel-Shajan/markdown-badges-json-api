import pandas as pd
import json
import markdown2
from bs4 import BeautifulSoup

def extract_url(markdown_string):
    start_pos = markdown_string.find('(') + 1
    end_pos = markdown_string.find(')')
    return markdown_string[start_pos:end_pos]

# Read the markdown file with UTF-8 encoding
with open('README.md', 'r', encoding='utf-8') as file:
    content = file.read()

# Convert markdown to HTML using markdown2 with extras for tables
html = markdown2.markdown(content, extras=["tables"])

# Parse HTML to extract tables
soup = BeautifulSoup(html, 'html.parser')
tables = soup.find_all('table')

# Define the specific header you are looking for
specific_header = ["Name", "Badge", "Markdown"]  # Example headers

# Initialize a list to store the JSON output
json_output = []
name_map = {}

# Process each table
for table in tables:
    # Read the HTML table into a pandas DataFrame
    df = pd.read_html(str(table))[0]
    
    # Check if the table has the specific header
    if df.columns.tolist() == specific_header:
        # Extract the link only
        df["Link"] = df["Markdown"].apply(extract_url)
        
        for index, row in df.iterrows():
            name_map[row["Name"]] = row["Link"]


# Optionally, save the JSON output to a file
with open('markdown-badges.json', 'w', encoding='utf-8') as json_file:
    json.dump(name_map, json_file, indent=4, ensure_ascii=False)