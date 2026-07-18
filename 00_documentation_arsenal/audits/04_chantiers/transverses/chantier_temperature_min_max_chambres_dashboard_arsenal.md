# Chantier TRANSVERSE (C27) — Agrégats de température MIN/MAX des chambres et leur restitution sur le dashboard Arsenal

| Champ | Valeur |
|---|---|
| **Chantier** | Arbitrage et contractualisation des agrégats de température MIN/MAX des chambres et de leur restitution sur le dashboard Arsenal. |
| **Domaine** | TRANSVERSE (Chauffage ↔ Climatisation ↔ production Météo/température intérieure ↔ UI Lovelace). |
| **Statut** | **ouvert — Lot 2A contractualisé ; contrat de restitution requis (Lot 2B).** |
| **Priorité** | **P2** (proposée) — voir justification §Priorité. |
| **Ouvert le** | 2026-07-18. |
| **Preuve de départ** | [`01_rapports/transverses/audit_cartes_temperature_min_max_dashboard_arsenal.md`](../../01_rapports/transverses/audit_cartes_temperature_min_max_dashboard_arsenal.md) (mergé par la PR #410). |
| **Prochain jalon** | **Lot 2B — contrat de sémantique et restitution des bornes thermiques des chambres de l'étage**. |

> **⚠️ Portée de l'ouverture.** L'ouverture de C27 **ne vaut ni arbitrage rendu, ni décision de
> contractualiser, ni décision de corriger.** Ce document est une **ouverture documentaire de
> gouvernance** : il enregistre l'objet, l'état réel, les antécédents et les questions ouvertes, et
> fixe le prochain jalon (arbitrage propriétaire consolidé). **Aucune décision, aucun contrat, aucun
> runtime, aucun dashboard, aucun template, aucun checker n'est créé par ce chantier au Lot 0.** Le
> présent dossier est **descriptif et non normatif**.

---

## Priorité (justification)

**P2 proposée.** L'objet a des **conséquences diagnostiques démontrées** (restitution potentiellement
trompeuse sur le **dashboard principal** Arsenal) et concerne des **agrégats sans autorité** consommés
par plusieurs domaines (Chauffage, Climatisation, Aération). Il ne présente toutefois **aucun défaut
fonctionnel ou de sûreté démontré** : le classement reste donc en dessous de P0/P1. La priorité
définitive relève de l'arbitrage propriétaire (Lot 1).

---

## 1. Objet

Gouverner, par **arbitrage** puis **contractualisation**, un objet transversal aujourd'hui **sans
autorité normative directe** : les agrégats `sensor.temperature_min_chambres` /
`sensor.temperature_max_chambres` et leur **restitution** par les deux cartes du dashboard Arsenal
(« Température minimale » / « Température maximale »). Le chantier vise à **définir la vérité
gouvernante** (production, sémantique, restitution) **avant** toute correction.

Trois couches sont à gouverner, à ne pas confondre :

1. **Production** des agrégats.
2. **Sémantique transversale** (ce que représentent MIN et MAX, articulation Chauffage/Climatisation).
3. **Restitution UI** (ce que traduit la couleur de chaque carte).

---

## 2. Preuve de départ, antécédents et travail propre à C27

**Preuve de départ (constat factuel opposable au démarrage) :**
- [`01_rapports/transverses/audit_cartes_temperature_min_max_dashboard_arsenal.md`](../../01_rapports/transverses/audit_cartes_temperature_min_max_dashboard_arsenal.md) — audit transversal statique, lecture seule, **non normatif**, mergé par la PR #410.

**Antécédents documentaires (descriptifs, non normatifs, non opposables comme décisions) :**
- [`02_arbitrages/temperature_interieure/arbitrage_temperature_interieure_agregats.md`](../../02_arbitrages/temperature_interieure/arbitrage_temperature_interieure_agregats.md) — note d'arbitrage **existante** sur les agrégats. Elle constituera la **base canonique du Lot 1** : elle y sera réexaminée puis **remplacée par une version consolidée** (intégrant B1–B6, C-prod-1…6, les constats #410, et la distinction production / sémantique / restitution). L'historique reste porté par Git ; **aucun avenant empilé ni document parallèle** ne sera créé.
- [`03_plans_action/temperature_interieure/plan_action_temperature_interieure_agregats.md`](../../03_plans_action/temperature_interieure/plan_action_temperature_interieure_agregats.md) — plan d'action **existant**, cité ici comme **antécédent descriptif non normatif**. Il **n'est pas** un plan automatiquement retenu par C27 et **n'est pas** présenté comme opposable. Son éventuel remplacement, reclassement ou retrait de l'état courant sera **décidé seulement après l'arbitrage du Lot 1**.

**Travail propre à C27 (à produire au fil des lots) :**
- décision propriétaire **consolidée** (Lot 1) ;
- **contractualisation** (Lot 2) ;
- **éventuelle évolution de production** (Lot 3) ;
- **éventuelle correction UI** (Lot 4) ;
- validation statique puis terrain (Lots 5–6) ;
- clôture documentaire (Lot 7).

---

## 3. État réel synthétique (issu du rapport #410)

- **Rendu fidèle à la source** : les cartes projettent fidèlement l'état des agrégats ; le calcul MIN/MAX est correct dès qu'au moins une façade de chambre est vivante.
- **Fraîcheur de la source non garantie** : les agrégats republient `this.state` sans borne temporelle (ni TTL, ni `time_pattern`) ; en régime établi, l'indisponibilité totale peut rester masquée par une ancienne valeur numérique.
- **Périmètre réel** : 3 chambres (Arnaud, Matthieu, Parents) ; le RDC (`sensor.temperature_max_rdc`) est un agrégat séparé ; `petite_maison` est exclue.
- **Couleur sans sémantique unifiée** : combinaison locale (franchissement clim basé sur MAX + seuil chauffage recalculé + résiduel) ; pas de réalité unique, claire et documentée.
- **Cas cross-entity** : sur la carte MIN, la couleur RED est pilotée par un franchissement basé sur `temperature_max_chambres` (**ambiguïté sémantique forte, conséquence diagnostique** ; pas une non-conformité métier).
- **Aucune autorité normative directe** ne gouverne ces agrégats ni ces cartes.

Bilans du rapport #410 (pour mémoire, non ré-ouverts ici) : `OBJ` 1 CONFORME / 1 PARTIEL / 4 NON CONFORME / 2 INDÉTERMINABLE ; familles **A=2 écarts UI · B=6 ambiguïtés sémantiques · C=3 limites de production · D=5 dettes documentaires**.

---

## 4. Périmètre

1. **Production des agrégats** : périmètre des chambres, calcul MIN/MAX, comportement en indisponibilité, mémoire et fraîcheur, abstention, observabilité éventuelle.
2. **Sémantique transversale** : ce que représentent MIN et MAX ; articulation Chauffage / Climatisation ; distinction température physique / franchissement / besoin / autorisation / décision / action ; traitement du modèle cross-entity ; place éventuelle du HEAT d'appoint.
3. **Restitution UI** : réalité unique traduite par chaque carte ; régime de palette ; neutre ; indisponibilité ; signal éventuel de mémoire/fraîcheur ; suppression éventuelle de complexité locale après contractualisation.

---

## 5. Hors périmètre

- Fonctionnement métier général du Chauffage et de la Climatisation.
- Verdicts `CH-DIAG-*` / `CLIM-DIAG-*` (non importés, non modifiés).
- `sensor.temperature_max_rdc`, zones hors chambres, chaîne extérieure / jardin.
- Réconciliation de plausibilité 8–40 / 5–45 (dette documentaire) : signalée, traitée seulement si l'arbitrage la rattache explicitement.
- Toute correction (production, UI, contrat) tant que l'arbitrage et le(s) contrat(s) ne sont pas validés.

---

## 6. Risques

- **Vérité concurrente** : la note d'arbitrage et le plan d'action `temperature_interieure` existent déjà ; C27 doit les **réconcilier/absorber** (arbitrage) ou **référencer** (plan), sans créer de doctrine parallèle.
- **Changement métier involontaire** : toute décision sur l'abstention des agrégats modifie potentiellement Chauffage/Climatisation/Aération (consommateurs). À traiter par domaine.
- **Correction prématurée** : corriger la couleur avant l'arbitrage figerait une sémantique non décidée.
- **Masquage de production** : une correction UI de l'indisponibilité serait inopérante tant que la production masque l'état.
- **Extension de périmètre** : la tentation d'élargir (RDC, plausibilité) doit rester bornée.

---

## 7. Dépendances (ordre imposé)

1. Arbitrage validé **avant** tout contrat.
2. Contrat validé **avant** toute évolution de production.
3. Aucune correction UI de fond **avant** arbitrage + contrat.
4. Correction de l'indisponibilité : **UI seule insuffisante** tant que la production masque l'état → dépend d'une décision de production.
5. **Mutualisation seulement si démontrée utile après contractualisation.**
6. Réconciliation préalable avec la note d'arbitrage et le plan d'action existants.

---

## 8. Questions ouvertes

> Aucune n'est tranchée au Lot 0. Elles seront instruites au Lot 1 à partir de l'audit #410 et de la note d'arbitrage existante.

### Sémantique / restitution (B1–B6)

- **B1** — Quelle couche gouverne la couleur de chaque carte (physique / franchissement / besoin / admissibilité / décision / autorisation / combinaison documentée) ? Peut différer entre MIN et MAX.
- **B2** — Régime de palette : palette sémantique ou Exception thermique (le mélange étant interdit hors exception documentée) ? Dépend de B1.
- **B3** — Que signifie exactement l'état résiduel actuellement vert (nominal / à supprimer / neutre) ?
- **B4** — Une carte MIN peut-elle légitimement refléter une situation déterminée par MAX (modèle cross-entity à légitimer, restreindre ou documenter comme mixte) ?
- **B5** — Le HEAT d'appoint Climatisation doit-il intervenir dans cette restitution, et distinctement du chauffage principal ?
- **B6** — Quelle classification locale reste admissible une fois la vérité gouvernante définie (couleur externalisée / classification locale bornée / observation directe) ?

### Production (C-prod-1…6)

- **C-prod-1** — Durée ou absence de mémoire (TTL fixe / fraîcheur événementielle / abstention immédiate).
- **C-prod-2** — Règle d'abstention (jamais / après TTL / immédiat) et propagation aux consommateurs.
- **C-prod-3** — Périmètre exact des « chambres » (conserver / élargir / formaliser tel quel).
- **C-prod-4** — Définition et forme de la fraîcheur (entité compagnon de statut / attributs d'âge / aucune).
- **C-prod-5** — Comportement lorsque certaines chambres seulement sont disponibles (règle de dégradation partielle).
- **C-prod-6** — Statut à exposer aux consommateurs et à l'UI (entité compagnon / attributs / rien).

---

## 9. Lots

| Lot | Objet | Nature | Dépend de |
|---|---|---|---|
| **L0** | Ouverture documentaire du chantier (ce dossier + registre + index) | descriptif | — |
| **L1** | Arbitrage B1–B6 + C-prod, **consolidé** dans la note d'arbitrage existante | descriptif (décisions) | L0 |
| **L2** | Contrat(s) transversal(aux) — nombre, périmètre et emplacement **à arbitrer au Lot 1** | normatif | L1 |
| **L3** | **Éventuelle évolution de production** (mémoire / abstention / fraîcheur / statut / périmètre) | runtime | L2 |
| **L4** | **Éventuelle correction UI** (mapping couleur, neutre / indisponibilité, mémoire, complexité) | UI | L2 (+ L3 si l'indisponibilité en dépend) |
| **L5** | Validation statique (checkers UI / couleurs, rendu) | contrôle | L3 / L4 |
| **L6** | Validation terrain (indisponibilité réelle, gel, rendu) | preuve | L5 |
| **L7** | Clôture documentaire | descriptif | L6 |

---

## 10. Barrières entre lots

- Aucune PR ne mélange **ouverture / arbitrage / contrat / runtime / UI / clôture**.
- **L2** exclu sans **L1** validé.
- **L3** exclu sans **L2** validé.
- **L4** de fond exclu sans **L1 + L2** validés.
- Correction UI de l'indisponibilité **insuffisante** sans décision de production (masquage `this.state`).
- **Mutualisation** des templates MIN/MAX **seulement** sous preuve de nécessité post-L2.

---

## 11. Critères de clôture (bornés)

- **Arbitrage** B1–B6 + C-prod **rendu et validé** (L1), réconciliant les antécédents (pas de vérité concurrente).
- **Contrat(s)** transversal(aux) **écrit(s) et opposable(s)** (L2).
- **Politique de mémoire, d'abstention et de fraîcheur arbitrée puis contractualisée.**
- **Restitution conforme à la sémantique et au régime de palette décidés.**
- **Indisponibilité `rgba(158,158,158,0.1)` distincte du neutre `rgba(158,158,158,0.2)`** (règle déjà opposable).
- **Éventuelle évolution de production** livrée et conforme au contrat, **si décidée**.
- **Éventuelle correction UI** conforme au contrat, **si décidée**.
- **Mutualisation seulement si démontrée utile après contractualisation.**
- **Validation statique** verte et **validation terrain** de l'indisponibilité / du gel.
- **Clôture documentaire** ; registre et index à jour.

---

## 12. Suivi des lots

### Lot 1 — arbitrage propriétaire consolidé (terminé)

Arbitrage rendu et consigné dans la note d'arbitrage, **autorité descriptive de la décision
propriétaire** :
[`02_arbitrages/temperature_interieure/arbitrage_temperature_interieure_agregats.md`](../../02_arbitrages/temperature_interieure/arbitrage_temperature_interieure_agregats.md).

Décisions acquises (résumé, sans recopier la note) :
- **Vision A** — lecture physique thermique ; chaque carte qualifie sa propre grandeur (MIN
  froid/neutre/indisponible ; MAX chaud/neutre/indisponible) ; ni besoin, ni décision, ni cross-entity.
- **Restitution** — Exception 2 thermique ; **catégorie thermique portée par le backend**, mapping
  couleur appliqué par l'UI (**pas de RGBA métier backend**) ; neutre gris `0.2`, indisponibilité
  `0.1` ; HEAT d'appoint hors restitution.
- **Production** — **agrégats sans mémoire propre** ; abstention lorsque toutes les façades se sont
  déjà abstenues ; fraîcheur héritée des façades ; périmètre = 3 chambres ; couverture partielle
  observable ; pas d'entité compagnon d'emblée.
- **Contractualisation** — **deux contrats** distincts (production/agrégation + sémantique/restitution).

Précisions encore ouvertes (reportées au Lot 2, non décidées) :
- références physiques inférieure/supérieure ;
- forme exacte des catégories thermiques backend ;
- forme Home Assistant de l'indisponibilité de l'agrégat ;
- attributs de couverture ;
- noms et emplacements canoniques des deux contrats.

### Lot 2A — contrat de production (terminé)

Contrat normatif de production consigné :
[`../../contrats/meteo/temperature_interieure/bornes_thermiques_chambres_etage.md`](../../../contrats/meteo/temperature_interieure/bornes_thermiques_chambres_etage.md).
Gouverne `sensor.temperature_min_chambres` / `sensor.temperature_max_chambres` comme bornes MIN/MAX
des **trois chambres de l'étage** uniquement : périmètre souverain (3 façades), calcul sur façades
exploitables, validité dès une façade, **aucune mémoire/TTL propre**, **abstention à zéro façade
exploitable**, couverture observable, 12 invariants `INV-BTE-*`. **Exclut** RDC, petite maison,
catégories thermiques, couleurs et logique HVAC (renvoyés au Lot 2B et aux domaines concernés).

### Lot 2B — contrat de sémantique et restitution (prochain jalon)

Rédaction et validation du contrat de restitution : catégories `froid` / `neutre` / `chaud`,
références physiques **dédiées** (basse/haute, stables, non contextuelles), catégorie portée par le
backend, mapping UI vers l'Exception 2, neutre `0.2` / indisponibilité `0.1`. **Dépend du Lot 2A
mergé.** **Aucun runtime, UI, checker ou CI n'est décidé ou engagé à ce stade. C27 reste actif et
non clos.**
