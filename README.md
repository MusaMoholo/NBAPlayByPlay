This project is a comprehensive machine learning pipeline designed to predict the outcomes of individual plays during NBA games using highly granular play-by-play data.
By focusing on each individual event—rather than aggregate statistics like per-game or per-quarter metrics—it achieves significantly higher prediction accuracy, eliminating the need to assume interdependencies between player and team-level statistics. 
With millions of rows of data scraped from five full seasons of NBA games, each row represents a discrete event within a game, such as a two-point shot attempt, a defensive rebound, or a turnover.
Every event captures rich contextual information, including game state, player combinations, possession sequences, and defensive matchups, allowing us to build highly specialized predictive models.

The pipeline leverages XGBoost models trained for each distinct play type, ensuring predictions are precisely tailored to the unique dynamics of each event. 
Extensive feature engineering captures not only immediate game context but also underlying patterns, incorporating player involvement, historical performance, and detailed game state variables. 
This individualized modeling approach avoids overly simplistic assumptions about interactions between features, improving the accuracy and reliability of predictions.

Data preprocessing involved transforming five seasons of play-by-play data into structured datasets with millions of clean, labeled rows. 
Rigorous cross-validation ensures the models generalize well to unseen data, and hyperparameter tuning optimizes their performance. 
The result is a powerful predictive framework that offers unparalleled granularity, enabling entire games to be simulated realistically at the play level. 
This level of detail has broad applications, including sports betting, advanced game strategy analysis, and predictive analytics for front-office decision-making.
