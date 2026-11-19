"""Tests unitaires pour l'audit logger."""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from references.output_schemas import new_session, DirectorVote, BoardSynthesis, RecommendationLabel
from scripts.audit_logger import save_session, list_sessions, load_session, session_index


def test_save_and_load_session(tmp_path):
    """Une session sauvegardée doit pouvoir être rechargée."""
    session = new_session(
        question="Question de test unitaire",
        directors_consulted=["elon-musk", "sam-altman"],
        template_used="innovation-moonshot",
    )
    vote = DirectorVote(
        director_id="elon-musk",
        director_name="Elon Musk — Test",
        thesis="Thèse de test",
        argument="Argument de test",
        risks=["Risque test"],
        next_step="Étape test",
        recommendation_label=RecommendationLabel.PILOT,
        confidence=0.75,
        mental_models_used=["First Principles Thinking"],
    )
    session.votes.append(vote)
    session.synthesis = BoardSynthesis(
        summary="Synthèse de test",
        integrated_recommendation="Recommandation test",
        confidence=0.8,
        contingencies=[],
        directors_consulted=["elon-musk", "sam-altman"],
        conflicts_surfaced=[],
        mental_models_prioritized=["First Principles Thinking"],
    )

    path = save_session(session, audit_dir=tmp_path)
    assert path.exists(), "Le fichier de session doit exister"

    loaded = load_session(session.session_id, audit_dir=tmp_path)
    assert loaded is not None, "La session doit être rechargée"
    assert loaded.session_id == session.session_id
    assert loaded.question == session.question
    assert len(loaded.votes) == 1
    assert loaded.synthesis is not None


def test_list_sessions_returns_metadata(tmp_path):
    """list_sessions doit retourner des métadonnées pour chaque session."""
    # Aucune session au départ
    sessions = list_sessions(tmp_path)
    assert sessions == []

    # Créer une session
    session = new_session(
        question="Question pour list",
        directors_consulted=["elon-musk"],
    )
    save_session(session, audit_dir=tmp_path)

    sessions = list_sessions(tmp_path)
    assert len(sessions) == 1
    assert sessions[0]["session_id"] == session.session_id
    assert sessions[0]["question"] == session.question
    assert sessions[0]["directors_count"] == 1


def test_session_index_returns_markdown(tmp_path):
    """session_index doit retourner du Markdown non vide."""
    index = session_index(tmp_path)
    assert isinstance(index, str)
    assert "Audit Trail" in index


def test_load_nonexistent_session_returns_none(tmp_path):
    """Charger une session inexistante doit retourner None."""
    result = load_session("id_inexistant", audit_dir=tmp_path)
    assert result is None
