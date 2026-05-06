# ==========================================================
# 🧠 ARSENAL — DOCUMENT D’EXPLOITATION & DE MAINTENANCE
#     Chauffage — Réglages & Diagnostic Thermique (V3 PRO)
# ==========================================================
#
# 📌 STATUT :
#   DOCUMENT D’EXPLOITATION — NON NORMATIF
#
# 🔒 AUTORITÉ :
#   Ce document ne constitue PAS un contrat métier.
#   Il ne possède AUCUNE autorité décisionnelle ni normative.
#
#   En cas de divergence, seules font foi les références normatives :
#     - /00_documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#     - /00_documentation_arsenal/contrats/chauffage/30_decision_centrale.md
#     - /00_documentation_arsenal/contrats/chauffage/60_table_decision_canonique.md
#
# 🎯 RÔLE :
#   Fournir un guide PRATIQUE d’exploitation du système Chauffage :
#     - réglage de la loi d’eau,
#     - interprétation des diagnostics visuels,
#     - aide au réglage fin et à la maintenance courante.
#
#   Ce document est destiné :
#     • à l’usage quotidien,
#     • au réglage manuel assisté,
#     • au diagnostic rapide terrain.
#
# ----------------------------------------------------------
# 🧠 POSITIONNEMENT ARCHITECTURAL
# ----------------------------------------------------------
#
# Ce document se situe :
#   - EN AVAL des contrats normatifs,
#   - EN AVAL de l’architecture machine,
#   - EN AVAL de la décision centrale.
#
# Il décrit :
#   • des procédures opérateur,
#   • des interprétations UI,
#   • des règles empiriques de réglage,
#   • des bonnes pratiques de maintenance.
#
# Il ne décrit PAS :
#   ❌ la hiérarchie métier,
#   ❌ les règles décisionnelles,
#   ❌ la table de décision,
#   ❌ les triggers,
#   ❌ les mécanismes d’autorisation.
#
# ----------------------------------------------------------
# ⚠️ GARDE-FOUS FONCTIONNELS
# ----------------------------------------------------------
#
# - Les règles et procédures décrites ici :
#     • sont indicatives,
#     • peuvent évoluer sans modification contractuelle,
#     • ne doivent JAMAIS être utilisées pour modifier une règle métier.
#
# - Aucune procédure de ce document :
#     ❌ ne doit créer de logique automatique,
#     ❌ ne doit être implémentée en YAML comme règle décisionnelle,
#     ❌ ne doit court-circuiter la Décision Centrale.
#
# ----------------------------------------------------------
# 📌 VALEUR
# ----------------------------------------------------------
#
# - Nature :
#     Manuel d’exploitation et de réglage thermique.
#
# - Valeur principale :
#     Support de réglage fin, diagnostic rapide et maintien
#     des performances thermiques sur le long terme.
#
# ==========================================================


# 🛠️ EXPLOITATION & RÉGLAGES THERMIQUES

## 📐 RÉGLAGE DE LA LOI D'EAU
Le système s'auto-optimise par **Analyse Statistique** segmentée :

| Condition Climatique | Levier d'action | Capteur de référence |
| :--- | :--- | :--- |
| **Temps Doux** ($T_{ext} \ge 10^\circ\text{C}$) | **Parallèle** (Offset) | `sensor.ecart_consigne_instantane_doux` |
| **Temps Froid** ($T_{ext} \le 5^\circ\text{C}$) | **Pente** (Inclinaison) | `sensor.ecart_consigne_instantane_froid` |



### Procédure de validation des suggestions :
1. Observer le `sensor.chauffage_pente_suggeree`.
2. Si une suggestion apparaît, vérifier qu'aucune source de chaleur exceptionnelle (Poêle) n'a perturbé la mesure.
3. Activer l'ajustement automatique ou régler manuellement via les sliders de l'UI.

## 🔍 DIAGNOSTIC RAPIDE
- **La carte est ORANGE** : Un blocage métier est actif (Fenêtre, Poêle, etc.). Vérifier `sensor.chauffage_raison_calculee`.

- **La carte est BLEUE** : Le système est en attente (Hystérésis thermique). Tout est nominal, le bâtiment conserve sa chaleur.

- **La carte est ROUGE** : La commande n’a pas été correctement appliquée.
  Vérifier :
    • le statut ACK,
    • la correspondance des `request_id`,
    • l’état du boiler bridge.
