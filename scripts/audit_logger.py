#!/usr/bin/env python3
"""Audit Trail — système de logging des sessions Board of Directors.

Sauvegarde chaque session board en JSON pour gouvernance, debug et
apprentissage sur le long terme. Aucune dépendance externe requise
(au-delà de pydantic déjà utilisé par output_schemas).

Fichiers générés : audit-logs/board-session-<timestamp>-<session_id>.json
Ces fichiers ne sont pas commités (ignorés par .gitignore).
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from references.output_schemas import BoardSession


DEFAULT_AUDIT_DIR = Path("audit-logs")


def ensure_audit_dir(audit_dir: Path = DEFAULT_AUDIT_DIR) -> Path:
    """Crée le répertoire d'audit s'il n'existe pas."""
    audit_dir.mkdir(parents=True, exist_ok=True)
    return audit_dir


def save_session(
    session: BoardSession,
    audit_dir: Path = DEFAULT_AUDIT_DIR,
) -> Path:
    """Écrit une session board en JSON dans le répertoire d'audit.

    Retourne le chemin du fichier écrit.
    """
    ensure_audit_dir(audit_dir)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    filename = f"board-session-{timestamp}-{session.session_id[:8]}.json"
    path = audit_dir / filename
    path.write_text(session.to_json(indent=2), encoding="utf-8")
    session.export_path = str(path)
    return path


def list_sessions(audit_dir: Path = DEFAULT_AUDIT_DIR) -> List[dict]:
    """Liste toutes les sessions d'audit avec leurs métadonnées clés.

    Retourne une liste triée du plus récent au plus ancien.
    Chaque entrée : {session_id, timestamp, question, file, template_used, directors_count}
    """
    if not audit_dir.exists():
        return []

    sessions = []
    for path in sorted(audit_dir.glob("board-session-*.json"), reverse=True):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            sessions.append({
                "session_id": data.get("session_id"),
                "timestamp": data.get("timestamp"),
                "question": data.get("question"),
                "template_used": data.get("template_used"),
                "directors_count": len(data.get("directors_consulted", [])),
                "votes_count": len(data.get("votes", [])),
                "has_synthesis": data.get("synthesis") is not None,
                "file": str(path),
            })
        except (json.JSONDecodeError, OSError):
            # Fichier corrompu ou illisible : on saute mais on ne plante pas.
            continue

    return sessions


def load_session(session_id: str, audit_dir: Path = DEFAULT_AUDIT_DIR) -> Optional[BoardSession]:
    """Recharge une session board depuis son identifiant.

    Retourne None si aucune session correspondante n'est trouvée.
    """
    if not audit_dir.exists():
        return None

    for path in audit_dir.glob("board-session-*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("session_id") == session_id:
                return BoardSession.from_json(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, ValueError):
            continue

    return None


def session_index(audit_dir: Path = DEFAULT_AUDIT_DIR) -> str:
    """Génère un index lisible (Markdown) de toutes les sessions d'audit."""
    sessions = list_sessions(audit_dir)
    if not sessions:
        return "# Audit Trail — Aucune session enregistrée.\n"

    lines = ["# Audit Trail — Sessions du Board", ""]
    lines.append(f"Total : {len(sessions)} session(s)\n")
    lines.append("| Timestamp | Question | Template | Directeurs | Votes | Synthèse | Fichier |")
    lines.append("|---|---|---|---|---|---|---|")
    for s in sessions:
        ts = (s.get("timestamp") or "")[:16].replace("T", " ")
        q = (s.get("question") or "")[:60]
        tmpl = s.get("template_used") or "—"
        dirs = s.get("directors_count", 0)
        votes = s.get("votes_count", 0)
        synth = "Oui" if s.get("has_synthesis") else "Non"
        file = s.get("file", "")
        lines.append(f"| {ts} | {q} | {tmpl} | {dirs} | {votes} | {synth} | {file} |")

    return "\n".join(lines)
