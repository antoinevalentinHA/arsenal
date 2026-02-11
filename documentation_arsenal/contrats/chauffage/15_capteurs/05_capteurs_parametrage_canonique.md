# ==========================================================
# 🧠 ARSENAL — CONTRAT CAPTEURS DE PARAMÉTRAGE CANONIQUE
#     Référentiel thermique durable — Consignes de référence
# ----------------------------------------------------------
# Domaine : Chauffage / Paramétrage thermique
# Couche  : Référentiel canonique du moteur thermique
# Statut  : STRUCTURANT — FRONTIÈRE DE PARAMÉTRAGE CRITIQUE
#
# 🎯 Rôle global :
#   Définir la COUCHE DE PARAMÉTRAGE THERMIQUE CANONIQUE du moteur Chauffage Arsenal.
#
#   Cette couche fournit les PARAMÈTRES DE TEMPÉRATURE DE RÉFÉRENCE DURABLES :
#     - consigne de confort canonique,
#     - consigne réduite de protection thermique,
#
#   utilisés comme FONDATIONS de :
#     - la décision centrale,
#     - les seuils ON / OFF,
#     - le standby / hystérésis,
#     - la protection bâtiment en absence,
#     - les modèles inertiels,
#     - l’auto-ajustement futur de courbe.
#
# 🧱 Frontière d’autorité protégée :
#   RÉFÉRENTIEL THERMIQUE CANONIQUE DU MOTEUR
#
#   Cette couche :
#     - ne décide jamais,
#     - n’autorise jamais,
#     - ne bloque jamais,
#     - ne pilote jamais,
#     - ne calibre jamais elle-même,
#     - ne modifie aucun paramètre matériel.
#
#   Elle FOURNIT exclusivement DES VALEURS DE RÉFÉRENCE STABLES.
#
# ⛔ Interdictions cardinales (couche entière) :
#   - Aucune décision de mode thermique
#   - Aucune autorisation d’exécution
#   - Aucun déclenchement d’action
#   - Aucun pilotage matériel
#   - Aucune écriture de consigne
#   - Aucune logique métier thermique
#   - Aucune dépendance Cloud finale
#
# 🔒 Garanties exigées :
#   - Lecture exclusive de paramètres matériels locaux gouvernés
#   - Validation stricte numérique et bornée
#   - Fallback mémoire en cas d’indisponibilité
#   - Reload-safe / restart-safe / runtime-safe
#   - Valeurs toujours exploitables par le moteur décisionnel
#   - Stabilité sémantique garantie
#
# 🔗 Autorités amont légitimes :
#   - Paramètres matériels locaux gouvernés (ViCare local)
#   - Indicateur de stabilité système
#
# 🔗 Autorités aval autorisées :
#   - Décision centrale Chauffage
#   - Table de décision canonique
#   - Standby / hystérésis
#   - Protection thermique absence
#   - Diagnostics paramétriques structurants
#   - Auto-ajustement de courbe (lecture uniquement)
#
# ⚠️ Risques systémiques surveillés :
#   - Perte de cohérence si paramètre modifié hors Arsenal
#   - Couplage implicite avec logique API
#   - Valeur hors bornes affaiblissant la protection bâtiment
#   - Dérive d’usage comme décision primaire
#
# 🔒 Statut d’autorité :
#   RÉFÉRENTIEL DE PARAMÉTRAGE THERMIQUE OFFICIEL
#   Toute altération impacte directement l’ensemble des seuils et décisions thermiques.
#
# ==========================================================

### 🔒 sensor.chauffage_consigne_confort_local

- Domaine : Auto-ajustement / Calibration / Paramétrage durable  
- Autorité : STRUCTURANT  

🎯 Rôle :
Fournir une lecture locale fiable, stable et souveraine
de la consigne de confort réelle configurée dans ViCare,
servant de référence canonique de température de confort
pour la décision centrale, les offsets et les mécanismes de calibration.

🧭 Périmètre d’influence autorisé :
- Décision centrale (base de seuils comfort / neutre / reduced)
- Calcul des seuils ON / OFF
- Standby / hystérésis thermique
- Auto-ajustement de courbe (référence de confort)
- Diagnostics structurants de cohérence paramétrique

⛔ Interdictions absolues :
- Ne définit jamais un mode thermique
- Ne décide jamais d’une autorisation
- Ne déclenche jamais une action
- Ne pilote jamais directement un service
- Ne dépend jamais du cloud pour sa valeur finale
- Ne modifie jamais une consigne matérielle

🔒 Garanties exigées :
- Lecture exclusive d’un paramètre matériel local gouverné
- Validation stricte numérique et bornée (> 0)
- Fallback mémoire en cas d’indisponibilité
- Reload-safe / restart-safe
- Tolérance aux ruptures API
- Valeur toujours exploitable par le moteur décisionnel

🔗 Dépendances :
Source amont :
- number.vscotho1_200_11_temperature_de_confort

Déclencheurs de cohérence :
- input_boolean.systeme_stable

⚠️ Risques :
- Dérive d’usage comme source décisionnelle primaire (interdit)
- Couplage implicite avec logique API
- Perte de cohérence si consigne modifiée hors Arsenal
- Utilisation sans validation de bornes métier

❗ Statut critique :
PARAMÈTRE CANONIQUE DE CONFORT  
Toute altération impacte directement tous les seuils thermiques
et les dynamiques de décision.

✅ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Auto-ajustement / Calibration / Paramétrage durable

# ----------------------------------------------------------

### 🔒 sensor.chauffage_consigne_reduced_local

- Domaine : Auto-ajustement / Calibration / Paramétrage durable  
- Autorité : STRUCTURANT  

🎯 Rôle :
Fournir une lecture locale fiable, stable et souveraine
de la consigne réduite réelle configurée dans ViCare,
servant de référence canonique de température minimale de protection
pour les modes absence, reduced, standby et les garde-fous thermiques.

🧭 Périmètre d’influence autorisé :
- Décision centrale (seuils de maintien thermique en absence)
- Calcul des seuils reduced / neutre
- Protection thermique basse
- Standby / hystérésis en absence
- Auto-ajustement de courbe (borne basse de calibration)
- Diagnostics structurants de cohérence paramétrique

⛔ Interdictions absolues :
- Ne définit jamais un mode thermique
- Ne décide jamais d’une autorisation
- Ne déclenche jamais une action
- Ne pilote jamais directement un service
- Ne dépend jamais du cloud pour sa valeur finale
- Ne modifie jamais une consigne matérielle

🔒 Garanties exigées :
- Lecture exclusive d’un paramètre matériel local gouverné
- Validation stricte numérique et bornée (> 0)
- Fallback mémoire en cas d’indisponibilité
- Reload-safe / restart-safe
- Tolérance aux ruptures API
- Valeur toujours exploitable par le moteur décisionnel

🔗 Dépendances :
Source amont :
- number.vscotho1_200_11_reduced_temperature

Déclencheurs de cohérence :
- input_boolean.systeme_stable

⚠️ Risques :
- Dérive d’usage comme source décisionnelle primaire (interdit)
- Couplage implicite avec logique API
- Perte de cohérence si consigne modifiée hors Arsenal
- Utilisation sans validation de bornes métier
- Protection thermique affaiblie en cas de valeur incorrecte

❗ Statut critique :
PARAMÈTRE CANONIQUE DE PROTECTION THERMIQUE  
Toute altération impacte directement la stabilité en absence,
les seuils de sécurité et la sobriété globale du système.

✅ Décision :
INCLUS DANS `15_capteurs_thermiques.md`  
Section : Auto-ajustement / Calibration / Paramétrage durable