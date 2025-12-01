import pandas as pd
from jinja2 import Environment, FileSystemLoader

# Load Excel
df = pd.read_excel("30DayGISChallenge.xlsx")  # replace with your file path

# Prepare data
columns = df.columns.tolist()
rows = df.values.tolist()

# Setup Jinja environment
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('body.html')

# Render the template with data
output = template.render(columns=columns, rows=rows)

# Save to HTML
with open("output.html", "w", encoding="utf-8") as f:
    f.write(output)

print("HTML file created successfully!")
