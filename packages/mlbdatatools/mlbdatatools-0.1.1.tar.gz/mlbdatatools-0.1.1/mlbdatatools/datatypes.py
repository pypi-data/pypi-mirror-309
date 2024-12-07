from dataclasses import dataclass
from typing import List, TypeVar, Generic
from datetime import date
import pandas as pd

GenericEntry = TypeVar('GenericEntry', bound='Entry')

@dataclass
class Entry:
    def to_series(self) -> pd.Series:
        return pd.Series(self.__dict__)

class EntryList(List[GenericEntry], Generic[GenericEntry]):
    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame([e.__dict__ for e in self])

@dataclass
class Player(Entry):
    id: int # mlb.com player id
    full_name: str
    first_name: str
    last_name: str
    primary_number: str
    birth_country: str
    height: str # ft' in"
    weight: int # lbs
    current_team_id: int # team mlbam id
    primary_position_code: str # 1 - 9, 10 (DH), O (OF), Y (TWP)
    primary_position_abbrev: str # P, C, 1B, 2B, 3B, SS, LF, CF, RF, DH, OF, TWP
    bat_side: str # L, R, or S
    pitch_hand: str # L or R

@dataclass
class Team(Entry):
    id: int # mlb.com player id
    name: str
    season: int # current season/most recent
    venue_id: int # mlb.com venue id
    venue_name: str
    team_code: str # mlb.com team code
    abbreviation: str
    team_name: str
    location_name: str
    league_id: int # 103/104 for mlb teams (AL/NL)
    league_name: str
    division_id: int
    division_name: str
    sport_id: int # 1: MLB
    sport_name: str
    parent_org_id: int | None # parent organizations mlb.com team id
    parent_org_name: str | None

@dataclass
class Venue(Entry):
    id: int # mlb.com venue id
    name: str
    turf_type: str | None # Grass, Artificial Turf, etc...
    roof_type: str | None # Open, Rectractable
    left_line: int | None # not na for mlb venues
    left: int | None # can be na for mlb venues
    left_center: int | None # not na for mlb venues
    center: int | None # not na for mlb venues
    right_center: int | None # not na for mlb venues
    right: int | None # can be na for mlb venues
    right_line: int | None # not na for mlb venues
    azimuth_ange: int | None
    elevation: int | None

@dataclass
class Game(Entry):
    id: int # mlb.com game id
    type: str # R (Regular season), currently only regular season
    doubleheader: str
    season: int
    game_date: date
    game_time: str
    status_code: str
    home_team_id: int
    away_team_id: int
    home_team_name: str
    away_team_name: str
    venue_id: int
    venue_name: str
    weather_condition: str
    weather_temp: str
    weather_wind: str
    home_team_pitcher_id: int
    home_team_pitcher_name: str
    away_team_pitcher_id: int
    away_team_pitcher_name: str

@dataclass
class DefensePlay(Entry):
    fielder_id: str # mlb.com player id
    fielder_name: str
    fielder_team_id: str # mlb.com team id
    fielder_position: int
    year: str # plays are only known under mm/yy. No mapping to game, pitch, etc...
    month: str
    est_success: float # statcast est success rate
    outs_above_avg: float # statcast outs above average for fielder
    runs_prevented: float # statcast runs prevented for fielder
    is_out: bool

@dataclass
class Pitch(Entry):
    id: str
    inning: int
    ab_number: int
    batter: int
    stand: str
    pitcher: int
    p_throws: str
    team_batting_id: int
    team_fielding_id: int
    result: str
    events: str
    strikes: int
    balls: int
    outs: int
    pitch_type: str
    call: str
    pitch_call: str
    start_speed: float | None
    extension: float | None
    zone: int | None
    spin_rate: float | None
    x0: float | None
    z0: float | None
    breakx: float | None
    breakz: float | None
    inducedbreakz: float | None
    hit_speed: float | None
    hit_angle: float | None
    pitch_number: int
    gameid: int
    px: float | None
    pz: float | None
    y0: float | None
    ax: float | None
    ay: float | None
    az: float | None
    vx0: float | None
    vy0: float | None
    vz0: float | None
    hc_x_ft: float | None
    hc_y_ft: float | None
    runner_on_1b: bool
    runner_on_2b: bool
    runner_on_3b: bool
    runner_batter_score: bool
    runner_1b_score: bool
    runner_2b_score: bool
    runner_3b_score: bool

@dataclass
class BatterBoxscore(Entry):
    id: str
    playerid: int
    gameid: int
    flyouts: int
    groundouts: int
    runs: int
    homeruns: int
    strikeouts: int
    baseonballs: int
    hits: int
    atbats: int
    caughtstealing: int
    stolenbases: int
    plateappearances: int
    rbi: int
    doubles: int
    triples: int
    hitbypitch: int

@dataclass
class PitcherBoxscore(Entry):
    id: str
    playerid: int
    gameid: int
    groundouts: int
    airouts: int
    runs: int
    strikeouts: int
    baseonballs: int
    hits: int
    hitbypitch: int
    atbats: int
    numberofpitches: int
    inningspitched: float
    wins: int
    losses: int
    earnedruns: int
    battersfaced: int
    outs: int
    balls: int
    strikes: int

@dataclass
class GamefeedResponse:
    game: Game
    pitches: EntryList[Pitch]
    batter_boxscores: EntryList[BatterBoxscore]
    pitcher_boxscores: EntryList[PitcherBoxscore]

@dataclass
class GamefeedsResponse:
    games: EntryList[Game]
    pitches: EntryList[Pitch]
    batter_boxscores: EntryList[BatterBoxscore]
    pitcher_boxscores: EntryList[PitcherBoxscore]