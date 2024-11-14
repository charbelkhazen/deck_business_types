#!/usr/bin/env python
# coding: utf-8

# In[19]:


import json
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# Load your data
last_df = pd.read_csv('last_df.csv')  # Ensure this file is correctly formatted and contains 'category_level_3'

# Load and process your structured text data
with open('final_output.json', 'r') as f:
    text_data = json.load(f)  # Ensure this is a dict mapping category_level_3 to structured dicts

# Create the treemap
fig = px.treemap(
    last_df,
    path=['category_level_1', 'category_level_2', 'category_level_3'],
    title='Treemap with Subcategories',
    hover_data={'category_level_3': True},
    
)

# Initialize the Dash app
app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='treemap', figure=fig),
    html.Div(
        id='text-display',
        style={
            'padding': '20px',
            'fontSize': '16px',
            'whiteSpace': 'pre-wrap',
            'overflowY': 'auto',
            'height': '600px',
            'border': '1px solid #ccc',
            'borderRadius': '5px',
            'marginTop': '20px',
            'backgroundColor': '#f9f9f9'
        }
    )
], style={'width': '100%', 'margin': 'auto'})

# Callback to update text display
@app.callback(
    Output('text-display', 'children'),
    Input('treemap', 'clickData')
)
def display_text(clickData):
    if clickData is None:
        return 'Click on a node to see details here.'
    else:
        category = clickData['points'][0]['label']
        data = text_data.get(category, None)

        if data is None:
            return 'No details available for this category.'
        
        # Determine the title
        title = data.get('title') or data.get('business_type_name') or category
        
        # Determine sections (supports both 'sections' and 'activities')
        sections = data.get('sections') or data.get('activities') or []
        
        if not sections:
            return html.Div([
                html.H2(title),
                html.P("No detailed sections available.")
            ])
        
        # Build the HTML structure
        children = []
        
        # Title
        children.append(html.H2(title))
        
        # Sections/Activities
        for section in sections:
            # Activity Name as a subheading
            activity_name = section.get('activity') or section.get('activity_name') or ''
            children.append(html.H3(activity_name, style={'marginTop': '20px'}))
            
            # Use cases as bullet points
            use_cases = section.get('use_cases') or []
            if use_cases:
                children.append(html.Ul([
                    html.Li(case) for case in use_cases
                ], style={'marginLeft': '20px', 'marginBottom': '10px'}))
        
        return html.Div(children, style={'lineHeight': '1.6'})

if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




