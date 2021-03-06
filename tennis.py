import random


class Player(object):
    """
    Player has a name and a skill indicator from 0.0 to 1.0
    """
    def __init__(self, name, skill):
        assert 0 <= skill <= 1, "skill should be from 0 to 1"
        self.name = name
        self.skill = float(skill)

    def get_skill(self):
        return self.skill

    def get_name(self):
        return self.name


class Score(object):
    def __init__(self, balls, diff, min_games, max_games, games_diff,
                 min_sets):
        """
        balls - min. number of balls in game (15-30-40 means 3)
        diff - difference needed to win a game (usually 2)
        min_games - max. number of games required to win a set
        max_games - max. number of games required to win a set
        games_diff - games diff required to win if less than max_games
        min_sets - min. number of sets to win a match
        """
        assert balls > 0, "balls > 0 "
        assert diff > 0, "diff > 0 "
        assert min_games > 0, "min_games > 0 "
        assert max_games > 0, "max_games > 0 "
        assert games_diff > 0, "games_diff > 0"
        assert min_sets > 0, "min_sets > 0 "
        self.balls = balls
        self.diff = diff
        self.min_games = min_games
        self.max_games = max_games
        self.games_diff = games_diff
        self.min_sets = min_sets

#Formula to simulate a match in five sets (three needed to win)
#classic_score = Score(3, 2, 6, 7, 2, 3)


def ball_result(player1, player2, std1=0.1, std2=0.0, boundary=1.0):
    """
    The result (res) depends mainly on both players' skills and some random
    noise.
    If res falls outside [-boundary/2, boundary/2], then one player scores.
    Otherwise, players score depending on their cumulative skills (prob_error).
    If they are good players, errors are rarer.
    std1, std2 and boundary are parameters used for fine tuning.
    
    """
    # Calculate the skill differential and add some random noise:
    res = player1.get_skill() - player2.get_skill() + \
        (random.random()-0.5)*std1
    # If outside boundaries ( = clear cut outcome), return result
    if res < -boundary/2.0:
        return 2
    elif res > boundary/2.0:
        return 1
    # If not outside boundaries:
    else:
        # Calculate some cumulative probability of an error in the exchange
        # If no error, return 0
        prob_error = 1.0 - (player1.get_skill()+player2.get_skill())/2.0
        if random.random() > prob_error:
            return 0
        # Otherwise, randomize error according to skills and weigh with std2
        else:
            if random.random() < (player1.get_skill() + std2) / \
                    (player1.get_skill() + player2.get_skill() + 2*std2):
                return 1
            else:
                return 2

        
def convert_scores(ball_count1, ball_count2, diff):
    """
    Useful to display the score.
    """
    game_dict = {0: 0, 1: 15, 2: 30, 3: 40}
    score1 = ''
    score2 = ''
    if ball_count1 < 4:
        score1 = game_dict[ball_count1]
    if ball_count2 < 4:
        score2 = game_dict[ball_count2]
    if ball_count1 >= 4 or ball_count2 >= 4:
        if ball_count1 - ball_count2 >= diff:
            score1 = 'WON'
            score2 = 'LOST'
        elif ball_count2 - ball_count1 >= diff:
            score1 = 'LOST'
            score2 = 'WON'
        elif ball_count1 > ball_count2:
            score1 = 'A'
            score2 = '-'
        elif ball_count2 > ball_count1:
            score1 = '-'
            score2 = 'A'
        elif ball_count1 == ball_count2:
            score1 = 'D'
            score2 = 'D'
    return score1, score2


def play_game(player_1, player_2, balls=3, diff=2, show_game=False, std1=0.1,
              std2=0.0, boundary=1.0):
    """
    It plays a game between two players until one wins it.
    - balls: minimum numbers of balls to win before checking the diff[erence]
    - diff: required difference between balls won in order to call a winner
    - show: a True value prints the scores on the screen
    - the remaining parameters (std1, std2, boundary) are passed to ball_result
    The traditional scoring system requires balls=3, diff=2

    """
    ball_count1 = 0
    ball_count2 = 0
    while (ball_count1 <= balls and ball_count2 <= balls) or \
            abs(ball_count1-ball_count2) < diff:
        res = ball_result(player_1, player_2, std1, std2, boundary)
        if res == 1:
            ball_count1 += 1
        elif res == 2:
            ball_count2 += 1
        if show_game:
            score1, score2 = convert_scores(ball_count1, ball_count2, diff)
            print score1,  " : ", score2
    if ball_count1 > ball_count2:
        return 1
    else:
        return 2


def play_set(player_1, player_2, min_games=6, max_games=7,
             games_diff=2, show_set= False, balls=3, diff=2, show_game=False, std1=0.1,
              std2=0.0, boundary=1.0):
    """
    It plays a set between two players.
    - min_games: minimum numbers of games won to win a set
    - max_games: maximum numbers of games won to win a set
    - games_diff: minimum difference between player's won games to win set if
    less than max_games (i.e. win with 6-4, but not with 6-5)
    - show_set is a boolean parameter to display the set on the screen
    - the remaining parameters are passed to play_game
    The traditional scoring system is min_games=6, max_games=7, games_diff=2
    """
    game_count1 = 0
    game_count2 = 0
    while (game_count1 < min_games and game_count2 < min_games) or \
            (abs(game_count1 - game_count2) < games_diff
             and game_count1 < max_games and game_count2 < max_games):
        res = play_game(player_1, player_2, balls, diff, show_game, std1,
              std2, boundary)
        if res == 1:
            game_count1 += 1
        else:
            game_count2 += 1
        if show_set:
            print game_count1, ' : ', game_count2
    return game_count1, game_count2


def play_match(player_1, player_2, score, show_match=False, show_set=False,
               show_game=False, std1=0.1, std2=0.0, boundary=1.0):
    """
    It lays a match between two players
    - score - Score object
    - show_match = display match on screen
    """
    min_sets = score.min_sets
    sets = []
    sets1 = 0
    sets2 = 0
    while sets1 < min_sets and sets2 < min_sets:
        res = play_set(player_1, player_2, score.min_games, score.max_games,
                       score.games_diff, show_set, score.balls, score.diff,
                       show_game, std1, std2, boundary)
        sets.append(res)
        if res[0] > res[1]:
            sets1 += 1
        else:
            sets2 += 1
    if show_match:
        print sets
    if sets1 > sets2:
        return 1
    else:
        return 2
        
    
def simulation(player1, player2, score, num, show_match=False, show_set=False,
               show_game=False, std1=0.1, std2=0.0, boundary=1.0):
    """
    Simulate num games and return percentage won by first player
    """
    win_one = 0.0
    for i in range(num):
        res = play_match(player1, player2, score, show_match, show_set,
                         show_game, std1, std2, boundary)
        if res == 1:
            win_one += 1
    return win_one/num


def sim_ball_res(player_1, player_2, std1=0.1, std2=0.0, boundary=1, num=100):
    res_one = 0.0
    res_two = 0.0
    res_zero = 0.0
    for i in range(num):
        res = ball_result(player_1, player_2, std1, std2, boundary)
        if res == 1:
            res_one += 1
        elif res == 2:
            res_two += 1
        else:
            res_zero += 1
    return res_one/num, res_two/num, res_zero/num


p1 = Player('Nadal', 0.95)
p2 = Player('Federer', 0.95)
p3 = Player('Filip', 0.1)
p4 = Player('Oana', 0.15)
p5 = Player('Djokovic', 0.9)
p6 = Player('Tsonga', 0.8)
classic_score = Score(3, 2, 6, 7, 2, 3)
play_match(p1, p2, classic_score)
weird_score = Score(100, 3, 1, 1, 1, 1)
classic_score_3sets = Score(3, 2, 6, 7, 2, 2)

simulation(p1, p2, classic_score, 1000)
simulation(p3, p4, classic_score, 1000)
simulation(p1, p5, classic_score, 10000)
simulation(p1, p6, classic_score, 10000)
simulation(p1, p2, weird_score, 1000)
simulation(p1, p2, classic_score_3sets, 10000)
simulation(p1, p5, classic_score_3sets, 10000)

sim_ball_res(p1, p5, std1=0.1, std2=0.0, boundary=1, num=100)