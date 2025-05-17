from transformers import pipeline
from sklearn.metrics import precision_recall_fscore_support

# Texto de ejemplo en inglés
texto = """
Microsoft and OpenAI are partnering to advance artificial intelligence technologies.
The project received funding from the Government of Spain and Stanford University.
"""

# Entidades esperadas (ground truth)
entidades_esperadas = [
    {"entity_group": "ORG", "word": "Microsoft"},
    {"entity_group": "ORG", "word": "OpenAI"},
    {"entity_group": "LOC", "word": "Government of Spain"},
    {"entity_group": "ORG", "word": "Stanford University"}
]

# Modelos de NER actualizados (2024-2025)
modelos = {
    "dslim/bert-large-NER": "English (BERT Large)"
}

resultados = {}

for model_id, descripcion in modelos.items():
    print(f"\n Testing model: {descripcion} ({model_id})")
    ner = pipeline("ner", model=model_id, aggregation_strategy="simple")
    predicciones = ner(texto)

    # Formatear predicciones
    pred_entidades = [(ent["entity_group"], ent["word"]) for ent in predicciones]
    real_entidades = [(ent["entity_group"], ent["word"]) for ent in entidades_esperadas]

    # Crear lista de palabras únicas
    all_words = list(set([w for _, w in pred_entidades + real_entidades]))

    y_true = []
    y_pred = []

    for palabra in all_words:
        etiqueta_real = next((tag for tag, w in real_entidades if w == palabra), "O")
        etiqueta_pred = next((tag for tag, w in pred_entidades if w == palabra), "O")
        y_true.append(etiqueta_real)
        y_pred.append(etiqueta_pred)

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="macro", zero_division=0
    )

    print(" Precision:", round(precision, 3))
    print(" Recall:", round(recall, 3))
    print(" F1-score:", round(f1, 3))

    resultados[model_id] = {"descripcion": descripcion, "f1": f1}

# Mostrar mejor modelo
mejor_modelo = max(resultados.items(), key=lambda x: x[1]["f1"])
print("\n Best Model:")
print(f"{mejor_modelo[1]['descripcion']} ({mejor_modelo[0]}) with F1 = {round(mejor_modelo[1]['f1'], 3)}")
