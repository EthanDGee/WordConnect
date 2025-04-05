from django.shortcuts import render
from django.http import JsonResponse
import sqlite3
import json
from pathlib import Path

def get_random_puzzle():
    db_path = Path(__file__).parent.parent.parent / 'src' / 'game_data.db'
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT start_word, end_word, solution_length FROM puzzles ORDER BY RANDOM() LIMIT 1")
    puzzle = cursor.fetchone()
    conn.close()
    return {
        'start_word': puzzle[0],
        'end_word': puzzle[1],
        'solution_length': puzzle[2]
    }

def game_view(request):
    puzzle = get_random_puzzle()
    return render(request, 'game.html', {
        'start_word': puzzle['start_word'],
        'end_word': puzzle['end_word'],
        'solution_length': puzzle['solution_length']
    })

def check_word(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            current_word = data.get('current_word')
            next_word = data.get('next_word')
            
            # Check if words differ by exactly one letter
            if len(current_word) == len(next_word):
                # Check for letter swap
                differences = sum(1 for a, b in zip(current_word, next_word) if a != b)
                if differences == 1:
                    return JsonResponse({'valid': True})
            elif len(current_word) + 1 == len(next_word):
                # Check for letter addition
                for i in range(len(next_word)):
                    if current_word == next_word[:i] + next_word[i+1:]:
                        return JsonResponse({'valid': True})
            elif len(current_word) - 1 == len(next_word):
                # Check for letter removal
                for i in range(len(current_word)):
                    if next_word == current_word[:i] + current_word[i+1:]:
                        return JsonResponse({'valid': True})
            
            return JsonResponse({'valid': False, 'error': 'Words must differ by exactly one letter'})
        except Exception as e:
            return JsonResponse({'valid': False, 'error': str(e)})
    return JsonResponse({'valid': False, 'error': 'Invalid request method'}) 