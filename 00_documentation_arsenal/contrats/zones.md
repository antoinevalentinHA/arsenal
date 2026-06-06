# zones.md
# Arsenal — Référentiel des zones géographiques
# Version : 1.0.3
# Statut : Normatif

---

## 1. Objet

Ce contrat définit le référentiel canonique des zones géographiques utilisées dans Arsenal.
Il établit la nature, le rôle, les invariants et les contrats d'usage de chaque zone.

---

## 2. Principes architecturaux

- Toute zone est un **objet passif** : elle publie un état de présence, elle ne déclenche aucune action.
- Aucune automatisation métier ne consomme directement une zone sans passer par une couche de décision intermédiaire.
- Les zones métier Arsenal sont gouvernées en YAML (`zones/`). Elles ne sont pas éditables via l'UI HA.
- `zone.home` est une **primitive système HA**. Elle n'est pas gouvernée par Arsenal et ne doit pas être manipulée.
- Les coordonnées GPS de référence Arsenal sont celles de `zone.home` : `44.8522979, -0.5875885`.

---

## 3. Référentiel des zones

### 3.1 `zone.home` — Zone système HA

| Attribut              | Valeur                  |
|-----------------------|-------------------------|
| Source                | `.storage/core.config`  |
| Gouvernance           | HA natif — hors Arsenal |
| Latitude              | 44.8522979              |
| Longitude             | -0.5875885              |
| Rayon                 | 824 m                   |
| Éditable UI           | Non                     |
| Éditable YAML Arsenal | Non                     |

**Rôle** : Zone de confort large. Utilisable pour la logique de présence générale (chauffage,
automatismes de confort). Non utilisable pour la sécurité.

**Statut Arsenal** : Primitive système tolérée. Consommée en lecture uniquement.

---

### 3.2 `zone.maison_securite` — Zone métier sécurité

| Attribut     | Valeur                                  |
|--------------|-----------------------------------------|
| Fichier      | `zones/maison_securite.yaml`            |
| Gouvernance  | Arsenal YAML                            |
| Latitude     | 44.8522979                              |
| Longitude    | -0.5875885                              |
| Rayon        | 40 m                                    |
| Icon         | `mdi:shield-home`                       |
| Passive      | false                                   |
| Éditable UI  | Non (grisé post-migration YAML)         |

**Rôle** : Périmètre strict de la maison. Zone de référence pour les décisions de sécurité
(armement / désarmement alarme).

**Domaine consommateur** : Sécurité / alarme uniquement.

---

### 3.3 `zone.approche_securite` — Zone métier infrastructure

| Attribut     | Valeur                                  |
|--------------|-----------------------------------------|
| Fichier      | `zones/approche_securite.yaml`          |
| Gouvernance  | Arsenal YAML                            |
| Latitude     | 44.8522979                              |
| Longitude    | -0.5875885                              |
| Rayon        | 400 m                                   |
| Icon         | `mdi:map-marker-radius`                 |
| Passive      | false                                   |
| Éditable UI  | Non (grisé post-migration YAML)         |

**Rôle** : Périmètre d'approche. Utilisé pour déclencher les mécanismes d'infrastructure
préparatoires (activation GPS haute précision, pré-conditionnement système).

**Domaine consommateur** : Infrastructure technique uniquement. 
Est exploitée exclusivement comme signal d’approche
dans les logiques Arsenal.
Ne déclenche aucune décision métier finale.

---

### Classification vis-à-vis de la présence

| Zone                   | Sécurité | Confort  |
|------------------------|----------|----------|
| zone.home              | ❌       | ✅      |
| zone.maison_securite   | ✅       | ✅      |
| zone.approche_securite | ❌       | ✅      |

### 🔗 Référence normative

La contribution effective d’une zone à la présence canonique
(sécurité ou confort) n’est pas définie dans ce contrat.

Elle est définie exclusivement dans :
[`presence.md`](presence.md) — section "États techniques de projection reconnus".

Toute divergence entre ce contrat et [`presence.md`](presence.md)
constitue une incohérence structurelle et doit être arbitrée.

---

## 4. Invariants

| #  | Invariant |
|----|-----------|
| I1 | `zone.home` n'est jamais modifiée par Arsenal. |
| I2 | Aucun composant du domaine sécurité (automatisation, script, template, capteur) ne consomme `zone.home`. |
| I3 | `zone.maison_securite` est le seul référentiel valide pour les décisions d'armement / désarmement. |
| I4 | `zone.approche_securite` ne doit être utilisée que comme signal d'infrastructure. Elle ne doit jamais être utilisée dans une décision métier finale. |
| I5 | Les coordonnées GPS des zones métier Arsenal sont alignées sur `zone.home` : `44.8522979, -0.5875885`. |
| I6 | Toute modification de rayon d'une zone métier fait l'objet d'un incrément de version de ce contrat. |
| I7 | Les zones sont gouvernées exclusivement en YAML. Toute création de zone via l'UI est interdite. |
| I8 | `zone.maison_securite` ne doit jamais être utilisée pour des logiques d'anticipation ou d'infrastructure. |
| I9 | Les attributs des zones (`latitude`, `longitude`, `radius`) peuvent être utilisés dans des capteurs ou templates uniquement pour des calculs dérivés. Toute duplication de logique géographique est interdite. |
| I10 | Les zones définies dans ce contrat sont non interchangeables. Toute substitution d'une zone par une autre dans un composant constitue une violation contractuelle, même si les rayons sont proches. |

---

## 5. Contrats d'usage par domaine

### 5.1 Domaine Sécurité / Alarme

- **Zone autorisée** : `zone.maison_securite` uniquement.
- **Zone interdite** : `zone.home` (rayon trop large, non discriminant), `zone.approche_securite` (signal d'infrastructure, non métier).
- **Usage** : détection d'entrée/sortie stricte pour armement / désarmement alarme.
- **Contrainte** : toute logique de sécurité basée sur la position doit référencer `zone.maison_securite`, jamais `zone.home` ni `zone.approche_securite`.

### 5.2 Domaine Infrastructure (présence technique)

- **Zone autorisée** : `zone.approche_securite`.
- **Usage** : signal d'approche, déclenchement GPS haute précision, pré-conditionnement système.
- **Interdit** : toute décision métier finale (présence canonique, sécurité, confort).
- **Contrainte** : cette zone ne produit qu'un état d'approche. Elle ne commande aucune action métier.

### 5.3 Domaine Confort (chauffage, automatismes généraux)

- **Zone autorisée** : `zone.home`.
- **Usage** : présence large, logique souple, non nerveuse.
- **Contrainte** : acceptable uniquement pour les décisions à faible criticité (chauffage, éclairage de confort). Jamais pour la sécurité ni pour déclencher des mécanismes d'infrastructure.

---

## 6. Impact sur la présence

### 🧠 Principe

Les zones influencent indirectement la présence via les états des entités `person.*`.

Chaque zone peut devenir un état de `person`, et donc
participer à la détermination de la présence canonique.

### ⚖️ Obligation

Toute zone définie dans Arsenal doit être explicitement classée comme :

- contributrice à la présence (`présent`)
- ou non contributrice

Cette classification doit être cohérente avec :

- le contrat [`presence.md`](presence.md)
- les capteurs de présence amont

### 🛑 Interdictions

Il est interdit de :

- supposer qu’une zone contribue implicitement à la présence
- ignorer l’impact d’une zone sur les états `person`
- introduire une zone sans analyser son effet sur la présence

### 📌 Conséquence

Toute création ou modification de zone impose :

- une revue des capteurs de présence (`person.*`)
- une validation de cohérence avec les vérités canoniques
- une mise à jour éventuelle des listes d’états reconnus

Aucune zone ne peut être ajoutée sans validation de son rôle
dans la sémantique de présence.

---

## 7. Gouvernance

### 7.1 Fichiers
```
config/
  configuration.yaml          # zone: !include_dir_merge_list zones/
  zones/
    maison_securite.yaml
    approche_securite.yaml
```

### 7.2 Règles de modification

- Toute modification de coordonnées, rayon ou `passive` d'une zone métier → incrément de version du contrat.
- Toute création d'une nouvelle zone Arsenal → ajout d'une section §3.x et d'un contrat d'usage §5.x.
- `zone.home` n'apparaît jamais dans `zones/`. Sa modification relève de la configuration
  générale HA (`Paramètres > Système > Général`), hors Arsenal.

### 7.3 Audit

Commande de vérification des fuites de `zone.home` dans le domaine sécurité :
```bash
grep -r "zone.home" 11_automations/ 12_template_sensors/ 10_scripts/ 13_sensor_platforms/ 01_customize/
```

Toute occurrence dans ces dossiers est une violation de I2 et doit être arbitrée.

---

## 8. Historique des versions

| Version | Date       | Modification                                                    |
|---------|------------|-----------------------------------------------------------------|
| 1.0.0   | 2026-03-30 | Création — migration zones UI → YAML                            |
| 1.0.1   | 2026-03-30 | Renforcement I2, I4 — ajout I8, I9 — audit étendu — §5.2 revu   |
| 1.0.2   | 2026-03-30 | Ajout I10 — non-interchangeabilité explicite des zones          |
| 1.0.3   | 2026-03-30 | Ajout 6 — Impact sur la présence                                |