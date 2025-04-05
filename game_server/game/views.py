from django.shortcuts import render
from django.http import JsonResponse
from game.src.database import Database
from game.src.main import Game
import json
from pathlib import Path


def get_random_puzzle(difficulty_level: int = 4):
    db_path = "game/data/game_data.db"
    db = Database(db_path)
    puzzle = db.get_random_score_puzzle(difficulty_level)
    return {
        'start_word': puzzle.start,
        'end_word': puzzle.goal,
        'solution': puzzle.solution,
        'score': puzzle.score
    }


def game_view(request):
    puzzle = get_random_puzzle()
    return render(request, 'game/game.html', {
        'start_word': puzzle['start_word'],
        'end_word': puzzle['end_word'],
        'score': puzzle['score'],
        'solution': puzzle['solution']
    })


def check_word(request):
    if request.method == 'POST':
        try:
            word_data_path = 'game/data/filtered_words.txt'
            game = Game(word_data_path)
            data = json.loads(request.body)
            current_word = data.get('current_word')
            next_word = data.get('next_word')
            if next_word not in game.possible_words:
                return JsonResponse({'valid': False, 'error': 'Word is not in the dictionary'})

            # Check if words differ by exactly one letter
            elif len(current_word) == len(next_word):
                # Check for letter swap
                differences = sum(1 for a, b in zip(current_word, next_word) if a != b)
                if differences == 1:
                    return JsonResponse({'valid': True})
            # check for invalid lengths
            elif len(current_word) - len(next_word) >= 2:
                return JsonResponse({'valid': False, 'error': 'You can only remove 1 letter at a time'})
            elif len(current_word) - len(next_word) <= -2:
                return JsonResponse({'valid': False, 'error': 'You can only add 1 letter at a time'})

            # Check for letter addition
                # if a letter was added
            elif len(current_word) < len(next_word):
                changed_letters = 0
                start_index = 0
                next_index = 0
                while start_index < len(current_word) and next_index < len(next_word):
                    if current_word[start_index] != next_word[next_index]:
                        next_index += 1
                        changed_letters += 1
                    else:
                        start_index += 1
                        next_index += 1

                if changed_letters == 0 and next_index == len(next_word) - 1:
                    changed_letters += 1

                if changed_letters != 1:
                    return JsonResponse({'valid': False, 'error': 'You can only add one letter at a time'})
                else:
                    return JsonResponse({'valid': True})

            elif len(current_word) > len(next_word):
                dropped_letters = 0
                start_index = 0
                next_index = 0

                while start_index < len(current_word) and next_index < len(next_word):
                    if current_word[start_index] != next_word[next_index]:
                        start_index += 1
                        dropped_letters += 1
                    else:
                        start_index += 1
                        next_index += 1

                if dropped_letters == 0 and start_index == len(current_word) - 1:
                    # Letter is dropped at the very end (valid scenario)
                    dropped_letters += 1

                elif dropped_letters != 1:
                    return JsonResponse({'valid': False, 'error': 'You can only drop one letter at a time'})
                else:
                    return JsonResponse({'valid': True})

            return JsonResponse({'valid': False, 'error': 'Words must differ by exactly one letter'})
        except Exception as e:
            return JsonResponse({'valid': False, 'error': str(e)})
    return JsonResponse({'valid': False, 'error': 'Invalid request method'})
