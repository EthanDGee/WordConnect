# Word Connect Game 🌟

Welcome to **Word Connect**, a fun and challenging puzzle game where your vocabulary, and mental gymnastics are out to
the test as you try to get from point A to point B

## 🎲 About the Game:

In **Word Connect**, the goal is simple: you'll be presented with two completely random words, and your challenge is to
transform one word into the other in the fewest possible moves. Each move you make can only involve changing **one
letter**: you can swap a letter, add a letter, or remove a letter.
Try your best to match the computer's shortest solutions to win bragging rights! However, brace yourself: outsmarting
the computer might just be impossible!

## 🎮 How to Play:

You will be prompted with puzzle with 2 words, these are your 2 end points.

1. Your starting word, the beginning of your journey.
2. Your end word, what your final end destination will be, and the goal of the puzzle.

On each move your goal is to "jump" to a word that brings you closer to your destination. You can do that by changing
your current word by one letter. YOu can only do one action at a time, so making sure to plan carefully is important.
You can:

1. Swap one letter, the traditional word chains move.
    - **C**at -> **B**at
    - Hou**s**e -> Horse
    - Ben**d** -> Ben**t**
2. Add a letter, place a new letter into the current word at any point you like.
    - Clan -> Clank
    - gave -> g**r**ave
    - water ->  wa**i**ter
    - row ->  **c**row
3. Remove a letter, remove any letter from the current word that you like.
    - Part**y** -> Part

Made a mistake and want to backtrack to a previous word? Enter **B** to go back to the last word at no penalty to your
final score.

Your goal is to minimize the total number of moves to get from your start word to your end word. For an added difficulty
try and beat/tie the bot. The bot is programmed to find an optimal path between the two words.In order to make things
more fair the bot has been given a much smaller vocabulary than you. The bot has access to around 5,000 words, as
compared to your ~27,000. This will still be quite the challenge, and tie-ing the bot will be its own everest to summit.

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

- **Graph Structure** (`graph.py`): Each word is a vertex in the graph, and edges connect words that differ by exactly
  one letter. This complex graph underpins the entire gameplay.
- **Shortest Path Algorithm**: Uses Breadth-First Search (BFS) to determine the minimum number of transformations needed
  from one word to another.
- **Word Filtering** (`FileParser.py`): Before gameplay, words are filtered to exclude inappropriate words and those
  containing invalid characters.
- **Disjoint Sets for Efficiency** (`DisjointSet.py`): A union-find data structure helps manage the connectivity of
  words and optimize the puzzle creation process.
- **Database Management** (`database.py`): Stores puzzles (word pairs, shortest path solutions, difficulty scores) in an
  SQLite database for fast retrieval and ensuring variety during gameplay.

### Under the Hood:

1. **Word Loading and Filtering**: Valid words are loaded from a text file (`filtered_words.txt`) and processed through
   filtering processes.
2. **Graph Creation & Connectivity Checking**: A graph connecting words (vertices) is built efficiently and analyzed to
   remove isolated nodes, ensuring every puzzle provides solvable fun.
3. **Puzzle Generation**: Random puzzles are generated and verified before gameplay.
4. **Gameplay Loop**: Players interact via a clean command-line interface until solving or quitting the puzzle, with
   puzzle solution hints provided at the end.

## 🛠️ Technologies Used:

- Python 3.13.1
- SQLite Database
- Breadth-First Search (shortest path algorithm)

## Enjoy and sharpen your word mastery! Happy Connecting! 🌟📚
