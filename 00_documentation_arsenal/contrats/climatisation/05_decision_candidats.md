# CONTRAT ARSENAL — CLIMATISATION
## 05 — Admissibilité — Production des besoins admissibles

**Version contrat :** v1.4

---

## Principe

Cette section définit, pour chaque mode climatique, les conditions
de formation d'un **besoin admissible**.

Un besoin admissible est un besoin thermique ou hygrométrique :

- né dans un contexte d'autorisation valide,
- décisionnellement exploitable,
- indépendant des variations ultérieures d'autorisation.

La production d'un besoin admissible repose sur un **verrou de
requalification à deux portes causales**.

---

## Nature des signaux

Le besoin brut (`binary_sensor.besoin_clim_*`) est un signal **continu**,
entretenu par l'état thermodynamique ou hygrométrique du logement.
Tant qu'aucune action correctrice ne s'applique, un besoin légitime
peut rester actif indéfiniment.

L'autorisation (composée des conditions énumérées par mode ci-dessous)
est un signal **contextuel**, potentiellement oscillant.

L'admissibilité est un **état qualifié**, inscrit par événement et
jamais dérivé par template.

---

## Règle fondamentale

Un besoin admissible naît exclusivement d'un front causal qualifié,
selon l'une des deux portes suivantes.

### Porte 1 — Front montant du besoin brut

L'admissibilité naît si :

- un front montant du besoin brut est observé,
- et l'ensemble des conditions d'autorisation du mode est satisfait
  à cet instant.

Aucune garde temporelle. Un besoin qui naît sous autorisation est
immédiatement admissible.

### Porte 2 — Front montant de l'autorisation (requalification)

L'admissibilité naît si :

- un front montant d'une des conditions d'autorisation du mode est
  observé,
- et le besoin brut correspondant est déjà actif,
- et l'ensemble des conditions d'autorisation est resté stable
  pendant 5 minutes.

Ce délai constitue une garde anti-oscillation. Il pourra être réduit
ou supprimé ultérieurement si les autorisations consommées intègrent
déjà une consolidation équivalente en amont.

### Extinction (asymétrie assumée)

Un besoin admissible s'éteint **immédiatement** lorsque :

- le besoin brut correspondant repasse à `off`,
- ou qu'une condition d'autorisation du mode devient invalide.

L'asymétrie (extinction instantanée, activation gardée) est
délibérée : *couper vite, rallumer prudemment*. La sécurité prime
sur le confort.

### Réconciliation au démarrage

Au démarrage, deux cas sont traités explicitement :

- **Signaux KO** (l'un des deux est `off`, `unknown`, ou `unavailable`
  après attente bornée) → l'admissibilité est forcée à `off`.
- **Signaux stables à `on`** (besoin et autorisation tous deux actifs
  après attente bornée) → l'admissibilité est activée après une
  garde de 5 minutes, sous réserve que les deux signaux restent `on`
  pendant toute cette période.

Cette logique au boot reproduit explicitement le comportement de la
porte 2. Le système ne dépend d'aucun effet secondaire implicite du
moteur d'automation (`last_changed`, `restore_state`, ordre de
chargement des intégrations).

La réconciliation au démarrage est portée par des automatisations
dédiées, distinctes des automatisations runtime d'admissibilité,
afin d'éviter tout blocage concurrent des fronts causaux runtime.

### Garanties

- Aucune réanimation implicite : toute activation est tracée par un
  front causal explicite.
- Aucune oscillation : la porte 2 absorbe les bascules courtes
  d'autorisation.
- Aucun deadlock thermique : un besoin légitime persistant au-delà
  d'une fenêtre d'interdiction est requalifié dès le retour stable
  de l'autorisation.

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
