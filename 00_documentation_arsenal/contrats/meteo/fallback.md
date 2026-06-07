# ARSENAL — Contrat météo · Fallback

> **Statut : v1.0 — NORMATIF.** Ce contrat documente le runtime réel du
> mécanisme de continuité météo. En cas de divergence, le comportement réel des
> templates prévaut. Aucune entité, aucune borne et aucune règle ne sont
> inventées : les valeurs et entités citées sont des exemples observés au runtime
> (axe de référence : `humidite_relative/jardin`), les paramètres par axe
> restant déclarés dans les contrats d'axe.

## 1. Objet et position

Ce contrat définit la **continuité de la donnée météo** : ce que le système
publie lorsque les sources attendues sont absentes, invalides, indisponibles,
aberrantes ou non fiables. Il centralise les responsabilités que les contrats
voisins lui délèguent explicitement :

- `gouvernance.md` : « la continuité est assurée **exclusivement par
  `fallback.md`** » (hiérarchie des sources, mémoire de continuité, TTL,
  abstention) ; gouvernance « n'implémente aucune logique de fallback ».
- `validation.md` §6 : « hiérarchie entre sources valides » et « stratégie en
  l'absence de source valide » → délégués ici.
- `meteo.md` : tout capteur météo applique `validation.md` puis `fallback.md` ;
  les axes déclarent source primaire/secours, plausibilité, `TTL_override`,
  autorisation du niveau 3.

Position dans l'architecture :

```
gouvernance.md
        ↓
validation.md   fallback.md
        ↓
contrats d'axe (température int./ext., humidité relative, etc.)
```

## 2. Principe fondateur

> La continuité ne crée jamais de donnée. Elle **sélectionne** la meilleure
> valeur disponible selon une hiérarchie, **qualifie** son origine par un statut,
> et **s'abstient** plutôt que de propager une valeur invalide, obsolète ou non
> qualifiée.

## 3. Hiérarchie des niveaux

La valeur publiée par un axe est déterminée par ordre de priorité décroissante :

- **Niveau 1 — sources directes validées.** Les sources de l'axe ayant passé
  `validation.md` (recevabilité + plausibilité) sont agrégées en une **cible
  robuste instantanée** (§5). C'est le niveau nominal.
- **Niveau 2 — source(s) de secours.** Source(s) de secours **déclarée(s) par le
  contrat d'axe** (le cas échéant), soumise(s) à la même validation. Un axe peut
  n'avoir aucune source de secours (à déclarer explicitement côté axe).
- **Niveau 3 — mémoire de continuité.** Dernière valeur publiée valide,
  ré-exposée tant que son âge n'excède pas le TTL (§6, §7). Niveau **autorisé ou
  interdit par l'axe** (`meteo.md` §5).
- **Abstention.** Si aucun niveau n'est exploitable, l'axe publie un statut
  d'absence (`inconnu`) et **ne publie aucune valeur** (§8).

Runtime de référence (axe `humidite_relative/jardin`) : le `statut final`
arbitre la hiérarchie — cible robuste exploitable → statut « live » ; sinon
`binary_sensor.*_memoire_valide` ON → statut `memoire` ; sinon `inconnu`.

## 4. Validation amont (rappel)

Seules les sources dont la validation est `valide` (non `unknown`/`unavailable`,
valeur dans la plage de plausibilité de l'axe) entrent dans le mécanisme. La
définition de la recevabilité et des plages relève de `validation.md` et des
contrats d'axe, **pas** de ce contrat. Exemple runtime :
`binary_sensor.humidite_relative_jardin_N_valide` (plage HR `[-1, 101]`).

## 5. Cible robuste instantanée (niveaux 1–2)

À partir des sources validées, le runtime écarte les valeurs **suspectes**
(aberrantes au regard de la médiane des sources valides) puis agrège les valeurs
**retenues** (validées **et** non suspectes) en une cible robuste. Exemple
runtime (`humidite_relative/jardin`) :

- `*_mediane_sources_valides` — médiane des sources valides.
- `binary_sensor.*_N_suspect` — source valide mais écartée si son écart à la
  médiane dépasse le seuil de l'axe (HR : `6`).
- `*_valeurs_retenues` — sources valides ∧ non suspectes.
- `*_cible_robuste_instantanee` — 1 valeur retenue → cette valeur ; ≥ 2 → moyenne
  des deux plus proches si leur écart est faible, sinon médiane.

Le **statut instantané** qualifie ce niveau : `nominal`, `degrade` (source
unique), `suspect_*` (aberrance détectée), `incoherence_retenue` (écart résiduel
entre retenues), `inconnu` (aucune retenue). Le vocabulaire exact des statuts est
propre à l'axe.

## 6. Mémoire de continuité (niveau 3)

Lorsque le niveau direct n'est pas exploitable, l'axe peut ré-exposer la
**dernière valeur publiée valide**. Le patron runtime (par axe, entités propres)
comporte :

- une **valeur mémorisée** — ex. `input_number.humidite_relative_jardin_valeur_stabilisee`,
  `input_number.temperature_jardin_etat_publie` ;
- un **horodatage de dernière publication valide** — ex.
  `input_datetime.humidite_relative_jardin_derniere_publication_valide`,
  `input_datetime.temperature_jardin_etat_publie_ts` ;
- un **âge mémoire** recalculé périodiquement — ex.
  `sensor.humidite_relative_jardin_age_memoire_minutes` ;
- une **validité mémoire** — la mémoire est exploitable si la valeur est dans la
  plage de plausibilité **et** si `âge ≤ TTL` (ex.
  `binary_sensor.humidite_relative_jardin_memoire_valide`).

La mémoire n'est publiée que sous un statut explicite (`memoire`) : elle est
**toujours qualifiée**, jamais présentée comme une mesure live.

## 7. TTL de rétention

- **TTL_DEFAULT = 30 minutes.** Observé au runtime sur les axes jardin
  (`humidite_relative/jardin` : `âge ≤ 30 min`, attribut `ttl_minutes: 30` ;
  `temperature/jardin` : `âge ≤ 1800 s`).
- **Surcharge par axe (`TTL_override`).** Seul le TTL est surchargeable
  localement (`meteo.md`) ; la hiérarchie ne l'est pas.
- **Expiration effective.** L'axe doit ré-évaluer l'âge à une période ≤ TTL
  (runtime : `time_pattern` ≤ TTL, ex. `minutes: "/1"`), afin que la mémoire
  expire réellement.
- **Variante intérieure.** L'axe `temperature/interieur_multi_capteurs` applique
  une stabilisation à **double TTL** (nominal `1800 s` / post-boot `7200 s`),
  régime propre à cet axe. Le TTL de continuité (§6) ne doit pas être confondu
  avec le **TTL par source** (fraîcheur d'une source brute, défini en validation
  d'axe).

## 8. Conditions d'abstention et qualification

- Si aucune cible robuste exploitable **et** mémoire invalide (absente, hors
  plage, ou `âge > TTL`) → statut `inconnu`, **aucune valeur publiée**.
- La valeur publiée est **toujours accompagnée d'un statut** qui qualifie son
  origine (live nominal/dégradé/suspect/incohérence, `memoire`, ou `inconnu`).
- L'abstention est un **état nominal** du mécanisme, pas une erreur : mieux vaut
  ne rien publier qu'exposer une valeur non fiable.

## 9. Interdictions normatives

Reprises et centralisées depuis `gouvernance.md` :

- Publier ou exploiter une donnée `unknown` / `unavailable`.
- Propager une valeur obsolète **sans qualification** (la mémoire n'est publiable
  que sous statut `memoire`, dans la limite du TTL).
- Masquer une invalidité par un calcul, inférer une météo par extrapolation.
- Introduire une **source implicite** dans un fallback.
- Utiliser un axe météo comme source de secours d'un **autre** axe (`meteo.md` §5).
- Publier une mémoire de continuité sur un axe qui **interdit** le niveau 3.

## 10. Séparation des responsabilités

| Contrat | Responsabilité |
|---|---|
| `gouvernance.md` | Cadre, interdictions absolues, architecture |
| `validation.md` | Recevabilité et validité **par source** (plausibilité, fraîcheur source) |
| `fallback.md` (ce contrat) | Hiérarchie des niveaux, cible robuste, mémoire de continuité, TTL, abstention, qualification |
| Contrats d'axe | Sources primaire/secours, plages de plausibilité, `TTL_override`, autorisation du niveau 3, variantes |

## 11. Variantes par axe (observées)

- **Axes « jardin » (`temperature/jardin`, `humidite_relative/jardin`)** : chaîne
  complète validation → suspect → rétention → cible robuste → statut → mémoire de
  continuité (niveau 3) → façade.
- **`temperature/interieur_multi_capteurs`, `humidite_relative/interieur_multi_capteurs`** :
  sous-architecture consolidation → stabilisation (double TTL) → façade par pièce.
- Le détail des sources, seuils et l'autorisation du niveau 3 sont **déclarés par
  chaque contrat d'axe**, jamais redéfinis ici.

## 12. Dettes / limites connues

- **DETTE-FB-1 — Nommage par axe non uniforme.** Les entités de mémoire diffèrent
  selon l'axe (`*_valeur_stabilisee` / `*_derniere_publication_valide` côté HR
  jardin ; `temperature_jardin_etat_publie` / `*_ts` côté température jardin).
- **DETTE-FB-2 — Expression du TTL.** Le TTL_DEFAULT (30 min) est exprimé tantôt
  en minutes, tantôt en secondes (`1800 s`) selon l'axe.
- **DETTE-FB-3 — Vocabulaire de statut par axe.** Les libellés de suspicion
  (`suspect_hr`, `suspect_chaud`, …) sont propres à chaque axe.

## 13. Renvois canoniques

- Cadre et interdictions → [`gouvernance.md`](gouvernance.md)
- Validation des sources → [`validation.md`](validation.md)
- Cadre du domaine → [`meteo.md`](meteo.md)
- Paramètres par axe → contrats d'axe (`axe_temperature.md`,
  `axe_temperature_jardin.md`, `axe_humidite_relative_jardin.md`, sous-domaines
  `temperature_interieure/`, `humidite_relative_interieure/`)

## 14. Historique des versions

| Version | Date       | Modification                                                                                  |
|---------|------------|-----------------------------------------------------------------------------------------------|
| v1.0    | 2026-06-07 | Consolidation depuis le runtime réel. Formalisation des responsabilités déléguées par les contrats voisins : hiérarchie des niveaux, cible robuste, mémoire de continuité, TTL (DEFAULT 30 min, `TTL_override` par axe), abstention et qualification, interdictions, séparation des responsabilités, variantes par axe. Promotion en normatif. |
| —       | —          | Stub de continuité (« contenu normatif détaillé reste à consolider »), créé pour restaurer la navigation. Remplacé.                                                                                            |
