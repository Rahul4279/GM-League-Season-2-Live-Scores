from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_socketio import SocketIO, emit
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Score
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gmu_score.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    scores = {}
    games = ['Football', 'Kabaddi', 'Basketball', 'Badminton']
    
    for game in games:
        score_obj = Score.query.filter_by(game=game).first()
        if score_obj:
            scores[game] = {
                'score': score_obj.score_data,
                'is_live': score_obj.is_live
            }
        else:
            scores[game] = {
                'score': 'No live match',
                'is_live': False
            }
    
    return render_template('index.html', scores=scores)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/get_scores')
def get_scores():
    scores = {}
    games = ['Football', 'Kabaddi', 'Basketball', 'Badminton']
    
    for game in games:
        score_obj = Score.query.filter_by(game=game).first()
        if score_obj:
            scores[game] = {
                'score': score_obj.score_data,
                'is_live': score_obj.is_live
            }
        else:
            scores[game] = {
                'score': 'No live match',
                'is_live': False
            }
    
    return jsonify(scores)

@app.route('/update_score', methods=['POST'])
@login_required
def update_score():
    data = request.json
    game = data.get('game')
    score_data = data.get('score_data')
    
    if not game or not score_data:
        return jsonify({'success': False, 'error': 'Missing game or score data'})
    
    score_obj = Score.query.filter_by(game=game).first()
    if score_obj:
        score_obj.score_data = score_data
    else:
        score_obj = Score(game=game, score_data=score_data, is_live=True)
        db.session.add(score_obj)
    
    db.session.commit()
    
    # Emit real-time update
    socketio.emit('update_score', {
        'game': game,
        'score_data': score_data,
        'is_live': score_obj.is_live
    })
    
    return jsonify({'success': True})

@app.route('/toggle_live', methods=['POST'])
@login_required
def toggle_live():
    data = request.json
    game = data.get('game')
    
    if not game:
        return jsonify({'success': False, 'error': 'Missing game'})
    
    score_obj = Score.query.filter_by(game=game).first()
    if score_obj:
        score_obj.is_live = not score_obj.is_live
        db.session.commit()
        
        # Emit real-time update
        socketio.emit('update_live_status', {
            'game': game,
            'is_live': score_obj.is_live
        })
        
        return jsonify({'success': True, 'is_live': score_obj.is_live})
    
    return jsonify({'success': False, 'error': 'Game not found'})

# Leaderboard functionality
@app.route('/api/leaderboard')
def get_leaderboard():
    sport_filter = request.args.get('sport', '')
    
    # Load leaderboard data from file or create default
    leaderboard_file = 'leaderboard.json'
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, 'r') as f:
            teams = json.load(f)
    else:
        # Default leaderboard data
        teams = [
            {'name': 'Team Alpha', 'sport': 'Football', 'points': 15},
            {'name': 'Team Beta', 'sport': 'Football', 'points': 12},
            {'name': 'Team Gamma', 'sport': 'Basketball', 'points': 28},
            {'name': 'Team Delta', 'sport': 'Kabaddi', 'points': 35},
            {'name': 'Team Echo', 'sport': 'Badminton', 'points': 18},
            {'name': 'Team Foxtrot', 'sport': 'Football', 'points': 10},
            {'name': 'Team Golf', 'sport': 'Basketball', 'points': 22},
            {'name': 'Team Hotel', 'sport': 'Kabaddi', 'points': 30}
        ]
        # Save default data
        with open(leaderboard_file, 'w') as f:
            json.dump(teams, f, indent=2)
    
    # Filter by sport if specified
    if sport_filter:
        teams = [team for team in teams if team['sport'] == sport_filter]
    
    # Sort by points (descending)
    teams.sort(key=lambda x: x['points'], reverse=True)
    
    return jsonify(teams)

@app.route('/api/leaderboard/add', methods=['POST'])
@login_required
def add_team_to_leaderboard():
    data = request.json
    team_name = data.get('name')
    sport = data.get('sport')
    points = data.get('points', 0)
    
    if not team_name or not sport:
        return jsonify({'success': False, 'error': 'Missing team name or sport'})
    
    # Load existing leaderboard
    leaderboard_file = 'leaderboard.json'
    teams = []
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, 'r') as f:
            teams = json.load(f)
    
    # Check if team already exists
    existing_team = next((team for team in teams if team['name'] == team_name and team['sport'] == sport), None)
    
    if existing_team:
        # Update existing team's points
        existing_team['points'] = points
    else:
        # Add new team
        teams.append({
            'name': team_name,
            'sport': sport,
            'points': points
        })
    
    # Save updated leaderboard
    with open(leaderboard_file, 'w') as f:
        json.dump(teams, f, indent=2)
    
    return jsonify({'success': True})

@app.route('/api/leaderboard/update', methods=['POST'])
@login_required
def update_team_in_leaderboard():
    data = request.json
    team_name = data.get('name')
    sport = data.get('sport')
    points = data.get('points', 0)
    
    if not team_name or not sport:
        return jsonify({'success': False, 'error': 'Missing team name or sport'})
    
    # Load existing leaderboard
    leaderboard_file = 'leaderboard.json'
    teams = []
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, 'r') as f:
            teams = json.load(f)
    
    # Find and update team
    team_found = False
    for team in teams:
        if team['name'] == team_name and team['sport'] == sport:
            team['points'] = points
            team_found = True
            break
    
    if not team_found:
        return jsonify({'success': False, 'error': 'Team not found'})
    
    # Save updated leaderboard
    with open(leaderboard_file, 'w') as f:
        json.dump(teams, f, indent=2)
    
    return jsonify({'success': True})

@app.route('/api/leaderboard/delete', methods=['POST'])
@login_required
def delete_team_from_leaderboard():
    data = request.json
    team_name = data.get('name')
    sport = data.get('sport')
    
    if not team_name or not sport:
        return jsonify({'success': False, 'error': 'Missing team name or sport'})
    
    # Load existing leaderboard
    leaderboard_file = 'leaderboard.json'
    teams = []
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, 'r') as f:
            teams = json.load(f)
    
    # Remove team
    teams = [team for team in teams if not (team['name'] == team_name and team['sport'] == sport)]
    
    # Save updated leaderboard
    with open(leaderboard_file, 'w') as f:
        json.dump(teams, f, indent=2)
    
    return jsonify({'success': True})

@app.route('/api/scores/delete', methods=['POST'])
@login_required
def delete_score():
    data = request.json
    game = data.get('game')
    
    if not game:
        return jsonify({'success': False, 'error': 'Missing game'})
    
    score_obj = Score.query.filter_by(game=game).first()
    if score_obj:
        score_obj.score_data = 'No live match'
        score_obj.is_live = False
        db.session.commit()
        
        # Emit real-time update
        socketio.emit('update_score', {
            'game': game,
            'score_data': 'No live match',
            'is_live': False
        })
        
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': 'Game not found'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create admin user if it doesn't exist
        if not User.query.filter_by(username='your_new_admin').first():
            user = User(username='yashaswini', password='yashu@1704')
            db.session.add(user)
            db.session.commit()
        
        # Initialize default scores
        games = {
            'Football': 'India 2 - 1 Pakistan',
            'Kabaddi': 'Team A 35 - 28 Team B',
            'Basketball': 'Lakers 108 - 102 Bulls',
            'Badminton': 'Player X 21 - 19 Player Y'
        }
        
        for game, score_data in games.items():
            if not Score.query.filter_by(game=game).first():
                db.session.add(Score(game=game, score_data=score_data, is_live=True))
        
        db.session.commit()
    
    socketio.run(app, debug=True)
