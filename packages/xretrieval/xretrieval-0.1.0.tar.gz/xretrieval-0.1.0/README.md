
# x.retrieval

Retrieve and evaluate with X (any) models.

This project simplifies automated text-image retrieval benchmarks.

Inputs:

- A dataset
- A model
- A mode (e.g. `image-to-image`)


Outputs:

- A retrieval results dataframe
- A retrieval metrics dataframe

## 🌟 Key Features

- ✅ Supports a wide range of models and datasets.
- ✅ Installation in one line.
- ✅ Run benchmarks with one function call.

## 🚀 Quickstart

```python
import xretrieval

xretrieval.run_benchmark(
    dataset_name="coco-val-2017",
    model_id="transformers/Salesforce/blip2-itm-vit-g",
    mode="text-to-text",
)
```

Output:

```bash
{
    'MRR': 0.2953,
    'NormalizedDCG': 0.3469,
    'Precision': 0.2226,
    'Recall': 0.4864,
    'HitRate': 0.4864,
    'MAP': 0.2728
}

```

## 📦 Installation

```bash
pip install xretrieval
```

## 🛠️ Usage

List datasets:

```python
xretrieval.list_datasets()
```

List models:

```python
xretrieval.list_models()
```

## 🧰 Supported Models and Datasets

Models:

```
                         Available Models                         
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Model ID                                         ┃ Model Input ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ transformers/Salesforce/blip2-itm-vit-g          │ text-image  │
│ transformers/Salesforce/blip2-itm-vit-g-text     │ text        │
│ transformers/Salesforce/blip2-itm-vit-g-image    │ image       │
│ sentence-transformers/paraphrase-MiniLM-L3-v2    │ text        │
│ sentence-transformers/paraphrase-albert-small-v2 │ text        │
│ sentence-transformers/multi-qa-distilbert-cos-v1 │ text        │
│ sentence-transformers/all-MiniLM-L12-v2          │ text        │
│ sentence-transformers/all-distilroberta-v1       │ text        │
│ sentence-transformers/multi-qa-mpnet-base-dot-v1 │ text        │
│ sentence-transformers/all-mpnet-base-v2          │ text        │
│ sentence-transformers/multi-qa-MiniLM-L6-cos-v1  │ text        │
│ sentence-transformers/all-MiniLM-L6-v2           │ text        │
│ timm/resnet18.a1_in1k                            │ image       │
└──────────────────────────────────────────────────┴─────────────┘
```

Datasets:

- `coco-val-2017`
