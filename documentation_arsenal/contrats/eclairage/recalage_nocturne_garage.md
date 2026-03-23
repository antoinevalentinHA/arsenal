# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
# Recalage nocturne multi-fenetres — Eclairage Garage
# ==========================================================

#
# 📌 Statut :
# CONTRAT MÉTIER — Recalage différé de cohérence logique
#
# 📌 Domaine :
# Eclairage — Systèmes non observables en nominal
#
# 📌 Dépendance :
# Subordonné au Contrat Métier Principal — Eclairage Garage
#
# ==========================================================

## 🎯 Objet

Ce contrat définit le mécanisme de **recalage nocturne multi-fenetres**
du sous-système **Eclairage Garage**.

Il a pour finalité de :

- corriger les divergences entre état logique et état réel estimé,
- améliorer la cohérence du système par recalages passifs répétés,
- sans altérer le fonctionnement nominal,
- sans introduire de dépendance temps réel au matériel.

---

## 🔒 Principe fondamental

Le système reste :

> **non observable en nominal**

Mais devient :

> **partiellement observable en conditions nocturnes contrôlées**

Le recalage nocturne constitue une **capacité de réalignement différé**,
sans remise en cause du modèle nominal.

---

## 🔒 Invariant R1 — Séparation stricte des couches

Le recalage nocturne constitue une couche indépendante du fonctionnement nominal.

Interdictions :

- aucune modification du rôle de `script.garage_toggle`
- aucune injection de logique d’observation dans le script autoritaire
- aucune dépendance des automatisations nominales au recalage nocturne

---

## 🔒 Invariant R2 — Observation passive uniquement

Le recalage repose exclusivement sur l’observation de :

- `sensor.luminosite_garage_illuminance`

Interdictions :

- aucune action physique de test
- aucun appel à `button.garage_1`
- aucun appel à `button.garage_2`
- aucune modification volontaire de l’état réel de la lumière
- aucun protocole actif de validation

---

## 🔒 Invariant R3 — Fenêtres nocturnes multiples

Le recalage est exécuté dans plusieurs fenêtres temporelles fixes :

- `02:00`
- `03:00`
- `04:00`

Chaque fenêtre :

- est indépendante des autres,
- applique exactement la même logique,
- ne dépend d’aucun historique inter-fenêtres.

Objectifs :

- augmenter la robustesse du recalage,
- tolérer une mesure ponctuellement non exploitable,
- améliorer la probabilité de réalignement nocturne.

---

## 🔒 Invariant R3bis — Condition de quiescence locale

Le recalage n’est autorisé que si l’environnement du garage est stable.

Condition minimale :

- `binary_sensor.mouvement_garage = off`

Condition recommandée (implémentation) :

- absence de mouvement pendant une durée minimale définie
  (ex : 10 à 15 minutes)

### Catégorie contractuelle

| Catégorie    | Rôle autorisé                        |
|--------------|--------------------------------------|
| Autorisation | autoriser / bloquer le recalage      |

### Interdictions

- ne jamais déduire l’état de la lumière depuis ce capteur
- ne jamais corriger `input_boolean.garage_light_state` depuis ce capteur
- ne jamais remplacer l’observation lumineuse par ce capteur

---

## 🔒 Invariant R4 — Inférence par seuils fixes

L’état réel estimé est déduit de `sensor.luminosite_garage_illuminance`
à partir de seuils fixes opposables.

Règles :

- `lux <= seuil_bas` → état réel estimé = `off`
- `lux >= seuil_haut` → état réel estimé = `on`
- `seuil_bas < lux < seuil_haut` → état estimé = indéterminé

---

## 🔒 Invariant R5 — Zone d’incertitude obligatoire

Une zone intermédiaire d’incertitude est définie contractuellement.

Dans cette zone :

> **aucune décision ne doit être prise**

Interdictions :

- correction en zone grise
- interprétation probabiliste
- heuristique adaptative
- extrapolation depuis une mesure ambiguë

---

## 🔒 Invariant R6 — Correction conditionnelle minimale

La correction de `input_boolean.garage_light_state` n’est autorisée
que si les deux conditions suivantes sont réunies :

1. l’état estimé est déterminé (`on` ou `off`)
2. l’état estimé diffère de l’état logique courant

Sinon :

> **aucune action**

---

## 🔒 Invariant R7 — Correction logique uniquement

Le recalage agit exclusivement sur :

- `input_boolean.garage_light_state`

Interdictions :

- aucune action physique
- aucune pression sur un actionneur
- aucune tentative de synchronisation matérielle
- aucune relecture post-correction obligatoire

Le recalage corrige la **référence logique**, jamais le réel.

---

## 🔒 Invariant R8 — Non-intrusion absolue

Le recalage nocturne ne doit jamais :

- allumer volontairement la lumière
- éteindre volontairement la lumière
- produire un effet visible pour l’utilisateur
- perturber l’usage physique du sous-système

---

## 🔒 Invariant R9 — Indépendance des passages

Chaque passage nocturne doit être :

- autonome,
- stateless,
- auto-suffisant.

Interdictions :

- aucune mémoire entre `02:00`, `03:00`, `04:00`
- aucune logique de vote
- aucune logique cumulative
- aucune dépendance à un résultat antérieur

---

## 🔒 Invariant R10 — Tolérance au non-résultat

Le recalage peut légitimement :

- ne rien corriger,
- rencontrer une mesure indéterminée,
- être bloqué par la condition de quiescence,
- échouer silencieusement.

Garanties :

- aucune dégradation du fonctionnement nominal
- aucune tentative de forçage
- aucune escalade automatique

---

## 🧠 Paramètres de référence

Valeurs validées :

- `seuil_bas = 5`
- `seuil_haut = 20`

Observations :

- nuit + lumière éteinte → ~1 lux
- nuit + lumière allumée → ~28 lux

Ces seuils sont volontairement conservateurs
pour préserver une zone d’incertitude protectrice.

---

## 🧩 Résultat attendu

Le sous-système devient :

- cohérent en nominal,
- auto-correctif en différé,
- non intrusif,
- robuste face aux dérives logique/réel,
- sécurisé contre les perturbations humaines nocturnes.

---

## 🔒 Garanties contractuelles

Ce contrat garantit :

- absence totale d’intrusion matérielle,
- maintien intégral du modèle nominal,
- correction uniquement sous certitude,
- robustesse renforcée par répétition temporelle,
- recalage exécuté uniquement en conditions stables,
- respect strict des invariants Arsenal.

# ==========================================================
# FIN CONTRAT — RECALAGE NOCTURNE MULTI-FENETRES ECLAIRAGE GARAGE
# ==========================================================