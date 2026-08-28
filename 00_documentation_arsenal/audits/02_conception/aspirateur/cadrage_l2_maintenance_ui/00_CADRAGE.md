# Cadrage complet — domaine Aspirateur — **V4, ratifiée**

> ### 2026-08-28 — le cadrage est **ratifié** (`D-44`)
>
> Il devient la **référence architecturale opposable** des lots **L2**,
> **Maintenance**, **Notifications** et **UI**.
>
> **Cette ratification n'autorise aucune implémentation** hors du périmètre et
> des dépendances propres à chaque lot. La table d'engageabilité courante est en
> [`10_LOTS.md`](10_LOTS.md) §5.2 : **trois engageables, trois sous condition,
> deux bloqués**. **Ratifier n'est pas engager.**

> ### V4 — les quinze arbitrages sont rendus
>
> **Quatorze totalement, un partiellement** (`A-5`, sur ses seules icônes et
> ses cinq raccourcis). Le §7 change donc
> d'objet : il cesse d'énumérer ce qui n'est pas tranché, pour donner l'**état
> de décision** des quinze. Registre :
> [`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md).
>
> **Les §1 à §6 sont inchangés** — aucun fait, aucun relevé, aucune limite de
> preuve n'est modifié par un arbitrage.

> ### ⚠ Passage caduc — conservé pour l'historique, annoté le 2026-08-28
>
> **Le cadrage est ratifié depuis le 2026-08-28** — décision `D-44`,
> [`01_DECISIONS_ACQUISES.md`](01_DECISIONS_ACQUISES.md) §G bis. L'énoncé
> ci-dessous était exact jusqu'à cette date.
>
> **L'autorité courante est `D-44`.**

> **Le cadrage reste NON RATIFIÉ, et aucun lot n'est engageable.** Rendre les
> arbitrages ne ratifie pas le cadrage : `D-37` et `D-38` sont inchangées.

> **V3.1 — correction `R-4` : la synthèse du §7 annonçait encore quatorze arbitrages et omettait les trois apports de la V3.**

**Révision de dépôt :** `112ad3c3d64a619f8ec883dcd645ec0187d884bb` (`main`)
**État du domaine :** lot runtime **L1 livré**, mergé, déployé, rechargé et
vérifié passivement. **Aucun lot L2, aucune maintenance, aucune UI.**
**Statut :** cadrage **RATIFIÉ le 2026-08-28** — décision `D-44`. Il est la
**référence architecturale opposable** des lots L2, Maintenance, Notifications
et UI. **Trois lots engageables, trois sous condition, deux bloqués**
(`10_LOTS.md` §5.2). **Aucune implémentation n'est autorisée hors du périmètre
et des dépendances propres à chaque lot.**
**Version :** **V4** — les **quinze** arbitrages sont **rendus** : quatorze
totalement, un partiellement. Voir `11_ARBITRAGES_RENDUS.md` et
`DELTA_V3_2_V4.md`.
*(La V3.1 était la V3 normalisée en `LF`, avec les corrections `R-2` à `R-5` ;
la V3.2 corrigeait le seul finding `F-1`. Voir `DELTA_AUDIT_V2_V3.md`.)*

---

## 1. État de départ vérifié

| Contrôle | Résultat |
|---|---|
| `main` aligné sur `origin/main` | conforme |
| Arbre de travail | propre |
| Checker de domaine `check_aspirateur_contracts.py` | **27 contrôles, 0 écart** |
| **Auto-test du même checker** | **27 contrôles, 366 cas** — 66 conformes, 300 violations attendues détectées |
| Contrat transverse **`arsenal_self`** — `check_arsenal_self_contracts.py` | **10 tests, `T01` → `T10`, conforme** |
| Verdict de mission courant | `VALIDATION_EN_COURS` |

### 1.1 Runtime existant — cinq fichiers, et rien d'autre

```
04_input_texts/aspirateur/mission.yaml
10_scripts/aspirateur/lancer_mission.yaml
12_template_sensors/aspirateur/etat_canonique.yaml
12_template_sensors/aspirateur/motif_lisible.yaml
12_template_sensors/aspirateur/conditions_lancement_hors_carte.yaml
```

**Aucune automation. Aucune couche d'intention. Aucune surface Lovelace.**

---

## 2. Constats structurants

### 2.1 L'entretien est hors du contrat V1

Le chapitre `08_etats_et_observation.md` §6 exclut nommément toute
« mesure de rendement (… durée de vie des consommables) ». Aucun des quatorze
chapitres ne couvre l'entretien.

> **Conséquence.** Le lot Maintenance exige un **acte contractuel**.
> Arbitrage **A-6**.

### 2.2 La conduite et la supervision sont, elles aussi, un acte contractuel

> **Correction V2 — la V1 se trompait de nature.** Elle présentait L2 comme un
> **amendement de CI**. C'est faux.

Le texte de `ASP-INV-31` énumère **nommément** les gestes que la décision D-01
confierait à un second script : « Toute écriture vers le robot — sélection de
carte, intensité d'eau, aspiration, commande de mission, **interruption, retour
à la base** — passe exclusivement par lui. » `ASP-INV-42` le redit pour les
gestes de conduite.

Créer un second script de conduite **rompt ces deux invariants**, pas seulement
le contrôle qui les garde. Un checker amendé sans amendement du contrat rendrait
la CI verte sur une violation d'invariant restée intacte — exactement ce qu'un
contrat opposable interdit.

> **Arbitrage A-9 ouvert** : forme de l'acte contractuel L2 — nouveau chapitre
> de conduite, ou extension du chapitre `07` ? Situation **symétrique de A-6**,
> qui était correctement ouvert pour la Maintenance.

### 2.3 Portée exacte des verrous de CI

**`ASP-CI-11`** refuse, hors des cinq fichiers L1 : les deux helpers de mission,
**et** les lignes `action:` / `service:` valant littéralement `vacuum.<x>` ou
`roborock.<x>`.

> **Portée exacte — corrigée en V3.** Le chargeur du contrôle n'itère **que** les
> répertoires de premier niveau dont le nom correspond à `^\d{2}_`. Il balaie
> ainsi **1 772 fichiers**, sur les **1 794** que compte le dépôt. Restent hors
> balayage : `blueprints/`, `custom_components/`, `esphome/`, `zigbee2mqtt/`,
> `tools/`, `scripts/` et les YAML de racine.
> *La V2 écrivait « tout le YAML du dépôt » — dans le tableau même qui
> prétendait donner la portée exacte de chaque contrôle.*

**`ASP-CI-14`** ne parcourt **que** les cinq fichiers L1. Un fichier L2 nouveau
y échapperait : la primitive de démarrage, que le contrat n'autorise que sous
la garde fermée `ASP-INV-62`, circulerait sans contrôle.

> **Conclusion opposable, restreinte en V2.** Ce raisonnement vaut pour le lot
> de conduite et de supervision, qui appelle bien des services `vacuum.*`.
>
> **Il ne vaut pas pour le lot Maintenance.** La remise à zéro passe par une
> pression de bouton sur une entité native `button.…`, qui n'est **ni** un
> service `vacuum.*` **ni** un service `roborock.*`. `ASP-CI-11` ne l'attrape
> pas ; `ASP-CI-7`, seul contrôle qui connaisse le domaine `button`, ne balaie
> que `18_lovelace/` et `19_button_card_templates/`.
>
> **La seule primitive irréversible du périmètre Maintenance circule donc
> aujourd'hui sans aucune garde** — et le trou est **plus large** que la seule
> pression de bouton : tout appel d'appareil logé hors des répertoires balayés
> échappe également au contrôle. Le raisonnement que la V1 s'appliquait à
> elle-même — « ouvrir sans étendre créerait un trou de contrôle sur la seule
> primitive dangereuse du domaine » — vaut ici, et n'était pas tenu.
> **Arbitrage A-14 ouvert.**

### 2.4 Vidage du bac — fonction native autonome

**Fait arrêté par l'opérateur** (D-12) : le dock **vide physiquement et
automatiquement** le bac, hors des heures interdites configurées. Le compteur
relevé — 608 cycles depuis l'enregistrement de l'appareil en août 2022 — est
**cohérent** avec ce fonctionnement, sans l'établir.

**Qualification retenue : fonction native autonome du couple robot/dock.**
Ni geste opérateur, ni objet Arsenal.

| Point | Décision |
|---|---|
| Bouton, script, commande brute, lot Arsenal de vidage | **Aucun** |
| Compteur de cycles comme durée de vie d'un sac | **Proscrit** (D-17) |
| Absence de primitive Home Assistant confirmable | **N'est plus un manque fonctionnel** (D-18) |
| Observation | Arsenal **peut** notifier une **erreur** de dock ou de vidage, **si** un signal fiable existe (D-16) |

**Le signal fiable existe déjà et est déjà contractualisé.** Quatre des onze
valeurs du témoin d'erreur de dock sont exactement des défauts de vidage. Sa
valeur nominale est arrêtée par `ARB-5`, et le moteur L1 la lit **déjà** comme
condition de lancement. **Rien n'est à créer.**

**Deux bornes d'honnêteté, à écrire au contrat :**

1. Le champ protocolaire d'état de collecte **n'est exposé par aucune entité**.
   Un vidage **en cours** n'est pas observable depuis Arsenal ; seule l'**erreur**
   l'est.
2. Les entités qui porteraient la **fenêtre d'heures interdites** sont
   **désactivées**. Arsenal ne voit pas cette fenêtre et ne doit donc **jamais**
   construire une alerte d'absence de vidage : pendant la fenêtre, un silence
   est nominal et indiscernable d'une panne.

---

## 3. Faits établis par lecture de source

Détail et citations : `04_REFERENCES_SOURCES.md`.

| Fait | Établi |
|---|---|
| Les quatre plafonds sont des **constantes littérales** amont | oui — 300 h / 200 h / 150 h / 30 h |
| Le temps restant est calculé **par la bibliothèque**, avec une garde de valeur absente | oui — `<CONSTANTE> − <travail>` si le champ est renseigné, sinon **valeur absente** |
| Les capteurs exposent des **secondes**, converties en heures à l'affichage | oui |
| Aucun `state_class` ⇒ **aucune statistique longue durée** | oui |
| Primitive **envoyée** lors d'une remise à zéro | commande de remise à zéro, paramètre = nom du champ de travail |
| La bibliothèque **relit** aussitôt après l'envoi | oui |
| Le bouton Home Assistant **ne force aucun rafraîchissement d'entité** sur la voie V1 | oui — la variante A01 en porte un, l'absence est donc spécifique |
| Intervalles **nominaux** de planification | 30 s en local, 60 s en repli nuage — **périodes nominales, sans borne supérieure démontrable** |
| Aucune primitive de vidage exposée pour un appareil V1 | oui |

> **Deux corrections V2, appliquées après audit :**
>
> - **« 60 s est la borne haute » est retiré.** Le coordinateur replanifie
>   **à la fin** de chaque rafraîchissement : l'écart réel vaut au moins
>   l'intervalle augmenté de la durée du cycle et d'un décalage
>   d'échelonnement, et un `retry_after` l'allonge. De plus, 60 s est la cadence
>   du **repli nuage**, pas une borne : le coordinateur démarre en local à 30 s
>   et ne bascule que si la connexion locale échoue.
> - **« Le capteur remonte exactement au plafond, prédictible sans essai » est
>   reclassé.** Les sources établissent l'envoi et la relecture ; elles
>   n'établissent **pas** que le micrologiciel remet le champ à zéro. C'est un
>   **comportement prédit, non testé** — et c'est exactement ce que la
>   confirmation par relecture doit vérifier. Le classer en fait acquis retirait
>   son objet au contrôle.

> **Rappel de la correction déjà portée en V1.** Une version antérieure
> concluait qu'aucun plafond n'était déterminable et qu'un **test irréversible**
> s'imposait. Cette conclusion était fausse : elle reposait sur l'absence
> d'attribut côté Home Assistant, sans avoir lu la source amont.

---

## 4. Faits établis par observation passive

Détail sanitaire : `05_DIAGNOSTICS_SANITISES.md`.

- Appareil de **protocole V1**, modèle et micrologiciel relevés.
- **45 entités** au registre, **33 actives**, **12 désactivées**, aucune masquée.
- Les quatre valeurs brutes de travail **recoupent exactement** les états
  d'entités, une fois le calcul amont appliqué — à la seconde près.
- Le dock est de **type 5**, absent de l'ensemble des docks à bac reconnus par
  la bibliothèque, alors que l'appareil déclare la collecte automatique active.
  Désaccord **rapporté tel quel**, tranché par D-12.
- Aucune entité de la plateforme n'est historisée ; historique vide sur quatorze
  jours, aucune statistique. Conforme au chapitre `08` §6.
- Le dépôt ne porte **aucun** appel de service de notification en dur.
- **Le mode de connexion — local ou nuage — n'a pas été relevé.**

> **Correction V2.** La V1 présentait « aucun rafraîchissement observé à +87 s »
> comme une mesure de cadence. Ce n'en était pas une, et la V2 ne fonde plus
> aucune conclusion de cadence sur une observation d'instance.

---

## 5. Périmètre V1 Maintenance — arrêté

Quatre éléments : **filtre**, **brosse principale**, **brosse latérale**,
**nettoyage des capteurs**. Le dock ne porte ni filtre à charpie ni brosse de
lavage — les boutons correspondants sont conditionnés à une capacité absente de
cet appareil. Le vidage sort du périmètre.

Détail : `06_ENTITES_ENTRETIEN.md`.

---

## 6. Synthèse

| Domaine | Document | État |
|---|---|---|
| Entités et plafonds | `06_ENTITES_ENTRETIEN.md` | établi par source, vérifié par recoupement ; **seuil rendu en V4** |
| Machine L2 et writers | `07_MACHINE_L2.md` | vocabulaire **arrêté en V4 — 34 valeurs** ; partition ratifiée ; course résolue |
| Notifications | `08_NOTIFICATIONS.md` | canaux arrêtés ; **seuil et routage rendus en V4** |
| Interface | `09_UI.md` | **architecture arrêtée** par décision opérateur ; **vingt objets rendus en V4** ; confrontation du référentiel **obligatoire**, portée par le contrôle dédié `ASP-CI-28` |
| **Arbitrages rendus** | `11_ARBITRAGES_RENDUS.md` | **quatorze fermés, un partiel, zéro non rendu** |
| Lots | `10_LOTS.md` | **ratifié** — trois engageables, trois sous condition, deux bloqués (§5.2) |

---

## 7. État de décision des quinze arbitrages — **rendu en V4**

Les quinze arbitrages restent **isolés** dans `02_ARBITRAGES_OUVERTS.md`, jamais
comblés par déduction. **Ils sont désormais rendus** — quatorze totalement, un
partiellement.

| Réf. | Décision rendue | Statut |
|---|---|---|
| `A-1` | Seuil unique : **restant ≤ 10 %**, pour les quatre postes | **fermé** |
| `A-2` | Pression unique, aucun retry, fenêtre de **30 s**, **terminal explicite**, poste toujours dû | **fermé** |
| `A-3` | **Quatre** identifiants attribués — `…01` à `…04` | **fermé** |
| `A-4` | Vocabulaire de **34 valeurs**, énumérées writer par writer | **fermé** |
| `A-5` | Les **vingt objets** de la couche d'intention | **partiel** — icônes, cinq raccourcis |
| `A-6` | Nouveau chapitre **`14_entretien.md`**, amendement minimal du `08` | **fermé** |
| `A-7` | Capteur existant **intact** ; capteur de santé **neuf** en `U1` | **fermé** |
| `A-8` | **Pendant mission** → mobile ; **hors mission** → rien de nouveau | **fermé** |
| `A-9` | Nouveau chapitre **`15_conduite_et_supervision.md`** | **fermé** |
| `A-10` | Voie **`O1`** ; partition **`O`, `O-R`, `T`, `H`** ratifiée | **fermé** |
| `A-11` | Exclusion **par le verdict**, sans helper ; amarrage à **W3** | **fermé** |
| `A-12` | **Automation dédiée `10280000000004`**, deux déclencheurs | **fermé** |
| `A-13` | Confrontation **obligatoire**, objet fixé, **contrôle dédié `ASP-CI-28`** dans le checker existant | **fermé** |
| `A-14` | **Liste d'autorisation nominative** du seul script Maintenance | **fermé** |
| `A-15` | **30 s** mutualisées ; amarrage événementiel ; extensions de portée | **fermé** |

> ### ⚠ Passage caduc — conservé pour l'historique, annoté le 2026-08-28
>
> **Le cadrage est ratifié depuis le 2026-08-28** — décision `D-44`,
> [`01_DECISIONS_ACQUISES.md`](01_DECISIONS_ACQUISES.md) §G bis. L'énoncé
> ci-dessous était exact jusqu'à cette date.
>
> **`D-44` a ratifié le cadrage.** L'engageabilité courante est en
> [`10_LOTS.md`](10_LOTS.md) §5.2. **Ce qui reste vrai :** rendre un arbitrage
> n'engage aucun lot, et ratifier non plus.

> **Ce que rendre quinze arbitrages ne fait pas.** Cela ne ratifie pas le
> cadrage, et cela n'engage aucun lot. **`D-37` et `D-38` sont inchangées**, et
> [`10_LOTS.md`](10_LOTS.md) §5.1 maintient les huit lots à **non engageables**.

**Ce qui reste réellement ouvert** — **sept** points, dont **deux seulement**
relèvent encore d'un arbitrage partiellement rendu — est énuméré dans
[`11_ARBITRAGES_RENDUS.md`](11_ARBITRAGES_RENDUS.md) §7.

> **Une conséquence de ce cadrage est falsifiée par `A-1`.** L'énoncé, répété de
> la V1 à la V3.2, selon lequel « tout seuil raisonnable rendra l'élément
> *nettoyage des capteurs* dû dès le déploiement » est **faux à 10 %** : ce poste
> est à **13,38 %** de restant, donc **au-dessus** du seuil, et **aucun des
> quatre postes n'est dû au relevé**. L'énoncé est **conservé et daté** partout
> où il figure ; il était honnête **sans seuil connu**.

**Trois faits techniques restent par ailleurs non établis, et ne sont pas
complétés par déduction :**

- la **signature positive de l'arrêt** ;
- le **résultat effectif d'une remise à zéro** — comportement de micrologiciel
  prédit, non testé ;
- le **délai réel de propagation** vers l'entité, sans borne supérieure
  démontrable.
