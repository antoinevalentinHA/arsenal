# 🧠 ARSENAL — CONTRAT NORMATIF RACINE · CHAUFFAGE — DOCTRINE DES REGISTRES (V3 PRO) · Sécurité système vs Stabilisation thermique
#
# 📌 STATUT :
#   CONTRAT NORMATIF RACINE — CLÉ DE LECTURE DU DOMAINE
#
# 🔒 AUTORITÉ :
#   Ce document définit la grille de lecture fondamentale du
#   sous-système Chauffage Arsenal : la distinction entre
#   SÉCURITÉ SYSTÈME et STABILISATION THERMIQUE.
#
#   Il est subordonné à la constitution du domaine
#   (`00_gouvernance_chauffage.md`) et gouverne l'interprétation
#   de TOUS les autres contrats Chauffage : blocages, décision
#   centrale, table canonique, standby, géofencing, autorisation.
#
#   En cas de divergence d'interprétation entre deux contrats de
#   domaine, la classification posée ici fait foi.
#
# ==========================================================

---

## 1. Objet du contrat

Ce contrat formalise la **clé de lecture doctrinale** du domaine Chauffage.

Il établit que le domaine manipule **deux familles de mécanismes** de natures
irréductibles, longtemps confondues parce qu'elles produisent parfois le même
effet observable (`reduced`) :

- la **sécurité système**, qui protège l'intégrité, la souveraineté et la
  cohérence d'exécution, et qui s'exprime par des **interdictions** ;
- la **stabilisation thermique** (incluant la sobriété), qui optimise la
  régulation, l'inertie et la dépense, et qui s'exprime par des
  **préférences qualifiées**.

Cette distinction n'est pas une commodité descriptive. Elle détermine, pour
chaque mécanisme du domaine : la couche où il vit, l'outil par lequel ses
conflits se résolvent, son effet sur la décision, et la raison qu'il produit.

---

## 2. Principe fondateur (D0)

> **D0 — Irréductibilité des registres.**
> Une interdiction de sécurité et une préférence de stabilisation ne sont
> jamais le même objet, **même lorsqu'elles produisent le même régime**.
> Elles ne vivent pas dans la même couche, ne se résolvent pas avec les mêmes
> outils, et ne portent jamais la même raison.

Corollaire : produire `reduced` ne suffit jamais à qualifier un mécanisme.
Un mécanisme qui impose `reduced` parce qu'une fenêtre est ouverte (sécurité)
et un mécanisme qui préfère `reduced` parce que le confort est atteint
(stabilisation) sont deux objets distincts, qui doivent rester distincts à
tous les niveaux de l'architecture.

---

## 3. Caractérisation des deux registres

|                         | Sécurité système                                   | Stabilisation thermique                                        |
|-------------------------|----------------------------------------------------|----------------------------------------------------------------|
| **But**                 | intégrité, souveraineté, cohérence d'exécution     | inertie, sobriété, qualité de reprise, anti-pompage            |
| **Mode d'expression**   | interdiction                                       | préférence qualifiée                                           |
| **Outil de résolution** | dominance hiérarchique (Niveau 1, `elif` fort)     | qualité du signal, hystérésis, corroboration, verrou subordonné |
| **Effet sur décision**  | écrase tout, non négociable                        | proposée, subordonnée, écrasable                              |
| **Réversibilité**       | levée explicite, jamais par simple disparition     | retour nominal attendu                                         |
| **Lecture par un tiers**| « le chauffage est interdit » — sans glose         | « le chauffage préfère s'abstenir » — contextuelle            |

Note de nuance opposable : « stabilisation » ne signifie pas « accessoire ».
Le blocage post-aération est une **sécurité** parce qu'il protège un épisode
physique en cours et exige une temporisation non négociable ; le poêle est une
**stabilisation** parce que son objet (ne pas empiler deux apports) tolère
l'erreur des deux côtés. La frontière est « intégrité vs optimisation »,
jamais « important vs secondaire ».

---

## 4. Invariants doctrinaux

> **D1 — Réservation de la hiérarchie forte.**
> La dominance hiérarchique — l'ordre des `elif`, les capteurs de Niveau 1,
> le verrou `binary_sensor.chauffage_autorise_systeme` — est **strictement
> réservée à la sécurité système**. Utiliser cet outil pour arbitrer un
> conflit de stabilisation est une faute doctrinale, même si le résultat
> « fonctionne ».

> **D2 — Résolution des conflits de stabilisation par le signal.**
> Un conflit entre deux mécanismes de stabilisation **ne se tranche pas par
> le rang**. Il se tranche par la **fiabilité du signal** : le mécanisme dont
> le signal est corroboré l'emporte ; un signal non corroboré ne produit
> aucun effet décisionnel. L'ordre des branches devient alors indifférent.

> **D3 — Non-remontée des conséquences.**
> Une grandeur produite par la décision, ou en aval de celle-ci (une
> *conséquence*), ne peut jamais remonter alimenter une couche amont comme si
> elle en était une *cause*. La persistance, l'historisation ou l'exposition
> en diagnostic d'une telle grandeur ne la promeuvent jamais au rang de cause.
> Une conséquence qui se fait passer pour une cause est une inversion de
> responsabilité.

> **D4 — Classification opposable des mécanismes.**
> La classification suivante est normative et opposable :
>
> | Mécanisme                                | Registre                        |
> |------------------------------------------|---------------------------------|
> | Interdiction système, maintenance        | Sécurité                        |
> | Blocage post-aération                    | Sécurité                        |
> | Fenêtre ouverte (avec délai)             | Sécurité                        |
> | Bridge offline (garde d'exécution)       | Sécurité d'exécution            |
> | Poêle                                    | Stabilisation (anti-empilement) |
> | Inhibition géofencing                    | Stabilisation (reprise)         |
> | `standby_force`                          | Stabilisation (hystérésis appl.)|
> | Anticipation météo                       | Stabilisation (sobriété)        |
>
> Aucun mécanisme de stabilisation ne justifie une interdiction de Niveau 1.
> Aucun ne se déguise en sécurité.

---

## 5. Conséquences architecturales directes

De D0–D4 découlent, sans interprétation supplémentaire :

- `binary_sensor.chauffage_autorise_systeme` ne compose que des causes de
  sécurité. Aucune grandeur de stabilisation (notamment `standby_force`) n'y
  entre. — *voir `30`, `50`.*
- Les verrous de stabilisation (`standby_force`) vivent en couche
  application/hystérésis, subordonnés et observables, jamais causaux. —
  *voir `50`.*
- La qualification « poêle actif » destinée à une décision ou un blocage exige
  un signal de corroboration non thermique. — *voir `40`, `80`.*
- L'inhibition géofencing est une régulation de stabilisation hystérésée,
  réactivable, subordonnée. — *voir `60`.*
- La modulation météo est une modulation de sobriété (`comfort → neutre`
  uniquement), résidant dans la couche autorisation. — *voir `70`, `90`.*
- La raison métier distingue toujours interdiction de sécurité et abstention
  de sobriété ; jamais une stabilisation étiquetée comme interdiction. —
  *voir `30`, `90`.*

---

## 6. Invariants exposés à la vérification (CI)

Ces invariants sont la traduction testable de la doctrine. Ils sont opposables
et destinés à être vérifiés structurellement.

- **INV-D1** — Aucune cause de stabilisation (poêle, géofencing, standby,
  météo) ne compose un capteur de Niveau 1.
- **INV-D3** — Aucune grandeur produite par ou en aval de la décision ne
  figure en entrée d'une couche amont (autorisation, sécurité système).

Les invariants spécifiques par mécanisme sont portés par leurs contrats
respectifs (`40`, `50`, `60`, `70`, `80`).

---

## 7. Énoncé doctrinal de référence (opposable)

> Dans le domaine Chauffage Arsenal, la hiérarchie forte et les capteurs de
> Niveau 1 sont réservés à la sécurité système ; toute stabilisation thermique
> — poêle, géofencing, standby, anticipation météo — vit dans les couches
> autorisation et application, se résout par la qualité du signal, l'hystérésis
> et la corroboration, reste toujours subordonnée et observable, et ne se
> déguise jamais en interdiction système.

---

## 8. Dépendances contractuelles

**Subordonné à :** [`00_gouvernance_chauffage.md`](00_gouvernance_chauffage.md)

**Gouverne l'interprétation de :** `30_decision_centrale.md` ·
`40_blocages.md` · `50_standby_hysteresis.md` ·
`60_absence_inhibition_geofencing.md` · `70_autorisation_thermostat.md` ·
`80_table_decision_canonique.md` · `90_semantique_thermique.md`

---

## 9. Annexe factuelle — Runtime proof

Cette doctrine n'est pas posée a priori : elle est adossée à une analyse
runtime exhaustive du domaine, établissant des faits opposables.

### A. Désintrication `standby_force` — sûreté établie

Vérification des dépendances de `binary_sensor.chauffage_autorise_systeme`
avant retrait de la composante `standby_force` :

- **Réveil décisionnel** : aucun trou. La chaîne
  `autorisation_cible → automation d'application standby → standby_force →
  autorise_systeme` montre que tout changement d'autorisation réveille déjà
  le cerveau via le trigger `sensor.chauffage_autorisation_cible`, en amont
  et indépendamment du trigger `autorise_systeme`. Le trigger
  `autorise_systeme` reste utile pour les bascules de sécurité (aération),
  qui ne dépendent pas de l'autorisation.
- **Recorder / statistiques** : `autorise_systeme` n'est pas enregistré ;
  `standby_force` l'est et reste conservé. Les statistiques de sobriété
  (`history_stats` éco) sont ancrées sur l'état matériel
  `sensor.programme_chauffage`, jamais sur l'autorisation. Aucune rupture de
  continuité statistique.
- **Proxy implicite** : aucune lecture en UI, aucun couplage attributaire,
  aucun lecteur cross-domaine. Les seuls consommateurs de `autorise_systeme`
  sont internes au domaine (décision + diagnostic).
- **Correction des cascades** : la purification de `autorise_systeme` corrige
  simultanément les quatre cascades hiérarchiques (décision `desired_mode`,
  décision `reason`, diagnostic raison, diagnostic mode) sans édition
  manuelle, car elles lisent toutes le même capteur.

Conclusion : la désintrication supprime une ambiguïté structurelle sans
déplacer de complexité, et restaure la causalité correcte entre sécurité et
stabilisation.

### B. Moteur décisionnel poêle — sain de fait

Le chemin décisionnel poêle passe exclusivement par le flag corroboré
(`poele_en_fonction = signature thermique ∧ présence non thermique ∧
chaudière hors cause`), jamais par la signature thermique seule. Le seul
court-circuit résiduel concerne la mémoire de calibration (`poele_recent`),
dont l'effet est conservateur (figer la courbe, jamais relâcher).
Voir `40` §poêle et décision A.

---

## 10. Portée et stabilité

Ce contrat est racine, stable long terme, modifié uniquement lors d'évolutions
doctrinales majeures, versionné explicitement, et opposable à toute
implémentation et à tout autre contrat de domaine Chauffage.

# ==========================================================
