### server.py (Flask REST API)
from flask import Flask, request, jsonify
import sqlite3
import os
from conf import Conf

app = Flask(__name__)
DB_PATH = os.path.join(Conf.BASE_DIR, 'flappy_bird.db')

# Initialize database tables if not exist
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS players (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 highscore INTEGER DEFAULT 0,
                 sprite_file TEXT DEFAULT 'bird.png',
                 sprite_name TEXT DEFAULT 'Flappy Bird'
               )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'error': 'Username required'}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Try to find existing user
    c.execute('SELECT id, highscore, sprite_file, sprite_name FROM players WHERE username = ?', (username,))
    row = c.fetchone()
    if row:
        player_id, highscore, sprite_file, sprite_name = row
    else:
        # Create new user
        c.execute('INSERT INTO players (username) VALUES (?)', (username,))
        conn.commit()
        player_id = c.lastrowid
        highscore, sprite_file, sprite_name = 0, 'bird.png', 'Flappy Bird'

    conn.close()
    return jsonify({
        'id': player_id,
        'username': username,
        'highscore': highscore,
        'sprite_file': sprite_file,
        'sprite_name': sprite_name
    })

@app.route('/update_score', methods=['POST'])
def update_score():
    data = request.get_json()
    user_id = data.get('id')
    score = data.get('highscore')
    if user_id is None or score is None:
        return jsonify({'error': 'id and highscore required'}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE players SET highscore = ? WHERE id = ?', (score, user_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'ok'})

@app.route('/update_sprite', methods=['POST'])
def update_sprite():
    data = request.get_json()
    user_id = data.get('id')
    sprite_file = data.get('sprite_file')
    sprite_name = data.get('sprite_name')
    if user_id is None or not sprite_file or not sprite_name:
        return jsonify({'error': 'id, sprite_file, and sprite_name required'}), 400

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE players SET sprite_file = ?, sprite_name = ? WHERE id = ?'
              , (sprite_file, sprite_name, user_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(port=5000)


### main.py (Client Integration)

