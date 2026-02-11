# ==========================================================
# 🧠 ARSENAL — DOCUMENT D’ARCHITECTURE TECHNIQUE
#     Chauffage — Modèle Machine (V3 PRO)
# ==========================================================
#
# 📌 STATUT :
#   DOCUMENT D’ARCHITECTURE — RÉFÉRENCE TECHNIQUE
#   (NON NORMATIF — MAIS STRUCTURANT)
#
# 🔒 AUTORITÉ :
#   Ce document ne définit AUCUNE règle métier.
#   Il ne possède AUCUNE autorité décisionnelle.
#
#   Il est subordonné aux contrats normatifs Chauffage :
#     - /documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#     - /documentation_arsenal/contrats/chauffage/30_decision_centrale.md
#     - /documentation_arsenal/contrats/chauffage/60_table_decision_canonique.md
#
# 🎯 RÔLE :
#   Décrire l’ARCHITECTURE MACHINE du sous-système Chauffage :
#     - séparation des couches fonctionnelles,
#     - patterns de souveraineté et de protection Cloud,
#     - cycle Trigger → Decision → Action → Guard,
#     - mécanismes de sécurité (locking, filtrage, réalignement).
#
#   Ce document formalise :
#     • l’organisation interne du pipeline,
#     • les responsabilités techniques de chaque couche,
#     • les invariants d’exécution et de résilience.
#
# ----------------------------------------------------------
# 🧠 POSITIONNEMENT ARCHITECTURAL
# ----------------------------------------------------------
#
# - Ce document est :
#     ✅ conforme à la doctrine Chauffage V3 PRO,
#     ✅ aligné avec les contrats normatifs,
#     ✅ fidèle à l’implémentation réelle,
#     ✅ essentiel à la compréhension du fonctionnement interne.
#
# - Il ne décrit volontairement PAS :
#     • la hiérarchie métier,
#     • les règles thermiques,
#     • la table de décision,
#     • la sémantique des statuts.
#
#   Toute règle fonctionnelle doit être recherchée
#   exclusivement dans les contrats normatifs.
#
# ----------------------------------------------------------
# 🔒 RÈGLE DE GOUVERNANCE
# ----------------------------------------------------------
#
# - Ce document :
#     ❌ ne doit JAMAIS être utilisé pour définir une règle métier,
#     ❌ ne doit JAMAIS être opposé à un contrat,
#     ❌ ne doit JAMAIS servir d’arbitrage fonctionnel.
#
# - Il est la référence officielle pour :
#     ✅ l’architecture Chauffage,
#     ✅ les patterns de protection Cloud,
#     ✅ l’ordonnancement des couches,
#     ✅ les audits techniques et refactorings.
#
# ----------------------------------------------------------
# 📌 VALEUR
# ----------------------------------------------------------
#
# - Valeur principale :
#     Document de très haute valeur d’ingénierie système.
#
# - Rôle stratégique :
#     Garantir la maintenabilité, la résilience et la lisibilité
#     du pipeline Chauffage sur le long terme.
#
# ==========================================================


# 🏗️ ARCHITECTURE TECHNIQUE — CHAUFFAGE (V3 PRO)

## 🏛️ MODÈLE "TRIGGER - DECISION - ACTION - GUARD"
L'architecture repose sur un cycle asynchrone sécurisé pour traiter avec des API Cloud lentes ou instables.

### 🧩 LES COUCHES FONCTIONNELLES
1. **COUCHE MIROIR (Mirroring)** :
   - `sensor.chauffage_consigne_..._local` : Capturent et figent les valeurs valides du Cloud.
   - *Rôle* : Agit comme une mémoire tampon (Cache) pour protéger le système des états `unavailable`.

2. **COUCHE ANALYTIQUE (Expertise Statistique)** :
   - `sensor.chauffage_..._suggeree` : Analyse les dérives sur 24h (Doux vs Froid).
   - *Rôle* : Suggère des corrections de Pente ou de Parallèle pour auto-ajuster la loi d'eau.

3. **COUCHE DÉCISIONNELLE (Cerveau)** :
   - `script.chauffage_decision_centrale` : L'unique entité habilitée à modifier l'intention.
   - *Rôle* : Applique la Table de Décision Canonique du Contrat.

4. **COUCHE EXÉCUTIVE (Les Bras)** :
   - `script.chauffage_appliquer_...` : Gère les appels de services et les retries.
   - *Rôle* : Isole la complexité de l'API (ViCare) du reste du système.

5. **COUCHE DE SOUVERAINETÉ (La Garde)** :
   - `automation.realignement_vicare_ha` : Vérifie la cohérence toutes les 10 min.
   - *Rôle* : Si le Cloud change d'état sans ordre d'Arsenal, la Garde le réaligne sur la mémoire locale.



## 🔒 MÉCANISMES DE SÉCURITÉ
- **Verrou d'Atomicité** (`input_boolean.chauffage_application_en_cours`) : Suspend la surveillance pendant qu'une commande est envoyée pour éviter les faux positifs de la Garde.
- **Délai d'Absorption** : Une pause de 3s est appliquée sur les synchronisations inverses pour filtrer les paquets de données instables lors des mises à jour Cloud.
