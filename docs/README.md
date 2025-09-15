# Classificador de Estresse Acadêmico - Interface Web

Uma aplicação web Flask para visualização e uso do classificador de estresse acadêmico desenvolvido anteriormente.

## 🚀 Funcionalidades

### Dashboard Principal
- **Métricas do Modelo**: Visualização da acurácia, precision, recall e F1-score
- **Matriz de Confusão Interativa**: Gráfico interativo usando Plotly
- **Importância das Features**: Visualização das variáveis mais importantes para as predições
- **Relatório Detalhado**: Tabela completa com métricas por classe

### Predições Individuais
- **Formulário Dinâmico**: Interface amigável para entrada de dados
- **Validação em Tempo Real**: Validação dos campos conforme o usuário preenche
- **Resultado Instantâneo**: Predição imediata com nível de confiança
- **Interpretação**: Explicação dos níveis de estresse

### Upload de CSV
- **Processamento em Lote**: Upload de arquivos CSV para múltiplas predições
- **Validação de Arquivo**: Verificação de formato e tamanho
- **Visualização de Resultados**: Tabela com resultados e estatísticas
- **Download de Resultados**: Exportação dos resultados em CSV

### API REST
- **Endpoint de Métricas**: `/api/metrics` - Obter métricas do modelo
- **Endpoint de Predição**: `/api/predict` - Fazer predições via API
- **Formato JSON**: Comunicação padronizada

## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask 2.3.3**: Framework web
- **Scikit-learn 1.3.0**: Machine learning
- **Pandas 2.0.3**: Manipulação de dados
- **NumPy 1.24.3**: Computação numérica
- **Matplotlib 3.7.1**: Visualizações estáticas
- **Seaborn 0.12.2**: Visualizações estatísticas
- **Plotly 5.15.0**: Gráficos interativos
- **KaggleHub 0.2.0**: Download de datasets

### Frontend
- **Bootstrap 5.3.0**: Framework CSS
- **Bootstrap Icons**: Ícones
- **Plotly.js**: Gráficos interativos no frontend
- **JavaScript ES6+**: Interatividade
- **CSS3**: Estilos customizados

## 📁 Estrutura do Projeto

```
classificador_estresse_estudante/
├── app.py                      # Aplicação Flask principal
├── config.py                   # Configurações centralizadas
├── requirements.txt            # Dependências Python
├── run.bat                     # Script de execução
├── .env.example               # Exemplo de variáveis de ambiente
├── src/                       # Código fonte
│   ├── __init__.py
│   └── classificador_module.py # Módulo do classificador ML
├── scripts/                   # Scripts auxiliares
│   └── exercicio_original/
│       └── atividade_classificador.py # Script original do classificador
├── templates/                 # Templates HTML
│   ├── base.html             # Template base
│   ├── dashboard.html        # Dashboard principal
│   ├── predict.html          # Formulário de predição
│   └── upload.html           # Upload de arquivos
├── static/                   # Arquivos estáticos
│   ├── css/
│   │   └── style.css        # Estilos customizados
│   └── js/
│       └── main.js          # JavaScript principal
├── models/                   # Modelos treinados
│   └── model.pkl
├── uploads/                  # Diretório de uploads (criado automaticamente)
├── docs/                     # Documentação
│   ├── README.md
│   └── ESTRUTURA_FINAL.md
└── __pycache__/             # Cache Python (auto-gerado)
```

## 🔧 Instalação e Configuração

### 1. Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 2. Instalação das Dependências
```powershell
# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configuração
```powershell
# Definir variáveis de ambiente (opcional)
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
```

## 🚀 Como Executar

### 1. Inicialização
```powershell
# Executar a aplicação
python app.py
```

### 2. Acessar a Aplicação
- Abra o navegador e acesse: `http://localhost:5000`
- A aplicação estará disponível na porta 5000

### 3. Primeiro Uso
1. **Treine o Modelo**: Na primeira execução, clique em "Treinar Modelo" no dashboard
2. **Aguarde o Treinamento**: O processo pode levar alguns minutos
3. **Explore as Funcionalidades**: Após o treinamento, todas as funcionalidades estarão disponíveis

## 📊 Como Usar

### Dashboard
1. Acesse a página inicial para ver um resumo do modelo
2. Visualize métricas de performance, matriz de confusão e importância das features
3. Use as "Ações Rápidas" para navegar rapidamente

### Fazer Predições
1. Acesse "Predição Individual" no menu
2. Preencha o formulário com os dados do estudante
3. Clique em "Fazer Predição" para ver o resultado
4. O sistema mostrará o nível de estresse previsto e a confiança da predição

### Upload de Dados em Lote
1. Acesse "Upload CSV" no menu
2. Prepare um arquivo CSV com as colunas necessárias
3. Faça upload do arquivo
4. Visualize os resultados e faça download se necessário

### Usar a API
```javascript
// Exemplo de uso da API
fetch('/api/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        "Your Academic Stage": "undergraduate",
        "Peer pressure": 3,
        "Academic pressure from your home": 4,
        // ... outros campos
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 📝 Formato dos Dados

### Campos do Formulário (baseados no dataset real):
- `Your Academic Stage`: Estágio acadêmico ("high school", "undergraduate", "post-graduate")
- `Peer pressure`: Pressão dos colegas (escala 1-5)
- `Academic pressure from your home`: Pressão acadêmica de casa (escala 1-5)
- `Study Environment`: Ambiente de estudo ("Peaceful", "Noisy", "disrupted")
- `What coping strategy you use as a student?`: Estratégia de enfrentamento (3 opções)
- `Do you have any bad habits like smoking, drinking on a daily basis?`: Maus hábitos ("No", "Yes", "prefer not to say")
- `What would you rate the academic  competition in your student life`: Competição acadêmica (escala 1-5)

### Interpretação dos Resultados:
- **1-2**: Baixo estresse acadêmico
- **3**: Estresse acadêmico moderado
- **4-5**: Alto estresse acadêmico

## 🎨 Características da Interface

### Design Responsivo
- Interface adaptável para desktop, tablet e mobile
- Cards modernos com efeitos de hover
- Gradientes e animações suaves
- Tipografia otimizada para legibilidade

### Acessibilidade
- Suporte a navegação por teclado
- Contraste adequado para leitura
- Suporte a leitores de tela
- Feedback visual claro para ações

### Performance
- Carregamento otimizado de recursos
- Validação em tempo real
- Gráficos interativos com Plotly
- Cache adequado de arquivos estáticos

## 🔧 Desenvolvimento

### Estrutura do Código
- **Separação de responsabilidades**: Backend (Flask) e Frontend (JavaScript)
- **Modularização**: Classificador em módulo separado
- **Reutilização**: Templates base e componentes
- **Manutenibilidade**: Código bem documentado e organizado

### Boas Práticas Implementadas
- Validação de entrada de dados
- Tratamento de erros
- Logging apropriado
- Segurança básica (validação de arquivos, sanitização)
- Responsividade mobile-first

## 🚨 Importante

⚠️ **Esta aplicação é para fins educacionais e de demonstração.**
- Não deve ser usada como substituto para avaliação profissional
- Os resultados são estatísticos e não diagnósticos
- Em caso de problemas reais de saúde mental, procure ajuda profissional

## 🤝 Suporte

Para dúvidas ou problemas:
1. Verifique se todas as dependências foram instaladas
2. Certifique-se de que o Python 3.8+ está sendo usado
3. Verifique se o modelo foi treinado adequadamente
4. Consulte os logs da aplicação para erros específicos

## 📄 Licença

Projeto desenvolvido para fins acadêmicos - Aprendizado de Máquina, 8º período.