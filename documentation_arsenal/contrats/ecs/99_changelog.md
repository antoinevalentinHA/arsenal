# 🧠 ARSENAL — ECS  
# Changelog officiel

Chemin : `/homeassistant/documentation_arsenal/ecs/99_changelog.md`  
Statut : **RÉFÉRENTIEL — OPPOSABLE**  
Périmètre : Historique ECS

---

## Règles de gouvernance du changelog

Toute évolution du corpus ECS doit :

- être documentée ici
- être datée
- être justifiée
- référencer les documents impactés

Aucune modification n’est valide
sans entrée correspondante.

---

## Format standard

Chaque entrée respecte le modèle :

[YYYY-MM-DD] — vX.Y.Z — Statut
Contexte
Modifications
Impacts
Validation

---

## Historique

---

## [2026-02-08] — v1.0.0 — Institutionnalisation ECS

### Contexte
- Stabilisation complète du sous-système ECS
- Séparation documentaire alignée sur Chauffage
- Formalisation des sous-systèmes et invariants

### Modifications
- Création du dossier ecs/
- Découpage du contrat monolithique en corpus normatif
- Ajout des contrats spécialisés (00 → 10)

### Impacts
- Gouvernance ECS renforcée
- Auditabilité complète
- Extension future sécurisée

### Validation
- Mise en production documentaire
- Validation utilisateur