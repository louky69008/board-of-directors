# Exemples de sessions Board of Directors

Ce dossier contient 5 sessions complètes au format JSON, générées par le système d'audit trail.
Chaque fichier illustre un cas d'usage réel avec :

- La question stratégique soumise
- Le template de décision utilisé
- Les directeurs consultés avec leurs votes structurés
- La synthèse intégrée du board
- Les conflits entre mental models surfacés

## Fichiers disponibles

| Fichier | Cas d'usage | Template | Directeurs |
|---------|-------------|----------|------------|
| `agent-support-client.session.json` | Build vs Buy agent support | `build-vs-buy` | jensen-huang, satya-nadella, reid-hoffman |
| `ai-agent-design.session.json` | Conception agent de code | `ai-agent-design` | sam-altman, demis-hassabis, feifei-li, andrew-ng |
| `prompt-engineering.session.json` | Amélioration chatbot client | `prompt-engineering` | steve-jobs, andrew-ng, sam-altman |
| `software-architecture.session.json` | Monolithe vs Microservices IA | `software-architecture` | jensen-huang, satya-nadella, sundar-pichai |
| `ethics-review.session.json` | Scoring de crédit automatisé | `ethics-review` | feifei-li, satya-nadella, demis-hassabis |

## Utilisation

Ces fichiers peuvent être rechargés avec `scripts/audit_logger.py` :

```python
from scripts.audit_logger import load_session
from pathlib import Path

session = load_session("ex001-agent-support-client", audit_dir=Path("examples"))
print(session.synthesis.integrated_recommendation)
```

Ils servent également de cas de test pour la validation des schémas Pydantic (`references/output_schemas.py`).
