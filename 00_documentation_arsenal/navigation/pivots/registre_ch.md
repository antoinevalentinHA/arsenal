# 🔖 Pivot — Registre des identifiants « CH-x »

> **NAVIGATION — NON NORMATIF.** Ce pivot **agrège et explique** ; il ne définit ni ne corrige rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Objet

« CH-x » **n'est pas un identifiant global** : il est **relatif au domaine**. Plusieurs séries indépendantes emploient la notation « CH-n » et se télescopent par numéro. Ce pivot **désambiguïse**. Le **détail** de chaque chantier reste dans le **hub** du domaine (ce registre ne le recopie pas).

## Séries recensées

| Série | Domaine | Forme | Hébergement | Nature | Numéros | Hub |
|---|---|---|---|---|---|---|
| **Chauffage-CI** | Chauffage | `CH-n` (nu) | [`changelog/chantiers/climatisation/`](../../changelog/chantiers/climatisation/) | gouvernance CI | CH1–CH6 | [`chauffage`](../domaines/chauffage.md) |
| **Alarme** | Alarme | `CH-n` (nu) | `audits/**` (alarme) | chantiers d'audit | CH1, CH2, CH4, CH6 | [`alarme`](../domaines/alarme.md) |
| **Lovelace/CI** | Transverse (Lovelace/CI) | `CH-LL-CI-n` (**qualifié**) | [`CHANGELOG_CH-LL-CI-1.md`](../../changelog/chantiers/transverses/CHANGELOG_CH-LL-CI-1.md) | CI transverse | CH-LL-CI-1 | `ui_lovelace` (hub à venir) |

## Collision par numéro (séries à préfixe nu)

| N° | Chauffage-CI | Alarme |
|:--:|:--:|:--:|
| CH-1 | ✓ | ✓ |
| CH-2 | ✓ | ✓ |
| CH-3 | ✓ | — |
| CH-4 | ✓ | ✓ |
| CH-5 | ✓ | — |
| CH-6 | ✓ | ✓ |

Sur **CH-1/2/4/6**, le même token désigne **deux chantiers sans rapport** (familles et natures différentes). Le contenu de chacun est dans le hub correspondant — non recopié ici.

## Lever l'ambiguïté

En contexte, **toujours qualifier le domaine** : « CH-1 Alarme » vs « CH-1 Chauffage-CI ». Le préfixe qualifié `CH-LL-CI-n` (Lovelace) est la seule forme **nativement sans collision** — constat, non consigne.

## Ne pas confondre

- `CH-x` (Chauffage-CI) ≠ **« lot L-x »** (lots d'audit du chauffage, ex. `L1` / `validation_L1`).
- `CH-x` (Alarme) ≠ **« IMP-x »** (constats d'importance de l'audit alarme).

## Points de vigilance (non normatif)

- **Chauffage-CI** est physiquement sous `climatisation/` alors que son domaine est **Chauffage** : signalé, **non corrigé**. Si re-classé un jour, mettre à jour l'hébergement ci-dessus.
- **Collision de numéros** entre deux familles (`changelog` vs `audits`) et deux natures (CI vs audit).
- **Lovelace** évite la collision par préfixe qualifié : simple constat.

---

*Pivot non normatif. Agrège et explique la notation « CH-x » ; délègue le contenu aux hubs ; ne corrige aucune famille.*
