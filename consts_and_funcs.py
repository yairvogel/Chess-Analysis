import datetime as dt
import pandas as pd
import numpy as np
import seaborn as sns

one_year = dt.timedelta(days=365)
year_ago = dt.datetime.today() - one_year

def include_none(func, bool_ret=False):
    neg_ret_val = False if bool_ret else None
    def wrapper(*args):
        if args[0] and args[0] != np.nan:
            return neg_ret_val
        return func(args[0])
    return wrapper

sns.set(style='whitegrid')

games = pd.read_csv('datasets/games.csv', parse_dates=True, index_col='game_id')
games['end_time'] = pd.to_datetime(games.end_time)

f_last_year = games.end_time > year_ago
f_white = games.color_played == 'White'
f_black = ~f_white
f_above1450 = games.rival_rating >= 1450

top10 = set(games\
            .loc[f_last_year]\
            .groupby('opening')\
            .size()\
            .sort_values(ascending=False)\
            .head(5).index.tolist())
f_top10 = games.opening.apply(lambda x: x in top10)

g_months = games.end_time.apply(lambda x: dt.datetime(x.year, x.month, 1))

def color_openings(fil):
    return games.loc[fil]\
            .groupby('opening')\
            .size()\
            .sort_values(ascending=False)\
            .head(5)


def philidor_moves(x):
    PHILIDOR_MOVES = '1. e4 e5 2. Nf3 d6'
    if type(x) != str:
        return None
    return x.startswith(PHILIDOR_MOVES)

chess_scores_dict = {'win': 1, 'draw': .5, 'loss': 0}
chess_scores = lambda x: chess_scores_dict[x]
soccer_scores_dict = {'win': 3, 'draw': 1, 'loss': 0}
soccer_scores = lambda x: soccer_scores_dict[x]

def browns(n):
     return sns.cubehelix_palette(n, start=1.2, rot=0, dark=.35
                            , light=.7)

def to_rgb(array):
    f = np.vectorize(lambda x: hex(int(x))[2:])
    array = list(f(array))
    return '#' + ''.join(array)


c_white = np.array([221]*3)
c_black = np.array([100, 84, 68])

def extract_move(moves, move_num, color='white', show_line=False):
    c_map = {'white': 1, 'black': 2}
    if not moves or type(moves) == float:
        return None
    moves = moves.split()
    # moves = iter(moves)
    # moves = list(zip(moves, moves, moves))
    if move_num > len(moves):
        return None
    if not show_line:
        return moves[3*move_num + c_map[color]]
    return ' '.join(moves[:3*move_num + c_map[color] + 1])