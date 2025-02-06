from flask import Flask, jsonify, request
from flask_cors import CORS
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

@app.route('/')
def home():
    return "Welcome to the NBA Stats API! Use the /player-stats endpoint to get player statistics."

@app.route('/player-stats', methods=['GET'])
def get_player_stats():
    # Get the player's name from query parameters
    player_name = request.args.get('player_name')
    per_mode = request.args.get('per_mode', 'PerGame')  # Default to "PerGame"
    league_id = request.args.get('league_id', '00')  # Default to NBA league ("00")

    if not player_name:
        return jsonify({"error": "Player name is required"}), 400

    # Search for the player by name
    player_list = players.find_players_by_full_name(player_name)
    if not player_list:
        return jsonify({"error": "Player not found"}), 404

    player = player_list[0]  # Take the first match
    player_id = player['id']

    try:
        # Fetch career stats for the player
        career_stats = playercareerstats.PlayerCareerStats(
            player_id=player_id,
            per_mode36=per_mode,
            league_id_nullable=league_id
        )
        stats = career_stats.get_dict()

        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
