import os
from datetime import datetime

class Config:
    """Configuration de l'application"""
    
    # Configuration de base
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre_clé_secrète_super_sécurisée_2024'
    DEBUG = True
    
    # Configuration de la base de données
    DATABASE_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'hamzahamza2005',
        'database': 'gestion_utilisateur'
    }
    
    # Configuration des paiements
    PAYMENT_CONFIG = {
        'currency': 'DH',
        'success_rate': 0.9,  # 90% de succès pour les simulations
        'processing_time': 2,  # Temps de traitement en secondes
        'supported_cards': ['VISA', 'MasterCard', 'American Express']
    }
    
    # Configuration de l'application e-commerce
    ECOMMERCE_CONFIG = {
        'company_name': 'Votre Boutique en Ligne',
        'company_email': 'support@votresite.com',
        'company_phone': '+212 5XX XX XX XX',
        'company_address': '123 Rue Principale, Ville, Maroc',
        'tax_rate': 0.20,  # 20% de TVA
        'shipping_cost': 30,  # Coût de livraison en DH
        'free_shipping_threshold': 500  # Livraison gratuite au-dessus de 500 DH
    }
    
    # Configuration des notifications
    NOTIFICATION_CONFIG = {
        'default_duration': 3000,  # Durée d'affichage en ms
        'max_notifications': 5,  # Nombre max de notifications simultanées
        'position': 'top-right'  # Position des notifications
    }
    
    # Configuration de sécurité
    SECURITY_CONFIG = {
        'password_min_length': 8,
        'session_timeout': 3600,  # 1 heure en secondes
        'max_login_attempts': 3,
        'lockout_duration': 900  # 15 minutes en secondes
    }
    
    # Configuration des fichiers
    UPLOAD_CONFIG = {
        'max_file_size': 10 * 1024 * 1024,  # 10 MB
        'allowed_extensions': ['jpg', 'jpeg', 'png', 'gif', 'pdf'],
        'upload_folder': 'static/uploads'
    }
    
    @staticmethod
    def get_current_timestamp():
        """Retourne le timestamp actuel"""
        return datetime.now().isoformat()
    
    @staticmethod
    def generate_order_number():
        """Génère un numéro de commande unique"""
        timestamp = datetime.now()
        return f"CMD-{timestamp.year}-{timestamp.strftime('%m%d')}-{timestamp.strftime('%H%M%S')}"
    
    @staticmethod
    def generate_transaction_id():
        """Génère un ID de transaction unique"""
        return f"TXN{int(datetime.now().timestamp())}"
    
    @staticmethod
    def format_price(price):
        """Formate un prix avec la devise"""
        return f"{price:.2f} DH"
    
    @staticmethod
    def calculate_total_with_tax(subtotal):
        """Calcule le total avec TVA"""
        tax = subtotal * Config.ECOMMERCE_CONFIG['tax_rate']
        return subtotal + tax
    
    @staticmethod
    def calculate_shipping_cost(subtotal):
        """Calcule les frais de livraison"""
        if subtotal >= Config.ECOMMERCE_CONFIG['free_shipping_threshold']:
            return 0
        return Config.ECOMMERCE_CONFIG['shipping_cost']

# Configuration pour différents environnements
class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'hamzahamza2005',
        'database': 'gestion_utilisateur_dev'
    }

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_CONFIG = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD', ''),
        'database': os.environ.get('DB_NAME', 'gestion_utilisateur_prod')
    }

class TestingConfig(Config):
    TESTING = True
    DATABASE_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'hamzahamza2005',
        'database': 'gestion_utilisateur_test'
    }

# Configuration par défaut
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 