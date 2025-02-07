from flask import Flask, jsonify, request
from flask_cors import CORS 
import requests #rayat imported this to manually test the api key and also to manually make API calls. 
#from nba_api.stats.endpoints import playercareerstats
#from nba_api.stats.static import players

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend 

#this is where im gonna put the api key and the host. Rayat work: 
NBA_apiKey = 'f90dce8000msh2b1dfb6b42ed454p1b97dbjsna0f344935adf'
NBA_apiHost = 'api-nba-v1.p.rapidapi.com' 

@app.route('/')
def home():
    return "Welcome to the NBA Stats API! Use the /player-stats endpoint to get player statistics."

@app.route('/player-stats', methods=['GET']) #basically maps a specific url

def get_player_stats():
    # Get the player's name from query parameters
    player_name = request.args.get('player_name')
    per_mode = request.args.get('per_mode', 'PerGame')  # Default to "PerGame"
    league_id = request.args.get('league_id', '00')  # Default to NBA league ("00")

    if not player_name:
        return jsonify({"error": "Player name is required"}), 400 #returns a error basically. 

#according to the prev repo we had like a url thing i remember so it would be like this: 

    # Search for the player by name
    player_list = players.find_players_by_full_name(player_name) #assuming players are stored in a list and using a function to get players name.
    
    if not player_list:
        return jsonify({"error": "Player not found"}), 404

    player = player_list[0]  # Take the first match
    player_id = player['id'] #output the player name along with their id. 

    try:
        # Fetch career stats for the player 
        #changed playercareerstats
        career_stats = NBA_apiHost.PlayerCareerStats(
            player_id=player_id,
            per_mode36=per_mode,
            league_id_nullable=league_id
        )
        #career stats 
        stats = career_stats.get_dict() #Stats are stored in a dictionary. 

        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
