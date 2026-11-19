# TODO LIST - Suite aux réunions du bureau des directeurs

**Date :** 9 novembre 2026  
**Priorité :** PILOT contrôlé  
**Objectif :** Implémenter les améliorations validées par le conseil sans compromettre simplicité, transparence, confidentialité

## PHASE 1 - PRÉREQUIS (ACT NOW) - À faire EN PREMIER

- [ ] **Audit permissions TCC** - Lister toutes les permissions, justifier chacune, vérifier révocabilité
- [ ] **Journal d'actions** - Créer/renforcer affichage "ce qui va être fait / où / pourquoi" avant toute action sensible
- [ ] **Bouton "Tout révoquer"** - Tester et s'assurer qu'il fonctionne correctement
- [ ] **Mode dégradé** - Tester fonctionnement sans réseau/certains services
- [ ] **Vérifier accessibilité** - S'assurer respect `prefers-reduced-motion`, contraste suffisant
- [ ] **Audit aucun envoi non consenti** - Vérifier qu'aucune donnée personnelle ne quitte l'appareil sans consentement

## PHASE 2 - INTERFACE VISUELLE PLUS INTUITIVE (Semaine 1)

- [ ] **Matériaux natifs macOS** - Utiliser SF Symbols et `.ultraThinMaterial`/matériaux natifs existants
- [ ] **Animations fonctionnelles uniquement** - Uniquement pour feedback/transition, pas décoratif
- [ ] **Respect prefers-reduced-motion** - Désactiver animations si activé
- [ ] **Améliorer clarté visuelle** - Hiérarchie plus claire, espacement cohérent avec design system
- [ ] **Notifications discrètes** - Améliorer feedback sans alerter excessivement
- [ ] **Tests accessibilité** - Vérifier navigation clavier fonctionne

## PHASE 3 - RAISONNEMENT ET PRISE DE DÉCISION (Semaine 2)

- [ ] **Proposition avant action** - Renforcer (déjà présent mais vérifier strictement)
- [ ] **Alternatives concrètes** - Afficher 2-3 options avec avantages/inconvénients quand pertinent
- [ ] **Mode "Voir raisonnement" optionnel** - Permettre d'afficher raisonnement structuré sans l'afficher par défaut
- [ ] **Routage intelligent** - Utiliser modèle local en priorité, cloud uniquement si nécessaire + consentement
- [ ] **Limiter complexité** - Éviter analyse exhaustive par défaut, proposer décomposition si trop complexe
- [ ] **Être honnête sur limites** - Ne pas deviner, demander clarification si incertain

## PHASE 4 - COMMUNICATION PLUS NATURELLE ET EMPATHIQUE (Semaine 3)

- [ ] **Ton plus fluide** - Adapter subtilement sans caricature
- [ ] **Empathie fonctionnelle** - "Je comprends le problème" plutôt que simulation émotionnelle
- [ ] **Jamais manipuler** - Éviter flatterie pour obtenir accord
- [ ] **Ton collaboratif** - Partenaire égalitaire, pas serviteur
- [ ] **Langage clair** - Éviter anthropomorphisme excessif ("je pense/ressens")
- [ ] **Vérification** - S'assurer aucun langage suggérant émotions/relation personnelle

## PHASE 5 - INTÉGRATION ET STABILISATION (Semaine 4)

- [ ] **Tests de non-régression** - Vérifier fonctionnalités existantes intactes
- [ ] **Mesurer métriques** - Tester clarté, compréhensibilité, simplicité perçue
- [ ] **Vérifier performances** - Pas de ralentissement perceptible
- [ ] **Journal d'actions fonctionnel** - Test complet
- [ ] **Révocation testée** - "Tout révoquer" fonctionne
- [ ] **Revue finale avec utilisateur** - Validation avant élargissement

## À NE PAS FAIRE (Interdits par le conseil)

- [ ] **NE PAS** ajouter télémétrie/analytics cachés
- [ ] **NE PAS** envoyer données personnelles sans consentement explicite
- [ ] **NE PAS** agir automatiquement sans proposition + accord
- [ ] **NE PAS** simuler émotions/relations personnelles
- [ ] **NE PAS** sur-complexifier interface
- [ ] **NE PAS** généraliser sans pilote mesurable
- [ ] **NE PAS** compromettre accessibilité

## Critères de validation

- [ ] Toutes les actions sensibles passent par proposition + accord
- [ ] 100% respect prefers-reduced-motion
- [ ] Journal d'actions lisible et complet
- [ ] "Tout révoquer" fonctionne
- [ ] Aucun envoi non consenti
- [ ] Interface plus claire OU égale, jamais plus confuse
- [ ] Plus fluide sans perdre contrôle
- [ ] Utilisateur confirme "plus simple ou aussi simple"

**Principe directeur : "Un parcours bien fait > dix fonctionnalités"**
