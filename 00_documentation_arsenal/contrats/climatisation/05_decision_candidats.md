# CONTRAT ARSENAL — CLIMATISATION
## 05 — Admissibilité — Production des besoins admissibles

**Version contrat :** v1.3

---

## Principe

Cette section définit, pour chaque mode climatique, les conditions
de formation d'un **besoin admissible**.

Un besoin admissible est un besoin thermique ou hygrométrique :

- né dans un contexte d'autorisation valide,
- décisionnellement exploitable,
- indépendant des variations ultérieures d'autorisation.

La production d'un besoin admissible repose sur un **verrou de requalification**.

---

## Règle fondamentale

Un besoin admissible :

- naît uniquement sur front montant d'un besoin brut,
  lorsque l'ensemble des conditions d'autorisation du mode est satisfait,
- ne peut pas être créé rétroactivement,
- ne peut pas être réhabilité par le simple retour d'une autorisation,
- doit s'éteindre puis renaître pour redevenir admissible.

Un besoin admissible s'éteint lorsque :
- le besoin brut correspondant repasse à `off`,
- ou qu'une condition d'autorisation du mode devient invalide.

---

## COOL

Un besoin admissible COOL (`binary_sensor.besoin_clim_cool_admissible`)
est produit si :

- un besoin brut COOL apparaît (front montant),
- et que les conditions suivantes sont simultanément satisfaites :

  - température extérieure compatible,
  - fenêtres fermées,
  - aération non favorable,
  - aucun blocage horaire actif,
  - absence prolongée non inhibitrice.

---

## DRY

Un besoin admissible DRY (`binary_sensor.besoin_clim_dry_admissible`)
est produit si :

- un besoin brut DRY apparaît (front montant),
- et que les conditions suivantes sont simultanément satisfaites :

  - présence réelle détectée ou babysitting actif,
  - fenêtres fermées,
  - aération non favorable,
  - aucun blocage horaire actif.

---

## HEAT — Chauffage d'appoint

Un besoin admissible HEAT (`binary_sensor.besoin_clim_heat_admissible`)
est produit si :

- un besoin brut HEAT apparaît (front montant),
- et que les conditions suivantes sont simultanément satisfaites :

  - présence réelle détectée,
  - chauffage par climatisation autorisé,
  - température extérieure suffisante,
  - poêle inactif,
  - fenêtres fermées,
  - aucun blocage horaire actif.

**Note :** HEAT est strictement un appoint. Il ne constitue jamais une source de chauffage principale.

---

## Invariants

- L'admissibilité ne réalise aucune sélection de mode.
- L'admissibilité ne produit aucune priorité inter-mode.
- L'admissibilité ne déclenche aucune action.
- Chaque mode est traité indépendamment.

L'admissibilité constitue exclusivement une **requalification décisionnelle**.
