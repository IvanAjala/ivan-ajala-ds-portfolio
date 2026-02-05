# 🤖 Modelos Treinados
---
## 📊 Modelos Disponíveis

### 🎯 **Random Forest (Modelo Base)**

|Atributo|Valor|Descrição|
|---|---|---|
|**Arquivo**|`random_forest_final_model.pkl`||
|**Tipo**|RandomForestClassifier|Modelo de ensemble|
|**ROC-AUC**|0.8431|Excelente capacidade discriminativa|
|**Recall**|73.5%|Sensibilidade para capturar churn|
|**Precision**|56.5%|Precisão nas predições positivas|
|**Status**|🔄 Modelo base (não calibrado)|Para referência e comparação|

### ✅ **Random Forest Calibrado (Produção)**

|Atributo|Valor|Descrição|
|---|---|---|
|**Arquivo**|`random_forest_calibrated_final.pkl`||
|**Tipo**|CalibratedClassifierCV + Isotonic|Calibração isotônica|
|**ROC-AUC**|0.8431|Mantém performance original|
|**Erro Calibração**|3.14%|Calibração excelente|
|**Brier Score**|0.123|Score de confiabilidade|
|**Status**|✅ **Modelo em produção**|Recomendado para uso|

---

## 📁 Artefatos do Modelo
---

### 🎛️ **Features e Configuração**

|Arquivo|Conteúdo|Formato|
|---|---|---|
|`model_features.txt`|Lista de 64 features esperadas|Texto|
|`feature_importance.csv`|Importância relativa das features|CSV|

### 📈 **Métricas de Performance**

| Arquivo                         | Métricas Incluídas               | Uso             |
| ------------------------------- | -------------------------------- | --------------- |
| `model_metrics.json`            | ROC-AUC, Recall, Precision, F1   | Modelo base     |
| `model_metrics_calibrated.json` | Métricas + Calibration error     | Modelo produção |
| `confusion_matrix.csv`          | Matriz de confusão detalhada     | Avaliação       |
| `threshold_analysis.csv`        | Análise de diferentes thresholds | Otimização      |
| `cv_results.csv`                | Resultados cross-validation      | Validação       |

---

## 🚀 Como Usar

### 📥 **Carregar e Usar o Modelo**

#### Opção 1: Carregar Modelo Calibrado (Produção)

```python
import pickle
import pandas as pd

# Carregar modelo calibrado para produção

with open('models/random_forest_calibrated_final.pkl', 'rb') as f:
    model = pickle.load(f)

# Dados de exemplo (deve ter as 64 features)
# X deve ser um DataFrame do pandas
probabilities = model.predict_proba(X)[:, 1]  # Probabilidades de churn
predictions = model.predict(X)  # Predições binárias (threshold=0.5)

# Usar threshold customizado (ex: 0.4 para maior recall)
custom_predictions = (probabilities >= 0.4).astype(int)
```
#### Opção 2: Carregar Modelo Base (Referência)

```python

# Carregar modelo base para comparação
with open('models/random_forest_final_model.pkl', 'rb') as f:
    model_base = pickle.load(f)
```

### 🔧 **Carregar Features Esperadas**

```python

# Carregar lista de features esperadas
with open('models/model_features.txt', 'r') as f:
    expected_features = [line.strip() for line in f.readlines()]

print(f"Modelo espera {len(expected_features)} features")
print("Primeiras 10 features:", expected_features[:10])

# Garantir que os dados tenham as features corretas
X_processed = X[expected_features]  # Reordenar colunas
```

### 📊 **Carregar Métricas**

```python

import json
import pandas as pd

# Carregar métricas do modelo em produção
with open('models/model_metrics_calibrated.json', 'r') as f:
    metrics = json.load(f)

print("ROC-AUC:", metrics.get('roc_auc', 'N/A'))
print("Recall:", metrics.get('recall', 'N/A'))
print("Calibration Error:", metrics.get('calibration_error', 'N/A'))

# Carregar importância das features
feature_importance = pd.read_csv('models/feature_importance.csv')
top_features = feature_importance.head(10)
print("\nTop 10 features mais importantes:")
print(top_features[['feature', 'importance']])
```
---

## 🎯 **Exemplo Completo de Uso**

```python

"""
Exemplo completo de uso do modelo em produção
"""
import pickle
import pandas as pd
import json

class ChurnPredictor:
    def __init__(self, model_path='models/random_forest_calibrated_final.pkl'):
        """Inicializar preditor de churn"""
        # Carregar modelo
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        # Carregar features esperadas
        with open('models/model_features.txt', 'r') as f:
            self.expected_features = [line.strip() for line in f.readlines()]
        
        # Carregar métricas
        with open('models/model_metrics_calibrated.json', 'r') as f:
            self.metrics = json.load(f)
    
    def predict(self, customer_data, threshold=0.5):
        """
        Fazer predições para novos clientes
        
        Args:
            customer_data: DataFrame com dados dos clientes
            threshold: Threshold para classificação (default: 0.5)
        
        Returns:
            DataFrame com probabilidades e predições
        """
        # Garantir features corretas
        data_processed = customer_data[self.expected_features]
        
        # Calcular probabilidades
        probabilities = self.model.predict_proba(data_processed)[:, 1]
        
        # Fazer predições com threshold
        predictions = (probabilities >= threshold).astype(int)
        
        # Criar DataFrame de resultados
        results = pd.DataFrame({
            'customer_id': customer_data.index if hasattr(customer_data, 'index') else range(len(customer_data)),
            'churn_probability': probabilities,
            'churn_prediction': predictions,
            'risk_category': pd.cut(probabilities, 
                                   bins=[0, 0.3, 0.6, 1.0],
                                   labels=['Baixo', 'Médio', 'Alto'])
        })
        
        return results
    
    def get_model_info(self):
        """Retornar informações do modelo"""
        return {
            'model_type': str(type(self.model)),
            'features_count': len(self.expected_features),
            'performance_metrics': self.metrics,
            'recommended_threshold': 0.5
        }

# Uso:
# predictor = ChurnPredictor()
# results = predictor.predict(novos_clientes)
```
---

## 📋 **Versionamento do Modelo**

|Versão|Data|ROC-AUC|Calibração|Status|Notas|
|---|---|---|---|---|---|
|**1.0.0**|2026-02-05|0.8431|3.14%|✅ Produção|Modelo calibrado otimizado|
|0.5.0|2026-01-20|0.8431|12.96%|🔄 Teste|Modelo base sem calibração|
|0.1.0|2026-01-10|0.8150|N/A|📊 Baseline|Primeira versão|

---

## ⚠️ **Considerações Importantes**

### ✅ **Pré-requisitos**

1. **Features**: Os dados devem conter exatamente as 64 features listadas
    
2. **Pré-processamento**: Aplicar mesmo pré-processamento dos dados de treino
    
3. **Formato**: DataFrame do pandas com colunas nomeadas corretamente
    

### 🔧 **Otimização**

- **Threshold padrão**: 0.5 (balance entre precision e recall)
    
- **Para maior recall**: Use threshold 0.4 (captura mais churns)
    
- **Para maior precision**: Use threshold 0.6 (predições mais confiáveis)
    

### 📊 **Monitoramento**

```python

# Exemplo de monitoramento
def check_model_drift(new_data, reference_metrics):
    """
    Verificar drift do modelo
    """
    # Calcular métricas em novos dados
    # Comparar com métricas de referência
    # Alertar se diferença > 5%
    pass
```
---

## 🔗 **Links Relacionados**

### 📚 Documentação

- [Data Dictionary](https://../docs/data_dictionary.md) - Descrição das features
    
- [Model Documentation](https://../docs/model_documentation.md) - Documentação técnica
    
- [API Documentation](https://../docs/api_documentation.md) - API do modelo
    

### 🛠️ Scripts

- [train_model.py](https://../src/models/train_model.py) - Script de treino
    
- [predict_model.py](https://../src/models/predict_model.py) - Script de predição
    
- [evaluate_model.py](https://../src/models/evaluate_model.py) - Avaliação
    

### 📊 Análises

- [Model Performance](https://../reports/model_performance_dashboard.png) - Dashboard
    
- [Feature Importance](https://../reports/figures/model_performance/feature_importance.png) - Gráfico
    

---

## 🆘 **Suporte e Troubleshooting**

### Problemas Comuns

1. **"Missing features"**: Verifique se todas as 64 features estão presentes
    
2. **"Wrong data type"**: Certifique-se que os tipos de dados estão corretos
    
3. **"Low performance"**: Verifique se o pré-processamento foi aplicado
    

### Contato

- **Issues**: [GitHub Issues](https://.github/ISSUE_TEMPLATE/bug_report.md)
    
- **Documentação**: [docs/](https://../docs/)
    
- **Equipe**: time-ds@empresa.com
    

---

> **Nota**: Este modelo foi treinado com dados até janeiro de 2026. Recomenda-se retreinar periodicamente para manter performance.

---

*Última atualização: 05/02/2026*  
_Versão do documento: 1.0.0_