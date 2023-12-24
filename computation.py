"""CSC111 Course Project: Films for You

Content and Information
===============================

This module contains functions that are not in the RecommendationSystem
class but serves as helper functions in other functions and methods.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the professors
and TAs for CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2023 Juliana Zhang and Shih-Hsin Chuang.
"""
import random
import file_reading


def popular_movies(movie_file: str, rating_file: str) -> list[str]:
    """Return a list of 50 most popular movies in the movie file given.

    The popularity of a movie is defined as its average rating, and only the movies with 30 or more user ratings will be
    considered.
    """
    more_than_30_votes = []
    file = file_reading.combined_files(movie_file, rating_file)
    for movie in file:
        if movie[4] >= 30:
            more_than_30_votes.append([movie[1], movie[3]])

    more_than_30_votes.sort(reverse=True, key=lambda x: x[1])

    return [curr_movie[0] for curr_movie in more_than_30_votes[:50]]


def random_select_movies(num: int, movie_file: str, rating_file: str) -> set:
    """Randomly return a set of a specific number of movies from the given movie file.

    The movies have ratings 5.0 or above and user reviews 3.0 or above.
    """
    return_set = set()
    movies = file_reading.movie_title_id(movie_file, rating_file)

    for _ in range(0, num):
        selected_movie = random.choice(list(movies.keys()))
        movies.pop(selected_movie)
        return_set.add(selected_movie)

    return return_set


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['file_reading', 'random'],
        'disable': ['redefined-builtin'],
        'max-line-length': 120
    })
