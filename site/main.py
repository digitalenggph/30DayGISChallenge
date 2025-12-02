import pandas as pd
from jinja2 import Environment, FileSystemLoader


# Load the Excel file (one sheet for now hehe)
data_df = pd.read_excel("30DayGISChallenge.xlsx")
data = data_df.to_dict('records')

# print(data[0].keys())
# exit()

context = {
    'title': "#30DayMapChallenge2025",
    'data': data
    }

# Setup Jinja environment
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('body.html')

rendered_html = template.render(context)

# Save to HTML
with open("output.html", "w", encoding="utf-8") as f:
    f.write(rendered_html)

print("HTML file created successfully!")
