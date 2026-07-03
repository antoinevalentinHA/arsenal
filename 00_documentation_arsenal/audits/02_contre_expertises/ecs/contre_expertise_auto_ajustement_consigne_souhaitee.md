# Contre-expertise — ECS / Auto-ajustement de la consigne souhaitée

> **Statut :** contre-expertise adversariale de l'étude d'opportunité — idée d'**auto-ajustement de la consigne ECS souhaitée** jugée **prématurée et partiellement en rupture** avec l'architecture existante ; **écartée en l'état**. Une observabilité « conseil seulement » reste la seule déclinaison compatible, mais **non prioritaire** faute de problème observé.
> **Domaine :** `ecs` — consigne thermique, apprentissage, séparation observabilité / décision / action.
> **Destination d'archivage :** `00_documentation_arsenal/audits/02_contre_expertises/ecs/contre_expertise_auto_ajustement_consigne_souhaitee.md`
> **Documents de référence (en dépôt) :**
> - [`01_rapports/ecs/audit_auto_ajustement_consigne_souhaitee.md`](../../01_rapports/ecs/audit_auto_ajustement_consigne_souhaitee.md) — étude d'opportunité réexaminée ici.
> - `00_documentation_arsenal/contrats/ecs/11_ajustement_des_offsets.md` (§2.2, §6.1, §11).
> - `00_documentation_arsenal/contrats/ecs/reference_thermique_post_inertie_ecs.md` (§9.1).
> - `00_documentation_arsenal/contrats/ecs/09_invariants_et_interdictions.md`.
> - `recorder.yaml` (allowlist ECS + températures/contexte).
> **État du dépôt à la rédaction :** `origin/main` = `f291e67`.
> **Posture :** infirmer autant que confirmer ; laisser le dépôt trancher. Ce document ne cherche pas à valider l'idée.
> **Principe directeur :** *le runtime est la référence, le contrat documente le runtime.*

---

## 1. Objet

Réexaminer, en posture adversariale, la conclusion permissive de l'audit d'opportunité (« pertinent, en observabilité/conseil »). Déterminer, à partir du seul état réel du dépôt, si l'idée d'auto-ajustement de la consigne **souhaitée** est fondée, ou si elle doit être écartée. Acte documentaire — aucune modification runtime, contrat, CI ou UI.

---

## 2. Idée réexaminée (rappel)

Faire baisser automatiquement la consigne ECS **souhaitée** quand les usages laissent une marge d'eau chaude (forte chaleur / moindre besoin), sous garde de désinfection. L'audit conclut à une pertinence en couche observabilité/recommandation. La présente contre-expertise conteste cette pertinence même.

---

## 3. Hypothèses infirmées

Trois prémisses implicites de l'idée sont **contredites par le dépôt** :

- **H1 — « il y a un gaspillage / une consigne trop haute à corriger ».** Le dépôt ne contient **aucune** mesure ni série révélant un tel problème. L'idée répond à un problème **hypothétique que le système ne sait pas voir**.
- **H2 — « ajuster la souhaitée est dans la continuité de l'apprentissage existant ».** Faux : l'apprentissage est **délibérément confiné aux offsets** ; il ne touche jamais la cible. Ajuster la souhaitée **franchit** cette frontière.
- **H3 — « baisser la consigne va dans le sens du réglage du domaine ».** Faux : le domaine est **assumé côté disponibilité** d'eau chaude ; l'idée pousse à contre-sens.

---

## 4. Preuves (dépôt `f291e67`)

| # | Source | Fait |
|---|--------|------|
| P1 | `contrats/ecs/11_ajustement_des_offsets.md` §2.2 | Frontière explicite : « **Ne modifie aucune consigne chaudière … Ne corrige que des `input_number.ecs_off_*`** ». L'automatisme est confiné au moyen (offset), jamais à la cible souhaitée. |
| P2 | `contrats/ecs/11_…md` §6.1 (`ECS-OFF-4`) | Asymétrie de zone morte `[−0.3 ; +0.5]` : « l'équilibre appris **penche volontairement vers un léger dépassement, jugé préférable à une sous-atteinte pour la disponibilité d'eau chaude**. Caractéristique **assumée** ». Le domaine est réglé **côté disponibilité**, pas économie. |
| P3 | `contrats/ecs/reference_thermique_post_inertie_ecs.md` §9.1 | Le système **ne distingue pas** une montée d'inertie d'une remontée liée à un **tirage d'eau**. La brique d'observation du besoin réel **n'existe pas**. |
| P4 | `14_mqtt_sensors/boiler/`, `12_template_sensors/ecs/` (grep) | **Aucun** capteur d'énergie / débit / puisage / volume ECS ; **une seule** sonde ballon. La marge résiduelle n'est pas mesurable, seulement inférable. |
| P5 | `recorder.yaml` (allowlist) | `input_number.ecs_consigne_temperature` (consigne souhaitée) **non historisé** ; fenêtres d'usage **non historisées** ; **aucun** `statistics`/`history_stats` ECS. Corrélation consigne↔marge seulement indirecte. |
| P6 | `contrats/ecs/09_invariants_et_interdictions.md` | Désinfection = invariant absolu (écrivain souverain, idempotence, plancher sanitaire) ; nominal hors cycle = 10 °C. Toute baisse devrait l'exclure formellement. |

**Conclusion de chaîne :** l'idée (a) n'a **aucun problème observable** à résoudre (H1 infirmée par l'absence de signal), (b) **franchit la frontière offset-only** (P1) et (c) **contredit l'intention « disponibilité »** (P2), sur un socle de données **incapable de la fonder** (P3-P5).

---

## 5. Analyse critique (questions de gouvernance)

- **Problème objectivement observable ?** **Non** (P3-P5 : rien ne le mesure).
- **Les données permettent-elles de raisonner ?** **Faiblement** — proxy confondu (pertes de stand-by dépendant de l'ambiance du local ballon, douches non mesurées, consigne non historisée).
- **Conclusions robustes ?** **Non** — apprentissage sur proxy non fiable ; la doctrine impose l'abstention en donnée incertaine.
- **Gains significatifs ou marginaux ?** **Marginaux et non mesurables** (P4 : pas d'énergie ; physiquement, quelques °C pèsent peu face aux pertes de stand-by).
- **Risques > bénéfices ?** **Oui** — confort, sanitaire (légionellose/désinfection), faux positifs canicule, sonde unique, face à un bénéfice hypothétique.
- **Évolution naturelle ou complexité injustifiée ?** **Complexité injustifiée** + **tension architecturale** (P1-P2).
- **Respecte les principes ?** **Partiellement en rupture** (P1 frontière offset-only ; P2 parti pris disponibilité).

---

## 6. Arguments favorables (steelman honnête)

- Arsenal possède le bon **patron méthodologique** (observabilité-d'abord + apprentissage discret) : une couche d'observation serait *idiomatique*.
- `ecs_temperature_ballon_securisee` est **fiable et historisé** → un indicateur de marge est *techniquement dérivable*.
- L'idée s'inscrit dans un **ethos de sobriété** cohérent avec le système.

*Portée réelle :* ces arguments soutiennent, **au mieux**, une petite sonde d'observabilité en conseil — jamais l'auto-action sur la cible.

## 7. Arguments défavorables (dominants)

1. **Aucun problème observable** — solution en quête de problème.
2. **Rupture avec la frontière offset-only** (P1).
3. **Contre-sens de l'intention « disponibilité »** (P2, caractéristique assumée).
4. **Mesure impossible** (P3-P4) → base d'apprentissage confondue.
5. **Gain marginal et non prouvable** (P4).
6. **Risques élevés** (confort, sanitaire, faux positifs) sur un domaine sensible.
7. **Coût de gouvernance disproportionné** (2ᵉ boucle couplée → oscillation ; seuil sanitaire à nommer ; contrat + CI + observabilité + recorder).

## 8. Questions restant ouvertes

- Existe-t-il, côté usage réel, un **constat** (eau trop chaude, factures) motivant l'idée ? Le dépôt seul n'en montre aucun.
- La sonde ballon unique suffit-elle à un proxy **exploitable** (stratification, position) ? Non tranché.
- La consigne souhaitée est-elle vécue comme un **réglage rare et intentionnel** de l'opérateur ? Si oui, l'auto-baisser heurterait cette intention.

## 9. Informations manquantes (bloquantes)

- **Mesure du besoin** (tirage / volume / débit) — absente.
- **Énergie ECS** (kWh, temps de flamme) — absente → gain indémontrable.
- **Historisation** de la consigne souhaitée et des fenêtres d'usage — absente.
- **Seuil sanitaire minimal nommé** — absent du corpus.
- **Distinction inertie / tirage** — absente (P3).

---

## 10. Conclusion

> **🔴 Idée prématurée et partiellement en rupture — à écarter sous sa forme « auto-ajustement de la consigne souhaitée ».**
>
> Le dépôt ne fait apparaître **aucun problème observable**, **aucune donnée** permettant un raisonnement robuste, et **aucun moyen de prouver un gain** — qui serait de toute façon marginal. Surtout, l'idée **franchit deux frontières délibérées** de l'architecture ECS : automatisme **confiné aux offsets** (`11` §2.2) et réglage **assumé côté disponibilité** (`11` §6.1). Rapport risque/bénéfice **nettement défavorable** sur un domaine à fort enjeu confort/sanitaire.
>
> **Recommandation :** ne pas ouvrir de chantier d'auto-ajustement. **Tout au plus**, si un besoin se manifestait un jour côté usage réel, une **observabilité de marge en « conseil seulement »** (read-only, sans jamais écrire la consigne) serait la seule déclinaison compatible — mais **non prioritaire ni justifiée aujourd'hui** faute de problème observé. Cette contre-expertise **tempère** la conclusion permissive de l'[audit d'opportunité](../../01_rapports/ecs/audit_auto_ajustement_consigne_souhaitee.md) associé.

---

*Contre-expertise adversariale — lecture seule. Aucune modification du dépôt, aucun code, aucun plan d'implémentation. Aucun chantier ouvert.*
