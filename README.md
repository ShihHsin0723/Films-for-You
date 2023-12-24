# Films for You
**How can we optimize the movie selection process by making recommendations based on user movie history and community reviews?**

Films for You is a movie recommendation system that utilizes the collaborative filtering technique to offer movie recommendations by comparing a user’s behaviour to others in the system. This involves finding users with similar movie patterns and recommending some of the other movies they have liked to the current user.

## Functionalities 
1. **View Movie Recommendations**: The user selects three movies they have watched and liked in the past from a list of the 50 most popular movies. The  user will also be able to specify their preferred movie genre, and the system will provide a ranking of the top three films it recommends to the user.
2. **Add Movie Reviews**: The user adds their own movie review by entering the name of the movie they wish to review and the rate of the movie out of 10.0.

## Running the Program
1. Download the files
2. Unzip the **`data.zip`** file
3. Run the **`main.py`** file

## Technical Documentation
- The data is drawn from “The Movies Dataset”, which is a real-world dataset that contains over 45, 000 movies and 26 million ratings from over 270, 000 users. 
- The front end is constructed with Python's `TKinter` library - **`interface.py`** contains the main window GUI.
