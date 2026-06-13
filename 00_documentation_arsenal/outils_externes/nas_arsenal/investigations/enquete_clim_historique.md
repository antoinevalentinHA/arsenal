# Arsenal — NAS : enquête historique climatisation (`enquete_clim_historique.py`)

## Statut

- Outil d'investigation actif (écosystème d'analyse des backups NAS)
- Exécution NAS Synology — **lecture seule**
- Document normatif
- Domaine : NAS Arsenal / investigations / audit dynamique

---

## Objet

`enquete_clim_historique.py` reconstitue, à partir de l'historique **réellement
enregistré** par le Recorder Home Assistant, la décision théorique attendue de la
chaîne climatisation et la confronte à l'état réel constaté. Il alimente les
investigations empiriques du domaine clim (rapport
[`investigation_historique_clim_30j.md`](../../../audits/01_rapports/climatisation/investigation_historique_clim_30j.md)).

Emplacement NAS : `tools/investigations/enquete_clim_historique.py`.

---

## Invariants

Contrats durs de l'outil. Toute évolution doit les préserver.

- **Lecture seule** : aucun état écrit, aucun service appelé, **aucun YAML ni
  runtime modifié**. Interroge Home Assistant via **REST API** uniquement.
- **Le runtime est la référence** : les seuils/consignes (non historisés) sont
  lus dans leur valeur courante (`/api/states`) et appliqués comme **hypothèse de
  constance** sur la fenêtre, explicitement tracée.
- **Aucune entité inventée** : seules les entités présentes dans le dépôt et la
  liste blanche du Recorder sont consommées.
- **Honnêteté épistémique** : tout terme d'autorisation non historisé est marqué
  `NON_OBSERVABLE` ; la « décision attendue » est une **enveloppe instantanée**,
  pas une reconstitution de la mémoire d'admissibilité.
- **Jeton jamais affiché** : `HA_TOKEN` voyage dans l'en-tête `Authorization`,
  jamais dans l'URL ni les journaux.

---

## Entrées

| Variable | Rôle |
|---|---|
| `HA_URL` | Base URL Home Assistant (ex. `http://192.168.1.117:8123`) |
| `HA_TOKEN` | Jeton longue durée (lecture seule) — **ne jamais afficher** |

Entités consommées : primitives historisées (températures chambres / jardin,
humidex chambres, présence, mode maison, fenêtres *sans délai*, état réel via
`switch.clim_power` + `sensor.clim_mode_local`) ; helpers de seuils lus *live*.
Détail dans le rapport d'investigation, §2 (limites d'observabilité).

---

## Sortie

CSV événementiel (une ligne par changement d'état), croisant mesures réelles,
contexte, seuils appliqués, besoins reconstitués, décision attendue (enveloppe),
état réel, **écart** et **niveau de confiance** (`OBSERVABLE` /
`PARTIELLE_termes_non_observables` / `DATA_MANQUANTE`).

---

## Usage

```bash
# Variables d'environnement (jeton jamais affiché)
export HA_URL="http://192.168.1.117:8123"
export HA_TOKEN="<jeton longue durée>"

# Audit 30 jours
python3 enquete_clim_historique.py \
  --api "$HA_URL" --token "$HA_TOKEN" \
  --days 30 --out audit_clim_30j.csv

# Trace d'URL de diagnostic (sans le jeton)
python3 enquete_clim_historique.py --api "$HA_URL" --token "$HA_TOKEN" \
  --days 1 --out test.csv --debug
```

---

## Limites connues

- Ne reconstitue pas la mémoire d'admissibilité (verrou 2 portes, gardes 5 min).
- Les blocages horaire / aération étage / absence prolongée, la temporisation
  fenêtre et la consigne HEAT **ne sont pas historisés** → marqués non
  observables ; les écarts qui en dépendent restent des **hypothèses**.
- Profondeur bornée par la rétention du Recorder (`purge_keep_days`).

---

## Navigation

- [Retour aux outils externes](../../README.md)
- Rapport d'investigation associé : [`investigation_historique_clim_30j.md`](../../../audits/01_rapports/climatisation/investigation_historique_clim_30j.md)
- Hub domaine : [`navigation/domaines/climatisation.md`](../../../navigation/domaines/climatisation.md)
