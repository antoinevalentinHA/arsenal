# Arsenal — Changelog v11 beta 3
_20 mars 2026_

---

## Résumé

La v11 beta 3 marque une mutation structurelle majeure du pipeline ECS : passage d'un orchestrateur monolithique à une architecture modulaire par délégation, avec découplage strict entre gestion de session, application de consigne et sécurisation post-cycle.

| Indicateur | Valeur |
|---|---|
| Fichiers ajoutés | +212 |
| Fichiers modifiés | 13 |
| Fichiers supprimés | 0 |
| Domaines touchés | ECS, Lovelace, Zigbee2MQTT |

---

## 🧠 ECS — Éclatement du pipeline en scripts souverains

### Avant (v11 beta 2)

`ecs_cycle` concentrait en un seul script : verrouillage, watchdog, calcul de consigne, ACK bridge, boost de sécurité, armement gardien, fermeture. Monolithe critique, difficile à tester et à faire évoluer.

### Après (v11 beta 3)

`ecs_cycle` devient un **orchestrateur pur** qui délègue à cinq scripts souverains :

| Script | Responsabilité |
|---|---|
| `ecs_cycle_session_open` | Verrouillage exclusif, armement watchdog, garde anti-réentrance |
| `ecs_appliquer_consigne_confirmee` | Application consigne via bridge MQTT + vérification ACK corrélée |
| `ecs_cycle_boost_si_necessaire` | Boost de sécurité en cas de non-atteinte thermique |
| `ecs_armer_gardien_post_prelevement` | Armement du gardien post-prélèvement |
| `ecs_cycle_session_close` | Rabaissement consigne, libération verrou, nettoyage état |

### Modèle d'exécution
```
ecs_cycle
  → session_open          [garde : ecs_cycle_en_cours == on]
  → appliquer_consigne_confirmee
  → surveillance thermique
  → boost_si_necessaire
  → armer_gardien
  → session_close
```

### Changements dans `cycle.yaml`

- Étape 1 délègue à `script.ecs_cycle_session_open` ; une garde explicite sur `input_boolean.ecs_cycle_en_cours` conditionne la suite du cycle
- Responsabilités reformulées : séquencement de bout en bout, calcul consigne + epsilon, validation des entrées métier, mémorisation cible de session
- Suppression des blocs inline de verrouillage, nettoyage d'état et libération du verrou (désormais dans les sous-scripts dédiés)
- Correction des accents dans les commentaires (normalisation UTF-8)

---

## 🧾 Observabilité

- `input_text.ecs_cycle_last_action_status` — mémorisation du statut de la dernière action de cycle (ajout)
- `input_text.ecs_target_temp_session` — cible de session persistée pour traçabilité et debug post-mortem

---

## 📚 Documentation Arsenal

**Contrats ECS ajoutés** (`documentation_arsenal/contrats/ecs/`) :

- `ecs_cycle_session_open.md`
- `ecs_cycle_session_close.md`
- `ecs_appliquer_consigne_confirmee.md`
- `ecs_cycle_boost_si_necessaire.md`
- `ecs_armer_gardien_post_prelevement.md`

**Dossier évolutions futures** (`eclatement_pipeline_ecs/`) :

- `cartographie.md`, `checklist.md`, `plan_migration.md`, `matrice_non_regression.md`
- Squelettes : `armer_gardien`, `chauffage_ecs_cycle`, `ecs_appliquer_consigne_confirmee`, `ecs_cycle_session_open/close`

Le refactor est documenté avant d'être étendu.

---

## 🎛️ Lovelace — Dashboard système

- Section "Systèmes critiques" : grille unique 4 colonnes remplacée par deux grilles distinctes — 2 colonnes (secteur / batteries) + 3 colonnes (Zigbee et réseau)

---

## ⚙️ Infrastructure

- Backup coordinateur Zigbee2MQTT mis à jour (date : 2026-03-20, frame counter : 1 928 597 → +36 118)

---

## ⚠️ Points d'attention

**Dépendance aux sous-scripts** — la fiabilité du pipeline repose désormais sur la conformité de chaque script délégué à son contrat. Toute dérive locale peut casser l'orchestration globale.

**Rupture de paradigme** — fin du script tout-en-un, introduction d'un graphe d'exécution. Ouvre la voie à du retry ciblé, du rollback et d'une supervision fine par sous-unité.