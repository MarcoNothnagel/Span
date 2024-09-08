# testing worked out fine, test caught 1 issue which can be found in the comments

import unittest
from unittest.mock import patch
from io import StringIO
import main

class TestLeagueRanking(unittest.TestCase):

    def test_calculate_points(self):
        team_scores = {}
        main.calculate_points(('Lions', 3), ('Snakes', 1), team_scores)
        self.assertEqual(team_scores, {'Lions': 3, 'Snakes': 0})
        
        team_scores = {}
        main.calculate_points(('Lions', 2), ('Snakes', 2), team_scores)
        self.assertEqual(team_scores, {'Lions': 1, 'Snakes': 1})

    def test_display_rankings(self):
        sorted_teams = [('Tarantulas', 6), ('Lions', 5), ('FC Awesome', 1), ('Snakes', 1), ('Grouches', 0)]
        with patch('sys.stdout', new = StringIO()) as fake_out:
            main.display_rankings(sorted_teams)
            output = fake_out.getvalue()
            expected_output = (
                '1. Tarantulas, 6 pts\n'
                '2. Lions, 5 pts\n'
                '3. FC Awesome, 1 pt\n'
                '3. Snakes, 1 pt\n'
                '5. Grouches, 0 pts\n'
            )
            self.assertEqual(output, expected_output)

    def test_parse_match_line(self):
        line = 'Lions 3, Snakes 1'
        team1, team2 = main.parse_match_line(line)
        self.assertEqual(team1, ('Lions', 3))
        self.assertEqual(team2, ('Snakes', 1))


    # this test here actually found a flaw in my code. output does not give anything currently when score is 0
    def test_process_match_results(self):
        lines = [
            'Lions 3, Snakes 1',
            'Tarantulas 2, FC Awesome 1',
            'Lions 1, FC Awesome 1'
        ]
        team_scores = main.process_match_results(lines)
        self.assertEqual(team_scores, {'Lions': 4, 'Tarantulas': 3, 'FC Awesome': 1, 'Snakes': 0})

    def test_empty_file(self):
        lines = []
        team_scores = main.process_match_results(lines)
        self.assertEqual(team_scores, {})

    def test_whitespace_only(self):
        lines = ['', ' ', '   ']
        team_scores = main.process_match_results(lines)
        self.assertEqual(team_scores, {})

    def test_malformed_line(self):
        lines = ['Lions 3, Snakes', 'Tarantulas, FC Awesome 1']
        team_scores = main.process_match_results(lines)
        self.assertEqual(team_scores, {})

    def test_read_file_success(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data = 'Lions 3, Snakes 1\nTarantulas 2, FC Awesome 1')):
            lines = main.read_file('fakefile.txt')
            self.assertEqual(lines, ['Lions 3, Snakes 1\n', 'Tarantulas 2, FC Awesome 1'])

    def test_read_file_file_not_found(self):
        with patch('builtins.open', side_effect = FileNotFoundError):
            lines = main.read_file('fakefile.txt')
            self.assertEqual(lines, [])

if __name__ == '__main__':
    unittest.main()


# python -m unittest test.py