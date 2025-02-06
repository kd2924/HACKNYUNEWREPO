import React, { useState } from "react";

function Input() {
  const [search, setSearch] = useState(""); // Input value for player name
  const [perMode, setPerMode] = useState("PerGame"); // Per mode value
  const [leagueId, setLeagueId] = useState("00"); // League ID value
  const [playerStats, setPlayerStats] = useState(null); // Player stats
  const [loading, setLoading] = useState(false); // Loading state
  const [error, setError] = useState(null); // Error state

  const fetchPlayerStats = async () => {
    const url = `http://127.0.0.1:5000/player-stats?player_name=${search}&per_mode=${perMode}&league_id=${leagueId}`;
    try {
      setLoading(true);
      setError(null);
      setPlayerStats(null);

      const response = await fetch(url, {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      setPlayerStats(data.resultSets[0].rowSet); // Extract stats
    } catch (err) {
      setError(err.message);
      setPlayerStats(null);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    if (!search.trim()) {
      setError("Please enter a player name.");
      return;
    }
    fetchPlayerStats();
  };

  return (
    <div style={styles.container}>
      <h1>NBA Player Stats</h1>
      <input
        type="text"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Enter player name"
        style={styles.input}
      />
      <select value={perMode} onChange={(e) => setPerMode(e.target.value)} style={styles.select}>
        <option value="PerGame">Per Game</option>
        <option value="Per36">Per 36 Minutes</option>
      </select>
      <select value={leagueId} onChange={(e) => setLeagueId(e.target.value)} style={styles.select}>
        <option value="00">NBA</option>
        <option value="10">G-League</option>
      </select>
      <button onClick={handleSearch} style={styles.button}>
        Search
      </button>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {playerStats && (
        <div>
          <h2>Career Stats</h2>
          <table style={styles.table}>
            <thead>
              <tr>
                <th>Season</th>
                <th>Points</th>
                <th>Rebounds</th>
                <th>Assists</th>
              </tr>
            </thead>
            <tbody>
              {playerStats.map((stat, index) => (
                <tr key={index}>
                  <td>{stat[1]}</td>
                  <td>{stat[26]}</td>
                  <td>{stat[20]}</td>
                  <td>{stat[21]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    textAlign: "center",
    padding: "20px",
    fontFamily: "Arial, sans-serif",
  },
  input: {
    padding: "10px",
    width: "300px",
    marginBottom: "10px",
    fontSize: "16px",
  },
  select: {
    padding: "10px",
    margin: "10px",
    fontSize: "16px",
  },
  button: {
    padding: "10px",
    fontSize: "16px",
    backgroundColor: "blue",
    color: "white",
    border: "none",
    cursor: "pointer",
  },
  table: {
    margin: "20px auto",
    borderCollapse: "collapse",
    width: "80%",
  },
};

export default Input;
