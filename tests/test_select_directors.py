"""Tests unitaires pour le sélecteur de directeurs."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.select_directors import parse_registry, select_directors


REGISTRY_PATH = Path(__file__).resolve().parent.parent / "references" / "decision-templates" / "registry.yaml"


def test_parse_registry_returns_templates():
    """Le registre doit parser au moins un template."""
    templates = parse_registry(REGISTRY_PATH)
    assert len(templates) > 0, "Aucun template parsé depuis le registre"


def test_each_template_has_required_fields():
    """Chaque template doit avoir id, name, keywords, directors."""
    templates = parse_registry(REGISTRY_PATH)
    for t in templates:
        assert "id" in t and t["id"], f"Template sans id: {t}"
        assert "name" in t and t["name"], f"Template sans name: {t}"
        assert "keywords" in t, f"Template sans keywords: {t.get('id')}"
        assert "directors" in t and t["directors"], f"Template sans directors: {t.get('id')}"


def test_select_directors_returns_results_for_known_query():
    """Une demande avec mots-clés connus doit retourner des directeurs."""
    templates = parse_registry(REGISTRY_PATH)
    results = select_directors("concevoir un agent de support client autonome", templates)
    assert len(results) > 0, "Aucun directeur retourné pour une requête connue"
    # Le template ai-agent-design doit matcher
    template_ids = {r["template"] for r in results}
    assert "ai-agent-design" in template_ids, "ai-agent-design absent des résultats"


def test_select_directors_fallback_for_unknown_query():
    """Une demande inconnue doit retourner une liste vide (pas de crash)."""
    templates = parse_registry(REGISTRY_PATH)
    results = select_directors("zzzqwerty inconnu xyz", templates)
    assert isinstance(results, list)
    assert len(results) == 0


def test_select_directors_top_n_limit():
    """top_n doit limiter le nombre de résultats."""
    templates = parse_registry(REGISTRY_PATH)
    results = select_directors("produit stratégie croissance marché utilisateurs", templates, top_n=3)
    assert len(results) <= 3
