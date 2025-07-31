# import os

# class Config:
#     # Configuração do banco de dados MySQL
#     DB_HOST = 'localhost'
#     DB_USER = 'root'
#     DB_PASSWORD = ''
#     DB_NAME = 'ecommerce_loja'
#     DB_PORT = 3306  

#     # Configuração de upload
#     UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')

#     # Secret key
#     SECRET_KEY = '123456789'

#     # Outras configurações
#     MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
#     ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}




# Criando configuração atualizada
import os
import _mysql_connector

class Config:
    # Configuração do banco de dados MySQL/MariaDB
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PASSWORD = ''
    DB_NAME = 'ecommerce_loja'
    DB_PORT = 3306

    # Configuração de upload - CORRIGIDO
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    
    # Secret key para sessões
    SECRET_KEY = '123456789'

    # Configurações de arquivo
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Configurações adicionais
    DEBUG = True
    TESTING = False
    
    @staticmethod
    def init_app(app):
        """Inicializa configurações específicas da aplicação"""
        # Garante que a pasta de upload existe
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        # Configura o Flask
        app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
        app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
        
        print(f"📁 Pasta de uploads: {Config.UPLOAD_FOLDER}")
        print(f"🗄️  Banco de dados: {Config.DB_NAME} em {Config.DB_HOST}:{Config.DB_PORT}")

# Configuração para desenvolvimento
class DevelopmentConfig(Config):
    DEBUG = True
    
# Configuração para produção
class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-super-secreta-producao'




