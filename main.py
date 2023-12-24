"""CSC111 Course Project: Films for You

Content and Information
===============================

This Python module consists of the code necessary to run the entire movie recommendation
system from start to finish.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the professors
and TAs for CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2023 Juliana Zhang and Shih-Hsin Chuang.
"""
import interface
import recommendation_system as rs

# create a recommendation system and populate it with movies and users
system = rs.RecommendationSystem()
system.add_movies_users('data/movies_metadata.csv', 'data/ratings_small.csv')

# call the interface function that creates an interactive user interface
interface.interface(system, 'data/movies_metadata.csv', 'data/ratings_small.csv')
