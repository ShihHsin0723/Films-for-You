"""CSC111 Course Project: Films for You

Content and Information
===============================

This module contains the functions that are used for evaluating the accuracy
of our movie recommendations. Whether the recommendations are accurate is
determined by the percentage of overlapping movies between the training and
testing sets.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the professors
and TAs for CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2023 Juliana Zhang and Shih-Hsin Chuang.
"""
import computation, file_reading as fr, recommendation_system as rs


def testing_recommendation_accuracy(movie_file: str, rating_file: str, testing_file: str) -> list[float]:
    """Return the percetage of movie list from the testing user history that matches with the recommended movie list.
    """
    popular_users = check_popular_user(movie_file, rating_file, testing_file)
    percentage = []
    for user_tuple in popular_users:
        recommended_movies = get_recommended_movies(user_tuple[1][0:3], movie_file, rating_file)
        connected_movies = return_connected_movies(user_tuple[0], movie_file, testing_file)
        percentage.append(percent_matched(connected_movies, recommended_movies))

    return percentage


def check_popular_user(movie_file: str, rating_file: str, testing_file: str) -> list[tuple[int, list]]:
    """Return a list of tuples where the first item is the user id and the second item is a list of the user's connectd
    movies that are in our list of 50 popular movies.
    """
    popular_movies = computation.popular_movies(movie_file, rating_file)
    title_id = fr.movie_title_id(movie_file, rating_file)
    # a set of the 50 most popular movies' titles
    movie_ids = {title_id[movie_title] for movie_title in popular_movies}
    # a dictionary of users and their connected movies who are in the testing file
    users = fr.user_movies(movie_file, testing_file)

    popular_users = []

    for user_id in users:
        user_point = 0
        popular_linked_movies = set()
        for movie in users[user_id]:
            if movie in movie_ids:
                user_point += 1
                popular_linked_movies.add(movie)

        if user_point > 3:
            # converting movie ids into movie titles
            lst = [title for title in title_id if title_id[title] in popular_linked_movies]
            popular_users.append((user_id, lst))

    return popular_users


def return_connected_movies(user_id: int, movie_file: str, testing_file: str) -> list[str]:
    """Return a list of the user's connected movies (titles).
    """
    users = fr.user_movies(movie_file, testing_file)
    title_id = fr.movie_title_id(movie_file, testing_file)
    movie_ids = users[user_id]

    return [title for title in title_id if title_id[title] in movie_ids]


def get_recommended_movies(movie_list: list, movie_file: str, rating_file: str) -> list:
    """Return a list of recommended movies based on the liked movie list given using the RecommendationSystem.
    """
    system = rs.RecommendationSystem()
    system.add_movies_users(movie_file, rating_file)
    rec_movies = system.return_movies(movie_list, movie_file, rating_file)

    return [movie.title for movie in rec_movies]


def percent_matched(lst1: list, lst2: list) -> float:
    """Return the percetage that the two lists match with each other, excluding three items from the first list.
    """
    return round(len([movie for movie in lst1 if movie in lst2]) / (len(lst1) - 3), 3)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['computation', 'file_reading', 'recommendation_system'],
        'max-line-length': 120
    })
