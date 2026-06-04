# 🌬️ Hub de domaine — Aération → Blocage Chauffage

> **NAVIGATION — NON NORMATIF.** Ce hub **agrège et oriente** ; il ne définit rien. En cas de divergence, le **document de famille fait foi**.
> Registre : [`carte_domaines.md`](../carte_domaines.md) · Charte : [`navigation/README.md`](../README.md)

## Orientation

Machine d'état normative (V3 PRO) gérant le cycle de vie d'un épisode d'aération (M1..M5) et le blocage chauffage associé. Timers V3 PRO : monotonicité et anti-triggers fantômes. **Périmètre strict** : la reprise thermique (redémarrage chauffage) appartient exclusivement à la `décision_centrale` chauffage — hors scope de ce domaine. Aucune architecture-famille dédiée. Audit minimal (un rapport, classé sous chauffage).

## Contrat — « ce que le système doit faire »

Entrée : [`contrats/aeration_blocage_chauffage/README.md`](../../contrats/aeration_blocage_chauffage/README.md) — machine d'état V3 PRO, 7 états (`m0_recover_normatif` → `m6_refermeture`) + `socle_transversal/`.

> 37 fichiers répartis en 7 états + socle. La liste exhaustive relèvera du futur index intra-famille.

## Audits & état

> `aeration_blocage_chauffage` étant **absent de [`audits/index.md`](../../audits/index.md)** comme domaine propre, l'état se lit dans le seul artefact d'audit disponible : [`audit_blocage_post_aeration_adaptatif.md`](../../audits/01_rapports/chauffage/audit_blocage_post_aeration_adaptatif.md) (**classé sous chauffage**).

> **Changelog** (pas de chantier dédié) : mentions diffuses `v15_8_2`, `v15_8_3`, `v15_8_4`. Mention la plus récente : [`v15_8_9.md`](../../changelog/changelogs/v15/v15_8_9.md).

## Liens croisés (sens & appartenance)

- **Chauffage** — propriétaire : [`contrats/chauffage/`](../../contrats/chauffage/) ; consomme l'état d'aération (aval). Interfaces côté chauffage : [`45_aeration.md`](../../contrats/chauffage/45_aeration.md) · [`46_aeration_observation_thermique.md`](../../contrats/chauffage/46_aeration_observation_thermique.md).
- **Climatisation** — propriétaire : [`contrats/climatisation/`](../../contrats/climatisation/) ; consomme l'état d'aération comme condition de blocage (aval).

## Points de vigilance (non normatif)

- **`aeration_recommandation` ≠ ce domaine** : `contrats/aeration_recommandation.md` et `architecture/aeration_recommandation.md` constituent une paire distincte (contrat transverse — recommandation). Ne pas confondre avec cette machine d'état de blocage.
- **Audit minimal** : seul rapport disponible, classé sous chauffage (pas sous aération). Pas de chaîne d'audit dédiée.
- **Aucun doc `architecture/`** : `architecture/aeration_recommandation.md` couvre la recommandation, pas le blocage.
- **Périmètre strict** : le redémarrage chauffage après aération est hors scope — appartient à la `décision_centrale` chauffage.

---

*Hub de navigation non normatif (gabarit v2). Pointe les documents canoniques, signale les anomalies sans les corriger.*
