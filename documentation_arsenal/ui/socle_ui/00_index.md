# 🗂️ SOCLE UI — Index

## Objet

Inventaire factuel de l'arborescence réelle des templates button-card Arsenal.
Référence structurelle : fichiers, socles, héritages.

---

## Arborescence des fichiers
```text
/homeassistant/button_card_templates/socle/
├── 01_carte_base.md       → carte_base_v2
├── 02_action.md           → 5 socles
├── 03_decision.md         → 1 socle
├── 04_etat.md             → 3 socles
├── 05_info.md             → 1 socle
├── 06_kpi.md              → 6 socles
├── 07_status.md           → 9 socles
├── 08_toggle.md           → 3 socles
├── 09_diagnostic.md       → 3 socles
├── 10_badge.md            → 1 socle
└── 11_header.md           → 1 socle
```

**Total : 34 socles**

---

## Inventaire par famille

### Base (01)
| Socle | Héritage |
|-------|----------|
| `carte_base_v2` | — |

### Action (02)
| Socle | Héritage |
|-------|----------|
| `socle_action_simple` | `carte_base_v2` |
| `socle_action_simple_sans_couleur` | `carte_base_v2` |
| `socle_action_critical` | `carte_base_v2` |
| `socle_action_label_compact` | `carte_base_v2` |
| `socle_action_script_confirme` | `carte_base_v2` |

### Decision (03)
| Socle | Héritage |
|-------|----------|
| `socle_decision_72` | `carte_base_v2` |

### État (04)
| Socle | Héritage |
|-------|----------|
| `socle_etat_reel` | `carte_base_v2` |
| `socle_etat_lecture_principale` | — |
| `socle_etat_action_secondaire` | `carte_base_v2` + `socle_etat_lecture_principale` |

### Info (05)
| Socle | Héritage |
|-------|----------|
| `socle_info_72` | `carte_base_v2` |

### KPI (06)
| Socle | Héritage |
|-------|----------|
| `socle_kpi` | `carte_base_v2` |
| `socle_kpi_label` | `socle_kpi` |
| `socle_kpi_72` | `carte_base_v2` |
| `socle_kpi_72_sans_icone` | `carte_base_v2` |
| `socle_kpi_label_72` | `carte_base_v2` |
| `socle_kpi_label_72_sans_icone` | `carte_base_v2` |

### Status (07)
| Socle | Héritage |
|-------|----------|
| `socle_status` | `carte_base_v2` |
| `socle_status_72` | `carte_base_v2` |
| `socle_status_compact` | `carte_base_v2` |
| `socle_status_label` | `carte_base_v2` |
| `socle_status_label_72` | `carte_base_v2` |
| `socle_status_label_sans_nom` | `carte_base_v2` |
| `socle_status_label_xl` | `carte_base_v2` |
| `socle_status_label_xl_interactif` | `socle_status_label_xl` |
| `socle_status_state_bottom_72` | `socle_status_72` |

### Toggle (08)
| Socle | Héritage |
|-------|----------|
| `socle_toggle` | `carte_base_v2` |
| `socle_toggle_compact_68` | `carte_base_v2` |
| `socle_toggle_confirme` | `carte_base_v2` |

### Diagnostic (09)
| Socle | Héritage |
|-------|----------|
| `socle_diagnostic` | `carte_base_v2` |
| `socle_diagnostic_compact` | `carte_base_v2` |
| `socle_diagnostic_compact_readonly_72` | `socle_diagnostic_compact` |

### Badge (10)
| Socle | Héritage |
|-------|----------|
| `socle_badge_42` | — |

### Header (11)
| Socle | Héritage |
|-------|----------|
| `socle_header_base` | — |

---

## Arbres d'héritage
```text
carte_base_v2
├── socle_action_simple
├── socle_action_simple_sans_couleur
├── socle_action_critical
├── socle_action_label_compact
├── socle_action_script_confirme
├── socle_decision_72
├── socle_etat_reel
├── socle_etat_action_secondaire  ← aussi: socle_etat_lecture_principale
├── socle_info_72
├── socle_kpi
│   └── socle_kpi_label
├── socle_kpi_72
├── socle_kpi_72_sans_icone
├── socle_kpi_label_72
├── socle_kpi_label_72_sans_icone
├── socle_status
├── socle_status_72
│   └── socle_status_state_bottom_72
├── socle_status_compact
├── socle_status_label
├── socle_status_label_72
├── socle_status_label_sans_nom
├── socle_status_label_xl
│   └── socle_status_label_xl_interactif
├── socle_toggle
├── socle_toggle_compact_68
└── socle_toggle_confirme

socle_etat_lecture_principale       ← brique typo pure, pas instanciable seul
socle_diagnostic_compact
└── socle_diagnostic_compact_readonly_72

socle_badge_42                      ← géométrie autonome, pas de carte_base_v2
socle_header_base                   ← structure autonome, pas de carte_base_v2
```

---

## Socles non instanciables directement

| Socle | Raison |
|-------|--------|
| `carte_base_v2` | Socle racine — base uniquement |
| `socle_etat_lecture_principale` | Brique typographique pure — composition uniquement |