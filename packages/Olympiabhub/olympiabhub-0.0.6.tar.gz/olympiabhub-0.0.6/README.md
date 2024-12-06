<img src="static/Marianne.png" alt="Marianne" width="150"/>

# Olympiabhub

Olympiabhub est une librairie Python pour interagir avec l'API Olympia.

## Installation

Vous pouvez installer la librairie via pip :

```sh
pip install olympiabhub
```

## Documentation

1. Ajouter `OLYMPIA_API_TOKEN` à votre `.env` ou passer `token` en paramètre à `OlympiaAPI`

2. Si vous devez utiliser un proxy, ajouter à votre `.env` la variable `PROXY`

### Chat

#### Chat depuis Nubonyxia

```python
from olympiabhub import OlympiaAPI
from dotenv import load_dotenv

load_dotenv()

model = OlympiaAPI(model)
reponse = model.ChatNubonyxia(prompt)
```

#### Chat depuis un environnement sans proxy

```python
from olympiabhub import OlympiaAPI
from dotenv import load_dotenv

load_dotenv()

model = OlympiaAPI(model)
reponse = model.Chat(prompt)
```

### Embeddings

Créer des embeddings pour une liste de textes :

```python
model = OlympiaAPI(model)
embeddings = model.create_embedding(texts=["votre texte", "un autre texte"])
```

### Liste des modèles disponibles

#### Obtenir la liste des modèles LLM

```python
model = OlympiaAPI(model)
llm_models = model.get_llm_models()
print("Modèles LLM disponibles:", llm_models)
```

#### Obtenir la liste des modèles d'embedding

```python
model = OlympiaAPI(model)
embedding_models = model.get_embedding_models()
print("Modèles d'embedding disponibles:", embedding_models)
```
