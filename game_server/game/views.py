from django.shortcuts import render
from django.http import JsonResponse
from game.src.database import Database
from game.src.main import Game
import json
from pathlib import Path


def get_random_puzzle(difficulty_level: int = 5):
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
    try:
        difficulty_level = (request.GET.get('difficulty', 5))
    except ValueError:
        difficulty_level = 5

    puzzle = get_random_puzzle(difficulty_level)
    print(puzzle)
    return render(request, 'game/game.html', {
        'start_word': puzzle['start_word'],
        'end_word': puzzle['end_word'],
        'score': puzzle['score'],
        'solution': puzzle['solution']
    })


def check_word(request):
    if request.method == 'POST':
        game = Game()
        data = json.loads(request.body)
        current_word = data.get('current_word')
        next_word = data.get('next_word')
        valid, error = game.valid_jump(current_word, next_word)
        return JsonResponse({'valid': valid, 'error': error})
    return JsonResponse({'valid': False, 'error': 'Invalid request method'})
