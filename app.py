import pandas as pd
import streamlit as st
import plotly.express as px

# Read in the file
movies_data = pd.read_csv("movies.csv")
movies_data.dropna(inplace=True)

# Function to search movie by name
def search_movie_by_name(movie_name):
    movie_info = movies_data[movies_data['name'].str.contains(movie_name, case=False)]
    return movie_info

# Function to plot movie details
def plot_movie_details(movie_info):
    if not movie_info.empty:
        st.subheader("Movie Details:")
        st.write(movie_info)
        # Plotting budget and gross revenue for the selected movie
        fig = px.bar(movie_info, x='name', y=['budget', 'gross'], title='Budget vs Gross Revenue')
        st.plotly_chart(fig)
    else:
        st.write("No movie found with the given name.")

# Sidebar - Movie search
st.sidebar.subheader("Search Movie")
movie_name = st.sidebar.text_input("Enter movie name:")

if movie_name:
    movie_info = search_movie_by_name(movie_name)
    if not movie_info.empty:
        st.write("### Movie Details:")
        st.write(movie_info.iloc[0])  # Displaying the first row of matched movie
        # Visualization for budget vs gross revenue
        st.subheader("Budget vs Gross Revenue")
        fig = px.bar(movie_info, x='name', y=['budget', 'gross'], title='Budget vs Gross Revenue', labels={'value': 'Amount ($)'})
        st.plotly_chart(fig)
    else:
        st.write("No movie found with the given name.")

# Dynamic Text and Description
st.title("Movie Analytics Dashboard")
st.write(
    """
    Welcome to the Movie Analytics Dashboard! Explore movie data, filter by various criteria, 
    and gain insights into the movie industry.
    """
)

# Visualization 1 - Bar chart for average budget by genre
st.header("Average Movie Budget by Genre")
avg_budget_genre = movies_data.groupby('genre')['budget'].mean().round().reset_index()
fig1 = px.bar(avg_budget_genre, x='genre', y='budget', title='Average Movie Budget by Genre', color='genre')
st.plotly_chart(fig1)

# Sidebar - Filters
st.sidebar.write("### Filters")
new_score_rating = st.sidebar.slider(label="Choose a score range:", min_value=1.0, max_value=10.0, value=(3.0, 4.0))
year_list = movies_data['year'].unique().tolist()
selected_years = st.sidebar.multiselect('Choose Year(s):', year_list, default=year_list)
selected_genre = st.sidebar.selectbox('Choose Genre:', ['All'] + movies_data['genre'].unique().tolist(), index=0)
selected_company = st.sidebar.selectbox('Choose Company:', ['All'] + movies_data['company'].unique().tolist(), index=0)
selected_director = st.sidebar.selectbox('Choose Director:', ['All'] + movies_data['director'].unique().tolist(), index=0)
selected_writer = st.sidebar.selectbox('Choose Writer:', ['All'] + movies_data['writer'].unique().tolist(), index=0)
selected_star = st.sidebar.selectbox('Choose Star:', ['All'] + movies_data['star'].unique().tolist(), index=0)

# Configure and filter data based on user selection
score_info = (movies_data['score'].between(*new_score_rating))
filter_conditions = (movies_data['year'].isin(selected_years))
if selected_genre != 'All':
    filter_conditions &= (movies_data['genre'] == selected_genre)
if selected_company != 'All':
    filter_conditions &= (movies_data['company'] == selected_company)
if selected_director != 'All':
    filter_conditions &= (movies_data['director'] == selected_director)
if selected_writer != 'All':
    filter_conditions &= (movies_data['writer'] == selected_writer)
if selected_star != 'All':
    filter_conditions &= (movies_data['star'] == selected_star)

# If only score range is selected, show movies filtered by score
if sum(filter_conditions) == 0 and score_info.any():
    st.header("Movies Filtered by Score Range")
    filtered_movies_by_score = movies_data[score_info]
    st.write(filtered_movies_by_score)

# Visualization 2 - Lists of movies filtered by user selection
if sum(filter_conditions) > 0:
    st.header("Movies Filtered by User Selection")
    filtered_movies = movies_data[filter_conditions]
    st.write("### Movies Filtered by User Selection (Graph)")
    st.write(filtered_movies)

# Visualization 3 - Line chart for user score of movies by genre
# Visualization 3 - Line chart for user score of movies by genre
if selected_genre != 'All':
    st.header(f"User Score of Movies in {selected_genre}")
    rating_count_year = movies_data[score_info & (movies_data['genre'] == selected_genre)].groupby('year')['score'].mean().reset_index()
    fig3 = px.line(rating_count_year, x='year', y='score', title=f"User Score of Movies in {selected_genre}", color_discrete_sequence=['blue'])
    st.plotly_chart(fig3)  # Added this line to display the chart

# Sidebar - Customize number of companies and directors to display
num_companies = st.sidebar.slider("Number of Top Companies to Display", min_value=1, max_value=len(movies_data['company'].unique()), value=20)
num_directors = st.sidebar.slider("Number of Top Directors to Display", min_value=1, max_value=len(movies_data['director'].unique()), value=20)

# Visualization 4 - Bar chart for average budget by company (customizable)
st.header("Average Movie Budget by Company")
avg_budget_company = movies_data.groupby('company')['budget'].mean().reset_index()
avg_budget_company = avg_budget_company.sort_values(by='budget', ascending=False).head(num_companies)
fig4 = px.bar(avg_budget_company, x='company', y='budget', title=f'Top {num_companies} Companies by Average Budget', color='company')
st.plotly_chart(fig4)

st.header("Top Directors by Number of Movies")
director_counts = movies_data['director'].value_counts().head(num_directors)
# Choose a color palette for the bar chart
colors = px.colors.qualitative.Plotly
fig5 = px.bar(director_counts, x=director_counts.index, y=director_counts.values, title=f'Top {num_directors} Directors by Number of Movies',
              color=director_counts.index, color_discrete_sequence=colors)
fig5.update_layout(xaxis_title="Director", yaxis_title="Number of Movies", xaxis_tickangle=-45)
st.plotly_chart(fig5)