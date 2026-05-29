# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (SOCLE TRANSVERSAL)
#     OBJET — PÉRIMÈTRE — STATUT
# ==========================================================

# ----------------------------------------------------------
# 📌 STATUT CONTRACTUEL
# ----------------------------------------------------------
#
# Nature :
#   CONTRAT NORMATIF DE DOMAINE — ACTIF
#
# Domaine :
#   Aération → Blocage Chauffage (mode HEAT uniquement)
#
# Autorité d’exécution :
#   - Automation pipeline maître (ID 10010000000023)
#   - Scripts M0..M5 associés
#
# Hiérarchie :
#   Subordonné à :
#     /00_documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#
# Indépendant de :
#   - décision centrale chauffage
#   - offsets thermiques
#   - présence / absence
#   - UI
#
# ----------------------------------------------------------


## 🎯 OBJET DU DOMAINE

Ce domaine définit exclusivement :

- la gestion d’un épisode d’aération physique,
- le blocage thermique temporaire associé,
- l’analyse ΔT différée,
- la levée temporelle contrôlée du blocage,
- les mécanismes de cohérence et de remédiation.

Il ne pilote jamais directement le chauffage.


## 🧱 PÉRIMÈTRE COUVERT

Le domaine couvre :

1. La machine à états M0 → M5
2. Les timers aération (blocage + analyse ΔT)
3. Les snapshots thermiques (T_REF)
4. Les règles de monotonicité
5. Les mécanismes de neutralisation datetime
6. Les garde-fous :
   - mini-guard anti-zombie
   - sécurité démarrage
   - signal recover + M0
7. Les états canons et invariants structurels


## 🚫 HORS PÉRIMÈTRE

Explicitement exclus :

- Détection / agrégation des ouvertures  
  → couvert par le **Contrat Ouvertures (clos et figé)**

- Décision centrale chauffage  
  → relève du domaine Chauffage

- UI et pédagogie

- Toute action matérielle


## 🔁 MODÈLE CONCEPTUEL FONDAMENTAL

Un épisode d’aération est :

- borné dans le temps
- non fusionnable
- doté de références thermiques figées
- clôturé explicitement
- suivi d’un blocage monotone

La levée du blocage est autorisée uniquement en M4.


## 🛑 PRINCIPES STRUCTURELS NON NÉGOCIABLES

- Aucune reprise thermique n’est exécutée ici.
- Aucune échéance ne peut être raccourcie.
- Aucun état implicite n’est toléré.
- Toute remédiation transite par le pipeline maître.
- Aucun timer ne constitue une vérité métier.


## 📌 STATUT

- Contrat actif
- Périmètre strict
- Fusion : NON
- Extensions : soumises au mode opératoire Arsenal

# ==========================================================