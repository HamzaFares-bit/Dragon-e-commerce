from flask import Flask, request, jsonify
from config import get_db_connection
import hashlib
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_clé_secrète_ici'  # À changer en production

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/admin_api.py', methods=['POST'])
def handle_admin_request():
    data = request.get_json()
    action = data.get('action')

    if action == 'create_account':
        return create_admin_account(data)
    elif action == 'login':
        return login_admin(data)
    else:
        return jsonify({'error': 'Action non valide'}), 400

def create_admin_account(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({'error': 'Tous les champs sont requis'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Erreur de connexion à la base de données'}), 500

    try:
        cursor = connection.cursor()
        
        # Vérifier si l'email existe déjà
        cursor.execute("SELECT id FROM admins WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'error': 'Cet email est déjà utilisé'}), 400

        # Créer le compte administrateur
        hashed_password = hash_password(password)
        cursor.execute("""
            INSERT INTO admins (username, email, password, created_at)
            VALUES (%s, %s, %s, %s)
        """, (username, email, hashed_password, datetime.datetime.now()))
        
        connection.commit()
        return jsonify({'success': True, 'message': 'Compte créé avec succès'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

def login_admin(data):
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'error': 'Email et mot de passe requis'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Erreur de connexion à la base de données'}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        hashed_password = hash_password(password)
        
        cursor.execute("""
            SELECT id, username, email 
            FROM admins 
            WHERE email = %s AND password = %s
        """, (email, hashed_password))
        
        admin = cursor.fetchone()
        
        if admin:
            # Créer un token JWT
            token = jwt.encode({
                'user_id': admin['id'],
                'username': admin['username'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }, app.config['SECRET_KEY'])
            
            return jsonify({
                'success': True,
                'token': token,
                'user': {
                    'id': admin['id'],
                    'username': admin['username'],
                    'email': admin['email']
                }
            })
        else:
            return jsonify({'error': 'Email ou mot de passe incorrect'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True) 