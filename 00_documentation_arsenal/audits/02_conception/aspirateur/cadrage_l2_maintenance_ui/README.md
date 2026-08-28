# Artefact de cadrage — domaine Aspirateur Arsenal — **V3.2**

**Objet.** Livrable de chantier **non ratifié**, **antérieur à toute
implémentation**. Cet artefact est autonome : il doit permettre à une session
d'audit indépendante de vérifier les conclusions **sans accès à la conversation
d'origine et sans accès à l'instance Home Assistant**.

**Version :** **V3.2** — **la V3.1, corrigée du seul finding `F-1` de l'audit
du commit** (un compteur d'arbitrages resté à quatorze dans la table de contenu)
**et des deux libellés de version courante** signalés avec lui. Aucune autre
différence.

La **V3.1** était **la V3 normalisée en fins de ligne `LF`**, augmentée des
corrections documentaires `R-2` à `R-5` du contrôle documentaire final et de
l'annotation de levée de la réserve de chaîne de garde. La **V3** était
elle-même strictement corrective après réaudit delta de la V2.

**Relevés d'instance :** 2026-08-27 · **Artefact V3.2 constitué le :** 2026-08-28
**Dépôt de référence :** Arsenal — `main` à `112ad3c3d64a619f8ec883dcd645ec0187d884bb`
**Statut :** cadrage corrigé, **non ratifié**. **Aucun lot n'est engageable.**
**Arbitrages ouverts : quinze. Aucun rendu.**

> **Pourquoi une V3.1.** Treize des quinze fichiers de la V3 portaient des fins
> de ligne `CRLF`, alors que le manifeste déclarait `LF`. Le dépôt Arsenal
> impose `*.md text eol=lf` : committer ces fichiers les aurait normalisés, et
> **treize empreintes du manifeste auraient cessé de vérifier au moment même de
> l'intégration**. Les quinze fichiers sont désormais en `LF`, et le manifeste
> est **entièrement recalculé** sur les octets réellement destinés au dépôt.

---

## 1. Ce qui a changé depuis la V2

Le réaudit delta a conclu **`GO AVEC RÉSERVES`** : **26 des 27 findings levés**,
un partiellement (`M-6`), **aucune régression**, et **11 anomalies nouvelles**
dont trois majeures.

La V3 traite les douze points — `M-6` et `N-1` à `N-11`. Le détail est dans
**`DELTA_AUDIT_V2_V3.md`**, à lire en premier pour un contrôle documentaire.

**Les trois réserves majeures et leur traitement :**

| Réserve | Traitement V3 |
|---|---|
| `N-1` — le registre de couverture omis du lot L2 | Porté au lot, **conditionnellement à `A-9`**, et la règle est **généralisée** à toute création de chapitre contractuel |
| `N-2` — la clôture de la chaîne de retour sans écrivain déterminé | La valeur est **suspendue**, le décompte devient une **matrice à quatre issues**, et **`A-11` reçoit un second volet** |
| `N-3` — les fenêtres de relecture L2 ni spécifiées, ni couvertes, ni gardées | **`A-15` ouvert**, huit points à trancher séparément. **Aucune durée n'est proposée** |

**Deux sur-assertions retirées :** le nombre d'identifiants nouveaux, désormais
**conditionnel à `A-12`** ; et l'attribution de l'exigence d'atteignabilité à un
invariant, alors qu'elle relève d'un **checker**.

---

## 1 bis. Ce qui avait changé de la V1 à la V2

La V1 a reçu un verdict **GO AVEC RÉSERVES** pour l'intégration documentaire,
assorti de **3 bloquants, 11 majeurs, 8 mineurs et 5 informations**.

La V2 applique l'intégralité des corrections minimales demandées. Le détail
finding par finding est dans **`DELTA_AUDIT_V1_V2.md`**, qui est le document à
lire en premier pour un réaudit de delta.

Trois conclusions structurantes de la V1 ont été **retirées** :

| Conclusion V1 | Statut V2 |
|---|---|
| « 60 s est la borne haute de la cadence » | **Retirée.** 30 s et 60 s sont des périodes **nominales** ; aucune borne supérieure n'est démontrable |
| « L2 est un amendement de CI » | **Retirée.** C'est un **acte contractuel** touchant deux invariants opposables — arbitrage **A-9** ouvert |
| « Le capteur remonte exactement au plafond, prédictible sans essai » | **Reclassée** en comportement de micrologiciel **prédit, non testé** |

Le nombre d'arbitrages ouverts passe de **8 à 14**.

---

## 2. Contenu de l'artefact

| Fichier | Contenu |
|---|---|
| `README.md` | Ce document — contrôles attendus et limites de preuve |
| `DELTA_AUDIT_V2_V3.md` | **Correspondance finding → correction de la génération courante** — `M-6` et `N-1` à `N-11` |
| `DELTA_AUDIT_V1_V2.md` | Correspondance de la génération précédente, **conservée** — `B-1`…`B-3`, `M-1`…`M-11`, `m-1`…`m-8`, `i-1`…`i-5` |
| `00_CADRAGE.md` | Le cadrage complet corrigé |
| `01_DECISIONS_ACQUISES.md` | Registre des décisions opérateur déjà prises |
| `02_ARBITRAGES_OUVERTS.md` | Les **quinze** arbitrages ouverts |
| `03_REFERENCES_CONTRATS.md` | Références précises aux contrats et contrôles Arsenal |
| `04_REFERENCES_SOURCES.md` | Références Home Assistant 2026.8.3 et python-roborock 5.31.1 |
| `05_DIAGNOSTICS_SANITISES.md` | Extraits sanitaires, faits nécessaires uniquement |
| `06_ENTITES_ENTRETIEN.md` | Entités d'entretien et plafonds |
| `07_MACHINE_L2.md` | Machine d'états L2, trois writers, vocabulaires envisagés |
| `08_NOTIFICATIONS.md` | Architecture des notifications |
| `09_UI.md` | Architecture d'interface arrêtée |
| `10_LOTS.md` | Découpage proposé — **non ratifié** |
| `MANIFESTE.md` | Inventaire et SHA-256 |

---

## 3. Contrôles attendus de l'auditeur

### C1 — Intégrité

Recalculer le SHA-256 de chaque fichier et le confronter à `MANIFESTE.md`.
Le manifeste ne se couvre pas lui-même : **son intégrité est couverte
transitivement par l'empreinte de l'archive**, transmise hors bande dans le
message de remise. C'est cette empreinte d'archive qui fait la chaîne de garde,
et c'est bien celle qui est transmise.

### C2 — Chaîne de calcul des compteurs d'usure *(inchangé, réussi en V1)*

1. Vérifier dans `python-roborock` v5.31.1 les quatre constantes de
   `roborock/const.py` ;
2. vérifier dans `roborock/data/v1/v1_containers.py` que les propriétés
   `*_time_left` valent `<CONSTANTE> − <work_time>` **si le champ est
   renseigné, sinon `None`** ;
3. vérifier dans `homeassistant/components/roborock/sensor.py` au tag
   `2026.8.3` les quatre `value_fn` et l'unité native en secondes ;
4. **refaire l'arithmétique** de `06_ENTITES_ENTRETIEN.md` §3 depuis les valeurs
   brutes de `05_DIAGNOSTICS_SANITISES.md` §3.

Contrôle **falsifiable** : le restant de la brosse latérale (668 299 s) exclut
à lui seul trois des quatre constantes.

### C3 — Verrous de CI, avec leur portée exacte

Vérifier au dépôt, à la révision citée :

- `ASP-CI-11` refuse, hors des cinq fichiers L1, les deux helpers de mission
  **et les lignes `action:` / `service:` valant littéralement `vacuum.<x>` ou
  `roborock.<x>`** — et **rien d'autre** ;
- `ASP-CI-14` ne parcourt que les cinq fichiers L1 ;
- **`ASP-CI-20` ne parcourt lui aussi que les cinq fichiers L1** : une
  temporisation logée dans un fichier L2 y échapperait entièrement. C'est le
  fondement de l'arbitrage **`A-15`** *(ajouté en V3)* ;
- **`ASP-CI-7` ne balaie que `18_lovelace/` et `19_button_card_templates/`** :
  une pression de bouton sur entité native depuis un script échappe donc à tout
  contrôle. C'est le fondement de l'arbitrage **A-14** ;
- **`ASP-CI-11` ne balaie que les répertoires de premier niveau nommés `NN_`** —
  **1 772 fichiers sur 1 794** — laissant hors portée `blueprints/`,
  `custom_components/`, `esphome/`, `zigbee2mqtt/`, `tools/`, `scripts/` et les
  YAML de racine. *(Corrigé en V3 : la V2 écrivait « tout le YAML du dépôt ».)*
  **Le trou de `A-14` est donc plus large que la seule pression de bouton.**

> **Correction V2.** La V1 affirmait que la CI refusait « tout appel d'appareil
> hors des cinq fichiers L1 ». **C'est faux** et cela masquait un trou de
> contrôle réel sur la seule primitive irréversible du périmètre Maintenance.

### C4 — Conformité au contrat Notifications

Confronter `08_NOTIFICATIONS.md` au contrat et aux contrôles `T1` à `T6`.
Vérifier en particulier que la V2 ne promet plus une re-projection immédiate
après suppression manuelle.

### C4 bis — Aucun choix implicite sur les trois arbitrages sensibles

| Réf. | Ce qui doit être constaté |
|---|---|
| **`A-11`** | Aucune valeur de clôture de chaîne de retour n'est attribuée à un writer ; le décompte du vocabulaire est une **matrice**, jamais un nombre unique |
| **`A-12`** | Le nombre d'automations est **trois ou quatre** ; les identifiants nouveaux sont **deux certains plus un conditionnel** |
| **`A-15`** | **Aucune durée de fenêtre L2** n'apparaît — ni proposée, ni suggérée, ni citée en exemple |

### C5 — Cohérence du vocabulaire et totalité de la machine

- Les trois ensembles de writers sont deux à deux disjoints **et** la V2 ne
  présente **plus** cette disjonction comme une propriété de sûreté ;
- la **partition terminale** des valeurs est explicitement énoncée ;
- la définition de « mission ouverte » est **unique** et cohérente entre §3,
  §5.1 et §6 ;
- la table de réconciliation est **totale** et ne peut adopter aucune mission
  externe ;
- le décompte du vocabulaire est **conditionnel aux arbitrages `A-10` et
  `A-11` volet 2** — quatre issues possibles — et n'est donc pas arrêté ;
- l'exigence d'atteignabilité est attribuée à **`ASP-CI-18`**, jamais à un
  invariant du contrat.

### C6 — Frontière UI et duplication du référentiel

Confronter `09_UI.md` au chapitre `11_frontiere_ui.md`. Vérifier que la V2
**reconnaît** que la couche d'intention constitue une seconde matérialisation
du référentiel des segments, et ouvre l'arbitrage **A-13** au lieu de conclure
qu'aucun amendement de contrôle n'est nécessaire.

### C7 — Aucun arbitrage rendu

Vérifier que les **quinze** arbitrages de `02_ARBITRAGES_OUVERTS.md` sont
**posés et non tranchés**, et qu'aucun lot de `10_LOTS.md` n'est présenté comme
engageable. Le contrôle `C4 bis` porte sur les trois plus exposés au choix
implicite.

---

## 4. Limites de preuve

### L1 — Prouvé par lecture de source

Les quatre plafonds ; la chaîne de calcul et sa garde de valeur absente ;
la **primitive envoyée** lors d'une remise à zéro et la relecture par la
bibliothèque ; l'absence de forçage de rafraîchissement d'entité sur la voie
V1 ; les **intervalles nominaux** de planification du coordinateur et sa bascule
locale → nuage ; le périmètre à quatre éléments ; l'absence de primitive de
vidage exposée pour un appareil V1 ; la classification amont du dock.

### L2 — Prouvé par observation passive, daté et non reproductible

États d'entités, registre d'entités, valeurs brutes de diagnostic, services
exposés. L'auditeur ne peut vérifier que leur cohérence interne et leur accord
avec les sources.

### L3 — Déclaration opérateur

Le dock vide physiquement et automatiquement le bac (**D-12**). Le compteur
relevé est **cohérent** avec cette déclaration ; il ne l'établit pas. Régime de
preuve identique aux arbitrages `ARB-3` et `ARB-5` du contrat.

### L4 — Non établi

- **Le résultat effectif d'une remise à zéro.** Les sources établissent l'envoi
  de la primitive et la relecture par la bibliothèque ; elles n'établissent
  **pas** que le micrologiciel remet le champ à zéro. **Comportement prédit,
  non testé** — c'est précisément ce que la confirmation par relecture est
  censée vérifier. *(Déplacé de L1 en V2.)*
- **Le délai réel de propagation d'une remise à zéro vers l'entité.** Le
  coordinateur replanifie **après** la fin de chaque rafraîchissement : l'écart
  réel vaut au moins l'intervalle augmenté de la durée du cycle et d'un décalage
  d'échelonnement, et un échec ou un `retry_after` l'allonge. **Aucune borne
  supérieure n'est démontrable.** *(Déplacé de L1 en V2.)*
- **Le mode de connexion de l'instance** — local ou nuage. **Non relevé.** La
  cadence en dépend.
- La signature positive de l'arrêt. **Non déduite, non complétée.**
- Le comportement du témoin de session après un arrêt opérateur.
- Le comportement du capteur de fin de nettoyage sur un arrêt opérateur.

### L5 — Délibérément absent

Aucun secret, aucun identifiant d'appareil, aucune adresse, aucun jeton, aucune
trace complète de diagnostic, aucun chemin propre à une machine, **aucun patch
d'implémentation**, aucun fichier de dépôt modifié.

Les chemins cités sont **relatifs à la racine du dépôt Arsenal** et servent de
références de lecture, jamais de cibles d'écriture.

---

## 5. Ce que l'artefact ne demande pas

Aucun contrôle décrit ici n'exige de lancer une mission, de presser un bouton,
d'émettre un service d'appareil, ni d'écrire un helper.
