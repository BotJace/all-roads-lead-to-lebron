import os
import json
import time
from nba_api.stats.endpoints import commonallplayers, playercareerstats, commonteamroster

# Save paths relative to the script location
# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DATA_DIR = os.path.join(SCRIPT_DIR, "../public/data")
BASE_DATA_DIR = os.path.normpath(BASE_DATA_DIR)  # Normalize the path

os.makedirs(f"{BASE_DATA_DIR}/players", exist_ok=True)
os.makedirs(f"{BASE_DATA_DIR}/teams", exist_ok=True)

print(f"Data will be saved to: {os.path.abspath(BASE_DATA_DIR)}")
print(f"Players directory: {os.path.abspath(f'{BASE_DATA_DIR}/players')}")
print(f"Teams directory: {os.path.abspath(f'{BASE_DATA_DIR}/teams')}")

def crawl_nba_network(after_year=2020):
    """
    Crawls NBA data starting from a specific year.
    Stores results as JSON in the public/data folder.
    """
    current_year = 2025
    player_ids_to_fetch = set()

    for year in range(after_year, current_year + 1):
        season_str = f"{year}-{str(year+1)[-2:]}"
        print(f"--- Processing {season_str} ---")
        
        try:
            # 1. Get all players for this season to find the teams
            all_players = commonallplayers.CommonAllPlayers(
                is_only_current_season=0, season=season_str
            ).get_data_frames()[0]
            
            # Filter unique Team IDs (excluding Free Agents / ID 0)
            valid_teams = all_players[all_players['TEAM_ID'] != 0]['TEAM_ID'].unique()
            
            # 2. Save Roster for each Team in this Season
            for team_id in valid_teams:
                team_file = f"{BASE_DATA_DIR}/teams/{team_id}_{season_str}.json"
                if not os.path.exists(team_file):
                    print(f"  Fetching Roster: Team {team_id} ({season_str})")
                    try:
                        roster = commonteamroster.CommonTeamRoster(team_id=team_id, season=season_str).get_data_frames()[0]
                        roster.to_json(team_file, orient='records')
                        # Verify file was created
                        if os.path.exists(team_file):
                            print(f"    ✓ Saved to {team_file} ({os.path.getsize(team_file)} bytes)")
                        else:
                            print(f"    ✗ ERROR: File not created at {team_file}")
                        time.sleep(0.8) # Critical rate limit buffer
                    except Exception as e:
                        print(f"    ✗ Error saving team {team_id}: {e}")

            # Build a list of player IDs to get career paths later
            player_ids_to_fetch.update(all_players['PERSON_ID'].tolist())

        except Exception as e:
            print(f"  Error in {season_str}: {e}")

    # 3. Save Career Path for every player found
    print(f"--- Saving {len(player_ids_to_fetch)} player career paths ---")
    saved_count = 0
    error_count = 0
    skipped_count = 0
    
    for idx, p_id in enumerate(player_ids_to_fetch, 1):
        p_file = f"{BASE_DATA_DIR}/players/{p_id}.json"
        if not os.path.exists(p_file):
            try:
                career = playercareerstats.PlayerCareerStats(player_id=p_id).get_data_frames()[0]
                # Filter out the "TOT" trade summary rows
                career = career[career['TEAM_ABBREVIATION'] != 'TOT']
                career.to_json(p_file, orient='records')
                # Verify file was created
                if os.path.exists(p_file):
                    saved_count += 1
                    if idx % 100 == 0 or idx <= 5:  # Show first 5 and then every 100
                        print(f"  Progress: {idx}/{len(player_ids_to_fetch)} - Saved player {p_id} ({os.path.getsize(p_file)} bytes)")
                else:
                    error_count += 1
                    print(f"  ✗ ERROR: File not created for player {p_id} at {p_file}")
                time.sleep(0.7)
            except Exception as e:
                error_count += 1
                if error_count <= 10:  # Print first 10 errors for debugging
                    print(f"  Error fetching player {p_id}: {e}")
                elif error_count == 11:
                    print(f"  (Suppressing further error messages...)")
                continue
        else:
            skipped_count += 1
    
    print(f"--- Complete: Saved {saved_count}, Skipped {skipped_count}, Errors {error_count} ---")

if __name__ == "__main__":
    crawl_nba_network(after_year=2023)