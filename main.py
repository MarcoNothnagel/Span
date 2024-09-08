# I used Python 3 as it is OS agnostic so it should run fine on my Windows machine and OS X
import argparse
import os


# overall time complexity: O(p * n + k log k)

# O(1)
def parse_arguments():
    parser = argparse.ArgumentParser(description = 'Process match results from a file')
    parser.add_argument('filename', type = str, help = 'Name of the input file containing match results')
    args = parser.parse_args()
    return os.path.abspath(args.filename)


# O(n)
def read_file(filename):
    try:
        with open(filename, 'r', newline = None) as f:
            return f.readlines()
    except FileNotFoundError:
        print(f'ERROR: {filename} does not exist')
        return []
    except IOError:
        print(f"ERROR: Program can't read file: {filename}")
        return []


def parse_match_line(line):
    # O(n) to split
    try:
        team1, team2 = line.split(', ')
        team1_name, team1_score = team1.rsplit(' ', 1)
        team2_name, team2_score = team2.rsplit(' ', 1)

        # O(1) to convert int
        return (team1_name.strip(), int(team1_score)), (team2_name.strip(), int(team2_score))
    except ValueError:
        print(f'WARNING: Skipping malformed line: {line}')
        return None, None


# O(p * n)
def process_match_results(lines):
    team_scores = {}
    
    for line in lines:
        line = line.strip()
        if line:
            team1, team2 = parse_match_line(line)
            if team1 and team2:
                calculate_points(team1, team2, team_scores)

    return team_scores


# O(1)
def calculate_points(team1, team2, team_scores):
    team1_name, team1_score = team1
    team2_name, team2_score = team2

    # thanks to testing we can now initialise a 0 score team
    if team1_name not in team_scores:
        team_scores[team1_name] = 0
    if team2_name not in team_scores:
        team_scores[team2_name] = 0

    # O(1) for basic updates
    if team1_score > team2_score:
        team_scores[team1_name] += 3
    elif team1_score < team2_score:
        team_scores[team2_name] += 3
    else:
        team_scores[team1_name] += 1
        team_scores[team2_name] += 1


# O(k log k)
def generate_rankings(team_scores):
    # built in sort, was thinking to do a basic bubble sort for fun but this is easier and maybe even a bit faster than quicksort
    return sorted(team_scores.items(), key = lambda item: (-item[1], item[0]))


# O(k)
def display_rankings(sorted_teams):
    current_rank = 1
    previous_score = None
    for index, (team, score) in enumerate(sorted_teams):
        if previous_score is not None and score < previous_score:
            current_rank = index + 1
        score_text = f'{score} pt' if score == 1 else f'{score} pts'
        print(f'{current_rank}. {team}, {score_text}')
        previous_score = score


def main():
    filename = parse_arguments()
    lines = read_file(filename)
    if not lines:
        return
    team_scores = process_match_results(lines)
    if not team_scores:
        print('No valid matches found')
        return
    sorted_teams = generate_rankings(team_scores)
    display_rankings(sorted_teams) 


if __name__ == '__main__':
    main()


# python main.py input.txt
