# Note d'arbitrage — Agrégats de température MIN/MAX des chambres et leur restitution

> **Statut : dossier d'arbitrage — descriptif, non normatif.** Version consolidée **remplaçant**
> l'état antérieur de ce fichier (historique porté par Git ; aucun avenant empilé). Les décisions
> propriétaire ci-dessous sont **acquises** (Lot 1), **amendées par le réexamen propriétaire
> pré-Lot 2B** (2026-07-18) sur la seule restitution de l'état non-froid / non-chaud : la catégorie
> résiduelle grise « neutre » est **remplacée** par une **catégorie physique `dans_plage`**
> rendue en **vert de l'Exception 2 thermique étendue** (voir B2, B3, B6). Cette note **ne rédige aucun
> contrat**, **ne modifie aucun runtime, UI, checker ou CI**, et n'implémente rien : elle **fixe les
> frontières et les choix** de production et de restitution ; le contrat de production est
> **mergé au Lot 2A** et le contrat de restitution **reste à établir au Lot 2B**.
>
> - **Chantier :** C27 — [`04_chantiers/transverses/chantier_temperature_min_max_chambres_dashboard_arsenal.md`](../../04_chantiers/transverses/chantier_temperature_min_max_chambres_dashboard_arsenal.md)
> - **Preuve de départ :** [`01_rapports/transverses/audit_cartes_temperature_min_max_dashboard_arsenal.md`](../../01_rapports/transverses/audit_cartes_temperature_min_max_dashboard_arsenal.md) (PR #410).
> - **Antécédent descriptif non normatif :** [`03_plans_action/temperature_interieure/plan_action_temperature_interieure_agregats.md`](../../03_plans_action/temperature_interieure/plan_action_temperature_interieure_agregats.md) — **inchangé au Lot 1** (cf. §8).
> - **Portée :** production des bornes thermiques MIN/MAX des **trois chambres de l'étage** (`sensor.temperature_min_chambres`, `sensor.temperature_max_chambres`) **et** restitution de ces bornes sur les deux cartes du dashboard Arsenal. Ces bornes **ne représentent pas** toute la température intérieure.

---

## 0. Cadre et distinction des trois plans

Trois plans strictement séparés :

- **Production** (C-prod-1…6) — ce que valent et garantissent les agrégats.
- **Sémantique transversale** (B1, B3, B4, B5) — ce que représentent MIN et MAX.
- **Restitution UI** (B2, B6) — comment la couleur est produite et rendue.

Doctrine opposable mobilisée (rappel, non ré-ouverte) :
- `ui/couleurs/05_regles.md` : **une couleur = une réalité unique, claire et documentée**.
- `ui/couleurs/01_principes.md` : **le backend décide, l'UI observe et rend**.
- `ui/couleurs/02_palette.md` : gris neutre `rgba(158,158,158,0.2)` vs gris indisponibilité `rgba(158,158,158,0.1)`.
- `ui/couleurs/03_exceptions.md` (Exception 2) : palette thermique **catégorielle, non décisionnelle**.
- `ui/architecture_transverse.md` : classification locale de présentation tolérée ; interdits (recalcul de seuil de décision, reproduction de logique backend, état implicite réutilisé).
- `ui/architecture.md` : deux stratégies de couleur coexistent (externalisée / seuils locaux).

---

## 1. Faits établis (rappel #410, non ré-ouverts)

- **Rendu fidèle à la source** ; calcul MIN/MAX correct dès qu'au moins une façade est vivante.
- **Fraîcheur non garantie** : agrégats republiant `this.state` sans TTL ni `time_pattern` → indisponibilité totale **masquée** en régime établi.
- **Périmètre réel** : 3 chambres (Arnaud, Matthieu, Parents) ; RDC (`sensor.temperature_max_rdc`) séparé ; `petite_maison` exclue.
- **Couleur sans réalité unique** : combinaison locale (franchissement clim basé sur MAX + seuil chauffage recalculé + résiduel).
- **Cross-entity** : le RED de la carte MIN piloté par un franchissement basé sur `temperature_max_chambres`.
- **Bloc couleur hérité mort** : `socle_kpi` expose un mécanisme de couleur externalisée ombré par le bloc local ; `sensor.couleur_temperature_min/max_chambres` n'existent pas.
- **Façades par zone déjà gouvernées** : validation, plage `5..45`, **TTL 1800 s**, mémoire bornée, `time_pattern /5`, **abstention `unknown`**, disponibilité explicite.
- **Autorité normative — état daté :** le rapport #410 avait constaté **l'absence d'autorité normative directe** sur les agrégats et sur les cartes. **Depuis le Lot 2A (PR #413 mergée),** la **production** des bornes est gouvernée par le contrat normatif [`contrats/meteo/temperature_interieure/bornes_thermiques_chambres_etage.md`](../../../contrats/meteo/temperature_interieure/bornes_thermiques_chambres_etage.md) ; la **sémantique et la restitution** restent à contractualiser au **Lot 2B**.

---

## 2. Décision racine — Vision cible

**DÉCISION PROPRIÉTAIRE ACQUISE : Vision A — lecture physique thermique.**

Les deux cartes restent des **indicateurs de température** :
- MIN **affiche et qualifie la borne basse physique** ;
- MAX **affiche et qualifie la borne haute physique** ;
- elles ne représentent **ni besoin, ni admissibilité, ni autorisation, ni décision, ni action** ;
- elles ne constituent **pas** un diagnostic HVAC croisé ;
- chaque carte qualifie **exclusivement sa propre grandeur**.

**Vision B (diagnostic de besoin croisé) : REJETÉE pour cet objet.**

Motifs consignés :
- titres des cartes et emplacement dans la section « 🌡️ Températures » ;
- correspondance immédiate entre valeur affichée et couleur ;
- disparition du modèle cross-entity ;
- suppression du mélange Chauffage / Climatisation dans un même arbre de couleur ;
- modèle plus simple, lisible et stable ;
- aucune dépendance à l'état d'exécution des systèmes HVAC.

---

## 3. Arbitrages sémantiques (B1, B3, B4, B5)

### B1 — Couche gouvernante

**MIN — DÉCISION ACQUISE : état thermique physique de `sensor.temperature_min_chambres`.**
- `froid` lorsque la borne basse franchit **strictement** la **référence physique basse dédiée**
  (`MIN < référence physique basse`) ;
- `dans_plage` sinon (`MIN >= référence physique basse` — **égalité incluse dans `dans_plage`**) ;
- **indisponibilité native** lorsque l'agrégat est indisponible ;
- ne devient **jamais** rouge en fonction de MAX.

**MAX — DÉCISION ACQUISE : état thermique physique de `sensor.temperature_max_chambres`.**
- `chaud` lorsque la borne haute franchit **strictement** la **référence physique haute dédiée**
  (`MAX > référence physique haute`) ;
- `dans_plage` sinon (`MAX <= référence physique haute` — **égalité incluse dans `dans_plage`**) ;
- **indisponibilité native** lorsque l'agrégat est indisponible.

La couche gouvernante n'est donc **ni** le besoin COOL, **ni** son admissibilité, **ni** `clim_target_mode`, **ni** l'autorisation chauffage, **ni** un franchissement.

**Options rejetées :** franchissement seul (couche observation, INT-2) ; besoin / admissibilité / décision / autorisation (relèvent de la Vision B rejetée) ; combinaison multi-couches (OBJ-3).

**Précision reportée au Lot 2B et à l'audit runtime, sans réouvrir la Vision A :** les catégories utilisent **deux références physiques dédiées, stables et non contextuelles** : une **référence basse** pour MIN et une **référence haute** pour MAX. Elles **ne sont pas** définies par une consigne, un offset, un seuil d'autorisation, un seuil COOL contextuel, un besoin, une admissibilité, une décision ou une action HVAC. Le contrat de restitution fixe leur **rôle normatif** ; leurs **valeurs numériques**, leurs **identifiants** et leur **support runtime** restent à déterminer lors de l'**audit d'implémentation**.

### B3 — État non-froid / non-chaud

**DÉCISION (réexamen pré-Lot 2B) : catégorie physique `dans_plage`, rendue en vert de l'Exception 2 thermique étendue `rgba(76,175,80,0.2)` — remplace l'ancienne décision « neutre gris, pas de tempéré vert ».**

Le cas non-froid (MIN) / non-chaud (MAX) est une **catégorie backend explicite, factuelle et bornée** : la borne concernée **ne franchit pas strictement** sa référence physique défavorable. Sa **réalité unique** est l'**absence de franchissement défavorable sur cette borne** — rien de plus. Ce vert **n'affirme pas** un confort global, une conformité à une consigne, une nominalité système, ni l'absence de toute anomalie ; il ne qualifie que **la borne de la carte**.

Ce n'est **pas** un vert résiduel de fall-through : il correspond à une catégorie nommée `dans_plage` produite par le backend (voir B6), et non à une retombée implicite après d'autres conditions.

Réalité unique par carte :
- **MIN : `froid` / `dans_plage`** + **indisponibilité native** ;
- **MAX : `chaud` / `dans_plage`** + **indisponibilité native**.

Il n'existe donc plus, pour ces deux catégories, d'état textuel `neutre`, `indisponible` ou `non_calculable` : si l'agrégat ou sa référence physique est inexploitable, la **catégorie elle-même est indisponible** (gris indisponibilité `0.1`, prioritaire). Aucune valeur périmée n'est jamais rendue en `dans_plage`.

### B4 — Modèle cross-entity

**DÉCISION ACQUISE : chaque carte qualifie exclusivement sa propre grandeur.**
- MIN ne dépend jamais de MAX pour sa couleur ;
- MAX ne dépend jamais de MIN pour sa couleur ;
- aucun état système global n'est injecté dans ces deux cartes.

Le modèle cross-entity actuel est **abandonné**.

### B5 — HEAT d'appoint Climatisation

**DÉCISION ACQUISE : hors restitution de ces deux cartes.**
- n'intervient pas dans la couleur MIN ;
- n'est pas fusionné avec le Chauffage principal ;
- pourra faire l'objet d'une restitution **distincte** si un besoin autonome est ultérieurement démontré (hors C27).

---

## 4. Arbitrages de restitution (B2, B6)

### B2 — Régime de palette

**DÉCISION (réexamen pré-Lot 2B) : Exception 2 thermique ÉTENDUE d'une catégorie physique `dans_plage` (vert).** *(Remplace l'ancienne décision « Exception 2 sans vert ».)*

Mapping de principe :
- **MIN froid** / **MAX chaud** : franchissement strict → bleu thermique `rgba(144,202,249,0.25)` (froid) / rouge thermique `rgba(244,67,54,0.2)` (chaud) ;
- **`dans_plage`** (borne non défavorable) : **vert de l'Exception 2 étendue `rgba(76,175,80,0.2)`** ;
- **indisponibilité native** : gris indisponibilité `rgba(158,158,158,0.1)`, prioritaire.

Le vert est **une couleur de l'Exception 2 elle-même** (extension documentée, analogue au précédent de l'Exception 8 humidex), **non** un vert de la palette sémantique générale posé à côté : il n'y a donc **aucun régime hybride**. Le vert n'est disponible que **parce qu'un contrat définit explicitement** la catégorie physique `dans_plage`.

Exclus : le bleu sémantique « information » `rgba(33,150,243,0.2)` ; toute RGBA exposée comme vérité backend ; toute couleur « chauffe en cours » (les cartes n'affichent pas une action HVAC) ; tout gris neutre `0.2` intermédiaire dans la machine d'états de ces deux cartes.

### B6 — Localisation de la logique

**DÉCISION ACQUISE (principe inchangé) : le backend expose la sémantique thermique ; l'UI applique la palette.**

- **Backend** : détermine la **catégorie thermique** — MIN : `froid` / `dans_plage` ; MAX : `chaud` / `dans_plage` ; **indisponibilité native** (aucun état textuel `neutre`, `indisponible` ou `non_calculable`).
- **UI** : **mappe** la catégorie vers les couleurs de l'Exception 2 **étendue** (dont le vert `dans_plage`).
- **Socle** : restitue l'indisponibilité selon la doctrine générale (gris `0.1` prioritaire).

La couleur RGBA **n'est pas** une vérité métier backend : le backend fournit une **catégorie sémantique** consommable, pas un code couleur. La stratégie « `sensor.couleur_*` exposant directement une RGBA » **n'est pas retenue**.

Le **nom exact, la forme exacte et le nombre d'entités** portant cette catégorie seront définis au **contrat de restitution (Lot 2B) et à l'audit d'implémentation** — non fixés ici.

Conséquences attendues (à implémenter plus tard, pas au Lot 1) :
- aucune comparaison de seuil dans les cartes ;
- aucune lecture directe des helpers Chauffage par les cartes ;
- aucune lecture du franchissement COOL par les cartes ;
- suppression du JS local RED/BLUE/GREEN ;
- mapping UI **trivial et documenté** (catégorie → couleur Exception 2) ;
- **mutualisation** des deux templates **seulement si elle reste utile** après implémentation.

---

## 5. Arbitrages de production (C-prod-1…6)

> **État post-Lot 2A.** Les décisions **C-prod-1 à C-prod-6** ci-dessous ont été **contractualisées au Lot 2A** dans le contrat normatif [`bornes_thermiques_chambres_etage.md`](../../../contrats/meteo/temperature_interieure/bornes_thermiques_chambres_etage.md) (mergé). Elles sont **conservées ici à titre d'historique d'arbitrage** : en cas de différence de niveau d'autorité, **le contrat normatif de production prévaut**, et la présente note **ne le redéfinit pas** (elle n'en est pas un résumé opposable).

### Principe de simplification (préalable)

Les façades par zone disposent **déjà** de : validation, TTL 1800 s, mémoire bornée, `time_pattern`, abstention, disponibilité explicite. **L'agrégat ne doit pas recréer une deuxième politique de mémoire/fraîcheur au-dessus de ses opérandes.** Les constructions « mémoire événementielle + canal valeur + canal confiance + second TTL + entité compagnon » du brouillon précédent **ne sont pas retenues**.

### C-prod-1 — Mémoire

**DÉCISION ACQUISE : aucune mémoire propre aux agrégats.**
- suppression du principe `{{ last }}` non borné ;
- pas de mémoire événementielle supplémentaire, pas de nouvel `input_datetime`, pas de second TTL, pas de continuité artificielle de la valeur agrégée.

La continuité et la fraîcheur sont **déjà** traitées par les façades sources.

### C-prod-2 — Abstention

**DÉCISION ACQUISE : abstention immédiate lorsque plus aucune façade chambre n'est exploitable.**
- tant qu'au moins une façade est numérique : agrégat calculé sur les façades valides ;
- lorsqu'aucune façade n'est exploitable : agrégat **non disponible** (forme Home Assistant appropriée à contractualiser), **sans republier aucune ancienne valeur** ;
- **aucun délai propre à l'agrégat**.

**Distinction explicite :** ceci **n'est pas** une réaction immédiate à la panne d'un capteur physique. Chaque façade conserve **déjà** sa propre fenêtre de continuité bornée (TTL 1800 s). L'abstention de l'agrégat n'intervient que **lorsque les façades elles-mêmes se sont abstenues**.

### C-prod-3 — Périmètre

**DÉCISION ACQUISE : trois chambres uniquement.**
- **Incluses** : chambre Arnaud, chambre Matthieu, chambre Parents.
- **Exclues** : séjour, entrée, petite maison, agrégat RDC.

Périmètre à contractualiser tel quel.

### C-prod-4 — Fraîcheur

**DÉCISION ACQUISE : fraîcheur héritée de la validité des façades, sans horloge supplémentaire.**
- l'agrégat est exploitable dès qu'au moins une façade est exploitable ;
- il n'a **pas** de notion temporelle indépendante ;
- la recommandation « durée depuis indisponibilité simultanée des façades » (nouvelle machine temporelle) est **retirée**.

Le contrat distinguera : **fraîcheur des mesures sources** (gouvernée par les façades) vs **couverture de l'agrégat** (nombre de façades exploitables).

### C-prod-5 — Disponibilité partielle

**DÉCISION ACQUISE : agrégat valide dès qu'au moins une façade est exploitable.**
- calcul MIN/MAX sur les façades valides restantes (redondance conservée) ;
- aucune valeur figée si le nombre tombe à zéro (→ abstention, C-prod-2) ;
- la **perte de représentativité** doit être **observable**, sans invalider automatiquement l'agrégat.

### C-prod-6 — Signal exposé

**DÉCISION ACQUISE : pas d'entité compagnon de fraîcheur créée d'emblée.**
- le contrat prévoira **au minimum une observabilité de couverture** par **attributs** de l'agrégat (si cette forme est compatible avec les conventions Arsenal), par exemple **conceptuellement** : nombre de façades exploitables, nombre de façades attendues, liste des façades utilisées, chambre portant le MIN ou le MAX — **noms exacts non figés ici** ;
- une **entité compagnon** ne sera créée **que si** un consommateur démontre qu'un état autonome, historisable ou déclencheur est nécessaire.

Le statut principal reste porté par : la **disponibilité** de l'agrégat, la **catégorie thermique** backend destinée à la restitution, et les **attributs de couverture** pour le diagnostic.

---

## 6. Modèle cible (principe)

```text
façades chambres gouvernées et bornées
        ↓
agrégat MIN/MAX sans mémoire propre
        ↓
catégorie thermique backend simple
        ↓
mapping UI Exception 2 étendue
```

**États utiles**
- **MIN** : `froid` / `dans_plage` + indisponibilité native.
- **MAX** : `chaud` / `dans_plage` + indisponibilité native.

**Éléments supprimés du modèle** (par rapport à l'existant / au brouillon précédent) :
- mémoire non bornée des agrégats ;
- seconde horloge de fraîcheur ;
- second TTL ;
- entité compagnon créée par principe ;
- RED-sur-MIN ;
- classification croisée Chauffage/Climatisation ;
- vert **résiduel** de fall-through (indéterminé) — **remplacé** par la catégorie physique nommée `dans_plage` (vert de l'Exception 2 étendue) ;
- gris neutre `0.2` intermédiaire dans la machine d'états de ces deux cartes ;
- calcul local `consigne − offset_on` ;
- lecture locale du franchissement COOL ;
- couleur RGBA comme vérité backend.

---

## 7. Impact sur le(s) contrat(s) futur(s)

**DÉCISION ACQUISE : deux contrats distincts.**

### Contrat 1 — Production et agrégation — **rédigé, validé et mergé (Lot 2A)**
Responsabilités : périmètre ; opérandes ; règle MIN/MAX ; disponibilité partielle ; abstention ; **absence de mémoire propre** ; couverture observable ; relation avec les façades gouvernées.
**Chemin canonique :** `00_documentation_arsenal/contrats/meteo/temperature_interieure/bornes_thermiques_chambres_etage.md`. Il gouverne les bornes des **trois chambres de l'étage** et **ne doit pas être rouvert par le Lot 2B**.

### Contrat 2 — Sémantique thermique et restitution — **reste à rédiger (Lot 2B)**
**Chemin décidé :** `00_documentation_arsenal/contrats/meteo/temperature_interieure/restitution_chambres_etage.md`.
Le Lot 2B doit gouverner :
- le **rôle normatif** des **deux références physiques dédiées et stables** (basse pour MIN, haute pour MAX) ;
- les **catégories** thermiques MIN/MAX (`froid` / `dans_plage` / `chaud` selon la carte) et la séparation MIN/MAX ;
- l'**indisponibilité native** (prioritaire) ;
- le **mapping** vers l'**Exception 2 étendue** (dont le vert `dans_plage`) ;
- les **obligations de l'UI**, avec **exclusion des couches décisionnelles HVAC**.

Il **consomme** le contrat de production **sans le redéfinir**. Il **ne fixe pas prématurément** les **valeurs numériques** ni le **support runtime** des références : ceux-ci relèvent de l'**audit d'implémentation**.

**Dépendance normative :** le contrat de restitution **consomme** les bornes définies par le contrat de production ; il **ne redéfinit pas** leur validité, leur périmètre ou leur disponibilité.

---

## 8. Sort du plan d'action antérieur

Les recommandations antérieures fondées sur **mémoire événementielle supplémentaire**, **statut compagnon systématique** et **continuité de valeur au-delà de la disponibilité des façades** **ne sont pas retenues** par le présent arbitrage.

Le plan d'action existant (`03_plans_action/temperature_interieure/plan_action_temperature_interieure_agregats.md`) **reste inchangé au Lot 1** ; son état courant devra être **réexaminé au lot documentaire approprié** afin qu'il ne demeure pas une proposition concurrente active.

---

## 9. Hors périmètre (explicite)

- Réconciliation de plausibilité 8–40 (`axe_temperature.md`) vs 5–45 (`consolidation.md`) — dette documentaire.
- `sensor.temperature_max_rdc`, zones hors chambres, chaîne extérieure/jardin.
- HEAT d'appoint Climatisation (restitution distincte éventuelle, hors C27).
- Toute implémentation (production, UI, contrat, checker, CI).
- Noms/formes exacts des entités et attributs (relèvent du Lot 2B / audit runtime).

---

## 10. Tableau récapitulatif

### A. Décisions acquises (Lot 1, B2/B3/B6 amendées au réexamen pré-Lot 2B)

| Réf | Décision |
|---|---|
| Vision | **A — lecture physique thermique** (B rejetée) |
| B1 MIN | état thermique physique de `temperature_min_chambres` (`froid` si `MIN < réf. basse` / `dans_plage` si `MIN >= réf. basse`, égalité incluse) + indisponibilité native |
| B1 MAX | état thermique physique de `temperature_max_chambres` (`chaud` si `MAX > réf. haute` / `dans_plage` si `MAX <= réf. haute`, égalité incluse) + indisponibilité native |
| B2 | **Exception 2 étendue** (froid `rgba(144,202,249,0.25)` / **`dans_plage` vert `rgba(76,175,80,0.2)`** / chaud `rgba(244,67,54,0.2)` / indispo native `rgba(158,158,158,0.1)`) ; aucun hybride ; aucune RGBA backend ; aucun bleu info ; aucun gris neutre `0.2` intermédiaire |
| B3 | non-froid / non-chaud = **catégorie physique `dans_plage`** (vert Exception 2 étendue) ; réalité unique = **absence de franchissement défavorable sur la borne** ; pas de confort global ni nominalité système ; **égalité = `dans_plage`** |
| B4 | chaque carte qualifie **sa propre grandeur** (cross-entity abandonné) |
| B5 | HEAT d'appoint **hors** de ces cartes |
| B6 | backend expose une **catégorie sémantique** (MIN `froid`/`dans_plage` ; MAX `chaud`/`dans_plage` ; indisponibilité native) ; UI mappe vers **Exception 2 étendue** ; **pas de RGBA backend** |
| C-prod-1 | **aucune mémoire propre** à l'agrégat |
| C-prod-2 | **abstention immédiate** quand aucune façade exploitable ; pas de délai propre ; pas de republication |
| C-prod-3 | **3 chambres** (Arnaud/Matthieu/Parents) ; séjour/entrée/petite maison/RDC exclus |
| C-prod-4 | fraîcheur **héritée** des façades, sans horloge propre |
| C-prod-5 | valide dès **≥ 1 façade** ; perte de représentativité observable |
| C-prod-6 | **pas d'entité compagnon d'emblée** ; couverture via attributs (forme à valider) |
| Contrats | **deux** contrats : production **mergé (Lot 2A)** + restitution **à rédiger (Lot 2B)**, dépendance normative |

### B. Précisions réellement ouvertes (Lot 2B ou audit runtime)

- **valeurs numériques** des références physiques basse et haute ;
- **support runtime exact** de ces références ;
- **noms et forme exacte** des entités de catégorie (`froid` / `dans_plage` / `chaud`) ;
- **mécanisme YAML concret** de leur disponibilité (indisponibilité native lorsque l'agrégat ou la référence est inexploitable) ;
- **stratégie de mapping commun** dans le socle ou les templates (catégorie → couleur Exception 2 étendue) ;
- **noms YAML exacts** des attributs de couverture, **uniquement comme sujet d'implémentation du contrat de production déjà mergé**.

*(Retirés car désormais décidés/contractualisés au Lot 2A : nom et emplacement du contrat de production ; emplacement du contrat de restitution ; forme normative de l'abstention des agrégats ; principe de couverture observable.)*

### C. Hors périmètre

- Plausibilité 8–40 / 5–45 ; `temperature_max_rdc` et zones hors chambres ; HEAT d'appoint ; toute implémentation ; réexamen du plan d'action (lot documentaire ultérieur).

---

*Fin de la note d'arbitrage consolidée (dossier de décision, non normatif). Aucun contrat, runtime ou UI n'est modifié par ce document.*
