"""Schémas de sortie structurés pour le Board of Directors.

Modèles Pydantic v2 pour valider automatiquement :
- le vote de chaque directeur (thesis, argument, risques, prochaine étape, label, confiance)
- la synthèse intégrée du board (recommandation, confiance, contingences, conflits)
- une session board complète (métadonnées, votes, synthèse, export)

Ces schémas garantissent que toutes les sorties du board ont une structure
uniforme, parseable par des systèmes externes, et qu'aucune sortie n'est
incomplète ou mal formée.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class RecommendationLabel(str, Enum):
    """Étiquettes de recommandation utilisées par tous les directeurs."""

    ACT_NOW = "Act Now"
    PILOT = "Pilot"
    INVESTIGATE_FURTHER = "Investigate Further"
    DISCARD = "Discard"


class DirectorVote(BaseModel):
    """Vote structuré d'un directeur sur une question donnée.

    Chaque directeur doit produire un vote suivant ce schéma, ce qui
    garantit l'uniformité des outputs à travers les 10 profils.
    """

    director_id: str = Field(
        ...,
        description="Identifiant du directeur (ex: elon-musk, sam-altman).",
    )
    director_name: str = Field(
        ...,
        description="Nom complet du directeur (ex: Elon Musk — Innovation & First Principles).",
    )
    thesis: str = Field(
        ...,
        min_length=1,
        description="Thèse principale du directeur en une phrase.",
    )
    argument: str = Field(
        ...,
        min_length=1,
        description="Argumentaire détaillé soutenant la thèse.",
    )
    risks: List[str] = Field(
        default_factory=list,
        description="Risques identifiés par ce directeur.",
    )
    next_step: str = Field(
        ...,
        min_length=1,
        description="Prochaine étape concrète recommandée.",
    )
    recommendation_label: RecommendationLabel = Field(
        ...,
        description="Étiquette de recommandation (Act Now / Pilot / Investigate Further / Discard).",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Niveau de confiance du directeur (0.0 à 1.0).",
    )
    mental_models_used: List[str] = Field(
        default_factory=list,
        description="Modèles cognitifs mobilisés (référence à references/mental-models.md).",
    )

    @field_validator("risks")
    @classmethod
    def risks_must_be_non_empty_strings(cls, v):
        for r in v:
            if not r or not r.strip():
                raise ValueError("Chaque risque doit être une chaîne non vide.")
        return v

    @field_validator("mental_models_used")
    @classmethod
    def mental_models_must_be_non_empty_strings(cls, v):
        for m in v:
            if not m or not m.strip():
                raise ValueError("Chaque mental model doit être une chaîne non vide.")
        return v


class BoardSynthesis(BaseModel):
    """Synthèse intégrée du board après récolte de tous les votes.

    Produite à l'étape 5 de la méthodologie de décision.
    """

    summary: str = Field(
        ...,
        min_length=1,
        description="Résumé exécutif de la décision (2-3 phrases).",
    )
    integrated_recommendation: str = Field(
        ...,
        min_length=1,
        description="Recommandation intégrée et priorisée.",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confiance globale du board (0.0 à 1.0).",
    )
    contingencies: List[str] = Field(
        default_factory=list,
        description="Scénarios de repli et conditions de réversibilité.",
    )
    directors_consulted: List[str] = Field(
        ...,
        min_length=1,
        description="Identifiants des directeurs ayant participé.",
    )
    conflicts_surfaced: List[str] = Field(
        default_factory=list,
        description="Conflits explicites entre les mental models des directeurs.",
    )
    mental_models_prioritized: List[str] = Field(
        default_factory=list,
        description="Modèles cognitifs ayant guidé la synthèse finale.",
    )


class BoardSession(BaseModel):
    """Session board complète, exportable pour audit trail.

    Représente une session décisionnelle de bout en bout.
    """

    session_id: str = Field(
        default_factory=lambda: uuid4().hex,
        description="Identifiant unique de la session.",
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="Horodatage UTC de la session (ISO 8601).",
    )
    question: str = Field(
        ...,
        min_length=1,
        description="Question stratégique soumise au board.",
    )
    template_used: Optional[str] = Field(
        default=None,
        description="Identifiant du template de décision utilisé (ex: ai-agent-design).",
    )
    directors_consulted: List[str] = Field(
        ...,
        min_length=1,
        description="Identifiants des directeurs consultés.",
    )
    votes: List[DirectorVote] = Field(
        default_factory=list,
        description="Votes de chaque directeur.",
    )
    synthesis: Optional[BoardSynthesis] = Field(
        default=None,
        description="Synthèse intégrée du board (ajoutée après step 5).",
    )
    export_path: Optional[str] = Field(
        default=None,
        description="Chemin du fichier d'export audit trail (si généré).",
    )

    def to_json(self, indent: int = 2) -> str:
        """Sérialise la session en JSON pour export audit trail."""
        return self.model_dump_json(indent=indent)

    @classmethod
    def from_json(cls, data: str) -> "BoardSession":
        """Désérialise une session depuis du JSON."""
        return cls.model_validate_json(data)


def new_session(question: str, directors_consulted: List[str], template_used: Optional[str] = None) -> BoardSession:
    """Crée une nouvelle session board vide, prête à recevoir les votes."""
    return BoardSession(
        question=question,
        template_used=template_used,
        directors_consulted=directors_consulted,
    )
