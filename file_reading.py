"""CSC111 Course Project: Films for You

Content and Information
===============================

This module contains functions that read and clean the datasets and sort
them into forms that allow the computation processes to be easier.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the professors
and TAs for CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2023 Juliana Zhang and Shih-Hsin Chuang.
"""
import ast
import pandas as pd


def movie_file_reading(movie_file: str) -> list:
    """Read the movie file given and clean the dataset to obtain the columns we are using, which include id, title,
    genres, vote_count, and vote_average.

    Filter out the movies with vote_average less than 5.0 out of 10.0 and return the remaing list of movies and their
    corresponding id, title, genres, vote count, and vote average.
    """
    movie_text = []
    df = pd.read_csv(movie_file, dtype={'popularity': str})
    df = df.dropna()
    df = df[df['vote_average'] >= 5.0]

    for row in df.itertuples():
        curr_id = -1 * int(row.id)
        title = str(row.title)
        genres = [curr_genre['name'] for curr_genre in ast.literal_eval(row.genres)]
        vote_avg = row.vote_average
        vote_count = int(row.vote_count)
        movie_text.append([curr_id, title, genres, vote_avg, vote_count])

    return movie_text


def rating_file_reading(rating_file: str) -> list:
    """Read and claen the rating file given to obtain the columns we are using, which include userId, movieId,
    and rating.

    Filter out the user ratings that are less than 3.0 out of 5.0 and return the remaing list of ratings and their
    corresponing user id and movie id.
    """
    rating_text = []
    df = pd.read_csv(rating_file)
    df = df.dropna()
    df = df[df['rating'] >= 3.0]

    for row in df.itertuples():
        user_id = int(row.userId)
        movie_id = -1 * int(row.movieId)
        rating = row.rating
        rating_text.append([user_id, movie_id, rating])

    return rating_text


def combined_files(movie_file: str, rating_file: str) -> list:
    """Return a list of movies like movie_file_reading but with an additional column that contains a list of linked
    users.

    The movies that do not have user reviews are excluded from the list.
    """
    movies = movie_file_reading(movie_file)
    users = rating_file_reading(rating_file)

    for movie in movies:
        viewed_users = []
        for user in users:
            if user[1] == int(movie[0]):
                viewed_users.append(user[0])

        movie.append(viewed_users)

    return_list = [curr_movie for curr_movie in movies if curr_movie[5] != []]

    return return_list


def movie_users(movie_file: str, rating_file: str) -> dict[int, set[int]]:
    """Return a dictionary that maps each movie id to a set of linked user ids. The movies that do not have user reviews
    are excluded from the dictionary.
    """
    movies = combined_files(movie_file, rating_file)
    ratings = rating_file_reading(rating_file)

    movie_users_dict = {}

    for movie in movies:
        viewed_users = set()

        for rating in ratings:
            if rating[1] == movie[0]:
                viewed_users.add(rating[0])

        movie_users_dict[movie[0]] = viewed_users

    return movie_users_dict


def user_movies(movie_file: str, rating_file: str) -> dict[int, set[int]]:
    """Return a dictionary that maps each user id to a set of reviewed movie ids. The users who do not have movie
    reviews are excluded from the dictionary.
    """
    movies = movie_users(movie_file, rating_file)
    ratings = rating_file_reading(rating_file)

    user_movies_dict = {}
    curr_user_id = None

    for rating in ratings:
        if curr_user_id != rating[0]:
            viewed_movies = set()

            add_viewed_movies(movies, curr_user_id, viewed_movies)

            if viewed_movies != set():
                user_movies_dict[curr_user_id] = viewed_movies

        curr_user_id = rating[0]

    return user_movies_dict


def add_viewed_movies(movies: dict[int, set[int]], curr_user_id: int, viewed_movies: set[int]) -> None:
    """Add movies into the user's viewed movies list if the movie is rated by the user.
    """
    for movie in movies:
        if curr_user_id in movies[movie]:
            viewed_movies.add(movie)


def movie_title_id(movie_file: str, rating_file: str) -> dict[str, int]:
    """Return a dictionary that maps each movie title to its id.
    """
    return {movie[1]: movie[0] for movie in combined_files(movie_file, rating_file)}


def return_genres(movie_file: str) -> set:
    """Return a list of all possible genres in the dataset.
    """
    movies = movie_file_reading(movie_file)
    genres = set()

    for movie in movies:
        for genre in movie[2]:
            genres.add(genre)

    return genres


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['ast', 'pandas'],
        'allowed-io': ['movie_file_reading', 'rating_file_reading'],
        'max-line-length': 120
    })
