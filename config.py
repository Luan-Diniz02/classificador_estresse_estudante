# -*- coding: utf-8 -*-
"""
Configurações da Aplicação Flask - Classificador de Estresse Acadêmico
"""

import os
from datetime import timedelta

class Config:
    """Configuração base da aplicação"""
    
    # Configurações Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'academic_stress_classifier_secret_key_2025'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 'on']
    
    # Configurações de Upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'csv', 'txt'}
    
    # Configurações do Modelo
    MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
    MODEL_FILE = os.path.join(MODEL_PATH, 'model.pkl')
    
    # Configurações de Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Configurações de Plotly (se habilitado)
    PLOTLY_ENABLED = os.environ.get('PLOTLY_ENABLED', 'False').lower() in ['true', '1', 'on']
    
    @staticmethod
    def init_app(app):
        """Inicializar configurações específicas da aplicação"""
        # Criar diretórios necessários
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.MODEL_PATH, exist_ok=True)

class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False

class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    DEBUG = True

# Mapeamento de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Retorna a configuração baseada na variável de ambiente"""
    return config[os.environ.get('FLASK_CONFIG', 'default')]