from flask import Flask, render_template, request, redirect, flash, jsonify
import mysql.connector
import hashlib
import json
from datetime import datetime
from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

def connect_db():
    return mysql.connector.connect(**Config.DATABASE_CONFIG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inscription', methods=['POST'])
def inscription():
    nom = request.form['nom']
    email = request.form['email']
    password = request.form['password']
    confirm = request.form['confirm_password']

    if password != confirm:
        flash("❌ Les mots de passe ne correspondent pas.")
        return redirect('/')

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO utilisateurs (nom, email, mot_de_passe) VALUES (%s, %s, %s)",
                       (nom, email, hashed_password))
        conn.commit()
        flash("✅ Inscription réussie !")
    except mysql.connector.Error as err:
        flash(f"Erreur MySQL : {err}")
    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()

    return redirect('/')

@app.route('/connexion', methods=['POST'])
def connexion():
    email = request.form['email']
    password = request.form['password']
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM utilisateurs WHERE email = %s AND mot_de_passe = %s", (email, hashed_password))
        user = cursor.fetchone()

        if user:
            flash("✅ Connexion réussie !")
            return redirect('/index1')
        else:
            flash("❌ Email ou mot de passe incorrect.")
            return redirect('/')
    except mysql.connector.Error as err:
        flash(f"Erreur MySQL : {err}")
        return redirect('/')
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/index1')
def index1():
    return render_template('index1.html')

@app.route('/video.html')
def video():
    video_url = request.args.get('url')
    if not video_url:
        return "URL de la vidéo manquante.", 400
    return render_template('video.html', video_url=video_url)

@app.route('/paiement')
def paiement():
    return render_template('paiement.html')

@app.route('/facture')
def facture():
    return render_template('facture.html')

@app.route('/api/process-payment', methods=['POST'])
def process_payment():
    try:
        data = request.get_json()
        
        # Validation des données
        required_fields = ['firstName', 'lastName', 'email', 'cardNumber', 'expiryDate', 'cvv']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Champ manquant: {field}'}), 400
        
        # Simulation de traitement de paiement
        # En production, vous intégreriez un vrai processeur de paiement ici
        
        # Sauvegarde de la transaction (optionnel)
        transaction_data = {
            'customer_name': f"{data['firstName']} {data['lastName']}",
            'email': data['email'],
            'amount': data.get('amount', 0),
            'transaction_date': datetime.now().isoformat(),
            'status': 'completed'
        }
        
        return jsonify({
            'success': True,
            'transaction_id': Config.generate_transaction_id(),
            'message': 'Paiement traité avec succès'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/cart', methods=['GET'])
def get_cart():
    # Cette route pourrait récupérer le panier depuis une base de données
    # Pour l'instant, on retourne un exemple
    return jsonify({
        'items': [],
        'total': 0
    })

# ✅ ce bloc doit être en dernier
if __name__ == '__main__':
    app.run(debug=True)
