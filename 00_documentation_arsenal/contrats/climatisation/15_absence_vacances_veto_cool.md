# CONTRAT ARSENAL — CLIMATISATION
## 15 — Politique d'absence COOL : veto Vacances immédiat, absence longue réglable, veto composite

**Version contrat :** v1.0
**Statut :** Normatif — **opposable** (Chantier C20, Lot 1).
**Domaine :** Climatisation — mode COOL, couche autorisation/blocage.
**Subordonné à :** [`06_doctrine_blocages.md`](06_doctrine_blocages.md) · [`04_entrees_metier.md`](04_entrees_metier.md)
**Consommé par :** [`capteurs/autorisations/10_autorisations.md`](capteurs/autorisations/10_autorisations.md) (`binary_sensor.autorisation_clim_cool`)
**Origine :** note de décision D1–D15 — [`audits/02_conception/climatisation/cadrage_decision_politique_absence_vacances_cool.md`](../../audits/02_conception/climatisation/cadrage_decision_politique_absence_vacances_cool.md) · chantier [`C20`](../../audits/04_chantiers/climatisation/chantier_politique_absence_cool.md)

> **Périmètre.** Ce contrat régit **deux causes d'interdiction du COOL** (absence longue non qualifiée ; Vacances actives) et **leur agrégat** (veto composite). Il **ne crée aucune préparation du retour** : celle-ci relève du Chantier C21 et est **déclarée en §9 comme point d'extension**, non implémentée ici.

---

## 1. Objet

Fixer, sur la **seule autorité d'autorisation** `binary_sensor.autorisation_clim_cool`, la politique d'interdiction du COOL en absence, **sans décision centrale** :

1. **Veto immédiat des Vacances** (D1) : `binary_sensor.vacances_actives == on` interdit le COOL sur-le-champ, indépendamment de toute durée.
2. **Absence longue non qualifiée** (D2) : interdiction après une **durée réglable** d'absence, à **échéance de retour inconnue**.
3. **Veto composite** (D6/D7) : une vérité calculée unique agrège les deux causes ; l'autorisation la consomme sans dupliquer la formule.

---

## 2. Sources de vérité et entités

**Existantes (réutilisées) :**
| Entité | Rôle |
|---|---|
| `binary_sensor.vacances_actives` | Vérité métier finale du domaine Vacances (cause immédiate) |
| `binary_sensor.presence_confort_thermique_stabilisee` | Présence débruitée (120 s) — condition d'absence pour l'extinction |
| `binary_sensor.presence_famille_unifiee` | Présence canonique — déclencheur de l'horodatage |
| `binary_sensor.clim_extinction_absence_prolongee_autorisee` | Cause « absence longue qualifiée » (base **recomputée**, cf. §4) |
| `binary_sensor.autorisation_clim_cool` | Autorité unique d'autorisation COOL |
| `sensor.clim_raison_decision`, `sensor.clim_verdict_cool` | Diagnostics (causes étendues, cf. §7) |

**Nouvelles (IDs attribués par le propriétaire — C20) :**
| Rôle | Entité | Écrivain |
|---|---|---|
| Helper de durée d'absence longue | `input_number.clim_duree_absence_longue` | opérateur / UI |
| Horodatage de début d'absence | `input_datetime.clim_debut_absence` | automation `10030000000122` (unique) |
| Vérité du veto composite | `binary_sensor.clim_veto_absence_vacances` | aucun (calculé) |

**Hors périmètre, non modifiés (D14) :** `input_boolean.clim_blocage_absence_prolongee_actif` et la vérité `_reel` prévue par `06` — dette conservée, lot séparé.

---

## 3. Helper de durée d'absence longue (D3)

- **Type / unité :** `input_number`, en **heures**.
- **Bornes / granularité :** `min: 8`, `max: 48`, `step: 1` (*proposition validable — préférence opérateur au déploiement : **14 h**, non gravée comme constante physique*).
- **`initial:` INTERDIT** (doctrine `restauration_etat_helpers.md` R01) : la persistance est assurée par la restauration d'état HA.
- **Repli de lecture obligatoire** chez tout consommateur : `float(<défaut>)` — aucune logique ne dépend d'un `unknown` au premier démarrage (R04 ; pas de fallback silencieux).
- **Autorité d'écriture unique :** opérateur / UI. Exposé au dashboard Réglages climatisation en **affichage seul** (UI non décisionnaire).
- **Périmètre strict :** gouverne **exclusivement** l'absence longue non qualifiée ; **Vacances ignore ce seuil** (§5).

---

## 4. Continuité physique de l'absence longue (D4, D5)

**Horodatage de début d'absence** `input_datetime.clim_debut_absence` :
- **écrivain unique** = automation `10030000000122` ;
- **posé** au passage de `binary_sensor.presence_famille_unifiee` à `off` (début d'une absence) **si non déjà posé** (idempotent) ;
- **effacé** (sentinelle explicite) au retour de présence (`on`) ;
- **réconcilié au démarrage** (`homeassistant: start`) : si absent et horodatage déjà posé, l'état est reconstruit sans remise à zéro.

**Échéance et qualification :**
```
echeance         = clim_debut_absence + clim_duree_absence_longue (heures)
absence_qualifiee = presence_confort_thermique_stabilisee == off
                    ET horodatage_valide
                    ET now() >= echeance
```
- L'échéance est **recalculée sur état** : au démarrage, et à tout **changement du helper de durée** (D5) — un raccourcissement sous la durée écoulée **qualifie immédiatement** ; un allongement **repousse** l'échéance.
- **Idempotence :** un redémarrage ne réinitialise **jamais** la durée écoulée (l'ancre est l'horodatage persistant, pas un compteur volatil).
- **Observabilité (D — aucun ID) :** `binary_sensor.clim_extinction_absence_prolongee_autorisee` **expose en attributs** : `debut_absence`, `echeance`, `duree_ecoulee_h`.

**`clim_extinction_absence_prolongee_autorisee` (recomputée) :**
```
EXTINCTION = presence_confort_thermique_stabilisee == off  ET  absence_qualifiee (échéance dépassée)
```
> **Timer `absence_longue_clim` — proposition (validable au stop point) :** **retrait de son rôle décisionnel**, remplacé par l'ancrage horodaté ci-dessus (le timer figeait `08:00:00` et se réarmait au boot, incompatible avec la continuité physique). Décision finale au Lot 1 ; si conservé, il ne peut être qu'instrumental et **ne doit pas** imposer de remise à zéro au boot.

---

## 5. Veto immédiat des Vacances (D1)

`binary_sensor.vacances_actives == on` est une **cause de veto à part entière**, **indépendante** du timer, de `clim_duree_absence_longue` et de la durée écoulée. Elle est **reconstruite immédiatement au démarrage** (le domaine Vacances est boot-proof, `contrats/vacances.md §9`). Un départ en Vacances interdit le COOL **sans attendre** la qualification d'absence longue.

---

## 6. Veto composite et autorité (D6, D7)

**Vérité calculée unique** `binary_sensor.clim_veto_absence_vacances` (aucun écrivain) :
```
clim_veto_absence_vacances =
    clim_extinction_absence_prolongee_autorisee == on
    OU  vacances_actives == on
```
- **Attribut `cause`** (D — aucun ID) : `vacances` | `absence_prolongee` | `cumulé` | `aucune`.
- **Fail-closed :** toute source indisponible/`unknown` est traitée de façon **explicite** ; l'indisponibilité de `vacances_actives` **n'autorise pas** le COOL par défaut au titre de cette cause (repli défensif documenté, jamais silencieux).

**Autorité finale** `binary_sensor.autorisation_clim_cool` : la condition d'absence
`clim_extinction_absence_prolongee_autorisee == off` est **remplacée** par la lecture du composite :
```
... ET clim_veto_absence_vacances == off
```
Les **quatre autres conditions** (température extérieure, aération étage, fenêtres temporisées, blocage horaire) sont **inchangées**. L'autorisation **ne duplique pas** la formule composite : elle lit la vérité.

---

## 7. Diagnostics (F — extension, aucun ID)

Les diagnostics distinguent au minimum : **absence longue**, **Vacances**, **cumulé**, **absence ordinaire**, **autorisation normale**.

- `sensor.clim_raison_decision` : la cause de priorité « absence prolongée » (cascade `10_decision.md` §raison, rang 9) est **subdivisée**, sous garde `cool_besoin`, en `vacances` / `absence_prolongee` / `absence_et_vacances` (cumulé) selon l'attribut `cause` du composite.
- `sensor.clim_verdict_cool` : la valeur `absence_prolongee` est **complétée** par `vacances` et `absence_et_vacances`.

Les diagnostics restent en **lecture pure** ; ils ne recréent aucune décision et ne sont pas consommés par l'autorisation.

---

## 8. Comportement fail-closed et états dégradés

| Situation | Comportement | Explicite par |
|---|---|---|
| `clim_duree_absence_longue` `unknown`/non restauré | repli de lecture `float(<défaut>)` | consommateur (R04) |
| `clim_debut_absence` absent/sentinelle | absence **non** qualifiée (pas d'extinction sur horodatage manquant) | template défensif |
| `vacances_actives` indisponible | cause Vacances **non** affirmée par défaut ; veto Vacances non levé silencieusement | §6 |
| Toutes sources absence indisponibles | veto composite **ne s'affirme pas faussement** ; autorisation gouvernée par les autres conditions | §6 |

Aucun fallback mémoire, aucune valeur inventée.

---

## 9. Frontière avec le Chantier C21 (point d'extension déclaré, non implémenté)

Le veto composite (§6) est, dans ce contrat, **inconditionnel** dès qu'une cause est vraie. Le Chantier C21 pourra introduire une **exception bornée** (préparation du retour) neutralisant le composite dans une fenêtre avant `input_datetime.fin_vacances`. **Ce contrat déclare ce point d'extension** :
```
veto_effectif (cible C21) = clim_veto_absence_vacances == on  ET NON preparation_cool_active
```
**C20 ne crée aucune préparation, aucune fenêtre, aucune exception provisoire.** La neutralisation ne concernera **jamais** les autres blocages (aération, fenêtres, horaire, température extérieure).

---

## 10. Invariants (opposables, exposés CI)

- **INV-VETO-1** — Autorité unique : `autorisation_clim_cool` reste le seul point d'autorisation COOL ; aucune décision centrale.
- **INV-VETO-2** — Effet immédiat Vacances : `vacances_actives on` ⇒ veto, indépendant de tout seuil temporel.
- **INV-VETO-3** — Pas de durée fixe : aucune durée d'absence longue figée en dur ; la source unique est `input_number.clim_duree_absence_longue`.
- **INV-VETO-4** — `initial:` absent sur le helper de durée.
- **INV-VETO-5** — Continuité physique : qualification ancrée sur `clim_debut_absence` ; aucune remise à zéro au boot.
- **INV-VETO-6** — Composite sans écrivain, sans duplication : `clim_veto_absence_vacances` est calculé ; l'autorisation le lit, ne le recalcule pas.
- **INV-VETO-7** — Écrivain unique de l'horodatage : seul `10030000000122` écrit `clim_debut_absence`.
- **INV-VETO-8** — Fail-closed : aucune source indisponible ne produit une autorisation par défaut au titre de l'absence/Vacances.
- **INV-VETO-9** — Frontière C21 : aucune préparation/exception créée par C20.

> **Vérification CI (proposition, Lot 2) :** checker dédié `check_climatisation_absence_cool_contracts.py` + workflow `contracts_climatisation_absence_cool.yml` (nom à confirmer) — le domaine COOL/absence n'a aujourd'hui **aucun** checker.

---

## 11. Scénarios contractuels (mapping)

| # | Scénario | Attendu |
|---|---|---|
| 1 | Présence, pas de Vacances | COOL autorisé (autres conditions) ; veto composite `off` |
| 2 | Absence 10 h, seuil 14 h | non qualifiée ⇒ pas d'extinction ⇒ règles absence |
| 3 | Absence 16 h, seuil 14 h | qualifiée à 14 h ⇒ veto |
| 4 | Week-end sans Vacances | qualifiée ⇒ veto ; reprise réactive au retour |
| 5 | Vacances activées avant échéance | **veto immédiat** (cause `vacances`) |
| 6 | Vacances actives au démarrage | veto reconstruit immédiatement au boot |
| 7 | Reboot pendant absence > 14 h | **continuité physique** : reste qualifiée (échéance dépassée), pas de remise à zéro |
| 8 | Réduction du helper sous la durée écoulée | qualification immédiate |
| 9 | Augmentation du helper pendant l'absence | échéance repoussée |
| 10 | Vacances ET absence longue vraies | veto ; cause `cumulé` |
| 11 | Retour de présence | présence terminale : `vacances_actives off` + extinction off + horodatage effacé ⇒ veto tombe |
| 12 | Valeurs indisponibles/invalides | fail-closed explicite (§8) |

---

*Contrat de politique d'absence COOL — opposable. En cas de divergence, ce contrat fait foi pour la couche absence/Vacances/veto composite ; les contrats voisins y renvoient.*
