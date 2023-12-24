"""CSC111 Course Project: Films for You

Content and Information
===============================

This Python module contains the functions and Tkinter widgets
that constitute the graphical user interface.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the professors
and TAs for CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2023 Juliana Zhang and Shih-Hsin Chuang.
"""
import tkinter as tk
from tkinter.ttk import Notebook
from pathlib import Path
import recommendation_system as rs
import computation, file_reading
import cProfile



def interface(system: rs.RecommendationSystem, movie_file: str, rating_file: str) -> None:
    """Run the pop-up graphical user interface using the tkinter library
    >>> cProfile.runctx('interface(system, movie_file, rating_file)', globals=globals(), locals=locals())
    """
    # create a recommendation system and populate it with movies and users

    system = rs.RecommendationSystem()
    system.add_movies_users(movie_file, rating_file)

    # functions
    def get_recommended_movies(lst: list, genre: str) -> None:
        """Generate and display the top 3 recommended movies for the user based on their movie history and
        preferred genre"""
        movies = system.return_movies(lst, movie_file, rating_file)
        results = system.apply_filters(movies, genre)
        clear_frame(recommendation_tab)
        text1 = "Here are your top 3 recommended movies:"
        tk.Label(recommendation_tab, text=text1, font=("Helevetica", 15, "bold"), fg="midnight blue").pack()
        rank = 1

        for result in results:
            tk.Label(recommendation_tab, text=f'{rank}. {result[0]}', font=("Helevetica", 15, "bold")).pack()
            genres = ', '.join(result[1])
            tk.Label(recommendation_tab, text=f'Genre: {genres}', font=("Helevetica", 15)).pack()
            tk.Label(recommendation_tab, text=f'Rating: {result[2]}', font=("Helevetica", 15)).pack()
            rank += 1

    def get_filter_frame() -> None:
        """Create and display the widgets associated with the genre filtering process.

        This includes a drop-down menu containing the genres of the movies in the dataset,
        as well as a button that triggers the recommendation stage."""
        text2 = "Step 2: Select your desired movie genre:"
        tk.Label(recommendation_tab, text=text2, font=("Helevetica", 15, "bold"), fg="midnight blue").pack()

        genre_options = list(file_reading.return_genres(movie_file))

        genre_value = tk.StringVar(recommendation_tab)
        genre_value.set("Select a movie genre")

        genre_menu = tk.OptionMenu(recommendation_tab, genre_value, *genre_options)
        genre_menu.pack()

        tk.Button(recommendation_tab, text="Enter",
                  command=lambda: [return_filters(genre_value),
                                   get_recommended_movies(top_3, return_filters(genre_value))]).pack()

    def add_review() -> None:
        """Add the name and rating of the user's reviewed movie into the recommendation system graph"""
        review = [f'{e1.get()}', float(f'{e2.get()}')]
        system.add_reviews(review[0], review[1], movie_file, rating_file)
        clear_frame(review_tab)
        tk.Label(review_tab, text="Thank you for your review!", font=("Helevetica", 15, "bold"),
                 fg="midnight blue").pack()

    def clear_frame(f: tk.Frame) -> None:
        """Clear the widgets in the given frame."""
        for widget in f.winfo_children():
            widget.destroy()

    def return_filters(user_selection: tk.StringVar) -> str:
        """Return a string of the user's selected genre."""
        return f'{user_selection.get()}'

    # creating and setting up the main window
    window = tk.Tk()
    window.geometry("1000x1000")
    window.title("Films for You")
    window.configure(bg="gray15")

    tk.Label(window, text="Films for You", font=("Helevetica", 50, "bold"), bg="gray15", fg="white").pack()

    # creating the tab control and tabs
    tab_control = Notebook(window)

    home_tab = tk.Frame(tab_control)
    recommendation_tab = tk.Frame(tab_control)
    review_tab = tk.Frame(tab_control)

    tab_control.add(home_tab, text="Home")
    tab_control.add(recommendation_tab, text="Movie Recommendations")
    tab_control.add(review_tab, text="Write a Review")
    tab_control.pack(expand=tk.TRUE, fill=tk.BOTH)

    # creating a scroll bar
    canvas = tk.Canvas(recommendation_tab, highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

    scrollbar = tk.Scrollbar(recommendation_tab, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind(
        '<Configure>', lambda x: canvas.configure(scrollregion=canvas.bbox("all")))

    scroll_frame = tk.Frame(canvas)
    canvas.create_window((200, 0), window=scroll_frame, anchor="nw")

    # loading the logo image
    directory = Path(__file__).parent.absolute()
    path = directory / "Logo.ppm"
    img = tk.PhotoImage(file=str(path))
    resized_img = img.subsample(10, 10)

    # home tab
    tk.Label(home_tab, image=resized_img).grid(row=0, column=0)
    tk.Label(home_tab, width=14).grid(row=0, column=1)
    text3 = "Welcome to Films for You"
    tk.Label(home_tab, text=text3, font=("Helevetica", 30, "bold"), fg="midnight blue").grid(row=0, column=2)
    text4 = "Get personalized movie recommendations for your next movie night"
    tk.Label(home_tab, text=text4, font=("Times", 25, "bold")).place(x=100, y=280)
    tk.Label(home_tab, text="or write your own movie review.", font=("Times", 25, "bold")).place(x=300, y=320)
    text5 = "Choose your preferred configuration to get started today!"
    tk.Label(home_tab, text=text5, font=("Times", 20)).place(x=240, y=380)

    # recommendation tab
    text6 = "Step 1: Select your top three choices from the following popular movies:"
    tk.Label(scroll_frame, text=text6, font=("Helevetica", 15, "bold"), fg="midnight blue").pack()

    # displaying a list of 50 popular movies into checkboxes and extracting the user's top 3 choices
    pop_movies = computation.popular_movies(movie_file, rating_file)
    top_3 = []

    for movie in pop_movies:
        var = tk.IntVar()
        box = tk.Checkbutton(scroll_frame, text=movie, variable=var, command=lambda x=movie: top_3.append(x))
        box.pack()

    tk.Button(scroll_frame, text="Enter", command=lambda: [clear_frame(recommendation_tab), get_filter_frame()]).pack()

    # review tab
    text7 = "Please enter the name of the movie you wish to review:"
    tk.Label(review_tab, text=text7, font=("Helevetica", 15, "bold"), fg="midnight blue").pack()
    e1 = tk.Entry(review_tab)
    e1.pack()
    text8 = "Please enter your rating out of 10.0:"
    tk.Label(review_tab, text=text8, font=("Helevetica", 15, "bold"), fg="midnight blue").pack()
    e2 = tk.Entry(review_tab)
    e2.pack()

    tk.Button(review_tab, text="Enter", command=add_review).pack()

    window.mainloop()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'tkinter.ttk', 'pathlib', 'recommendation_system', 'computation', 'file_reading'],
        'max-line-length': 120,
        'disable': ['E1120', 'too-many-locals', 'too-many-statements']
    })
