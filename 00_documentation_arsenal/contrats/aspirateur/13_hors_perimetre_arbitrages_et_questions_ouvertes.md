# CONTRAT ARSENAL — ASPIRATEUR
## 13 — Hors périmètre, arbitrages et questions ouvertes

**Version contrat :** v1.0
**Statut :** Normatif pour les exclusions ; **traçant** pour les arbitrages et
les questions ouvertes
**Objet :** Dire explicitement ce que ce contrat exclut, ce qu'il a arbitré sans
preuve complète, et ce qu'il laisse ouvert.

---

## 1. Hors périmètre de ce contrat

| Objet | Statut |
|---|---|
| **Implémentation runtime** — helpers, scripts, automations, capteurs | **Hors lot.** Aucun n'est créé, aucun n'est nommé. |
| **Checker CI contractuel** du domaine | **Hors lot.** Aucun invariant de ce contrat n'est aujourd'hui vérifié par la CI. |
| **Dashboard Aspirateur** | **Hors lot** — seules les frontières sont posées ([`11`](11_frontiere_ui.md)). |
| **Navigation Arsenal** — carte des domaines, hubs, réorganisation d'un domaine voisin | **Hors lot** et **hors métier Aspirateur**. La couche navigation est non normative et détachable ; ce lot ne la modifie pas. |
| **Historisation `recorder`** | **Hors lot.** Aucune entité n'y est inscrite ; extension optionnelle d'observabilité, hors chemin critique. |
| **Qualification du Garage** | **Hors lot** ([`01`](01_finalite_et_perimetre.md) §5). |
| **Nouveau lot terrain** | **Non demandé par ce contrat.** Les arbitrages du §2 sont assumés en l'état. |
| **Toute modification du domaine alarme** | **Hors lot** — l'acquis est préservé, pas rouvert (`ASP-INV-4`). |

> **Ce contrat ne crée rien.** Il norme une conduite. Sa mise en œuvre est
> subordonnée à une **validation humaine** et à des lots ultérieurs.

---

## 2. Arbitrages contractuels explicites

Ces points **sont tranchés** par ce contrat — mais sans preuve terrain complète.
Ils sont inscrits ici pour que la décision soit **visible et révisable**, jamais
tacite.

### `ARB-1` — Partition fermée des états de lancement

**Question.** Depuis quels états stables l'appareil accepte-t-il une mission
segmentée ?

**Ce qui est établi.** Les deux essais validés partaient d'un robot **présent sur
la carte demandée**. Aucune liste positive d'états de lancement n'est prouvée.

**Arbitrage retenu.** Le contrat **partitionne** les valeurs de l'état machine en
quatre classes fermées et exhaustives ([`07`](07_moteur_de_mission.md) §5.0) : une
classe de **repos admissible** restreinte aux deux valeurs de repos attestées
(`charger_disconnected`, `charging`), une classe d'**activité**, une classe
d'**erreur ou d'indisponibilité**, et une classe **non qualifiée** qui absorbe
toute valeur que le contrat ne nomme pas — y compris future — et **refuse par
défaut** (`ASP-INV-60`).

Le contrat **n'exige ni `docked` ni `charging`** : `charger_disconnected`, l'état
d'un robot hors de son dock, est **admissible**. Le lancement après transport
physique vers un étage sans base reste donc possible, conformément au besoin.

**Ce que cela n'affirme pas.** Que tout lancement hors base aboutira. L'issue est
**qualifiée** comme toute autre ([`07`](07_moteur_de_mission.md) §4).

**Ce que cela ferme.** La classe de repos étant **énumérée** et non plus
seulement définie par la négative, aucun état de mouvement — `returning_home`,
`docking` — ni aucun état futur ne peut plus traverser les conditions de
lancement. C'est la correction du seul trou normatif relevé à l'audit
indépendant.

**Révision.** Un lot terrain établissant qu'un état aujourd'hui classé en repos
admissible n'accepte pas la commande, ou qu'une valeur non qualifiée est en
réalité un repos, amenderait la partition du §5.0 — et elle seule.

### `ARB-2` — Session inachevée, robot inactif ⇒ refus

**Question.** Que fait une commande segmentée émise alors qu'une session est
ouverte et que le robot ne nettoie pas ?

**Ce qui est établi.** Cet état **existe** — il a été observé. Le comportement de
la commande dans cet état **ne l'est pas**.

**Arbitrage retenu.** **Refus** au motif `SESSION_INACHEVEE`, avec geste attendu
nommé. Le contrat préfère dire « je ne sais pas ce que cela ferait » plutôt que
de présumer une issue.

**Portée exacte, depuis la partition.** Ce refus ne s'applique qu'à l'état machine
en **classe R** avec témoin de session `on` ([`08`](08_etats_et_observation.md)
§3.1). Un robot en pause relève, lui, de la classe A et refuse au motif
`MISSION_DEJA_OUVERTE` — la pause reste par ailleurs le **seul** état depuis
lequel la reprise est autorisée (`ASP-INV-62`).

**Alternative écartée à ce stade.** Émettre puis qualifier l'issue — recevable
**sur preuve terrain**, pas avant.

### `ARB-3` — Deux fenêtres temporelles arrêtées

**Question.** Quelles durées d'attente, de confirmation et d'observation de
transition retenir ?

**État antérieur.** La version v1.0 du contrat ne fixait **aucune valeur** :
aucun précédent Arsenal ni arbitrage opérateur ne la fondait, et l'inventer
aurait été une clause opposable sans fondement.

**Arbitrage retenu — valeurs déclarées par l'opérateur.** Deux constantes, et
deux seulement ([`07`](07_moteur_de_mission.md) §3.1, `ASP-INV-69`) :

| Fenêtre | Valeur | Opérations couvertes | Issue en dépassement |
|---|---|---|---|
| **Confirmation** | **30 s** | Confirmation de **carte** (étape 7), d'**intensité d'eau** (étape 8), d'**aspiration** (étape 10) | Refus — `CARTE_NON_CONFIRMEE` ou `REGLAGE_NON_CONFIRME` |
| **Observation de transition** | **60 s** | **Uniquement** la transition de démarrage après émission (étape 13) | Échec — `TRANSITION_NON_OBSERVEE` |

**Niveau de preuve, dit franchement.** Ces deux valeurs sont **déclarées par
l'opérateur**, comme les valeurs nominales des témoins d'erreur (`ARB-5`). Elles
ne sont **adossées à aucune mesure terrain** de ces opérations : le lot T1/T2 n'a
chronométré ni une confirmation de réglage, ni un délai de démarrage. Le contrat
les **assume** à ce titre, et ne prétend pas les avoir mesurées.

**Ce que « révisable » signifie ici — et ne signifie pas.** La révision est un
**amendement conjoint** du contrat, du checker et du runtime, dans un même lot.
Ces valeurs ne sont **pas** modifiables à chaud : le domaine **n'expose aucun
helper temporel**, aucune entité et aucun paramètre d'appel qui les porterait.
Un réglage temporel exploitable serait un **second arbitre de la sûreté**, hors
contrat et hors CI — exactement ce que l'autorité unique proscrit.

**Aucun fallback.** Une échéance atteinte refuse ou qualifie un échec ; elle ne
retombe sur aucune valeur de repli et n'accorde aucune seconde attente.

**Ce que cela ferme.** Le lot runtime n'a plus de dimensionnement à proposer :
il **écrit littéralement** ces deux constantes. Le modèle de la stabilisation
post-allumage du domaine climatisation
([`../climatisation/08_execution.md`](../climatisation/08_execution.md)) reste la
référence de méthode pour une **révision** ultérieure, plus pour une invention
initiale.

**Révision.** Une mesure terrain établissant qu'une de ces fenêtres est trop
courte — une confirmation honnête arrivant après son échéance — amenderait le
§3.1 du chapitre [`07`](07_moteur_de_mission.md), le contrôle CI correspondant et
le moteur, **ensemble**.

### `ARB-4` — `×3` par déduction protocolaire

**Arbitrage déjà acquis, rappelé ici.** `×3` est retenu comme `repeat: 3` par
**déduction** de la sémantique de comptage établie, **sans essai terrain**, sur
acceptation explicite de l'opérateur ([`04`](04_nombre_de_passages.md) §1).

### `ARB-5` — Valeurs nominales des témoins d'erreur

**Question.** Quelle valeur d'un témoin d'erreur vaut « pas d'erreur » ?

**Ce qui est établi.** Le relevé d'audit atteste l'**existence** des deux témoins
et une **valeur d'erreur observée** (`wheels_suspended`), sans énumérer leur
valeur de repos.

**Arbitrage retenu.** Les valeurs nominales sont `none` pour l'aspirateur et `ok`
pour le dock, **déclarées par l'opérateur** ([`07`](07_moteur_de_mission.md)
§5.2). La règle est opposable **par sa forme** — toute valeur non nominale
refuse, sans exception ni liste de tolérance — et sa **littéralité** est adossée
à cette déclaration, non à une preuve terrain.

**Pourquoi ce choix plutôt qu'une pertinence graduée.** Distinguer les erreurs
« bloquantes » des autres serait un second arbitrage, qu'aucune preuve ne fonde,
et rouvrirait l'échappatoire discrétionnaire que la règle observable ferme.

**Révision.** Un relevé établissant les énumérations exactes de ces deux témoins
amenderait le §5.2 — et lui seul.

---

## 3. Questions ouvertes — non tranchées, non normées

Ces points **ne sont pas arbitrés**. Le contrat les **isole** plutôt que de
combler le vide.

### `QO-1` — Segments `2_17` (`Ext`) et `2_18` (`Chambre1`) de l'Annexe

Ces deux segments **existent dans la carte** et **ne portent aucun rôle métier**.
Le besoin V1 de l'Annexe est explicite — `Chambre` et `Salle de bain` — et les
deux segments correspondants sont identifiés sans ambiguïté par le relevé
d'audit : le référentiel Annexe est donc **figé sans incertitude**
([`02`](02_referentiel_cartes_et_pieces.md) §2).

**Ce qui reste ouvert** est la **nature** de `2_17` et `2_18` : segment extérieur,
doublon de cartographie, pièce réelle non exprimée dans le besoin — rien ne
permet de trancher. Une **vigilance de nommage** subsiste : `Chambre1` est proche
de `Chambre`, et les libellés sont modifiables hors du dépôt (`ASP-INV-7`,
`ASP-INV-9`).

**Traitement contractuel en attendant :** hors référentiel, donc **non
commandables**, donc refusés au motif `SEGMENT_INCONNU`. Aucun rôle ne leur est
attribué par défaut.

**Leur présence ne bloque pas l'Annexe.** La confirmation de carte procède par
**inclusion**, jamais par égalité ([`06`](06_integrite_mono_carte.md) §3.1,
`ASP-INV-63`) : voir `Ext` et `Chambre1` exposés **confirme** la carte Annexe,
sans les rendre commandables pour autant. Confirmer une carte et autoriser un
segment sont deux contrôles distincts.

**Ce qui débloquerait :** un arbitrage opérateur, ou un relevé établissant leur
nature.

### `QO-2` — `mapStatus` comme confirmation protocolaire

Ce champ a fourni une confirmation indépendante précieuse sur le terrain. Il
n'est **pas promu** en dépendance runtime, faute de preuve qu'une entité ou une
primitive exploitable dans Arsenal l'expose (`ASP-INV-30`).

**Ce qui débloquerait :** la preuve d'une primitive consommable.

### `QO-3` — Comportement multi-cartes

Restent non établis : le comportement de la carte active après **déplacement
physique** du robot dans d'autres conditions que celle observée, et
l'**acceptation d'un changement de carte** lorsque le robot se trouve
physiquement sur une autre carte.

**Ces questions ne bloquent pas** un pilotage mono-carte : `ASP-IMC-1` exige une
confirmation **avant chaque mission**, ce qui rend le contrat robuste à leur
issue.

### `QO-4` — Saturation multi-cartes et stabilité des index

Le robot est à **4 cartes sur 4**. Toute re-cartographie invaliderait les index
consignés (`ASP-INV-9`). Aucun mécanisme de détection de dérive n'est imposé —
aucune primitive exploitable n'est prouvée.

### `QO-5` — Historisation

Inscrire ou non des entités du domaine au `recorder` reste un **arbitrage
optionnel**, hors chemin critique.

### `QO-6` — Divergences de casse et de pluriel entre référentiels

Sans effet sur ce contrat (`ASP-INV-8`), la restitution passant par les libellés
canoniques Arsenal (`ASP-INV-7`). Consigné pour mémoire.

---

## 4. Visibilité documentaire du domaine

Le domaine est inscrit aux **deux** index de contrats — l'[index français](../index.md)
et l'[aperçu anglais](../index.en.md) — ainsi qu'au compteur de domaines
dossiérisés de [`../README.md`](../README.md), et au **registre de couverture de
vérification** ([`../../audits/REGISTRE_COUVERTURE_VERIFICATION.md`](../../audits/REGISTRE_COUVERTURE_VERIFICATION.md)),
dont le compteur de contrats Markdown est confronté mécaniquement par la CI.

**Écart préexistant, non traité par ce lot.** L'aperçu anglais porte **six
compteurs de fichiers désynchronisés** sur d'autres domaines, antérieurs à ce lot
et non gardés par la CI. Ce lot y ajoute **la seule ligne du domaine
`aspirateur`**, à son compte réel, et **ne corrige pas** les six écarts
historiques : ils relèvent d'une passe documentaire propre.

**Ce n'est pas une omission silencieuse** : c'est un écart **constaté et
consigné**.

---

## Renvois

- Finalité et périmètre : [`01_finalite_et_perimetre.md`](01_finalite_et_perimetre.md)
- Référentiel : [`02_referentiel_cartes_et_pieces.md`](02_referentiel_cartes_et_pieces.md)
- Moteur de mission : [`07_moteur_de_mission.md`](07_moteur_de_mission.md)
- Audit canonique du domaine : [`../../audits/01_rapports/aspirateur/audit_faisabilite_roborock_q7_max.md`](../../audits/01_rapports/aspirateur/audit_faisabilite_roborock_q7_max.md)
- Index du domaine : [`README.md`](README.md)
