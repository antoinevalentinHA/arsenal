# Protocole de preuve VMC (C35 — Lot 3)

| Champ | Valeur |
|---|---|
| **Chantier** | C35 — Mise en conformité du domaine VMC avec le contrat v2.1 |
| **Lot** | **L3 — définition du dispositif de preuve** |
| **Nature** | Document **normatif de définition des preuves**. Il ne produit aucune preuve, ne calibre aucun paramètre, ne crée aucun outil |
| **Frontière de propriété** | **Arsenal définit et interprète les preuves ; `arsenal-runtime` les acquiert, les extrait et en assure la reproductibilité opérationnelle** (§6) |
| **Contrat de référence** | [`../../../contrats/vmc.md`](../../../contrats/vmc.md) **v2.1** (§14 paramètres ouverts, §2.2 bis observation glissante, §9.1 bis, §15) |

> **Ce document définit les questions probatoires, les preuves attendues, les
> critères de suffisance et les propriétaires.** Il n'exécute aucune campagne, ne
> télécharge aucune sauvegarde, ne commande jamais la VMC. La calibration relève
> du L2b, postérieur à L5.

---

## 1. Objet

Répondre à une question unique :

> **Quelles observations minimales permettront de trancher chaque paramètre
> encore ouvert du §14, avec quelle méthode, quelle durée et quel critère
> d'acceptation ?**

Ce document est **auto-suffisant sur la définition**. Ce qu'il ne peut pas
trancher est **explicitement reporté à L4** (§8).

---

## 2. Constat structurant — observabilité actuelle

Établi par observation Home Assistant en lecture seule (rétention Recorder
≈ 30,8 jours, `purge_keep_days: 30`).

| Entité | Historisée ? | Rôle probatoire |
|---|---|---|
| `sensor.humidite_relative_sdb_parents` | Oui (pas 0,1 ; réémission ~1 pt) | Entrée — épisodes SdB parents |
| `sensor.humidite_relative_sdb_enfants` | Oui (**valeurs entières**) | Entrée — granularité dégradée |
| `sensor.humidite_relative_sejour` | Oui | Entrée — séjour |
| `sensor.humidite_absolue_sdb_parents` | Oui | Test psychrométrique |
| `sensor.co2_sejour` | Oui | Voie CO₂ |
| `input_boolean.vmc_haute_vitesse` | Oui | **Voir §2.1** |
| `switch.vmc_l1` / `switch.vmc_l2` | **Non** | Sorties relais non reconstituables |
| `binary_sensor.vmc_haute_vitesse_requise` | **Non** | Décision métier non historisée |

### 2.1 Statut exact de `input_boolean.vmc_haute_vitesse`

> **Cette entité n'est pas une « preuve d'exécution » au sens physique.** C'est
> une **trace de l'état de haute vitesse, non corroborée par la décision ni par
> les sorties relais historisées.**

La concordance **décision → commande → exécution** n'est donc pas démontrable par
plusieurs sources indépendantes : toute observation du comportement en haute
vitesse repose sur cette trace unique. **C'est un fait constaté** ; la question
de savoir s'il est acceptable est tranchée ci-dessous.

> **Exigence posée par L3, tranchée en L4.**

**Décision propriétaire (2026-07-21) — la trace est jugée suffisamment
autoritative par construction.** Aucune exposition diagnostique supplémentaire
n'est requise ; ni la décision ni les relais ne seront historisés.

Éléments qui étayent cette conclusion, établis par l'audit :

- le reflet est écrit **depuis l'état des relais** (`synchro_booleen`), non
  depuis la décision — il rapporte donc bien une commutation, pas une intention ;
- le module de commande est en **mode couplé** (`detach_relay = DISABLE`) et
  **sans déclencheur externe** configuré : il n'existe **aucune voie de commande
  hors Home Assistant** ;
- une divergence ne pourrait donc provenir que d'un **échec de commande**
  (MQTT/Zigbee) ou d'une perte de lien, non d'une action manuelle non tracée.

**Limites conservées**, qui ne remettent pas en cause la décision :

- le reflet n'est **pas** une preuve du débit physique — aucun retour moteur
  n'existe (§3.F) ;
- il **n'est pas mis à jour** tant que l'état relais est invalide (`l1 = l2`) et
  conserve alors sa dernière valeur.

### 2.2 Statistiques long-terme

Non confirmées (l'API WebSocket Recorder a échoué sur la session d'observation).
À supposer présentes, leur granularité horaire/quotidienne serait **trop
grossière** pour des pics de douche dont la montée dure 3 à 35 minutes. **Elles
ne résolvent pas la libération (§5.E).**

---

## 3. Matrice décision → preuve

Pour chaque paramètre ouvert : preuve suffisante / méthode / critère
d'acceptation / propriétaire de l'acquisition.

### A — Périmètre des pièces (§14.1)

| Pièce | Bouche | Capteur | Preuve suffisante | Critère |
|---|---|---|---|---|
| **SdB parents** | Oui | Oui | Déjà admissible ; épisodes majeurs observés | Aucune preuve neuve |
| **SdB enfants** | Oui | Oui (entiers) | Salle de douche → admissible **par nature** | ≥ 1 usage réel étiqueté produisant un pic mesurable |
| **Séjour** | Oui | Oui | Existence d'un besoin humidité **local** relevant d'O1/O2, distinct du fond diurne | Montées rapides propres au séjour sur 30 j → justifier ; sinon **classer O3, retirer de la voie humidité** |
| **WC étage** | Oui | **Non** | — | Hors périmètre : aucun capteur d'humidité |

> Une bouche d'extraction ne prouve pas un besoin humidité autonome. Le séjour
> est le cas test de cette règle.

### B — Critère de niveau (§14.2)

| Sous-question | Preuve suffisante | Critère |
|---|---|---|
| Seuil absolu seul insuffisant | **Acquis** (audit de calibrabilité L2) | — |
| Niveau comme voie d'entrée forte | Part des épisodes captés par un niveau haut, sur épisodes étiquetés | Décision métier sur le taux visé |
| Distinguer épisode / régime diurne | Profil diurne sur journées calmes | Amplitude diurne caractérisée avec incertitude |
| Frontière de libération | Voir E |

### C — Critère d'évolution (§14.2, §2.2 bis)

| Paramètre | Preuve suffisante | Méthode | Réserve |
|---|---|---|---|
| Durée nominale de fenêtre | Séparation nette épisodes / bruit, stable sur plusieurs largeurs | Rejeu hors ligne 15/30/60 min | — |
| Profondeur minimale | Idem, avec cas de fenêtre partielle (§9.1 bis) | Rejeu | — |
| Valeur de référence | Référence glissante vs figée | Rejeu | Glissante = historique borné (§2.2 bis) ; figée = seuil absolu |
| Grandeur + frontière d'évolution | Courbe détection/faux positifs par seuil, sur épisodes **étiquetés** | Rejeu | Indécidable sans étiquetage |
| Sensibilité au pas de restitution | Effet mesuré SdB parents vs SdB enfants (entiers) | Rejeu comparatif | **SdB enfants : critère possiblement inopérant** — 1 point/fenêtre de 15 min |
| Intervalles irréguliers | Robustesse aux trous d'échantillonnage | Rejeu | Intervalle médian SdB parents 4 min, p90 24,7 min |

**La preuve doit séparer quatre causes** : bruit/réémission, évolution physique
réelle, variation diurne, épisode humide réel. Cela **exige l'étiquetage** (§4.D).

### D — Combinaison « niveau OU évolution »

| Preuve suffisante | Méthode |
|---|---|
| Le scénario domine les alternatives sur épisodes étiquetés | Rejeu comparant, sur le **même jeu étiqueté** : taux de détection, épisodes manqués, faux positifs, durée d'activation théorique, comportement au redémarrage avec fenêtre insuffisante |

Critère : détecter les épisodes vespéraux modestes **sans** dépasser un plafond
de faux positifs, fixé une fois la variabilité connue.

### E — « Suffisamment assaini » et frontière OFF (§14.2)

> **Distinction fondatrice (arbitrage 2026-07-21).** La frontière de libération
> est un **niveau**, non une **cinétique**.
>
> - le **niveau** dit *à quel point de retour* on libère le besoin ;
> - la **cinétique** dit *combien de temps* il faut pour l'atteindre.
>
> Quelle que soit la vitesse d'extraction, **on s'arrête au même niveau** — on y
> parvient seulement plus ou moins vite. **Une redescente observée en haute
> vitesse renseigne la cinétique ; elle ne fixe pas la frontière.**

**Conséquence : « suffisamment assaini » est calibrable dès maintenant**, sur
l'historique Recorder existant, sans attendre d'épisode en haute vitesse.

| Objet | Nature | Preuve suffisante |
|---|---|---|
| **Frontière de libération** (le niveau) | **Paramètre §14** | Ligne de base de la pièce, établie sur l'historique disponible, plus la marge de bande morte |
| Cycle diurne | Contexte du précédent | Profil sur journées calmes |
| Chute rapide vs traîne | **Cinétique** | Observable en basse vitesse ; ne fixe aucune frontière |
| Désorption vs dilution | **Cinétique** | Non requis pour fixer la frontière |
| **Durée réelle d'activation en haute vitesse** | **Effet attendu à vérifier (§15)**, non paramètre | Observable **après** mise en conformité |

**Garde-fou requalifié.** L'interdiction antérieure — « ne jamais calibrer la
libération sur des redescentes de basse vitesse » — visait la **cinétique**.
Appliquée au **niveau**, elle bloquait à tort. Elle devient :

> Une **cinétique** mesurée en basse vitesse ne doit pas être présentée comme
> celle du régime renforcé, ni servir à prédire une durée d'activation. En
> revanche, le **niveau** de retour, lui, se déduit légitimement de l'historique
> disponible : il ne dépend pas du régime.

**Critère de ressenti (arbitrage propriétaire).** L'objectif n'est pas
d'optimiser un assèchement physique jusqu'à un état cible démontré, mais
d'obtenir un comportement satisfaisant : la VMC doit réagir quand l'humidité
d'une salle de bain monte du fait d'une douche ou d'un bain. La frontière de
libération doit être fixée en conséquence — **retour vers l'état habituel de la
pièce**, non poursuite d'un optimum hygrométrique.

### F — Effet de la haute vitesse — *le débit n'est pas une preuve requise*

> **Décision propriétaire (2026-07-21).** Le fait que la haute vitesse produise
> un effet réel **est acquis par la connaissance d'usage** et n'a pas à être
> démontré. **La mesure du débit sort du chemin critique du chantier.**

Quatre grandeurs, dont **une seule** est probatoire ici :

| Grandeur | Statut |
|---|---|
| Débit nominal constructeur (L / H) | **Information de contexte.** Non requise |
| Débit réel de l'installation | **Information de contexte.** Non requise |
| Gain relatif L → H | **Information de contexte.** Non requise |
| **Effet observé sur l'humidité** | ✅ **Seule grandeur probatoire** — c'est elle qui calibre « suffisamment assaini » (§E) |

**Motif de la requalification.** Connaître un débit nominal n'apporte rien
d'opérationnel aux paramètres ouverts : « suffisamment assaini » se calibre sur
l'**effet observé**, la durée minimale sur la protection du relais et la
condition métier, le coût acoustique et énergétique sur le ressenti. Le débit
avait été promu « preuve prioritaire » sur l'hypothèse qu'un écart négligeable
aurait vidé la révision de son objet — **hypothèse écartée**.

**Conséquences :**

- **aucune identification du moteur n'est requise** ;
- **aucune inspection terrain du caisson n'est requise** ;
- **aucune mesure anémométrique, électrique ou d'achat de matériel** n'est requise ;
- ce qui reste nécessaire relève de **§E** — observer une redescente pendant que
  la haute vitesse tourne — c'est-à-dire d'**observabilité**, non de matériel.

> **Garde-fou conservé.** Si un jour une affirmation quantitative sur le débit
> devenait nécessaire, un proxy de cinétique **ne la fournirait pas** : il mêle
> débit, conditions de l'épisode, hygrométrie extérieure et désorption. Cette
> réserve reste valable, mais **aucune preuve du chantier n'en dépend**.

### G — Durée minimale d'exécution (§14.4)

| Composante | Preuve suffisante | Propriétaire |
|---|---|---|
| Protection du relais | **Spécification de cyclage du module** | Terrain — fiche module |
| Stabilité de la commande | Absence de battement sur `input_boolean.vmc_haute_vitesse` | arsenal-runtime |
| Bénéfice aéraulique | Dépend de E | — |
| Coût acoustique / énergétique | Mesure ponctuelle (dB, W) | Terrain |

> La spécification du module doit être auditée avant toute décision de durée de
> protection. À défaut, 15 min ne peut être ni reconduit ni supprimé.

---

## 4. Sources de données

### A — Recorder actuel
Rétention ≈ 30,8 j. **Ne pas augmenter `purge_keep_days` de façon permanente et
large.** Relais et décision hors historique (§2).

### B — Sauvegardes Home Assistant non chiffrées — **voie privilégiée**
Voie éprouvée par `arsenal-runtime` : sauvegarde `.tar` non chiffrée → NAS →
extraction hors ligne de `home-assistant_v2.db` → analyse `mode=ro` → provenance
SHA-256 → base **non versionnée, supprimée après usage**. Aucun accès API/SSH,
aucune charge durable sur Recorder.

> **Fenêtre de purge** : une sauvegarde fraîche contient 30 jours ; elle doit
> être prise **avant qu'un épisode ne sorte de cette fenêtre**.

### C — Mesure physique ponctuelle
**Sans objet pour le débit** (§3.F). Resterait envisageable pour la seule
composante acoustique/énergétique du §3.G, **si** elle devenait décisive —
ce qui n'est pas établi. **Aucun achat, aucune mesure, aucune inspection
matérielle n'est requise par le présent dispositif.**

### D — Étiquetage manuel minimal — **nécessaire**
Sans lui, C/D indécidables. Journal sobre, une ligne par épisode : date/heure
approx. début-fin, type (douche/bain), pièce, porte (ouverte/fermée), haute
vitesse constatée (oui/non), note atypique. Réaliste en usage domestique ;
aucune action artificielle.

---

## 5. Critères de suffisance — définis à l'avance

| Paramètre | Preuve suffisante | Seulement indicatif | Non concluant si |
|---|---|---|---|
| Séjour dans le périmètre | Montées locales rapides observées **ou** leur absence nette sur 30 j | Une montée ambiguë | Données trop rares |
| Forme du critère d'évolution | Séparation nette sur épisodes étiquetés, stable sur plusieurs largeurs | Bon score sur une seule largeur | Étiquetage insuffisant |
| « Assaini » / OFF (**niveau**) | Ligne de base de la pièce établie sur l'historique + marge de bande morte | Une seule journée de référence | Historique trop court ou trop bruité pour établir la base |
| ~~Débit L/H~~ | **Hors dispositif** (§3.F) — l'effet de la haute vitesse est acquis ; seule sa **conséquence observée sur l'humidité** est probatoire | — | — |
| Durée minimale | Spécification de cyclage | Absence de battement | Fiche introuvable |

**Minima opérationnels — proposés, motivés, non figés** : profil diurne sur
plusieurs journées calmes de météos variées (le L2 n'en avait que 2, insuffisant) ;
étiquetage couvrant matin marqué / soir modeste / ≥ 1 passage haute vitesse. Le
nombre exact dépend de la variabilité constatée, **révisable en cours de
collecte**. Aucune taille d'échantillon arbitraire.

---

## 6. Répartition des propriétaires

> **Frontière tranchée (gouvernance C35) :** *Arsenal est propriétaire de la
> définition des preuves et de leur interprétation métier ; `arsenal-runtime` est
> propriétaire de leur acquisition, extraction et reproductibilité
> opérationnelle.* Cohérent avec le précédent C15 et la doctrine « HA =
> intégration/UI ; Arsenal = sens/décision ».

| Élément | Propriétaire |
|---|---|
| Définition normative de la preuve, critères, confondants | **Arsenal** (le présent document) |
| Protocole d'observation | **Arsenal** |
| Sauvegardes, extraction de `home-assistant_v2.db` | **arsenal-runtime** |
| Scripts d'analyse hors ligne (`mode=ro`) | **arsenal-runtime** |
| Empreintes SHA-256, résultats reproductibles, conservation | **arsenal-runtime** |
| **Synthèse normative** des constats utiles au chantier, **après** campagne | **Arsenal** — sans recopier outils ni bases |
| Identification matériel, doc constructeur, mesures physiques | **Terrain** |
| Journal d'étiquetage des épisodes | **Terrain** |

> **Rien de ce qui appartient déjà à `arsenal-runtime` ne doit être déposé dans
> `arsenal`** : ni procédure d'extraction, ni script SQLite, ni base. `arsenal`
> reçoit la définition, le protocole et la synthèse consignée.

---

## 7. Facteurs confondants et garde-fous

| # | Confondant | Neutralisation |
|---|---|---|
| R1 | Variation diurne ≈ épisode vespéral (~6,8 pts) | Profil diurne établi **avant** tout seuil |
| R2 | Pas de restitution pris pour du signal | Mesure de bruit à pas homogène ; cas SdB enfants isolé |
| R3 | Proxy de cinétique pris pour un débit | Réserve conservée (§3.F) — **aucune preuve du chantier n'en dépend** |
| R4 | **Cinétique** de basse vitesse prise pour celle du régime renforcé | Garde-fou requalifié (§3.E) : la cinétique ne fixe aucune frontière ; seul le **niveau** est calibré |
| R5 | Épisode non étiqueté pris pour bruit (ou l'inverse) | Journal d'étiquetage |
| R6 | **Décision et relais non historisés** | **Non neutralisable par la conception — objet de L4** |
| R7 | Sauvegarde trop tardive (épisode purgé) | Cadence de sauvegarde < 30 j |

---

## 8. Ce qui est reporté à L4

L3 définit le dispositif **y compris les preuves actuellement impossibles**. Les
dépendances suivantes sont **explicitement reportées à L4** :

1. ~~**Corroboration de la haute vitesse (R6).**~~ **✅ tranché en L4
   (2026-07-21) : moyens suffisants.** La trace est jugée suffisamment
   autoritative par construction (§2.1). **Aucune exposition diagnostique, aucune
   modification de `recorder.yaml`.**
2. **Spécification de cyclage du module de commande**, préalable à la seule
   composante « protection du relais » de la durée minimale (§3.G) — le module
   est identifié, sa fiche est consultable sans intervention. **Reporté à L2b.**

> **L4 est soldé.** Aucune preuve du dispositif n'est plus en attente
> d'observabilité : la frontière de libération relève d'un **niveau** calibrable
> sur l'historique existant (§3.E), et la durée d'activation en haute vitesse est
> un **effet à vérifier après changement**, non un préalable.

> **L'exclusion actuelle d'une commande artificielle de la VMC reste intacte.**
> L'absence de voie passive fiable pour capturer des épisodes en haute vitesse
> **ne présume pas** qu'une activation manuelle sera nécessaire : L4 déterminera
> d'abord si les épisodes naturels futurs, une trace autoritative et un étiquetage
> minimal suffisent.

---

## 9. Séquencement

| Étape | Objet | Verrou |
|---|---|---|
| **L3** | Le présent dispositif | Documentaire ; ne crée aucun outil ni instrumentation |
| ~~**L4**~~ ✅ | ~~Audit des moyens d'observation — R6~~ **conclu (2026-07-21) : moyens suffisants** | Aucune exposition diagnostique, aucune instrumentation, aucune mesure matérielle |
| **L5** | Référence terrain — extraction Recorder et étiquetage. **Allégée** : plus d'attente d'un épisode en haute vitesse (§3.E) | Après L4 |
| **L2b** | Calibration, **uniquement** à partir de la référence L5 | Aucune correction runtime avant L2b soldé |

---

## 10. Ce que L3 solde, ce qui reste ouvert

**Soldé par L3** : matrice décision → preuve, critères de suffisance,
propriétaires, voie d'extraction privilégiée, garde-fous, séquencement,
formalisation de l'exigence de corroboration.

**Tranché en L4** : R6 — moyens suffisants, aucune exposition diagnostique.
**Reporté à L5** : la campagne (extraction + étiquetage). **Reporté à L2b** :
toute valeur, dont la frontière de libération et la spécification de cyclage du
module. **Retiré du dispositif** : la mesure du débit et toute identification
matérielle du moteur (§3.F), ainsi que l'attente d'une redescente en haute
vitesse (§3.E).

> **L3 ne prétend pas que toutes les preuves sont obtenables dans l'état
> actuel.** Il définit ce qu'il faut prouver et par quels moyens, en nommant
> explicitement ce que l'observabilité actuelle ne permet pas encore.
