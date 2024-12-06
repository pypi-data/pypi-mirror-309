from itertools import permutations
from textblob import TextBlob

def choice():
    print("Press 1 to print the code for the Travelling Salesman Problem")
    print("Press 2 to print the code for Spam Detection using Naive Bayes")
    print("Press 3 to print the code for Weather Prediction using Decision Trees")
    print("Press 4 to print the code for Wumpus World Game")
    print("Press 5 to print the code for Sentiment Analysis using TextBlob")  # Added option
    print("Press 6 to print the code for Tic Tac Toe with Minimax")  # Added option
    print("Press 7 to print the code for Tic Tac Toe with Minimax (System vs System)")  # Added option
    print("Press 8 to print the code for Water Jug Problem")  # Added option
    print("Press 9 to print the code for Wumpus World Game with AI moves")  # Added option
    user_choice = input("Enter your choice: ")

    if user_choice == '1':
        code = '''
def travelling_salesman_problem(graph, start_node):
    nodes = list(graph.keys())
    nodes.remove(start_node)
    all_routes = permutations(nodes)
    shortest_path = None
    min_cost = float('inf')
    for route in all_routes:
        current_cost = 0
        current_path = [start_node] + list(route) + [start_node]  # Start and end at the same node
        for i in range(len(current_path) - 1):
            current_cost += graph[current_path[i]][current_path[i + 1]]
        if current_cost < min_cost:
            min_cost = current_cost
            shortest_path = current_path

    return shortest_path, min_cost


def inputGraph():
    graph={}
    nodes=input("Enter nodes space separated:").split()
    for node in nodes:
        graph[node]={}
        print(f"Enter distances from node {node} to other nodes:")
        for neighbour in nodes:
            weight=int(input(f"Enter distance from {node} to {neighbour}: "))
            graph[node][neighbour]=weight

    return graph

graph = inputGraph()
start_node = input("Enter start node: ")

shortest_path, min_cost = travelling_salesman_problem(graph, start_node)

print("Shortest Path:", shortest_path)
print("Minimum Cost:", min_cost)
'''
        print(code)

    elif user_choice == '2':
        code = '''
messages = [
    "Win a $1000 cash prize now!",
    "Hey, can we meet tomorrow?",
    "Congratulations, you won a lottery!",
    "Important update about your account",
    "Free entry in a contest for a chance to win",
    "Are you free this weekend?",
    "You are selected for a special reward",
    "Act now! Limited time offer",
    "Call now to claim your prize",
    "Reminder: Your appointment is tomorrow",
    "This is not a spam message, relax",
    "Great to see you yesterday, let's catch up soon"
]
labels = [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0]

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(messages, labels, test_size=0.2, random_state=42)

from sklearn.feature_extraction.text import CountVectorizer

vec = CountVectorizer()
X_train_counts = vec.fit_transform(X_train)
X_test_counts = vec.transform(X_test)

from sklearn.naive_bayes import MultinomialNB

clf = MultinomialNB()
clf.fit(X_train_counts, y_train)

y_pred = clf.predict(X_test_counts)

for msg, pred in zip(X_test, y_pred):
    label = "Spam" if pred == 1 else "Not Spam"
    print(f"{msg} -> {label}")
'''
        print(code)

    elif user_choice == '3':
        code = '''
import pandas as pd

data = {
    'Day': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Weather': ['Sunny', 'Cloudy', 'Sunny', 'Cloudy', 'Rainy', 'Rainy', 'Rainy', 'Sunny', 'Cloudy', 'Rainy'],
    'Temperature': ['Hot', 'Hot', 'Mild', 'Mild', 'Mild', 'Cool', 'Mild', 'Hot', 'Hot', 'Mild'],
    'Humidity': ['High', 'High', 'Normal', 'High', 'High', 'Normal', 'High', 'High', 'Normal', 'High'],
    'Wind': ['Weak', 'Weak', 'Strong', 'Strong', 'Strong', 'Strong', 'Weak', 'Strong', 'Weak', 'Strong'],
    'Play': ['No', 'Yes', 'Yes', 'Yes', 'No', 'No', 'Yes', 'No', 'Yes', 'No']
}

df = pd.DataFrame(data)
df = pd.get_dummies(df, columns=['Weather', 'Temperature', 'Humidity', 'Wind'])

X = df.drop('Play', axis=1)
y = df['Play']

from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from matplotlib import pyplot as plt

clf = DecisionTreeClassifier()
clf.fit(X, y)

plt.figure(figsize=(10, 7))
plot_tree(clf, filled=True)
plt.show()
'''
        print(code)

    elif user_choice == '4':
        code = '''
GRID_SIZE = 4
EMPTY = 0
WUMPUS = 'W'
PIT = 'P'
GOLD = 'G'
PLAYER = 'A'

def initialize_world_hardcoded():
    player_position = (0, 0)
    wumpus_position = (2, 1)
    gold_position = (3, 3)
    pit_positions = [(1, 2)]
    
    return player_position, wumpus_position, gold_position, pit_positions

def get_percepts(player_position, wumpus_position, pit_positions, gold_position, has_gold):
    percepts = []
    px, py = player_position
    wx, wy = wumpus_position

    if abs(px - wx) + abs(py - wy) == 1:
        percepts.append("You smell a stench.")

    for pit_x, pit_y in pit_positions:
        if abs(px - pit_x) + abs(py - pit_y) == 1:
            percepts.append("You feel a breeze.")

    if player_position == gold_position and not has_gold:
        percepts.append("You see a glitter.")

    return percepts

def move_player(player_position, direction):
    x, y = player_position
    if direction == "up" and x > 0:
        return (x - 1, y)
    elif direction == "down" and x < GRID_SIZE - 1:
        return (x + 1, y)
    elif direction == "left" and y > 0:
        return (x, y - 1)
    elif direction == "right" and y < GRID_SIZE - 1:
        return (x, y + 1)
    else:
        print("Invalid move.")
        return player_position

def check_status(player_position, wumpus_position, pit_positions, gold_position, has_gold):
    if player_position == wumpus_position:
        print("You've been eaten by the Wumpus! Game over.")
        return True, False
    elif player_position in pit_positions:
        print("You fell into a pit! Game over.")
        return True, False
    elif player_position == (3, 3) and has_gold:
        print("You escaped with the gold! You win!")
        return True, True
    return False, has_gold

def display_grid(player_position, gold_position, has_gold):
    display_grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    px, py = player_position
    display_grid[px][py] = PLAYER

    if not has_gold:
        gx, gy = gold_position
        display_grid[gx][gy] = GOLD

    for row in display_grid:
        print(" ".join(row))
    print()

def play():
    print("Welcome to the Wumpus World!")
    player_position, wumpus_position, gold_position, pit_positions = initialize_world_hardcoded()
    has_gold = False
    game_over = False

    while not game_over:
        display_grid(player_position, gold_position, has_gold)
        percepts = get_percepts(player_position, wumpus_position, pit_positions, gold_position, has_gold)
        if percepts:
            for percept in percepts:
                print(percept)
        else:
            print("You sense nothing.")

        move = input("Enter your move (up, down, left, right): ").strip().lower()
        player_position = move_player(player_position, move)

        if player_position == gold_position:
            print("You picked up the gold!")
            has_gold = True

        game_over, has_gold = check_status(player_position, wumpus_position, pit_positions, gold_position, has_gold)

play()
'''
        print(code)

    elif user_choice == '5':  # Added elif for sentiment analysis
        code = '''
from textblob import TextBlob
import copy
import random

neutral_texts = [
    "The event was held at the new venue and started on time.",
    "The product is available in three colors and costs $25.",
    "The report provides detailed statistics for the past quarter."
]

negative_texts = [
    "The service was terrible and the staff was unhelpful.",
    "I am disappointed with the quality of the product; it broke within a week.",
    "The software is full of bugs and crashes frequently."
]

positive_texts = [
    "The team provided excellent support and resolved my issue quickly.",
    "I love this new product! It's exactly what I was looking for.",
    "The experience was amazing; I would definitely recommend it to others."
]

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

for text in neutral_texts:
    sentiment = analyze_sentiment(text)
    print(f"Neutral text: {text} -> Sentiment: {sentiment}")
for text in negative_texts:
    sentiment = analyze_sentiment(text)
    print(f"Negative text: {text} -> Sentiment: {sentiment}")
for text in positive_texts:
    sentiment = analyze_sentiment(text)
    print(f"Positive text: {text} -> Sentiment: {sentiment}")
'''
        print(code)

    elif user_choice == '6':  # Added elif for Tic Tac Toe with Minimax
        code = '''

    def check_winner(board):
        if (board[0] == ['O', 'O', 'O'] or board[1] == ['O', 'O', 'O'] or board[2] == ['O', 'O', 'O'] or
            board[0][0] == board[1][0] == board[2][0] == 'O' or board[0][1] == board[1][1] == board[2][1] == 'O' or
            board[0][2] == board[1][2] == board[2][2] == 'O' or board[0][0] == board[1][1] == board[2][2] == 'O' or
            board[0][2] == board[1][1] == board[2][0] == 'O'):
            return False
        elif (board[0] == ['X', 'X', 'X'] or board[1] == ['X', 'X', 'X'] or board[2] == ['X', 'X', 'X'] or
              board[0][0] == board[1][0] == board[2][0] == 'X' or board[0][1] == board[1][1] == board[2][1] == 'X' or
              board[0][2] == board[1][2] == board[2][2] == 'X' or board[0][0] == board[1][1] == board[2][2] == 'X' or
              board[0][2] == board[1][1] == board[2][0] == 'X'):
            return True
        else:
            return None

    def is_terminal(board):
        if check_winner(board) is not None:
            return True
        elif '' not in board[0] and '' not in board[1] and '' not in board[2]:
            return True
        else:
            return False

    def get_utility(board):
        if check_winner(board):
            return 1
        elif not check_winner(board):
            return -1
        else:
            return 0

    def current_player(board):
        x_count = sum(row.count('X') for row in board)
        o_count = sum(row.count('O') for row in board)
        return 'X' if x_count == o_count else 'O'

    def get_actions(board):
        possible_moves = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    if current_player(board) == 'X':
                        board[i][j] = 'X'
                        possible_moves.append(copy.deepcopy(board))
                        board[i][j] = ''
                    elif current_player(board) == 'O':
                        board[i][j] = 'O'
                        possible_moves.append(copy.deepcopy(board))
                        board[i][j] = ''
        return possible_moves

    def minimax(board):
        if is_terminal(board):
            return get_utility(board)
        if current_player(board) == 'X':
            best_value = -1
            for action in get_actions(board):
                best_value = max(best_value, minimax(action))
            return best_value
        elif current_player(board) == 'O':
            best_value = 1
            for action in get_actions(board):
                best_value = min(best_value, minimax(action))
            return best_value

    def display_board(board):
        for row in board:
            for cell in row:
                if cell == '':
                    print('-', end='  ')
                else:
                    print(cell, end='  ')
            print('\\n')

    game_board = [['', '', ''], ['', '', ''], ['', '', '']]
    while not is_terminal(game_board):
        move = int(input("Enter the location of your X: "))
        row = int((move - 1) / 3)
        col = int((move - 1) % 3)
        game_board[row][col] = 'X'
        display_board(game_board)
        possible_moves = get_actions(game_board)
        for move in possible_moves:
            if minimax(move) == -1:
                game_board = move
                break
        else:
            for move in possible_moves:
                if minimax(move) == 0:
                    game_board = move
                    break
        print("Computer's move: ")
        display_board(game_board)

    if not check_winner(game_board):
        print("Computer wins!")
    elif check_winner(game_board) is None:
        print("Draw!")
    '''
        print(code)

    elif user_choice == '7':  # Added elif for Tic Tac Toe with Minimax (System vs System)
        code = '''

def check_winner(board):
    for player in ['X', 'O']:
        if (board[0] == [player] * 3 or
            board[1] == [player] * 3 or
            board[2] == [player] * 3 or
            [board[i][0] for i in range(3)] == [player] * 3 or
            [board[i][1] for i in range(3)] == [player] * 3 or
            [board[i][2] for i in range(3)] == [player] * 3 or
            [board[i][i] for i in range(3)] == [player] * 3 or
            [board[i][2 - i] for i in range(3)] == [player] * 3):
            return player
    return None

def is_terminal(board):
    return check_winner(board) is not None or all(cell != '' for row in board for cell in row)

def get_utility(board):
    winner = check_winner(board)
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    else:
        return 0

def current_player(board):
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)
    return 'X' if x_count == o_count else 'O'

def get_actions(board):
    possible_moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                new_board = copy.deepcopy(board)
                new_board[i][j] = current_player(board)
                possible_moves.append(new_board)
    return possible_moves

def minimax(board):
    if is_terminal(board):
        return get_utility(board)
    curr = current_player(board)
    if curr == 'X':
        best_value = -float('inf')
        for action in get_actions(board):
            best_value = max(best_value, minimax(action))
        return best_value
    else:
        best_value = float('inf')
        for action in get_actions(board):
            best_value = min(best_value, minimax(action))
        return best_value

def display_board(board):
    for row in board:
        print("  ".join([cell if cell != '' else '-' for cell in row]))
    print("\\n")

def best_move(board):
    curr = current_player(board)
    best_value = -float('inf') if curr == 'X' else float('inf')
    best_action = None
    for action in get_actions(board):
        value = minimax(action)
        if curr == 'X' and value > best_value:
            best_value = value
            best_action = action
        elif curr == 'O' and value < best_value:
            best_value = value
            best_action = action
    return best_action

game_board = [['', '', ''], ['', '', ''], ['', '', '']]

while not is_terminal(game_board):
    print("System 1 move:")
    game_board = best_move(game_board)
    display_board(game_board)
    
    if is_terminal(game_board):
        break
    
    print("System 2 move:")
    game_board = best_move(game_board)
    display_board(game_board)

winner = check_winner(game_board)
if winner:
    print(f"{winner} wins!")
else:
    print("Draw!")
'''
        print(code)

    elif user_choice == '8':  # Added elif for Water Jug Problem
        code = '''
    n = int(input("jugs: "))
    capacity = []
    for i in range(n):
        print(i + 1, ": ", end = "")
        capacity.append(int(input()))

    target = int(input("Enter the target: "))

    state = tuple([0] * n)
    parentMap = {state: (None, None)}

    def generateSuccessors(state, capacity):
        m = len(state)
        successors = []
        for i in range(m):
            # fill ith jug
            newState = list(state)
            newState[i] = capacity[i]
            successors.append((tuple(newState), f"Filled jug {i + 1}: {tuple(newState)}"))
            
            # empty ith jug
            newState = list(state)
            newState[i] = 0
            successors.append((tuple(newState), f"Emptied jug {i + 1}: {tuple(newState)}"))
            
            # ith to jth jug transfer
            for j in range(m):
                if i != j:
                    newState = list(state)
                    space = capacity[j] - newState[j]
                    if space < newState[i]:
                        newState[j] += space
                        newState[i] -= space
                    else:
                        newState[j] += newState[i]
                        newState[i] = 0
                    successors.append((tuple(newState), f"Poured water from jug {i + 1} to jug {j + 1}: {tuple(newState)}"))
        return successors

    def bfs(state, target, capacity):
        frontier = [state]
        visited = set()
        parentMap = {state: (None, None)}
        while frontier:
            currState = frontier.pop(0)
            visited.add(currState)
            if target in currState:
                path = []
                actions = []
                st = currState
                while st is not None:
                    path.append(st)
                    st, action = parentMap[st]
                    if action:
                        actions.append(action)
                path = path[::-1]
                actions = actions[::-1]
                return path, actions
            successors = generateSuccessors(currState, capacity)
            for successor, action in successors:
                if successor not in visited and successor not in frontier:
                    parentMap[successor] = (currState, action)
                    frontier.append(successor)
        return None, None

    solution, actions = bfs(state, target, capacity)
    if solution:
        for action in actions:
            print(action)
    else:
        print("No solution exists")
    '''
        print(code)

    elif user_choice == '9':  # Added elif for Wumpus World Game with AI moves
        code = '''

    n = 4
    m = 2  # number of pits
    board = []

    for i in range(n):
        temp = []
        for j in range(n):
            temp.append('.')
        board.append(temp)

    def printBoard(board, n, revealed):
        for i in range(n):
            for j in range(n):
                if (i, j) in revealed:
                    print(board[i][j], end=" ")
                else:
                    print('?', end=" ")
            print()
        print()
        print()

    def getSenses(board, pos):
        senses = {'stench': False, 'glitter': False, 'breeze': False}
        x, y = pos
        if board[x][y] == 'G':
            senses['glitter'] = True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                if board[nx][ny] == 'W':
                    senses['stench'] = True
                if board[nx][ny] == 'P':
                    senses['breeze'] = True
        return senses

    goldX = random.randint(0, n - 1)
    goldY = random.randint(0, n - 1)

    while goldX == 0 and goldY == 0:
        goldX = random.randint(0, n - 1)
        goldY = random.randint(0, n - 1)

    wumpusX = random.randint(0, n - 1)
    wumpusY = random.randint(0, n - 1)

    while (wumpusX == goldX and wumpusY == goldY) or (wumpusX == 0 and wumpusY == 0):
        wumpusX = random.randint(0, n - 1)
        wumpusY = random.randint(0, n - 1)

    pits = set()
    while len(pits) < m:
        pitX = random.randint(0, n - 1)
        pitY = random.randint(0, n - 1)
        if (pitX, pitY) != (goldX, goldY) and (pitX, pitY) != (wumpusX, wumpusY) and (pitX, pitY) != (0, 0):
            pits.add((pitX, pitY))

    # Place gold, wumpus, and pits on the board
    board[goldX][goldY] = 'G'
    board[wumpusX][wumpusY] = 'W'
    for pit in pits:
        board[pit[0]][pit[1]] = 'P'

    # Player movement
    def movePlayer(pos, move):
        x, y = pos
        if move == 'up' and x > 0:
            x -= 1
        elif move == 'down' and x < n - 1:
            x += 1
        elif move == 'left' and y > 0:
            y -= 1
        elif move == 'right' and y < n - 1:
            y += 1
        return (x, y)

    # Main game loop
    def playGame():
        playerPos = (0, 0)
        revealed = set()
        revealed.add(playerPos)
        while True:
            printBoard(board, n, revealed)
            senses = getSenses(board, playerPos)
            print("Senses:", senses)
            if senses['glitter']:
                print("Gold found! You win!")
                break
            if board[playerPos[0]][playerPos[1]] == 'W':
                print("You encountered the Wumpus! Game over!")
                break
            if board[playerPos[0]][playerPos[1]] == 'P':
                print("You fell into a pit! Game over!")
                break
            move = input("AI moves ").strip().lower()
            playerPos = movePlayer(playerPos, move)
            revealed.add(playerPos)

    playGame()
    '''
        print(code)
