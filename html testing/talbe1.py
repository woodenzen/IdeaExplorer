import pandas as pd

# Create a sample DataFrame with URLs
df = pd.DataFrame({
    'Name': ['John', 'Mary', 'Bob'],
    'Website': ['http://www.example.com', 'http://www.google.com', 'http://www.yahoo.com']
})

# Use the to_html() function to generate an HTML table with embedded URLs
html_table = df.to_html(escape=False, formatters=dict(Website=lambda x: '<a href="{}">{}</a>'.format(x, x)))

# Display the HTML table
print(html_table)

