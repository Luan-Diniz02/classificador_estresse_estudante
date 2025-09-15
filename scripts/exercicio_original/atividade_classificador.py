# -*- coding: utf-8 -*-
"""
SCRIPT ORIGINAL DO EXERCÍCIO - Classificador de Estresse Acadêmico

Este é o script original que treina e avalia um classificador para prever 
o índice de estresse acadêmico de estudantes.

NOTA: Este arquivo é mantido como referência do exercício original.
Para usar a aplicação web, execute: python app.py
"""

# --- BIBLIOTECAS ---
import kagglehub
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# --- DOWNLOAD E CARREGAMENTO DO DATASET ---
print("Baixando o dataset...")
try:
    path = kagglehub.dataset_download("poushal02/student-academic-stress-real-world-dataset")
    print("Caminho para os arquivos do dataset:", path)

    files = os.listdir(path)
    print("Arquivos encontrados:", files)

    # Carregar o arquivo CSV principal
    csv_files = [f for f in files if f.endswith('.csv')]
    if not csv_files:
        raise FileNotFoundError("Nenhum arquivo CSV encontrado no diretório baixado.")

    df = pd.read_csv(os.path.join(path, csv_files[0]))
    print("\n--- Análise Inicial do Dataset ---")
    print("Primeiras 5 linhas:")
    print(df.head())
    print("\nInformações sobre as colunas:")
    df.info()
    print("\nNomes exatos das colunas:")
    print(df.columns)

    # --- PRÉ-PROCESSAMENTO ---
    print("\n--- Iniciando Pré-processamento dos Dados ---")
    
    # 1. Renomear colunas para facilitar o acesso (remover espaços)
    df.columns = df.columns.str.strip()
    
    # 2. Remover coluna irrelevante
    if 'Timestamp' in df.columns:
        df = df.drop(columns=['Timestamp'])
        print("Coluna 'Timestamp' removida.")

    # 3. Tratar valores nulos (remover linhas com valores ausentes)
    initial_rows = len(df)
    df = df.dropna()
    print(f"{initial_rows - len(df)} linhas com valores nulos foram removidas.")

    # 4. Codificar variáveis categóricas para formato numérico
    le = LabelEncoder()
    categorical_cols = df.select_dtypes(include=['object']).columns
    print(f"Codificando as seguintes colunas categóricas: {list(categorical_cols)}")
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col])

    # 5. Separar features (X) e alvo (y)
    target_column = 'Rate your academic stress index'
    if target_column not in df.columns:
        raise KeyError(f"A coluna alvo '{target_column}' não foi encontrada após o pré-processamento.")
        
    X = df.drop(columns=[target_column])
    y = df[target_column]

    print("\nPré-processamento concluído.")
    print("Exemplo das features (X):")
    print(X.head())
    print("\nExemplo do alvo (y):")
    print(y.head())

    # --- DIVISÃO DOS DADOS EM TREINO E TESTE ---
    print("\n--- Dividindo os Dados em Conjuntos de Treino e Teste ---")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Tamanho do conjunto de treino: {X_train.shape[0]} amostras")
    print(f"Tamanho do conjunto de teste: {X_test.shape[0]} amostras")

    # --- TREINAMENTO DO MODELO ---
    print(f"\n--- Treinando o Modelo DecisionTreeClassifier (com max_depth=3) ---")
    # Inicializa o classificador limitando a profundidade para evitar overfitting
    # e com uma semente aleatória para reprodutibilidade
    model = DecisionTreeClassifier(random_state=42, max_depth=3)

    # Treina o modelo com os dados de treino
    model.fit(X_train, y_train)
    print("Modelo treinado com sucesso!")

    # --- AVALIAÇÃO DO MODELO ---
    print("\n--- Avaliando o Desempenho do Modelo ---")
    # Faz previsões nos dados de teste
    y_pred = model.predict(X_test)

    # Calcula a acurácia
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Acurácia do modelo: {accuracy:.4f}")

    # Exibe o relatório de classificação detalhado
    print("\nRelatório de Classificação:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # --- VISUALIZAÇÃO DA MATRIZ DE CONFUSÃO ---
    print("\nGerando a Matriz de Confusão...")
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=sorted(y.unique()), yticklabels=sorted(y.unique()))
    plt.title('Matriz de Confusão')
    plt.ylabel('Classe Verdadeira')
    plt.xlabel('Classe Prevista')
    plt.tight_layout()
    
    # Salvar a imagem da matriz de confusão
    plot_filename = "matriz_confusao.png"
    plt.savefig(plot_filename)
    print(f"Matriz de confusão salva como '{plot_filename}'")
    plt.show()

    # --- IMPORTÂNCIA DAS FEATURES ---
    print("\n--- Verificando a Importância das Features ---")
    importances = model.feature_importances_
    feature_names = X.columns
    
    feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Importance', y='Feature', data=feature_importance_df)
    plt.title('Importância de Cada Feature para o Modelo')
    plt.tight_layout()
    
    # Salvar a imagem das importâncias
    plot_filename_importance = "importancia_features.png"
    plt.savefig(plot_filename_importance)
    print(f"Gráfico de importância das features salvo como '{plot_filename_importance}'")
    plt.show()


except (FileNotFoundError, KeyError) as e:
    print(f"\nErro: {e}")
except Exception as e:
    print(f"\nOcorreu um erro inesperado: {e}")

