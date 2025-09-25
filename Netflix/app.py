from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
CSV_PATH = 'netflix_cleaned.csv'

@app.route('/', methods=['GET', 'POST'])
def home():
    # Load the cleaned CSV file
    df = pd.read_csv(CSV_PATH)
    filter_option = request.form.get('content_type', 'All')

    # Apply filter if selected
    if filter_option != 'All':
        df = df[df['type'] == filter_option]

    # Top 10 directors (excluding 'Unknown' and NaN)
    top_directors = (
        df[df['director'].notnull() & (df['director'] != 'Unknown')]
        .groupby('director').size().sort_values(ascending=False).head(10)
        .reset_index(name='count')
        .to_dict(orient='records')
    )

    # Top 10 countries (excluding 'Unknown' and NaN)
    top_countries = (
        df[df['country'].notnull() & (df['country'] != 'Unknown')]
        .groupby('country').size().sort_values(ascending=False).head(10)
        .reset_index(name='count')
        .to_dict(orient='records')
    )

    return render_template(
        'index.html',
        top_directors=top_directors,
        top_countries=top_countries,
        selected_type=filter_option
    )

if __name__ == "__main__":
    app.run(debug=True)