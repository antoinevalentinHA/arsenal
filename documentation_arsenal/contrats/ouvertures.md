# ==========================================================
# 🧠 ARSENAL — CONTRAT OUVERTURES
# ----------------------------------------------------------
# Domaine :
#   Ouvertures (portes / fenêtres)
#
# Portée :
#   Détection, normalisation, agrégation, temporisation,
#   qualification de fait métier, restitution UI
#
# Nature :
#   Contrat NORMATIF — aucun pilotage, aucune décision
#
# Statut :
#   Clos et figé
# ==========================================================


## 1. 🎯 OBJET DU CONTRAT

Ce contrat définit **exhaustivement** le cadre Arsenal relatif
aux **ouvertures de la maison** (portes et fenêtres).

Il couvre :

- la détection physique,
- la normalisation structurelle,
- l’agrégation logique,
- les temporisations de grâce,
- la qualification explicite d’un fait métier,
- la restitution UI,
- les helpers nécessaires.

Il établit une séparation stricte entre :

- événement physique (N0),
- état normalisé (N1),
- état agrégé (N2),
- canon d’orchestration,
- fait métier qualifié,
- décision métier (**hors périmètre**),
- restitution UI.

Aucune interprétation métier n’est autorisée dans ce contrat.


---

# 🧱 2. ARCHITECTURE EN COUCHES

---

## 2.1 N0 — Détection physique (source brute)

Les capteurs matériels `binary_sensor.capteur_*` constituent :

> la source unique de vérité physique.

Caractéristiques :

- retour brut du matériel,
- potentiellement `unknown` / `unavailable`,
- sans logique,
- sans temporisation,
- sans qualification.

### Usage actuel

À ce jour, certaines entités N0 peuvent encore être
référencées directement dans d’autres domaines
(historique Arsenal).

### Cible architecturale

La cible contractuelle est :

> Toute consommation d’un capteur physique doit passer par N1.

Cette cible ne constitue pas une obligation rétroactive,
mais un principe directeur pour toute évolution future.


---

## 2.2 N1 — NORMALISATION (contact stable)

Les entités `binary_sensor.contact_*` constituent la couche N1.

Rôle :

- abstraction structurelle,
- encapsulation de l’indisponibilité,
- production d’un état **toujours évaluable**,
- suppression de toute dépendance directe aux capteurs bruts.

Invariants N1 :

- Dépend exclusivement de N0.
- État toujours `on` ou `off`.
- Si la source est indisponible → état forcé `off`.
- L’indisponibilité est exposée uniquement en attribut.
- Aucun délai.
- Aucune qualification.
- Aucune décision.

Principe :

> N1 stabilise la structure, pas le temps.


---

## 2.3 N2 — AGRÉGATION (OR logique)

Les entités `binary_sensor.contact_<zone>` constituent la couche N2.

Rôle :

- agrégation OR de N1,
- exposition par pièce, étage, maison,
- calcul instantané,
- sans trigger-based,
- sans temporisation,
- sans interprétation.

Invariants N2 :

- Dépend exclusivement de N1.
- État :
  - `on` si au moins un membre est `on`
  - sinon `off`
- Aucun délai.
- Aucune qualification.
- Indisponibilité exposée en attribut uniquement.

Principe :

> N2 agrège, n’interprète pas.


---

## 2.4 CANONS OUVERTURES (stabilisation locale)

Les canons (ex. `fenetres_maison_fermees_stable`) fournissent
des signaux robustes pour l’orchestration.

Rôle :

- stabilisation temporelle localisée,
- suppression des "OFF furtifs",
- prévention des guards dispersés.

Invariants :

- Dépend exclusivement de N2.
- Délai localisé (delay_on / delay_off).
- Aucune qualification métier.
- Aucun effet de bord.

Principe fondamental :

> La stabilisation appartient aux canons, pas aux pipelines.


---

# ⏱️ 3. TEMPORISATION — FENÊTRES DE GRÂCE

## 3.1 Timers

Les timers définissent exclusivement le temps.

Caractéristiques :

- rôle : cadre temporel,
- états : `active` / `idle`,
- restaurables,
- aucune action automatique à expiration.

Invariant :

> Le timer définit le temps.  
> L’interprétation est externe.


## 3.2 Scripts de temporisation

Les scripts :

- démarrent / redémarrent les timers,
- lisent les durées via helpers,
- n’embarquent aucune logique métier.

Ils sont des middlewares techniques.

## 3.3 Automatisations de temporisation

Les automatisations :

- déclenchent les scripts,
- annulent les timers à fermeture complète,
- ne prennent aucune décision métier.

Toute temporisation :

- est déclenchée explicitement,
- est levée explicitement,
- est immédiatement réversible.


---

# 🧠 4. QUALIFICATION DE FAIT MÉTIER

## 4.1 Principe fondamental

Un fait métier :

- n’est jamais implicite,
- n’est jamais déduit,
- n’est jamais supposé.

Il est posé explicitement.

## 4.2 Aération confirmée

`aeration_confirmee` :

- déclenché après timer de grâce,
- conditionné à stabilité,
- sans déclencher aucune action métier.

Invariant :

> Un fait métier est posé explicitement,  
> sans effet de bord.


---

# 🧩 5. HELPERS

## 5.1 Helpers temporels

- `input_number`
- définissent des durées
- lus dynamiquement
- ne déclenchent rien

## 5.2 Helpers de qualification

- `input_boolean`
- matérialisent un fait métier
- ne décident rien

Invariant :

> Les helpers sont des paramètres ou des marqueurs,  
> jamais des décideurs.


---

# 🖥️ 6. RESTITUTION UI

Principe :

- lecture seule,
- sans logique métier,
- sans correction,
- sans interprétation.

Dashboards couverts :

- carte synthétique Arsenal,
- dashboard Ouvertures,
- dashboard Réglages,
- dashboard Diagnostics.

La navigation est informative uniquement.


---

# 🔒 7. INVARIANTS CONTRACTUELS

- Aucune décision métier n’est prise ici.
- Aucune action matérielle.
- Les délais concernent uniquement l’ouverture.
- La fermeture est instantanée.
- N0 n’est jamais utilisé ailleurs.
- N1 stabilise la structure.
- N2 agrège sans interpréter.
- Les canons stabilisent localement.
- Les timers n’interprètent rien.
- Les scripts n’évaluent rien.
- L’UI ne décide rien.
- Tout fait métier est posé explicitement.


---

# 🚫 8. HORS PÉRIMÈTRE

Sont exclus :

- décision chauffage,
- décision clim,
- décision alarme,
- optimisation comportementale,
- inférence contextuelle,
- pilotage matériel.


---

# 🛑 9. CLAUSE DE STABILITÉ

Toute évolution :

- nécessite demande explicite,
- respecte les couches N0 / N1 / N2 / CANON,
- conserve les invariants.

Aucune extension implicite n’est autorisée.


# ==========================================================
# ✅ CONTRAT OUVERTURES — CLOS ET FIGÉ
# ==========================================================