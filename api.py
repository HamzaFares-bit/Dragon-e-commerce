from flask import Flask, request, jsonify
from config import get_db_connection
import json

app = Flask(__name__)

@app.route('/api', methods=['GET', 'POST'])
def handle_request():
    action = request.args.get('action')
    
    if action == 'getStock':
        return get_stock()
    elif action == 'updateStock':
        return update_stock()
    elif action == 'getProductDetails':
        return get_product_details()
    else:
        return jsonify({'error': 'Action non valide'}), 400

def get_stock():
    product_id = request.args.get('productId')
    brand = request.args.get('brand')
    color = request.args.get('color')
    size = request.args.get('size')
    
    if not all([product_id, brand, color, size]):
        return jsonify({'error': 'Paramètres manquants'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Erreur de connexion à la base de données'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT quantity 
            FROM stock 
            WHERE product_id = %s AND brand = %s AND color = %s AND size = %s
        """, (product_id, brand, color, size))
        
        result = cursor.fetchone()
        if result:
            return jsonify({'quantity': result['quantity']})
        else:
            return jsonify({'error': 'Stock non trouvé'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

def update_stock():
    product_id = request.form.get('productId')
    brand = request.form.get('brand')
    color = request.form.get('color')
    size = request.form.get('size')
    quantity = request.form.get('quantity')
    
    if not all([product_id, brand, color, size, quantity]):
        return jsonify({'error': 'Paramètres manquants'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Erreur de connexion à la base de données'}), 500
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE stock 
            SET quantity = %s 
            WHERE product_id = %s AND brand = %s AND color = %s AND size = %s
        """, (quantity, product_id, brand, color, size))
        
        connection.commit()
        return jsonify({'success': True})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

def get_product_details():
    product_id = request.args.get('productId')
    
    if not product_id:
        return jsonify({'error': 'ID du produit manquant'}), 400
    
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Erreur de connexion à la base de données'}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Récupérer les détails du produit
        cursor.execute("""
            SELECT * FROM products WHERE id = %s
        """, (product_id,))
        product = cursor.fetchone()
        
        if not product:
            return jsonify({'error': 'Produit non trouvé'}), 404
        
        # Récupérer le stock
        cursor.execute("""
            SELECT brand, color, size, quantity 
            FROM stock 
            WHERE product_id = %s
        """, (product_id,))
        stock = cursor.fetchall()
        
        # Organiser le stock par marque, couleur et taille
        stock_data = {}
        for item in stock:
            if item['brand'] not in stock_data:
                stock_data[item['brand']] = {}
            if item['color'] not in stock_data[item['brand']]:
                stock_data[item['brand']][item['color']] = {}
            stock_data[item['brand']][item['color']][item['size']] = item['quantity']
        
        return jsonify({
            'product': product,
            'stock': stock_data
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True) 