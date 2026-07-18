# Note d'arbitrage — Agrégats de température MIN/MAX des chambres et leur restitution

> **Statut : dossier d'arbitrage — descriptif, non normatif.** Version consolidée **remplaçant**
> l'état antérieur de ce fichier (historique porté par Git ; aucun avenant empilé). Les décisions
> propriétaire ci-dessous sont **acquises** (Lot 1). Cette note **ne rédige aucun contrat**, **ne
> modifie aucun runtime, UI, checker ou CI**, et n'implémente rien : elle **fixe les frontières et les
> choix** avant contractualisation (Lot 2).
>
> - **Chantier :** C27 — [`04_chantiers/transverses/chantier_temperature_min_max_chambres_dashboard_arsenal.md`](../../04_chantiers/transverses/chantier_temperature_min_max_chambres_dashboard_arsenal.md)
> - **Preuve de départ :** [`01_rapports/transverses/audit_cartes_temperature_min_max_dashboard_arsenal.md`](../../01_rapports/transverses/audit_cartes_temperature_min_max_dashboard_arsenal.md) (PR #410).
> - **Antécédent descriptif non normatif :** [`03_plans_action/temperature_interieure/plan_action_temperature_interieure_agregats.md`](../../03_plans_action/temperature_interieure/plan_action_temperature_interieure_agregats.md) — **inchangé au Lot 1** (cf. §17).
> - **Portée :** couche d'agrégation thermique intérieure (`sensor.temperature_min_chambres`, `sensor.temperature_max_chambres`) **et** restitution des deux cartes du dashboard Arsenal.

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
- **Aucune autorité normative directe** sur les agrégats ni sur les cartes.

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
- `froid` lorsque la borne basse franchit le **seuil physique inférieur** décidé ;
- `neutre` sinon ;
- `indisponible` lorsque l'agrégat est indisponible ;
- ne devient **jamais** rouge en fonction de MAX.

**MAX — DÉCISION ACQUISE : état thermique physique de `sensor.temperature_max_chambres`.**
- `chaud` lorsque la borne haute franchit le **seuil physique supérieur** décidé ;
- `neutre` sinon ;
- `indisponible` lorsque l'agrégat est indisponible.

La couche gouvernante n'est donc **ni** le besoin COOL, **ni** son admissibilité, **ni** `clim_target_mode`, **ni** l'autorisation chauffage, **ni** un franchissement.

**Options rejetées :** franchissement seul (couche observation, INT-2) ; besoin / admissibilité / décision / autorisation (relèvent de la Vision B rejetée) ; combinaison multi-couches (OBJ-3).

**Précision reportée au Lot 2 (technique, sans réouvrir la Vision A) :** le contrat identifiera les **références physiques inférieure et supérieure** à employer, en vérifiant les contrats existants — référence basse cohérente avec la lecture thermique Chauffage, référence haute cohérente avec la lecture thermique Climatisation. Ces références **peuvent** provenir de paramètres métier existants, **mais les cartes n'affichent ni l'autorisation ni la décision correspondantes** : elles n'en tirent qu'un **seuil physique** de qualification.

### B3 — État résiduel

**DÉCISION ACQUISE : `neutre`, rendu en gris neutre `rgba(158,158,158,0.2)` — pas de « tempéré » vert.**

Le cas non-froid (MIN) / non-chaud (MAX) signifie uniquement : **aucun écart thermique pertinent pour cette borne**. Aucune bande verte « nominale / OK » n'est créée (elle ajouterait une affirmation inutile).

Réalité unique par carte :
- **MIN : froid / neutre / indisponible** ;
- **MAX : chaud / neutre / indisponible**.

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

**DÉCISION ACQUISE : Exception 2 thermique.**

Mapping de principe :
- **MIN froid** : bleu thermique `rgba(144,202,249,0.25)` ;
- **MAX chaud** : rouge thermique de l'Exception 2 (`rgba(244,67,54,0.2)`) ;
- **neutre** : gris neutre `rgba(158,158,158,0.2)` ;
- **indisponibilité** : gris indisponibilité `rgba(158,158,158,0.1)`.

Exclus : tout vert métier ; le bleu sémantique « information » `rgba(33,150,243,0.2)` ; tout régime hybride ; toute couleur « chauffe en cours » (les cartes n'affichent pas une action HVAC).

### B6 — Localisation de la logique

**DÉCISION ACQUISE : le backend expose la sémantique thermique ; l'UI applique la palette.**

- **Backend** : détermine la **catégorie thermique** — MIN : `froid` / `neutre` / `indisponible` ; MAX : `chaud` / `neutre` / `indisponible`.
- **UI** : **mappe** la catégorie vers les couleurs de l'Exception 2.
- **Socle** : restitue l'indisponibilité selon la doctrine générale.

La couleur RGBA **n'est pas** une vérité métier backend : le backend fournit une **catégorie sémantique** consommable, pas un code couleur. La stratégie « `sensor.couleur_*` exposant directement une RGBA » **n'est pas retenue**.

Le **nom exact, la forme exacte et le nombre d'entités** portant cette catégorie seront définis au **contrat et à l'audit d'implémentation** (Lot 2) — non fixés ici.

Conséquences attendues (à implémenter plus tard, pas au Lot 1) :
- aucune comparaison de seuil dans les cartes ;
- aucune lecture directe des helpers Chauffage par les cartes ;
- aucune lecture du franchissement COOL par les cartes ;
- suppression du JS local RED/BLUE/GREEN ;
- mapping UI **trivial et documenté** (catégorie → couleur Exception 2) ;
- **mutualisation** des deux templates **seulement si elle reste utile** après implémentation.

---

## 5. Arbitrages de production (C-prod-1…6)

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
mapping UI Exception 2
```

**États utiles**
- **MIN** : froid / neutre / indisponible.
- **MAX** : chaud / neutre / indisponible.

**Éléments supprimés du modèle** (par rapport à l'existant / au brouillon précédent) :
- mémoire non bornée des agrégats ;
- seconde horloge de fraîcheur ;
- second TTL ;
- entité compagnon créée par principe ;
- RED-sur-MIN ;
- classification croisée Chauffage/Climatisation ;
- vert résiduel ;
- calcul local `consigne − offset_on` ;
- lecture locale du franchissement COOL ;
- couleur RGBA comme vérité backend.

---

## 7. Impact sur le(s) contrat(s) futur(s)

**DÉCISION ACQUISE : deux contrats distincts.** *(Contenu non rédigé ici.)*

### Contrat 1 — Production et agrégation
Responsabilités : périmètre ; opérandes ; règle MIN/MAX ; disponibilité partielle ; abstention ; **absence de mémoire propre** ; couverture observable ; relation avec les façades gouvernées.
Emplacement pressenti : `00_documentation_arsenal/contrats/meteo/temperature_interieure/` (nom exact décidé au Lot 2 selon les conventions du dossier).

### Contrat 2 — Sémantique thermique et restitution
Responsabilités : catégories thermiques MIN/MAX ; références physiques ; séparation MIN/MAX ; **exclusion des couches décisionnelles HVAC** ; mapping vers l'Exception 2 ; neutralité et indisponibilité ; obligations de l'UI.
Emplacement canonique : **à proposer au Lot 2 après examen des contrats transversaux existants** — ne pas créer arbitrairement un nouveau dossier avant cet examen.

**Dépendance normative :** le contrat de restitution **consomme** les agrégats définis par le contrat de production ; il **ne redéfinit pas** leur validité, leur périmètre ou leur disponibilité.

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
- Noms/formes exacts des entités et attributs (relèvent du Lot 2).

---

## 10. Tableau récapitulatif

### A. Décisions acquises (Lot 1)

| Réf | Décision |
|---|---|
| Vision | **A — lecture physique thermique** (B rejetée) |
| B1 MIN | état thermique physique de `temperature_min_chambres` (froid/neutre/indisponible) |
| B1 MAX | état thermique physique de `temperature_max_chambres` (chaud/neutre/indisponible) |
| B2 | Exception 2 (froid `rgba(144,202,249,0.25)` / chaud `rgba(244,67,54,0.2)` / neutre `0.2` / indispo `0.1`) ; ni vert, ni bleu info, ni hybride, ni « chauffe » |
| B3 | résiduel = **neutre** gris `0.2` (pas de tempéré vert) |
| B4 | chaque carte qualifie **sa propre grandeur** (cross-entity abandonné) |
| B5 | HEAT d'appoint **hors** de ces cartes |
| B6 | backend expose une **catégorie sémantique** ; UI mappe vers Exception 2 ; **pas de RGBA backend** |
| C-prod-1 | **aucune mémoire propre** à l'agrégat |
| C-prod-2 | **abstention immédiate** quand aucune façade exploitable ; pas de délai propre ; pas de republication |
| C-prod-3 | **3 chambres** (Arnaud/Matthieu/Parents) ; séjour/entrée/petite maison/RDC exclus |
| C-prod-4 | fraîcheur **héritée** des façades, sans horloge propre |
| C-prod-5 | valide dès **≥ 1 façade** ; perte de représentativité observable |
| C-prod-6 | **pas d'entité compagnon d'emblée** ; couverture via attributs (forme à valider) |
| Contrats | **deux** contrats (production + restitution), dépendance normative |

### B. Précisions techniques reportées au Lot 2

- Références physiques inférieure/supérieure (B1) à identifier dans les contrats existants — sans que les cartes n'affichent autorisation/décision.
- Nom, forme et nombre d'entités portant la catégorie thermique (B6).
- Forme HA exacte de l'indisponibilité de l'agrégat (C-prod-2).
- Noms exacts des attributs de couverture (C-prod-6).
- Nom du contrat de production ; **emplacement canonique** du contrat de restitution (après examen des contrats transversaux).

### C. Hors périmètre

- Plausibilité 8–40 / 5–45 ; `temperature_max_rdc` et zones hors chambres ; HEAT d'appoint ; toute implémentation ; réexamen du plan d'action (lot documentaire ultérieur).

---

*Fin de la note d'arbitrage consolidée (dossier de décision, non normatif). Aucun contrat, runtime ou UI n'est modifié par ce document.*
