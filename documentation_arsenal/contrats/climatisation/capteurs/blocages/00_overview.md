# Arsenal — Climatisation · Couche Blocage
## Vue d'ensemble des entités

> **Périmètre** : ce document couvre les capteurs de blocage du domaine climatisation.
> Il regroupe des entités de natures différentes : vérité métier d'extinction, blocage de survol, et blocage horaire réel.
> Les couches besoin et autorisation sont documentées séparément.

---

## Table des entités

| Entité | Type | Rôle fonctionnel | Famille |
|---|---|---|---|
| `binary_sensor.clim_extinction_absence_prolongee_autorisee` | `binary_sensor` (template) | Indiquer si l'extinction complète de la climatisation est autorisée par absence prolongée confirmée | Blocage / extinction absence |
| `binary_sensor.clim_bloquee` | `binary_sensor` (template) | Exposer un voyant de survol des blocages structurels empêchant réellement la climatisation d'agir | Blocage / survol |
| `binary_sensor.clim_blocage_horaire_reel` | `binary_sensor` (template) | Exprimer la vérité métier du blocage horaire à l'instant T | Blocage / horaire |

---

## Position dans l'architecture Arsenal

```text
Observation / Contexte / Réglages opérateur
                  ↓
Blocage  ◄──────────────────────── CE DOCUMENT
                  ↓
Autorisation
                  ↓
Exécution

Observabilité ◄── clim_bloquee  (voyant transversal, hors chaîne décisionnelle)
```

`clim_blocage_horaire_reel` et `clim_extinction_absence_prolongee_autorisee` sont des **producteurs** consommés par la couche autorisation.
`clim_bloquee` est un **voyant de survol** positionné hors de la chaîne décisionnelle.

---

## Propriétés communes

| Propriété | Valeur |
|---|---|
| Type commun | `binary_sensor` template |
| Actions | Aucune |
| Temporisations internes | Aucune |
| Décision d'exécution | Aucune |

---

## Nature par entité

| Entité | Nature |
|---|---|
| `clim_extinction_absence_prolongee_autorisee` | Lecture combinatoire de validation d'un contexte d'absence prolongée |
| `clim_bloquee` | Agrégation booléenne OR de blocages structurels — voyant de survol |
| `clim_blocage_horaire_reel` | Synthèse combinatoire temporelle issue de réglages opérateur |

---

## Propriétés distinctives par entité

| Propriété | `clim_blocage_horaire_reel` | `clim_extinction_absence_prolongee_autorisee` | `clim_bloquee` |
|---|---|---|---|
| Logique interne | Calcul horaire + gestion minuit | AND 2 conditions | OR 5 conditions |
| Référence à `now()` | Oui | Non | Non |
| Timer lu | Non | Oui | Non |
| Mémoire | Aucune | Aucune | Aucune |
| Fallback explicite | Oui (`false` si inactif ou heures vides) | Non | Non |
| `icon` dynamique | Non | Non | Oui |
| Position dans la chaîne | Entrée autorisation (3 modes) | Entrée autorisation (COOL uniquement) | Observabilité |

---

## Dépendances globales recensées

| Domaine | Entités sources |
|---|---|
| Présence | `binary_sensor.presence_famille_unifiee` |
| Timer | `timer.absence_longue_clim` |
| Blocages système | `input_boolean.blocage_clim_poele`, `input_boolean.chauffage_blocage_aeration` |
| Ouvertures | `binary_sensor.fenetre_ouverte_maison`, `binary_sensor.fenetre_ouverte_etage` |
| Blocage horaire | `input_boolean.clim_blocage_horaire_actif`, `input_datetime.clim_heure_blocage_autom_on`, `input_datetime.clim_heure_blocage_autom_off` |

---

## Consommateurs documentés

| Entité | Consommée par |
|---|---|
| `clim_blocage_horaire_reel` | `autorisation_clim_cool`, `autorisation_clim_heat`, `autorisation_clim_dry` |
| `clim_extinction_absence_prolongee_autorisee` | `autorisation_clim_cool` |
| `clim_bloquee` | Non déterminable depuis le YAML fourni |
