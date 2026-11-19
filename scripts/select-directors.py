#!/usr/bin/env python3
"""Sélectionne les directeurs les plus pertinents pour une demande utilisateur.

Lit references/decision-templates/registry.yaml, fait du matching par mots-clés
sur la description de la demande, et affiche les directeurs recommandés par
ordre de pertinence.

Usage:
    python scripts/select-directors.py "<description de la demande>"
"""

import re
import sys
from pathlib import Path

REGISTRY_PATH = (
    Path(__file__).resolve().parent.parent
    / "references"
    / "decision-templates"
    / "registry.yaml"
)


def parse_registry(path: Path):
    """Parse minimaliste du registry.yaml (structure connue et régulière).

    Extrait pour chaque template : id, name, keywords, directors.
    Aucune dépendance externe requise.
    """
    text = path.read_text(encoding="utf-8")
    templates = []
    current = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("- id:"):
            if current is not None:
                templates.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
        elif current is not None:
            if line.startswith("name:"):
                current["name"] = line.split(":", 1)[1].strip()
            elif line.startswith("keywords:"):
                m = re.search(r"\[(.*)\]", line)
                if m:
                    current["keywords"] = [
                        k.strip().strip('"').strip("'")
                        for k in m.group(1).split(",")
                        if k.strip()
                    ]
                else:
                    current["keywords"] = []
            elif line.startswith("directors:"):
                m = re.search(r"\[(.*)\]", line)
                if m:
                    current["directors"] = [
                        d.strip().strip('"').strip("'")
                        for d in m.group(1).split(",")
                        if d.strip()
                    ]
                else:
                    current["directors"] = []

    if current is not None:
        templates.append(current)

    return templates


def select_directors(query: str, templates, top_n: int = 5):
    """Correspond les mots-clés de la query aux templates.

    Retourne une liste de dicts triés par score décroissant :
    {director, template, template_name, score, matched_keywords}
    """
    query_lower = query.lower()
    scored = []

    for t in templates:
        score = 0
        matched = []
        for kw in t.get("keywords", []):
            if kw.lower() in query_lower:
                score += 1
                matched.append(kw)
        if score > 0:
            scored.append((score, t, matched))

    scored.sort(key=lambda x: x[0], reverse=True)

    seen = set()
    results = []
    for score, t, matched in scored[:top_n]:
        for d in t.get("directors", []):
            if d not in seen:
                seen.add(d)
                results.append({
                    "director": d,
                    "template": t.get("id"),
                    "template_name": t.get("name"),
                    "score": score,
                    "matched_keywords": matched,
                })

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/select-directors.py '<description de la demande>'")
        sys.exit(1)

    query = sys.argv[1]
    templates = parse_registry(REGISTRY_PATH)
    results = select_directors(query, templates)

    if not results:
        print(f"Aucun template ne correspond aux mots-clés de : '{query}'")
        print("Directeurs par défaut recommandés : sundar-pichai, sam-altman, demis-hassabis")
        return

    print(f"Demande : {query}\n")
    print("Directeurs recommandés :")
    for r in results:
        kws = ", ".join(r["matched_keywords"])
        print(
            f"  - {r['director']} "
            f"(via '{r['template_name']}', score {r['score']}, mots-clés: {kws})"
        )


if __name__ == "__main__":
    main()
