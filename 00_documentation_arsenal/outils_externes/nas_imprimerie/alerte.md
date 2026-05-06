# 📜 Arsenal — Contrat Normatif

**Objet** : Décision d'alerte NAS Imprimerie
**Version** : 1.0
**Date** : 24 avril 2026
**Statut** : normatif
**Portée** : couche de décision déclarative déterminant si l'état synthétique du NAS Imprimerie mérite une notification

---

## 1. Position dans l'architecture Arsenal

Cette couche vient **après** :

- la synthèse de santé NAS Imprimerie :
  - `sensor.nas_imprimerie_sante_synthese`

Elle vient **avant** :

- la couche d'exécution de notification
- la couche UI / dashboard

Elle ne notifie pas.
Elle produit uniquement un état booléen exploitable par les couches aval.

---

## 2. Responsabilités exactes

### 2.1 Ce que la couche FAIT

- Lit l'état global de synthèse du NAS Imprimerie.
- Détermine si une alerte doit être considérée comme active.
- Applique un délai de confirmation temporelle sur l'entrée en alerte.
- Expose une entité binaire unique, auditable et consommable.

### 2.2 Ce que la couche NE FAIT PAS

- Aucune acquisition.
- Aucune lecture des axes détaillés.
- Aucune lecture de `raison`, `priorite_active` ou `defauts_actifs`.
- Aucune notification.
- Aucune écriture.
- Aucun appel de service.
- Aucun acquittement.
- Aucune re-notification.
- Aucune logique UI.
- Aucun filtrage horaire.

---

## 3. Frontières strictes

| Couche | Responsabilité | Exemple |
|---|---|---|
| Synthèse | classifier l'état global | `sensor.nas_imprimerie_sante_synthese = critical` |
| **Décision d'alerte** | décider si une alerte est active | `binary_sensor.nas_imprimerie_alerte_active = on` |
| Notification | envoyer le message | automation → `notify.mobile_app_pixel_7a` |
| UI | afficher | Lovelace |

La décision d'alerte lit la synthèse.
La notification lit la décision d'alerte.

---

## 4. Entrée autorisée

La couche lit exclusivement :

- `sensor.nas_imprimerie_sante_synthese`

Elle lit uniquement son **state**.

Lectures interdites :

- `axe_connectivite`
- `axe_vpn`
- `axe_ups`
- `axe_stockage`
- `axe_uptime`
- `raison`
- `priorite_active`
- `defauts_actifs`
- toute autre entité NAS Imprimerie

---

## 5. Sortie à créer

### `binary_sensor.nas_imprimerie_alerte_active`

- `on` : une alerte est active et confirmée.
- `off` : aucune alerte active confirmée.

Le capteur utilise le moteur `template:` moderne Home Assistant.

---

## 6. Règles de décision

### 6.1 États déclencheurs

La condition logique brute est :

```jinja
{{ states('sensor.nas_imprimerie_sante_synthese') in ['critical', 'offline'] }}
```

| État synthèse | Alerte brute |
| ------------- | ------------ |
| `critical`    | vraie        |
| `offline`     | vraie        |
| `ok`          | fausse       |
| `degraded`    | fausse       |
| `unknown`     | fausse       |
| `unavailable` | fausse       |
| autre valeur  | fausse       |

### 6.2 Debounce temporel

Le passage `off → on` est confirmé uniquement si la condition brute reste vraie continûment pendant :

```text
00:02:00
```

Le passage `on → off` est immédiat dès que la condition brute redevient fausse.

### 6.3 Comportement au redémarrage HA

Après redémarrage de Home Assistant, le délai `delay_on` est réinitialisé.

Si la synthèse est déjà `critical` ou `offline` au redémarrage, l'alerte active sera confirmée après 2 minutes de stabilité.

Ce comportement est accepté en v1.0.

---

## 7. Invariants normatifs

### I-ALERT-01 — Source unique

La décision d'alerte n'accède à aucune entité autre que `sensor.nas_imprimerie_sante_synthese`.

### I-ALERT-02 — Lecture du state uniquement

La décision ne lit aucun attribut de la synthèse.

### I-ALERT-03 — Enum d'entrée fermée

Seuls les états `critical` et `offline` satisfont la condition brute d'alerte.

Tous les autres états produisent une condition brute fausse.

Le déclenchement effectif de l'alerte reste soumis au debounce défini en I-ALERT-05.

### I-ALERT-04 — Décision pure

La couche ne déclenche aucune action, notification, écriture ou appel de service.

### I-ALERT-05 — Debounce asymétrique

- `off → on` : délai de confirmation de 2 minutes.
- `on → off` : immédiat.

### I-ALERT-06 — Pas de segmentation causale

La décision d'alerte ne distingue pas la cause de l'alerte.
La cause reste portée par la synthèse.

### I-ALERT-07 — Pas de politique de rappel

La couche ne porte aucune logique de re-notification, d'acquittement ou d'escalade.

---

## 8. Hors scope v1.0

- Notification mobile.
- Message de notification.
- Acquittement utilisateur.
- Re-notification périodique.
- Escalade.
- Silence horaire.
- Traitement de `degraded`.
- Traitement de `unknown` durable.
- Segmentation par cause (`vpn_down`, `stockage_critique`, etc.).
- Paramétrage du message de rétablissement.

---

## 9. Consommateur prévu

Le consommateur principal prévu est une automation de notification.

Elle devra écouter :

- passage `off → on` : notification d'alerte
- passage `on → off` : notification de rétablissement

Canal indicatif prévu, non contractuel dans cette couche :

- `notify.mobile_app_pixel_7a`

Cette automation relève d'un contrat ou fichier séparé.

---

## 10. Versioning

| Version | Date | Modification |
|---|---|---|
| 1.0 | 2026-04-24 | Création. Décision d'alerte basée sur `sensor.nas_imprimerie_sante_synthese`, déclenchement `critical/offline`, debounce `delay_on` 2 minutes, retour immédiat. |
