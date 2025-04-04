from flask import Flask, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load CSV and process data
def process_data():
    file_path = "FinalStack_Over_Flow_Data_Tags(2023-2025).csv"
    df = pd.read_csv(file_path)
    
    # Convert Published Date to Year
    df['Year'] = pd.to_datetime(df['Published Date']).dt.year
    
    # Count occurrences of each tag per year
    tag_trends = df.groupby(['Year', 'Tag']).size().reset_index(name='Count')
    
    # Get the total count of all tags per year
    yearly_totals = tag_trends.groupby('Year')['Count'].sum()
    
    # Calculate percentage of each tag relative to the total tags that year
    tag_trends['Percentage'] = tag_trends.apply(lambda row: (row['Count'] / yearly_totals[row['Year']]) * 100, axis=1)

    # Get the top 15 tags overall based on total count
    top_tags = tag_trends.groupby('Tag')['Count'].sum().nlargest(15).index
    
    # Filter data to include only top 15 tags
    filtered_data = tag_trends[tag_trends['Tag'].isin(top_tags)]
    
    return filtered_data

@app.route('/')
def index():
    return render_template('index.html')  # Ensure index.html exists in a "templates" folder

@app.route('/data')
def get_data():
    data = process_data()
    response = data.pivot(index='Year', columns='Tag', values='Percentage').fillna(0).to_dict()
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
