# League of Legends Draft Recommendation AI

### Overview

This project is a machine learning model that recommends champions during the draft phase in League of Legends based on real match data retrieved from the official Riot Games API.

The system analyzes:
 - Player role
 - Current picks and bans
 - Player historical statistics per champion

It then predicts the most favorable champion choice using a neural network built with TensorFlow / Keras.

### Data Source

Data is collected exclusively through the Riot API:
 - Match history retrieval
 - Full match details
 - Draft compositions and results

Only public match data is used. The project does not interact with the game client and respects Riot’s rate limits.
