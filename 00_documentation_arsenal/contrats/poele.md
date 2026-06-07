# 🧠 ARSENAL — CONTRAT NORMATIF
## Poêle — Apport thermique exogène : détection, mémoire 24 h, blocage chauffage / climatisation

## 📌 Statut

**v1.0 — NORMATIF, SOUVERAIN.** Ce contrat documente le runtime réel du domaine
`poele` (préfixe d'identifiant `1010`). En cas de divergence, le comportement réel
des automations et templates prévaut. Aucune entité, aucun seuil et aucune règle
ne sont inventés.

**Souveraineté partagée explicite.** Ce contrat est **souverain sur le cycle de
vie** du poêle (mémoire, blocage, sécurité, durée) et sur ses **effets
transverses**. La **couche détection** reste **souveraine dans les contrats
capteurs chauffage** existants (cf. §1) : ce contrat y **renvoie** sans les
déplacer ni les dupliquer.

## 🎯 Rôle

Le poêle est un **apport thermique exogène non piloté**. Quand il fonctionne, il
réchauffe le séjour indépendamment du chauffage : Arsenal le **détecte**, en
**mémorise** le fonctionnement récent, et **bloque temporairement** la montée du
chauffage **et** l'admissibilité HEAT de la climatisation, pour ne pas cumuler des
apports. C'est de l'**observabilité + blocage** ; il n'y a **aucun pilotage** du
poêle lui-même.

## 🧱 Sources de vérité (entités réelles)

| Rôle | Entité | Définition runtime |
|---|---|---|
| Détection — preuve candidate | `binary_sensor.signature_thermique_poele` | `12_template_sensors/poele/detection.yaml` |
| Détection — présence séjour | `binary_sensor.presence_humaine_sejour` | `12_template_sensors/poele/detection.yaml` |
| Détection — frontière finale niveau 1 | `binary_sensor.poele_en_fonction` | `12_template_sensors/poele/detection.yaml` |
| Détection — stabilisée | `binary_sensor.poele_en_fonction_stable` | `12_template_sensors/poele/capteur_stabilise.yaml` |
| Mémoire 24 h | `input_boolean.poele_recent` | `05_input_booleans/poele/poele_recent.yaml` |
| Timer mémoire 24 h | `timer.poele_24h` (24 h, `restore: true`) | `08_timers/poele/blocage_ajustement_courbe.yaml` |
| Blocage chauffage | `input_boolean.blocage_chauffage_poele` | `05_input_booleans/poele/chauffage_poele.yaml` |
| Blocage climatisation | `input_boolean.blocage_clim_poele` | `05_input_booleans/climatisation/blocage_poele.yaml` |
| Timer de blocage | `timer.poele_blocage_chauffage` (défaut `01:00:00`) | `08_timers/poele/blocage_chauffage.yaml` |
| Durée de blocage paramétrable | `input_number.poele_duree_blocage_chauffage_minutes` (30–180 min) | `03_input_numbers/chauffage/blocage_poele.yaml` |

Automations (préfixe `1010`) : `10100000000001` (mémoire on), `10100000000002`
(mémoire off), `10100000000005` (blocage début), `10100000000006` (blocage fin),
`10100000000007` (sécurité démarrage), `10100000000008` (ajustement durée).

## 1. Détection (couche déléguée — renvoi)

La détection du fonctionnement du poêle est **souveraine dans les contrats
capteurs chauffage** et n'est **pas** redéfinie ici :
- [`signature_thermique_poele.md`](chauffage/15_capteurs/03_capteurs_blocages_niveau1/signature_thermique_poele.md) — preuve thermique candidate (amorce 30 min + consolidation 60 min) ;
- [`poele_en_fonction.md`](chauffage/15_capteurs/03_capteurs_blocages_niveau1/poele_en_fonction.md) — frontière de blocage **niveau 1 finale** (triple preuve : signature thermique + présence + …).

Le présent contrat **consomme** ces capteurs ; il ne les produit pas.

## 2. Mémoire 24 h

- **Activation** (`10100000000001`) : sur passage à `on` de
  `binary_sensor.signature_thermique_poele` → `input_boolean.poele_recent` `on` +
  (re)démarrage de `timer.poele_24h` (24 h, `restore: true`).
- **Extinction** (`10100000000002`) : sur `timer.finished` de `timer.poele_24h`,
  si `poele_recent` est `on` → `input_boolean.poele_recent` `off`.

`poele_recent` mémorise donc un fonctionnement **récent** (fenêtre glissante de
24 h relancée à chaque nouvelle signature).

## 3. Blocage chauffage et climatisation

- **Début** (`10100000000005`) : sur passage à `on` de
  `binary_sensor.poele_en_fonction` → `turn_on` de **`input_boolean.blocage_chauffage_poele`
  ET `input_boolean.blocage_clim_poele`** + démarrage de
  `timer.poele_blocage_chauffage` (durée = `input_number.poele_duree_blocage_chauffage_minutes` × 60 s).
- **Fin** (`10100000000006`) : sur `timer.finished` de
  `timer.poele_blocage_chauffage` → `turn_off` des **deux** flags de blocage.
- **Ajustement de durée** (`10100000000008`) : si
  `input_number.poele_duree_blocage_chauffage_minutes` change **alors que le
  blocage est actif**, le timer est redémarré avec la nouvelle durée.
- **Sécurité démarrage** (`10100000000007`) : à la stabilisation système
  (`input_boolean.systeme_stable`), si le timer de blocage n'est plus actif mais
  qu'un flag de blocage est resté `on`, les deux flags sont remis à `off`
  (rattrapage d'un blocage orphelin après redémarrage).

Les deux flags de blocage sont **co-écrits** par les mêmes automations poêle : le
blocage chauffage et le blocage climatisation sont **synchrones**.

## 4. Effets transverses (consommateurs aval)

Le domaine poêle est **transverse** : ses flags sont lus par deux sous-systèmes
distincts (le poêle reste, lui, souverain sur leur écriture — §5) :

- **Chauffage — décision** : `10_scripts/chauffage/decision_centrale.yaml` lit
  `input_boolean.blocage_chauffage_poele` → motif `poele_actif` (blocage de la
  montée chauffage).
- **Chauffage — courbe** : `11_automations/chauffage/courbe_de_chauffe/auto_ajustement.yaml`
  lit `binary_sensor.poele_en_fonction_stable` → motif `baisse_bloquee_poele`
  (blocage de la baisse de courbe).
- **Climatisation — HEAT** : `12_template_sensors/climatisation/autorisation/heat.yaml`
  exige `input_boolean.blocage_clim_poele == off` pour autoriser le mode HEAT.

## 5. Écrivain souverain par flag

Chaque flag du domaine possède un écrivain souverain unique :
- `input_boolean.poele_recent` : automations mémoire (`…001` / `…002`) ;
- `input_boolean.blocage_chauffage_poele` et `input_boolean.blocage_clim_poele` :
  automations de blocage poêle (`…005` / `…006` / `…007`).

Les consommateurs (chauffage, climatisation) **lisent** ces flags ; ils ne les
écrivent **jamais**.

## 6. Hors périmètre

- **Aucun pilotage du poêle** ni **aucune commande matérielle** : le poêle est un
  apport **non piloté**, seulement observé.
- **Pas de généralisation** à d'autres apports thermiques exogènes.
- **Détection** : hors de ce contrat — souveraine dans les contrats capteurs
  chauffage (§1).
- Aucune modification du runtime, des contrats chauffage existants, de la
  climatisation, des dashboards ni de la CI.

## 7. Dettes / observations

- **OBS-POELE-1 — Fichier timer mal nommé.** `timer.poele_24h` (mémoire) est
  défini dans `08_timers/poele/blocage_ajustement_courbe.yaml`, dont le nom de
  fichier ne reflète pas le contenu. Observation runtime, non corrigée ici.
- **OBS-POELE-2 — Blocage chauffage/clim synchrone.** Les deux flags de blocage
  sont co-écrits ; il n'existe pas de blocage différencié par sous-système.

## 🔗 Renvois

- Détection (souveraine) : [`signature_thermique_poele.md`](chauffage/15_capteurs/03_capteurs_blocages_niveau1/signature_thermique_poele.md), [`poele_en_fonction.md`](chauffage/15_capteurs/03_capteurs_blocages_niveau1/poele_en_fonction.md)
- Consommation chauffage : pipeline chauffage (décision centrale, courbe de chauffe)
- Consommation climatisation : autorisation HEAT

## 🔒 Statut d'autorité

Contrat **souverain** du domaine `poele` pour le cycle de vie et les effets
transverses. Le runtime fait foi ; tout écart d'implémentation est une
non-conformité, pas une interprétation. La couche détection demeure régie par les
contrats capteurs chauffage référencés en §1.

## Changelog

| Version | Date | Modification |
|---|---|---|
| 1.0 | 2026-06-07 | Création du contrat souverain depuis le runtime réel : mémoire 24 h (`poele_recent` / `timer.poele_24h`), blocage chauffage **et** climatisation synchrone (`blocage_chauffage_poele` / `blocage_clim_poele` / `timer.poele_blocage_chauffage`, durée `poele_duree_blocage_chauffage_minutes`), ajustement de durée, sécurité démarrage, effets transverses (chauffage décision + courbe, climatisation HEAT), écrivain souverain par flag. Détection laissée souveraine aux contrats capteurs chauffage (renvoi). Hors périmètre : aucun pilotage du poêle, aucune généralisation. |
