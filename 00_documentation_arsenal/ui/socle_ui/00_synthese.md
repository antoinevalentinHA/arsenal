# 🧭 SOCLE UI — Synthèse de sélection

## Objet

Guide de sélection des socles button-card Arsenal.
Permet de choisir le bon socle sans ouvrir les fichiers thématiques.
Organisé par cas d'usage, critères de choix et avertissements sur variantes proches.

---

## 0. Convention de nommage des suffixes

Les suffixes des noms de socles sont contractuels et auto-documentés.

| Suffixe | Signification |
|---------|--------------|
| `_72` | hauteur standard 72px explicitement fixée |
| `_68` | hauteur compacte 68px (options secondaires) |
| `_88` | hauteur XL 88px |
| `_xl` | format synthèse visuelle (80px, icon 28px) |
| `_compact` | densité élevée, surface réduite |
| `_label` | champ label activé |
| `_sans_icone` | icône supprimée |
| `_sans_nom` | name supprimé |
| `_confirme` | confirmation utilisateur obligatoire |
| `_readonly` | toutes interactions verrouillées à none |
| `_interactif` | more-info autorisé (variante d'un socle non interactif) |
| `_base` | socle racine autonome (hors carte_base_v2) |

---

## 1. Arbre de décision rapide
```text
Quelle est la nature de la carte ?
│
├── Action utilisateur volontaire
│   ├── Avec confirmation obligatoire
│   │   ├── Toggle on/off              → socle_toggle_confirme
│   │   └── Script / service           → socle_action_script_confirme
│   ├── Sans confirmation
│   │   ├── Action standard
│   │   │   ├── Avec fond gris         → socle_action_simple
│   │   │   └── Sans fond              → socle_action_simple_sans_couleur
│   │   ├── Action critique            → socle_action_critical
│   │   └── Action avec feedback label → socle_action_label_compact
│   └── Toggle on/off
│       ├── Standard (72px)            → socle_toggle
│       └── Compact options (68px)     → socle_toggle_compact_68
│
├── Lecture seule — valeur mesurée / capteur
│   ├── Valeur mise en avant (KPI)
│   │   ├── Couleur depuis entité couleur
│   │   │   ├── Sans label             → socle_kpi
│   │   │   └── Avec label             → socle_kpi_label
│   │   └── Neutre (sans couleur auto)
│   │       ├── Avec icône             → socle_kpi_72
│   │       ├── Sans icône             → socle_kpi_72_sans_icone
│   │       ├── Avec label + icône     → socle_kpi_label_72
│   │       └── Avec label sans icône  → socle_kpi_label_72_sans_icone
│   └── Diagnostic capteur
│       ├── Format XL 88px             → socle_diagnostic
│       ├── Compact 72px (tap more-info hérité, surchargeable)
│       │                              → socle_diagnostic_compact
│       └── Compact 72px read-only strict
│                                      → socle_diagnostic_compact_readonly_72
│
├── Lecture seule — état système / équipement
│   ├── État réel (more-info autorisé) → socle_etat_reel
│   ├── État principal typographié     → socle_etat_lecture_principale (composition)
│   └── État + action secondaire       → socle_etat_action_secondaire
│
├── Lecture seule — décision système
│   └── Résultat décisionnel (name + state + label)
│                                      → socle_decision_72
│
├── Lecture seule — information système
│   └── Info infra / système (fond bleu fixe)
│                                      → socle_info_72
│
├── Lecture seule — statut équipement
│   ├── Interactif (more-info)
│   │   ├── Standard                   → socle_status
│   └── Non interactif
│       ├── Compact sans icône (64px)  → socle_status_compact
│       ├── Avec label sans icône      → socle_status_label
│       ├── Avec label sans nom        → socle_status_label_sans_nom
│       ├── Avec label 72px + icône    → socle_status_label_72
│       ├── XL avec label (80px)       → socle_status_label_xl
│       ├── State aligné bas-centre    → socle_status_state_bottom_72
│       └── Standard 72px             → socle_status_72
│
├── Structure visuelle
│   ├── Titre de section               → socle_header_base
│   └── Badge 42×42 en-tête           → socle_badge_42
```

---

## 2. Tableau comparatif par famille

### Action

| Socle | Confirmation | Fond | Label | Name weight |
|-------|-------------|------|-------|-------------|
| `socle_action_simple` | non | gris | non | 500 (hérité) |
| `socle_action_simple_sans_couleur` | non | aucun | non | 500 (hérité) |
| `socle_action_critical` | non | gris | non | **600** |
| `socle_action_label_compact` | non | hérité | oui (14px) | 500 (hérité) |
| `socle_action_script_confirme` | oui | on/off | non | 500 (hérité) |

**Critères discriminants**
- Fond présent ou non → `simple` vs `sans_couleur`
- Criticité visuelle → `critical` (name 600)
- Feedback textuel ligne 2 → `label_compact`
- Confirmation obligatoire → `script_confirme`

---

### KPI

| Socle | Couleur auto | Icône | Label | Height |
|-------|-------------|-------|-------|--------|
| `socle_kpi` | oui (entité couleur) | oui | non | 72px |
| `socle_kpi_label` | oui (hérité) | oui | oui | 72px |
| `socle_kpi_72` | non | oui | non | 72px |
| `socle_kpi_72_sans_icone` | non | non | non | 72px |
| `socle_kpi_label_72` | non | oui | oui | 72px |
| `socle_kpi_label_72_sans_icone` | non | non | oui | 72px |

**Critères discriminants**
- Entité `sensor.couleur_*` disponible → `socle_kpi` / `socle_kpi_label`
- Pas d'entité couleur → variantes `_72`
- Icône utile ou non → `_sans_icone`

---

### Status

| Socle | Height | Icône | Name | State | Label | Interactif |
|-------|--------|-------|------|-------|-------|------------|
| `socle_status` | 72px | oui | oui | oui | non | oui |
| `socle_status_72` | 72px | oui | oui | oui | non | non |
| `socle_status_compact` | 64px | non | oui | oui | non | non |
| `socle_status_label` | 72px | non | oui | oui (15/600) | oui | non |
| `socle_status_label_72` | 72px | oui | oui | non | oui | non |
| `socle_status_label_sans_nom` | 72px | oui | non | oui (15/600) | oui | non |
| `socle_status_label_xl` | 80px | oui | non | oui (15/600) | oui | non |
| `socle_status_state_bottom_72` | 72px | oui | oui | oui (bas) | non | non |

**Critères discriminants**
- Interactivité → `socle_status` ou `_xl_interactif`
- Format synthèse XL → `_xl`
- State en bas-centre → `_state_bottom_72`
- Label comme info principale (state masqué) → `_label_72`
- Sans nom → `_label_sans_nom`

---

### Diagnostic

| Socle | Height | State typo | Interactif |
|-------|--------|-----------|------------|
| `socle_diagnostic` | 88px | 14px / 400 | non |
| `socle_diagnostic_compact` | 72px | 16px / 700 | tap more-info hérité (surchargeable) |
| `socle_diagnostic_compact_readonly_72` | 72px | 16px / 700 | non (verrouillé) |

**Critères discriminants**
- Format XL → `socle_diagnostic`
- Emphase valeur capteur, interaction possible → `_compact`
- Anti-accident strict → `_readonly_72`

---

### Toggle

| Socle | Height | Confirmation | State visible |
|-------|--------|-------------|--------------|
| `socle_toggle` | 72px | non | oui |
| `socle_toggle_compact_68` | 68px | non | non |
| `socle_toggle_confirme` | 72px | oui | non |

**Critères discriminants**
- Confirmation obligatoire → `_confirme`
- Format compact options (68px) avec gestion indisponibilité native → `_compact_68`
- Standard → `socle_toggle`

---

### État

| Socle | Interactif | Composition | Usage |
|-------|------------|-------------|-------|
| `socle_etat_reel` | oui (more-info) | non | État réel équipement |
| `socle_etat_lecture_principale` | — | oui (typo seule) | Normalisation typo état/label |
| `socle_etat_action_secondaire` | oui (hérité) | oui | État + action secondaire |

**Critère discriminant** : `socle_etat_lecture_principale` n'est jamais instancié
seul — composition via `template:` multiple uniquement.

---

## 3. Variantes proches — avertissements

### `socle_action_simple` vs `socle_action_critical`
Visuellement identiques (fond gris, même géométrie).
Seule différence : `name` en 600 pour `_critical`.
Réserver `_critical` aux actions à conséquence importante.

### `socle_status` vs `socle_status_72`
Même affichage (icon + name + state, 72px).
Seule différence : `socle_status` autorise `more-info` au tap.
Carte non interactive → `socle_status_72`.

### `socle_status_label` vs `socle_status_label_sans_nom`
Même typographie (state 15/600, label 12/400).
`_label` : avec name, sans icône.
`_sans_nom` : sans name, avec icône.

### `socle_kpi` vs `socle_kpi_72`
`socle_kpi` : couleur de fond pilotée par entité `sensor.couleur_*` (JS).
`socle_kpi_72` : aucune logique couleur — fond géré par la carte métier.
Ne pas utiliser `socle_kpi` si aucune entité couleur n'existe.

### `socle_diagnostic_compact` vs `socle_diagnostic_compact_readonly_72`
Identiques visuellement.
`_compact` : tap `more-info` hérité — la carte métier peut surcharger.
`_readonly_72` : toutes actions verrouillées — anti-accident strict.
Ne pas dériver de `_readonly_72` pour une carte interactive.

### `socle_kpi_label_72` vs `socle_status_label`
Même structure apparente (name + state + label).
`socle_kpi_label_72` : state 18/700 — valeur mesurée en avant.
`socle_status_label` : state 15/600, sans icône — statut décisionnel.

---

## 4. Socles autonomes (hors carte_base_v2)

| Socle | Raison |
|-------|--------|
| `socle_badge_42` | Géométrie carrée 42×42 — incompatible avec carte_base_v2 |
| `socle_header_base` | Structure visuelle pure — fond et ombre supprimés |
| `socle_etat_lecture_principale` | Brique typo pure — composition uniquement |