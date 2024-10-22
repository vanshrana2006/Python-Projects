import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

user_item_matrix = ratings.pivot(index='user_id', columns='movie_id', values='rating').fillna(0)
user_similarity = cosine_similarity(user_item_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

def get_recommendations(user_id, user_item_matrix, user_similarity_df, movies, n_recommendations=3):
    similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:]
    similar_users_ratings = user_item_matrix.loc[similar_users.index]
    
    weighted_ratings = similar_users_ratings.T.dot(similar_users).T
    recommendations = weighted_ratings[weighted_ratings > 0].sort_values(ascending=False).head(n_recommendations)
    
    recommended_movies = movies[movies['movie_id'].isin(recommendations.index)]
    return recommended_movies[['title', 'genre']]

user_id = 1
recommended_movies = get_recommendations(user_id, user_item_matrix, user_similarity_df, movies)
print(f"Recommended movies for User {user_id}:")
print(recommended_movies)
