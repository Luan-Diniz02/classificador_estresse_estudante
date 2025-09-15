# -*- coding: utf-8 -*-
"""
Módulo do Classificador de Estresse Acadêmico para uso com Flask
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import kagglehub

class ClassificadorEstresse:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.feature_names = []
        self.target_classes = []
        self.X_test = None
        self.y_test = None
        self.y_pred = None
        self.is_model_trained = False
        
    def train_model(self):
        """Treinar o modelo de classificação"""
        try:
            print("Iniciando treinamento do modelo...")
            
            # Baixar e carregar dataset
            path = kagglehub.dataset_download("poushal02/student-academic-stress-real-world-dataset")
            files = os.listdir(path)
            csv_files = [f for f in files if f.endswith('.csv')]
            
            if not csv_files:
                raise FileNotFoundError("Nenhum arquivo CSV encontrado no diretório baixado.")
            
            df = pd.read_csv(os.path.join(path, csv_files[0]))
            
            # Pré-processamento
            df.columns = df.columns.str.strip()
            
            if 'Timestamp' in df.columns:
                df = df.drop(columns=['Timestamp'])
            
            df = df.dropna()
            
            # Codificar variáveis categóricas
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                self.label_encoders[col] = le
            
            # Separar features e alvo
            target_column = 'Rate your academic stress index'
            if target_column not in df.columns:
                raise KeyError(f"A coluna alvo '{target_column}' não foi encontrada.")
            
            X = df.drop(columns=[target_column])
            y = df[target_column]
            
            self.feature_names = X.columns.tolist()
            self.target_classes = sorted(y.unique())
            
            # Dividir dados
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Treinar modelo
            self.model = DecisionTreeClassifier(random_state=42, max_depth=3)
            self.model.fit(X_train, y_train)
            
            # Fazer predições para métricas
            self.y_pred = self.model.predict(X_test)
            self.X_test = X_test
            self.y_test = y_test
            
            self.is_model_trained = True
            
            # Salvar modelo treinado
            self.save_model()
            
            print("Modelo treinado com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro no treinamento: {e}")
            return False
    
    def save_model(self, filename='model.pkl'):
        """Salvar modelo treinado"""
        model_data = {
            'model': self.model,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names,
            'target_classes': self.target_classes,
            'is_trained': self.is_model_trained
        }
        
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Modelo salvo como {filename}")
    
    def load_model(self, filename='model.pkl'):
        """Carregar modelo salvo"""
        try:
            with open(filename, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.label_encoders = model_data['label_encoders']
            self.feature_names = model_data['feature_names']
            self.target_classes = model_data['target_classes']
            self.is_model_trained = model_data['is_trained']
            
            print(f"Modelo carregado de {filename}")
            return True
            
        except FileNotFoundError:
            print(f"Arquivo {filename} não encontrado. Treine o modelo primeiro.")
            return False
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            return False
    
    def is_trained(self):
        """Verificar se o modelo está treinado"""
        return self.is_model_trained and self.model is not None
    
    def prepare_input_data(self, form_data):
        """Preparar dados de entrada para predição"""
        if not self.is_trained():
            raise ValueError("Modelo não está treinado")
        
        # Criar dataframe com os dados do formulário
        df = pd.DataFrame([form_data])
        
        # Aplicar label encoders para colunas categóricas
        for col, le in self.label_encoders.items():
            if col in df.columns:
                try:
                    df[col] = le.transform(df[col])
                except ValueError as e:
                    # Log do erro para debug
                    print(f"Aviso: Valor não reconhecido para '{col}': {df[col].iloc[0]}")
                    print(f"Valores válidos: {list(le.classes_)}")
                    # Usar o valor mais comum (classe 0)
                    df[col] = 0
        
        # Garantir que todas as features estejam presentes
        for feature in self.feature_names:
            if feature not in df.columns:
                print(f"Aviso: Feature '{feature}' não encontrada nos dados de entrada, usando valor padrão 0")
                df[feature] = 0
        
        # Reordenar colunas para corresponder ao modelo
        df = df[self.feature_names]
        
        print(f"Dados preparados para predição: {df.iloc[0].to_dict()}")
        
        return df
    
    def predict_single(self, input_data):
        """Fazer predição para uma amostra"""
        if not self.is_trained():
            raise ValueError("Modelo não está treinado")
        
        prediction = self.model.predict(input_data)
        # Converter de volta para escala 1-5 (modelo usa 0-4)
        return prediction[0] + 1
    
    def predict_probability(self, input_data):
        """Obter probabilidades de predição"""
        if not self.is_trained():
            raise ValueError("Modelo não está treinado")
        
        probabilities = self.model.predict_proba(input_data)
        return probabilities[0]
    
    def predict_batch(self, df):
        """Fazer predições em lote"""
        if not self.is_trained():
            raise ValueError("Modelo não está treinado")
        
        # Pré-processar dados
        df = df.copy()
        
        # Aplicar label encoders
        for col, le in self.label_encoders.items():
            if col in df.columns:
                try:
                    df[col] = le.transform(df[col])
                except ValueError:
                    df[col] = 0
        
        # Garantir que todas as features estejam presentes
        for feature in self.feature_names:
            if feature not in df.columns:
                df[feature] = 0
        
        df = df[self.feature_names]
        
        predictions = self.model.predict(df)
        # Converter de volta para escala 1-5 (modelo usa 0-4)
        return predictions + 1
    
    def get_metrics(self):
        """Obter métricas de avaliação do modelo"""
        if not self.is_trained() or self.y_pred is None:
            return None
        
        accuracy = accuracy_score(self.y_test, self.y_pred)
        
        # Mapear labels de volta para 1-5 para exibição
        target_names = [str(i) for i in range(1, 6)]
        classification_rep = classification_report(
            self.y_test, self.y_pred, 
            output_dict=True, 
            zero_division=0,
            target_names=target_names
        )
        
        metrics = {
            'accuracy': float(accuracy),
            'classification_report': classification_rep,
            'confusion_matrix': confusion_matrix(self.y_test, self.y_pred).tolist(),
            'feature_importance': self.model.feature_importances_.tolist(),
            'feature_names': self.feature_names
        }
        
        return metrics
    
    def get_confusion_matrix(self):
        """Obter matriz de confusão"""
        if not self.is_trained() or self.y_pred is None:
            return None
        
        return confusion_matrix(self.y_test, self.y_pred)
    
    def get_feature_importance(self):
        """Obter importância das features"""
        if not self.is_trained():
            return None
        
        importances = self.model.feature_importances_
        importance_df = pd.DataFrame({
            'Feature': self.feature_names,
            'Importance': importances
        }).sort_values(by='Importance', ascending=False)
        
        return importance_df
    
    def get_feature_names_for_form(self):
        """Obter nomes das features para criar formulário dinâmico"""
        if not self.is_trained():
            return []
        
        return self.feature_names
    
    def get_label_encoder_classes(self, column_name):
        """Obter classes de um label encoder específico"""
        if column_name in self.label_encoders:
            return self.label_encoders[column_name].classes_.tolist()
        return []

# Instância global do classificador para uso na aplicação
classificador_global = ClassificadorEstresse()

def get_classificador():
    """Função para obter instância do classificador"""
    return classificador_global