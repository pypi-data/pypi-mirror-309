# MLB Data Tools
DataFrames, type-safety, and plotting for modern baseball analytics.

## Philosophy & Goals
- Expose useful endpoints and datasets (Savant Player Pages, OAA data by play, pitch by pitch statcast)
- Defined data schema/types
- Easily convert to DataFrames

## Example Usage
```py
from mlbdatafetch import mlbfetch

all_players = mlbfetch.players(sport_id=1, season=2024)

player = all_players[0]
print(player.full_name, player.primary_position_code)

players_df = all_players.to_df()
players_df.head(1)

```
```
Andrew Abbot P
```
|   | id     | full_name    | first_name | last_name | primary_number | ... |
| - | ------ | ------------ | ---------- | --------- | -------------- | --- |
| 0 | 671096 | Andrew Abbot | Andrew     | Abbot     | 41             | ... |

<!-- ## Future Supported Endpoints
- savant player pages
- savant park factors
- statsapi schedule -->
