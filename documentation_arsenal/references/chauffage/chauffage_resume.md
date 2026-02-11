# ==========================================================
# 🧠 ARSENAL — DOCUMENT DE RÉFÉRENCE
#     Chauffage — Synthèse doctrinale (V3 PRO)
# ==========================================================
#
# 📌 STATUT :
#   DOCUMENT DE RÉFÉRENCE — NON NORMATIF
#
# 🔒 AUTORITÉ :
#   Ce document ne constitue PAS un contrat opposable.
#   Il ne possède AUCUNE autorité métier ni décisionnelle.
#
#   En cas de divergence, seules font foi :
#     - /documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#     - /documentation_arsenal/contrats/chauffage/30_decision_centrale.md
#     - /documentation_arsenal/contrats/chauffage/60_table_decision_canonique.md
#
# 🎯 RÔLE :
#   Fournir une vue synthétique et pédagogique de la doctrine Chauffage,
#   destinée à :
#     - compréhension globale du système,
#     - communication interne,
#     - rappel des principes structurants.
#
#   Ce document privilégie la lisibilité à l’exhaustivité.
#
# ----------------------------------------------------------
# ⚠️ LIMITES & GARDE-FOUS
# ----------------------------------------------------------
#
# - Ce document simplifie volontairement plusieurs mécanismes :
#     • hiérarchie décisionnelle,
#     • distinction cause / effet,
#     • séparation décision / application,
#     • mécanismes de protection et d’hystérésis.
#
# - Il ne décrit PAS fidèlement :
#     • la table canonique réelle de décision,
#     • la sémantique officielle des statuts thermiques,
#     • le rôle exact des verrous mécaniques (standby, protection),
#     • la hiérarchie normative complète Arsenal.
#
# - Il contient des approximations historiques issues
#   d’une version antérieure du modèle mental Chauffage.
#
#   En particulier :
#     • le standby y est présenté comme un niveau décisionnel,
#       alors qu’il est un mécanisme d’application.
#     • la protection thermique y apparaît comme un niveau hiérarchique,
#       alors qu’elle ne produit aucune intention.
#     • le confort d’opportunité y est formulé comme décision,
#       alors qu’il constitue uniquement une autorisation conditionnelle.
#
# ----------------------------------------------------------
# 🧠 RÈGLE DE GOUVERNANCE DOCUMENTAIRE
# ----------------------------------------------------------
#
# - Ce document :
#     ❌ ne doit JAMAIS être cité comme référence normative,
#     ❌ ne doit JAMAIS être opposé au YAML,
#     ❌ ne doit JAMAIS servir de base à une implémentation,
#     ❌ ne doit JAMAIS être utilisé pour arbitrer une règle métier.
#
# - Toute conception, correction ou évolution Chauffage
#   doit se fonder exclusivement sur les contrats normatifs.
#
# ----------------------------------------------------------
# 📌 HISTORIQUE
# ----------------------------------------------------------
#
# - Origine :
#     Synthèse doctrinale issue d’une version intermédiaire
#     du modèle Chauffage Arsenal (antérieure à V3 PRO stabilisé).
#
# - Rôle conservé :
#     Mémoire conceptuelle et support de communication.
#
# - Validité :
#     Pédagogique uniquement.
#
# ==========================================================

# 📑 CONTRAT MÉTIER — CHAUFFAGE (V3 PRO)

## 🎯 OBJET
Garantir le confort thermique en présence et la sobriété en absence, tout en protégeant l'infrastructure matérielle contre les instabilités logicielles (Cloud/API).

## ⚖️ HIÉRARCHIE DES CAUSES (STRICTE)
La décision finale est dictée par une hiérarchie de priorités descendantes. Une cause de niveau supérieur écrase systématiquement les ordres des niveaux inférieurs.

1. **NIVEAU 1 — BLOCAGES ABSOLUS** : Fenêtre ouverte, Poêle actif, Mode Vacances, Aération.
   - *Action* : Mode **ECO** forcé.
2. **NIVEAU 2 — AUTORISATION SYSTÈME** : Hystérésis de protection post-blocage.
   - *Action* : **ATTENTE** (Maintien de l'état précédent).
3. **NIVEAU 3 — STANDBY (HYSTÉRÉSIS THERMIQUE)** : Seuil de température non atteint.
   - *Action* : **ATTENTE** (Repos nominal).
4. **NIVEAU 4 — CONFORT D’OPPORTUNITÉ** : Présence détectée ou Forçage manuel.
   - *Action* : Mode **CONFORT** requis.
5. **NIVEAU 5 — PROTECTION THERMIQUE** : Absence prolongée avec dérive excessive.
   - *Action* : Mode **CONFORT** ponctuel (Inhibition).



## 🚫 RÈGLES D'OR
- **Indépendance de la Présence** : La présence est une *autorisation* de chauffe, jamais une *autorité* thermique. C'est l'écart de température qui déclenche l'action.
- **Souveraineté Locale** : En cas de déconnexion Cloud, le système utilise sa dernière mémoire d'intention pour maintenir le service.
- **Transparence** : Chaque état doit être justifié par une `raison_calculee` explicite.
