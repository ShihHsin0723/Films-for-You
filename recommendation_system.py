"""CSC111 Course Project: Films for You

Content and Information
===============================

This module contains the a collection of Python classes that represent
the movie recommendation system, movies, and users.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the professors
and TAs for CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2023 Juliana Zhang and Shih-Hsin Chuang.
"""
from __future__ import annotations
from typing import Union, Any
import computation, file_reading


# @check_contracts
class RecommendationSystem:
    """A movie recommendation system that contains movie and user vertices who are connected to each other based on
    review history.

    Representation Invariants:
        - all([id == self._vertices[id].user_id for id in self._vertices if isinstance(self, User)])
        - all([id == self._vertices[id].movie_id for id in self._vertices if isinstance(self, Movie)])
    """
    _vertices: dict[int, Union[User, Movie]]

    def __init__(self) -> None:
        """Initialize an empty recommendation system (no vertices or edges)."""
        self._vertices = {}

    def add_movies_users(self, movie_file: str, rating_file: str) -> None:
        """Add movies and users as vertices into the recommendation system and add an edge between each user and each of
        their rated movie.

        The information about movies and users is based on the existing datasets.
        """
        file = file_reading.combined_files(movie_file, rating_file)

        for movie in file:
            self.add_movie_vertex(movie[0], movie[1], movie[3], movie[4], movie[2])

            for user_id in movie[5]:
                self.add_user_vertex(user_id)
                self.add_edge(user_id, movie[0])

    def return_movies(self, liked_movies: list[str], movie_file: str, rating_file: str) -> set[Movie]:
        """Return a set of at least 50 recommended movies that are chosen based on similar past users.

        Prioritize the movies that are connected to the users who have the highest number of points, which means they
        are the most similar past users to the current user.

        If there is no movie with similar users, randomly select and return 50 movies from the existing datset.

        Preconditions:
            - len(liked_movies) == 3
        """
        recommended_movies = set()
        users_info = file_reading.user_movies(movie_file, rating_file)

        # Get a set of similar users
        users = self.return_similar_users(liked_movies, movie_file, rating_file)

        for user in users:
            if user.point == 3:
                recommended_movies = recommended_movies.union(users_info[user.user_id])

        if len(recommended_movies) < 50:
            for user in users:
                if user.point == 2:
                    recommended_movies = recommended_movies.union(users_info[user.user_id])

        if len(recommended_movies) < 50:
            for user in users:
                if user.point == 1:
                    recommended_movies = recommended_movies.union(users_info[user.user_id])

        if len(recommended_movies) < 50:
            movie_subset = computation.random_select_movies(0 - len(recommended_movies), movie_file, rating_file)
            recommended_movies.union(movie_subset)

        movies = {self._vertices[movie] for movie in recommended_movies if self._vertices[movie].title not in
                  liked_movies}

        return movies

    def return_similar_users(self, liked_movies: list[str], movie_file: str, rating_file: str) -> set[User]:
        """Return a set of users who have watched at least one of the movies given. In other words, if the number of
        points the user has is greater than or equal to 1.

        Increase the user's point by one for each movie given that is connected to the movie.

        Preconditions:
            - len(liked_movies) == 3
        """
        movie_title_id = file_reading.movie_title_id(movie_file, rating_file)
        movie_ids = [movie_title_id[title] for title in liked_movies]
        users_info = file_reading.user_movies(movie_file, rating_file)
        users = set()

        for user_id in users_info:
            user = self._vertices[user_id]
            for movie_id in movie_ids:
                if movie_id in users_info[user_id]:
                    user.point += 1

            if user.point >= 1:
                users.add(user)

        return users

    def apply_filters(self, movie_set: set[Movie], genre: str) -> list[tuple[str, list[str], float]]:
        """Return a list of three movies, their genres, and average ratings. The returned movies belong to the
        genre given and are sorted based on their average ratings.

        If there are less than three movies that belong to the specified genre, fill the movie list with the ones with
        the highest ratings.

        Preconditions:
            - genre in file_reading.return_genres()
        """
        movie_vertex = list(movie_set)

        movie_list = []
        for movie in movie_vertex:
            if genre in movie.genre:
                movie_list.append(movie)

        movie_list.sort(key=lambda curr_movie: curr_movie.avg_rating, reverse=True)
        final_movie_list = [(curr_movie.title, curr_movie.genre, curr_movie.avg_rating)
                            for curr_movie in movie_list[0:3]]

        if len(final_movie_list) < 3:
            movie_vertex.sort(key=lambda curr_movie: curr_movie.avg_rating, reverse=True)
            final_movie_list += [(curr_movie.title, curr_movie.genre, curr_movie.avg_rating) for curr_movie in
                                 movie_vertex if curr_movie not in movie_list][0:3 - len(final_movie_list)]

        return final_movie_list

    def add_reviews(self, title: str, rating: float, movie_file: str, rating_file: str) -> None:
        """Add an edge between the movie vertex with given title and the user with given id.

        Recalculate the average rating of the movie with the new rating added. Increase the number of reviewers for the
        movie by one.

        If the movie is not in the system yet, assign a new id to it and add it to the system. The new id is generated
        based on the number follow the current last movie id (or the largest id) in the system.

        Preconditions:
            - 0.0 <= rating <= 10.0
        """
        movie_title_id = file_reading.movie_title_id(movie_file, rating_file)

        if title not in movie_title_id:
            movie_file = file_reading.movie_file_reading(movie_file)
            movie_id = movie_file[-1][0] + 1
            self.add_movie_vertex(movie_id, title, rating, 1)

        else:
            movie_id = movie_title_id[title]
            total_score = self._vertices[movie_id].avg_rating * self._vertices[movie_id].num_users + rating
            self._vertices[movie_id].num_users += 1
            self._vertices[movie_id].avg_rating = total_score / self._vertices[movie_id].num_users

        rating_file = file_reading.rating_file_reading(rating_file)
        user_id = rating_file[-1][0] + 1
        self.add_user_vertex(user_id)

        self.add_edge(user_id, movie_id)

    def return_avg_rating(self, title: str) -> Any:
        """Return the average rating for a movie.

        Return None is there is no such a movie found in the system.
        """
        for vertex in self._vertices:
            if isinstance(self._vertices[vertex], Movie):
                if title == self._vertices[vertex].title:
                    return round(self._vertices[vertex].avg_rating, 2)

        return None

    def add_user_vertex(self, user_id: int) -> None:
        """Add a user vertex with the given user id to this recommendation system.

        The new user vertex is not connected to any other movie vertices.
        """
        self._vertices[user_id] = User(user_id, set())

    def add_movie_vertex(self, movie_id: int, title: str, avg_rating: float, num_users: int, genre: list[str] = None) \
            -> None:
        """Add a movie vertex with the given movie id and information to this recommendation system.

        The new movie vertex is not connected to any other user vertices.
        """
        self._vertices[movie_id] = Movie(movie_id, set(), title, genre, avg_rating, num_users)

    def add_edge(self, user_id: int, movie_id: int) -> None:
        """Add an edge between the two vertices with the given user and movie ids in this recommendation system.

        Raise a ValueError if the user or the movie do not appear as vertices in this system.

        Preconditions:
            - user_id != movie_id
        """
        if user_id in self._vertices and movie_id in self._vertices:
            user = self._vertices[user_id]
            movie = self._vertices[movie_id]

            user.reviewed_movies.add(movie)
            movie.linked_users.add(user)
        else:
            raise ValueError


# @check_contracts
class Vertex:
    """An abstract class representing a vertex, which can either be a movie or a user.

    This class can be subclassed to implement different types of vertecies (User or Movie).
    """


# @check_contracts
class User(Vertex):
    """A User vertex, which contains information about the movies the user rated and the number of points it has.

    Instance Attributes:
        - user_id: The unique id that represents the user.
        - reviewed_movies: The movie vertices that are connected to this user vertex.
        - point: The number of point the user has with a defualt value 0.

    Representation Invariants:
        - self not in self.reviewed_movies
        - all(self in u.linked_users for u in self.reviewed_movies)
    """
    user_id: int
    reviewed_movies: set[Vertex]
    point: int

    def __init__(self, user_id: int, reviewed_movies: set[Movie], point: int = 0) -> None:
        """Initialize a new user vertex with the user id and corresponding reviewed movies. The number of point
        is set as 0 for default.
        """
        self.user_id = user_id
        self.reviewed_movies = reviewed_movies
        self.point = point


# @check_contracts
class Movie(Vertex):
    """A Movie vertex, which contains the information about the movie and users who rated the movie.

    Instance Attributes:
        - movie_id: The unique id that represents this movie.
        - linked_users: The user vertices that are connected to this movie vertex.
        - title: The title of this movie.
        - genre: The genres of this movie.
        - avg_rating: The average rating of this movie.
        - num_users: The number of users who rate this movie

    Representation Invariants:
        - self not in self.linked_users
        - all(self in u.reviewed_movies for u in self.linked_users)
    """
    movie_id: int
    linked_users: set[Vertex]
    title: str
    genre: list[str]
    avg_rating: float
    num_users: int

    def __init__(self, movie_id: int, linked_users: set[User], title: str, genre: list[str],
                 avg_rating: float, num_users: int) -> None:
        """Initialize a new movie vertex with the given movie id and linked users and other information."""
        self.movie_id = movie_id
        self.linked_users = linked_users
        self.title = title
        self.genre = genre
        self.avg_rating = avg_rating
        self.num_users = num_users


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['file_reading', 'computation'],
        'disable': ['unused-import', 'too-many-arguments'],
        'max-line-length': 120
    })
