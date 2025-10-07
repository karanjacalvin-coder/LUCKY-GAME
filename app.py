from flask import Flask, render_template, request
from threading import Lock

app = Flask(__name__)

ENTRY_FEE = 20
PRIZE = 100
PLAYERS_PER_ROUND = 6

# Shared data (all users share this one server memory)
players = []
round_number = 0
owner_profit = 0
lock = Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    global players, round_number, owner_profit
    name = request.form.get('name')
    contact = request.form.get('contact')

    if not name or not contact:
        return render_template('index.html', message="Please enter both name and contact.")

    with lock:  # Prevents data corruption when many users click at once
        players.append({"name": name, "contact": contact})
        position = len(players)

        if position < PLAYERS_PER_ROUND:
            message = f"Hi {name}, your entry was received. Try your luck again!"
            return render_template('index.html', message=message)

        # 6th player triggers the win
        winner = players[-1]['name']
        round_number += 1
        total_in = ENTRY_FEE * PLAYERS_PER_ROUND
        profit = total_in - PRIZE
        owner_profit += profit

        message = f"🎉 Congratulations {winner}! You are the winner of Round {round_number}! You won {PRIZE} virtual KSH."
        summary = f"Owner total profit: {owner_profit} virtual KSH"

        # Reset round
        players = []
        return render_template('index.html', message=message, summary=summary)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
