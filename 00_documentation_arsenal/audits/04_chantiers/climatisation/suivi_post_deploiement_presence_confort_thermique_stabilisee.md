# Suivi post-déploiement — Présence confort thermique stabilisée (V1 + V2)

| Champ | Valeur |
|---|---|
| **Type** | Note de suivi post-déploiement (observation) |
| **Domaine** | Climatisation / Présence — interface de stabilisation COOL/DRY |
| **Statut** | **Implémenté (V1 + V2) — sous observation — en attente de validation terrain** |
| **Non clôturé** | Le problème **n'est pas** considéré comme résolu. Correction déployée, **non encore validée en conditions réelles**. |
| **Version** | 0.1 (ouverture du suivi) |
| **Cadre** | Aucun runtime modifié par ce document. Reflète l'état réel après V1+V2 et redémarrage HA. |

> **Objet :** consigner l'état réel du chantier après déploiement de V1 puis V2,
> ouvrir la **phase d'observation**, et fixer les **critères de validation
> terrain** — sans clore, sans ratifier, sans nouveau patch.

---

## 1. Ce qui est déployé

**Signal.** `binary_sensor.presence_confort_thermique_stabilisee` — source unique
`binary_sensor.presence_famille_unifiee`, `delay_off: 120 s`, pas de `delay_on`.
Opérationnel après redémarrage HA.

**V1 — couche seuils / consignes COOL (5 fichiers rebranchés sur la stabilisée).**
`seuils_on_off/cool/on.yaml`, `seuils_on_off/cool/off.yaml`, `decision/consigne.yaml`,
`cool/maj_consignes/absence.yaml`, `cool/maj_consignes/presence.yaml`.

**V2 — couche autorisation (2 fichiers rebranchés sur la stabilisée).**
`autorisation/dry.yaml` (terme présence **direct**), `blocages/absence_longue.yaml`
(capteur `clim_extinction_absence_prolongee_autorisee`, qui gate COOL **via**
`autorisation/cool.yaml`).

**Non touchés** (par construction) : `presence_famille_unifiee`,
`presence_famille_securite`, alarme/sécurité, `target_mode`, `besoin`/`admissibilite`,
`timer.absence_longue_clim` (8 h), `cool/start_timer_absence.yaml`,
`autorisation/cool.yaml` (corrigé transitivement), HEAT, silence, chauffage.

---

## 2. Pourquoi V2 a été nécessaire (correction de périmètre)

V1 a couvert les **5 consommateurs COOL** de la Catégorie 1 de l'inventaire
([`inventaire_consommateurs_presence_famille_unifiee.md`](../../02_conception/climatisation/inventaire_consommateurs_presence_famille_unifiee.md)).
La contre-expertise runtime a montré que **deux consommateurs classés
Catégorie 3 (« à discuter »)** étaient en réalité des **chemins de coupure
actifs** restés sur la présence brute :

- `blocages/absence_longue.yaml` — l'inventaire le jugeait « déjà immunisé par
  le timer sur les drops courts » ; or la fenêtre de ~5 s **avant** le démarrage
  du timer ouvre une coupure COOL transitoire (observée).
- `autorisation/dry.yaml` — l'inventaire notait « impact non observé » ; l'impact
  DRY a ensuite été observé (séquence du 15/06, `autorisation_dry` off immédiat
  sur présence brute).

V2 a donc reclassé ces deux fichiers de « à discuter » vers « rebranché ». Voir
le détail dans l'inventaire (section *État de déploiement V1+V2*).

---

## 3. Comportement attendu post-V2 (à confirmer par l'observation)

- Un **faux-absent court (< 120 s)** ne doit plus couper COOL ni DRY : les deux
  portes de présence lisent la stabilisée, et le `delay_off` de 120 s absorbe le
  glitch.
- Les **toggles seconde-échelle d'origine présence** (coupure brute immédiate +
  blip de 5 s d'`absence_longue`) doivent disparaître.
- **Frontière de calibration assumée** : une absence **> 120 s** reste traitée
  comme réelle et coupe (par conception ; ce n'est pas un faux-absent). Une
  vraie absence longue sort inchangée — l'extinction réelle reste pilotée par le
  **timer 8 h**.

## 4. Ce que l'observation ne tranchera pas seule

Les **cycles courts d'origine non-présence** (blips sub-minute sous le seuil ON ;
arbitrage COOL↔DRY ; fluctuation dans la bande 1 °C) ne sont **pas** dans le
périmètre de ce chantier et ne doivent pas lui être imputés. Cf.
[`investigation_historique_clim_30j.md`](../../01_rapports/climatisation/investigation_historique_clim_30j.md).

---

## 5. Critères de validation terrain (à statuer après la fenêtre d'observation)

Aucune donnée post-V2 disponible à l'ouverture de ce suivi. La validation
s'appuiera sur la chaîne **désormais historisée** (`clim_target_mode`,
`autorisation_clim_cool/dry`, `clim_blocage_horaire_reel`, présence brute et
stabilisée). Critères proposés, **non ratifiés** :

1. **Absence de coupure < 120 s** : sur la fenêtre d'observation, aucun
   `autorisation_clim_cool`/`_dry` → off **corrélé** à un creux de présence brute
   de durée < 120 s.
2. **Réveil correct** : sur un creux > 120 s suivi d'un retour, restauration de
   l'autorisation sans latence ajoutée injustifiée (pas de `delay_on`).
3. **Vraies absences préservées** : extinction longue toujours pilotée par le
   timer 8 h, non anticipée par la stabilisée.
4. **Calibration `T`** : vérifier que 120 s couvre la distribution réelle des
   faux-absents (impacts mesurés à 7,2 s et 69,1 s ; cf.
   [`note_calibration_tenue_T_presence_confort_thermique.md`](../../02_conception/climatisation/note_calibration_tenue_T_presence_confort_thermique.md)).

> Un **document de validation terrain** sera produit **après** la fenêtre
> d'observation, lorsque des données post-V2 existeront. Il n'est **pas** créé à
> ce stade (rien à valider encore). Ce suivi ne préjuge pas de son verdict.

---

## 6. État du chantier

- **Implémenté** : V1 + V2 déployés, HA redémarré, signal opérationnel.
- **Sous observation** : phase en cours, aucun incident post-V2 encore disponible.
- **En attente de validation terrain** : critères §5 à statuer.
- **Non clôturé** : aucune `05_clotures/` n'est ouverte ; le problème n'est pas
  déclaré résolu.

---

## 7. Documents liés

- Cadrage contractuel : [`cadrage_contrat_presence_confort_thermique_stabilisee.md`](../../02_conception/climatisation/cadrage_contrat_presence_confort_thermique_stabilisee.md)
- Inventaire des consommateurs : [`inventaire_consommateurs_presence_famille_unifiee.md`](../../02_conception/climatisation/inventaire_consommateurs_presence_famille_unifiee.md)
- Note de calibration `T` : [`note_calibration_tenue_T_presence_confort_thermique.md`](../../02_conception/climatisation/note_calibration_tenue_T_presence_confort_thermique.md)
- Dette de modélisation présence (constat transverse) : [`cadrage_dette_modelisation_presence.md`](../../02_constats/transverses/cadrage_dette_modelisation_presence.md)
- Investigation historique 30 j : [`investigation_historique_clim_30j.md`](../../01_rapports/climatisation/investigation_historique_clim_30j.md)
- Hubs : [`navigation/domaines/climatisation.md`](../../../navigation/domaines/climatisation.md) · [`navigation/domaines/presence.md`](../../../navigation/domaines/presence.md)

---

*Note de suivi. Aucun runtime, contrat ou YAML modifié. Implémenté et sous
observation — non clôturé, non ratifié, non validé en conditions réelles.*
