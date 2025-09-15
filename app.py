# -*- coding: utf-8 -*-
"""
Flask Web Application para Visualização do Classificador de Estresse Acadêmico
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import pandas as pd
import numpy as np
import io
import base64
import json
import pickle
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from werkzeug.utils import secure_filename
from datetime import datetime

# Importar o módulo do classificador
try:
    from src.classificador_module import ClassificadorEstresse
except ImportError:
    print("Módulo classificador_module não encontrado. Execute primeiro o script principal.")

# Importar configurações
from config import get_config

app = Flask(__name__)
config_class = get_config()
app.config.from_object(config_class)
config_class.init_app(app)

# Variável global para armazenar o modelo treinado
classificador = None

def init_model():
    """Inicializar o modelo classificador"""
    global classificador
    try:
        classificador = ClassificadorEstresse()
        print("Modelo inicializado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao inicializar modelo: {e}")
        return False

@app.route('/')
def index():
    """Página principal do dashboard"""
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard com métricas e visualizações do modelo"""
    global classificador
    
    if classificador is None or not classificador.is_trained():
        flash('Modelo não foi treinado ainda. Treine o modelo primeiro.', 'warning')
        return render_template('dashboard.html', model_trained=False)
    
    # Obter métricas do modelo
    metrics = classificador.get_metrics()
    
    # Gerar gráficos
    confusion_matrix_plot = create_confusion_matrix_plot()
    feature_importance_plot = create_feature_importance_plot()
    
    return render_template('dashboard.html', 
                         model_trained=True,
                         metrics=metrics,
                         confusion_matrix=confusion_matrix_plot,
                         feature_importance=feature_importance_plot)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Página para fazer predições individuais"""
    global classificador
    
    if request.method == 'GET':
        return render_template('predict.html')
    
    if classificador is None or not classificador.is_trained():
        flash('Modelo não foi treinado ainda. Treine o modelo primeiro.', 'error')
        return render_template('predict.html')
    
    try:
        # Obter dados do formulário
        form_data = request.form.to_dict()
        
        # Converter para formato adequado para predição
        input_data = classificador.prepare_input_data(form_data)
        
        # Fazer predição
        prediction = classificador.predict_single(input_data)
        probability = classificador.predict_probability(input_data)
        
        result = {
            'prediction': prediction,
            'probability': probability,
            'input_data': form_data
        }
        
        return render_template('predict.html', result=result)
        
    except Exception as e:
        flash(f'Erro ao fazer predição: {str(e)}', 'error')
        return render_template('predict.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """Upload de arquivo CSV para predições em lote"""
    if request.method == 'GET':
        return render_template('upload.html')
    
    global classificador
    
    if classificador is None or not classificador.is_trained():
        flash('Modelo não foi treinado ainda. Treine o modelo primeiro.', 'error')
        return render_template('upload.html')
    
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado', 'error')
        return render_template('upload.html')
    
    file = request.files['file']
    
    if file.filename == '':
        flash('Nenhum arquivo selecionado', 'error')
        return render_template('upload.html')
    
    if file and file.filename.lower().endswith('.csv'):
        try:
            # Ler o arquivo CSV
            df = pd.read_csv(file)
            
            # Fazer predições em lote
            predictions = classificador.predict_batch(df)
            
            # Preparar resultados
            results_df = df.copy()
            results_df['Predicted_Stress_Level'] = predictions
            
            # Converter para JSON para exibição
            results_json = results_df.head(50).to_dict('records')  # Limitar a 50 registros para exibição
            
            return render_template('upload.html', 
                                 results=results_json,
                                 total_predictions=len(predictions))
            
        except Exception as e:
            flash(f'Erro ao processar arquivo: {str(e)}', 'error')
            return render_template('upload.html')
    
    else:
        flash('Por favor, selecione um arquivo CSV válido', 'error')
        return render_template('upload.html')

@app.route('/train')
def train_model():
    """Treinar o modelo"""
    global classificador
    
    try:
        if classificador is None:
            classificador = ClassificadorEstresse()
        
        classificador.train_model()
        flash('Modelo treinado com sucesso!', 'success')
        
    except Exception as e:
        flash(f'Erro ao treinar modelo: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/api/metrics')
def api_metrics():
    """API endpoint para obter métricas do modelo"""
    global classificador
    
    if classificador is None or not classificador.is_trained():
        return jsonify({'error': 'Model not trained'}), 400
    
    metrics = classificador.get_metrics()
    return jsonify(metrics)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint para fazer predições"""
    global classificador
    
    if classificador is None or not classificador.is_trained():
        return jsonify({'error': 'Model not trained'}), 400
    
    try:
        data = request.get_json()
        input_data = classificador.prepare_input_data(data)
        prediction = classificador.predict_single(input_data)
        probability = classificador.predict_probability(input_data)
        
        return jsonify({
            'prediction': int(prediction),
            'probability': float(probability.max())
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def create_confusion_matrix_plot():
    """Criar gráfico da matriz de confusão usando matplotlib"""
    global classificador
    
    if classificador is None or not classificador.is_trained():
        return None
    
    try:
        cm = classificador.get_confusion_matrix()
        
        # Criar o gráfico com matplotlib
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Matriz de Confusão')
        plt.ylabel('Classe Verdadeira')
        plt.xlabel('Classe Prevista')
        
        # Salvar como base64 para embedding
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
        plt.close()
        
        return img_base64
        
    except Exception as e:
        print(f"Erro ao criar matriz de confusão: {e}")
        return None

def create_feature_importance_plot():
    """Criar gráfico de importância das features usando matplotlib"""
    global classificador
    
    if classificador is None or not classificador.is_trained():
        return None
    
    try:
        importance_df = classificador.get_feature_importance()
        
        # Criar o gráfico com matplotlib
        plt.figure(figsize=(10, 8))
        plt.barh(range(len(importance_df)), importance_df['Importance'], color='skyblue')
        plt.yticks(range(len(importance_df)), importance_df['Feature'])
        plt.xlabel('Importância')
        plt.title('Importância das Features')
        plt.tight_layout()
        
        # Salvar como base64 para embedding
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
        plt.close()
        
        return img_base64
        
    except Exception as e:
        print(f"Erro ao criar gráfico de importância: {e}")
        return None

if __name__ == '__main__':
    # Inicializar o modelo ao iniciar a aplicação
    if init_model():
        print("Aplicação Flask iniciada com sucesso!")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Erro: Não foi possível inicializar o modelo. Certifique-se de que o classificador_module.py existe.")