# Word Connect Game 🌟
Welcome to **Word Connect**, a fun and challenging puzzle game where your vocabulary, spelling skills, and agility are put to the test!
## 🎲 About the Game:
In **Word Connect**, the goal is simple: you'll be presented with two completely random words, and your challenge is to transform one word into the other in the fewest possible moves. Each move you make can only involve changing **one letter**: you can swap a letter, add a letter, or remove a letter.
Try your best to match the computer's shortest solutions to win bragging rights! However, brace yourself: outsmarting the computer might just be impossible!
## 🎮 How to Play:
- Begin with the initial provided word.
- On each move, input a new word that differs by only one letter (add, remove, or swap a letter).
- Reach the provided final word one step at a time.
- Try to solve the puzzle in as few guesses as possible!
- Type `q` at any time to quit the current round.

### Example:
``` shell
Pair Found! - cat -> dog in 3
cat
cot
cog
dog
You got the word in 3 guesses!
The Computer got there in 3 guesses.
```
## 🚀 Running the Game:
Before starting `Word Connect`, make sure you have Python (specifically version **3.13.1**) installed on your system.
### Set-up steps:
1. Clone or download this repository.
2. Ensure the required word data file (filtered_words.txt) exists and is placed in the right directory (`data/` folder).

Directory structure example:
``` 
WordConnectGame/
│
├── data/
│   └── filtered_words.txt
│
├── main.py
├── graph.py
├── FileParser.py
├── DisjointSet.py
└── database.py
```
### Execution:
Open your terminal, navigate to your project directory, and execute:
``` shell
python main.py
```
Follow onscreen prompts, and enjoy the game!
## ⚙️ How the Game Works:
Here's a quick breakdown of the game's inner workings to give you an idea:
### Core Components:
- **Graph Structure** (`graph.py`): Each word is a vertex in the graph, and edges connect words that differ by exactly one letter. This complex graph underpins the entire gameplay.
- **Shortest Path Algorithm**: Uses Breadth-First Search (BFS) to determine the minimum number of transformations needed from one word to another.
- **Word Filtering** (`FileParser.py`): Before gameplay, words are filtered to exclude inappropriate words and those containing invalid characters.
- **Disjoint Sets for Efficiency** (`DisjointSet.py`): A union-find data structure helps manage the connectivity of words and optimize the puzzle creation process.
- **Database Management** (`database.py`): Stores puzzles (word pairs, shortest path solutions, difficulty scores) in an SQLite database for fast retrieval and ensuring variety during gameplay.

### Under the Hood:
1. **Word Loading and Filtering**: Valid words are loaded from a text file (`filtered_words.txt`) and processed through filtering processes.
2. **Graph Creation & Connectivity Checking**: A graph connecting words (vertices) is built efficiently and analyzed to remove isolated nodes, ensuring every puzzle provides solvable fun.
3. **Puzzle Generation**: Random puzzles are generated and verified before gameplay.
4. **Gameplay Loop**: Players interact via a clean command-line interface until solving or quitting the puzzle, with puzzle solution hints provided at the end.

## 🛠️ Technologies Used:
- Python 3.13.1
- SQLite Database
- Breadth-First Search (shortest path algorithm)

## Enjoy and sharpen your word mastery! Happy Connecting! 🌟📚
