# ==========================================================
# 🧠 ARSENAL — CONTRAT MÉTIER
#     Présence maison
# ==========================================================

## 📌 Statut
- **Contrat normatif et opposable**
- Domaine : **Transversal / Contexte global**
- Chemin : `homeassistant/documentation_arsenal/contrats/presence.md`

---

## 🎯 Objet du contrat

Ce contrat définit **la notion de "présence maison" dans Arsenal**,
ainsi que son **autorité**, sa **sémantique canonique** et
ses **modalités d'usage par domaine**.

Il établit :
- les **signaux de présence reconnus**,
- leur **portée normative**,
- leur **affectation par domaine fonctionnel**,
- les **invariants absolus** associés.

Ce contrat est **indépendant de toute implémentation technique**
et prime sur toute logique métier consommatrice.

---

## 🧱 Périmètre

Ce contrat couvre exclusivement :

- la **définition normative de la présence** dans Arsenal,
- la **distinction structurelle des usages de présence**,
- l'**autorité des signaux de présence par domaine**,
- les **interdictions de redéfinition locale**.

Il ne couvre pas :

- les mécanismes techniques de détection (GPS, Wi-Fi, helpers),
- les règles métier des domaines consommateurs,
- les implémentations YAML ou UI,
- les stratégies d'optimisation ou d'anticipation.

---

## 🧠 Principe fondamental

La **présence** est un **signal structurant de contexte**.

Elle :
- n'est **jamais décidée localement** par un domaine métier,
- n'est **jamais interprétée** "dans l'esprit",
- est **consommée telle quelle**, selon son domaine d'autorité.

La présence **ne décrit pas une intention**,
elle décrit **un état canonique exploitable**.

---

## 🧭 Présences canoniques reconnues

Le contrat reconnaît **deux présences canoniques distinctes**,
chacune ayant une **autorité exclusive par domaine**.

### 🔐 Présence Sécurité

- **Finalité** : protection des personnes et des biens
- **Domaine consommateur exclusif** :
  - sécurité
  - alarme
  - éclairage
  - surveillance périmétrique
- **Nature** :
  - détection stricte,
  - tolérance minimale aux faux positifs,
  - confirmation explicite de l'absence.
- **Rôle** :
  - décider si la maison est considérée **occupée ou non**
    du point de vue sécuritaire.

👉 La présence sécurité est **la seule autorité valide**
pour toute logique liée à la sécurité.

---

### 🌡️ Présence Confort (présence unifiée)

- **Finalité** : confort thermique, énergétique et d'usage
- **Domaines consommateurs** :
  - chauffage
  - climatisation
  - confort global
- **Nature** :
  - signal **stabilisé**,
  - tolérant aux fluctuations,
  - orienté expérience et sobriété.
- **Rôle** :
  - indiquer si le confort doit être maintenu ou réduit.

👉 La présence confort est **la seule autorité valide**
pour toute logique de confort.

### ⏱️ Temporalité et réactivité

La présence confort est un signal **stabilisé mais réactif**.

- Elle peut utiliser des temporisations courtes (quelques secondes),
  dès lors que l'architecture garantit :
    • absence d'écriture matérielle directe,
    • décisions centralisées et filtrées,
    • anti-redondance systématique.

- La présence confort peut donc être exploitée comme :
    • signal quasi temps réel de contexte,
    • sans risque d'oscillation thermique,
    • sans yoyo logique ou matériel.

👉 La réactivité de la présence confort est un **choix d'architecture validé**,
conditionné par :
  - séparation stricte décision / écriture,
  - pipelines idempotents,
  - matériel local ou fiabilisé.

La présence confort **ne devient pas un déclencheur** :
elle reste un **signal de contexte pur**, même à haute réactivité.

---

## 🧩 Séparation structurelle des usages

- La présence sécurité et la présence confort :
  - **ne sont pas interchangeables**,
  - **ne se substituent jamais l'une à l'autre**,
  - **ne se corrigent pas mutuellement**.

Un domaine :
- **consomme un signal de présence unique**,
- **ne choisit pas** entre plusieurs présences,
- **n'en redéfinit jamais la sémantique**.

---

## 🌍 Dépendance au modèle spatial

La présence canonique repose sur des états techniques
issus du modèle spatial (`zone`).
Ces états constituent des **projections techniques**
d'un même état canonique (`présent`).

### 🧠 Principe

Toute évolution du modèle spatial (création, modification,
suppression d'une zone) impacte potentiellement :
- les capteurs de présence,
- les vérités de présence canoniques,
- les signaux consommés par les domaines.

### ⚖️ Obligation

Toute modification du modèle spatial impose
une **revue explicite et exhaustive** de :
- toutes les vérités de présence amont,
- toutes les vérités de présence canoniques,
- tous les capteurs utilisant des états de type `person.*`.

Aucune évolution spatiale ne peut être considérée
comme terminée sans validation de cohérence
sur les signaux de présence.

### 🛑 Interdiction

Il est interdit de :
- supposer une hiérarchie implicite entre zones,
- considérer qu'un état spatial couvre automatiquement un autre,
- introduire une nouvelle zone sans analyser son impact
  sur la sémantique de présence.

### 📌 Rappel technique

Home Assistant ne gère pas de hiérarchie de zones.
Chaque état de `person` est évalué littéralement.

---

## 🧭 Zones reconnues comme présence

Le système distingue :
- les zones de présence (valides pour état `présent`)
- les zones non contributives

### ⚖️ Règle

Une zone n'est considérée comme présence
que si elle est explicitement reconnue comme telle
dans la logique de présence.

### 🛑 Interdiction

Il est interdit de :
- considérer qu'une zone est implicitement une présence,
- dériver la présence à partir d'une relation géométrique,
- étendre automatiquement la notion de présence
  lors de l'ajout d'une zone.

### 📌 Conséquence

Toute nouvelle zone doit être :
- soit explicitement intégrée à la présence,
- soit explicitement exclue.

Toute zone reconnue comme contributrice à la présence
doit être explicitement intégrée dans les listes de projections
définies au § "États techniques de projection reconnus".

---

## 🧾 États techniques de projection reconnus

Les états suivants constituent les **projections techniques valides**
de l'état canonique `présent`, par présence.

Ces listes sont **normatives** :
tout état absent de la liste est **non valide** pour la présence concernée,
quelles que soient ses propriétés géométriques ou sémantiques.

Tout état `person.*` non explicitement listé,
y compris `not_home`, est considéré comme `absent`.

### 🔐 Présence Sécurité — projections valides

| État `person.*`       | Valide ? | Motif                                     |
|-----------------------|----------|-------------------------------------------|
| `Maison – Sécurité`   | ✅ oui   | périmètre maison strict                   |
| `home`                | ❌ non   | périmètre trop large, non contrôlé        |
| `Approche – Sécurité` | ❌ non   | infra uniquement, hors périmètre sécurité |

### 🌡️ Présence Confort — projections valides

| État `person.*`       | Valide ? | Motif                              |
|-----------------------|----------|------------------------------------|
| `home`                | ✅ oui   | périmètre domestique général       |
| `Maison – Sécurité`   | ✅ oui   | inclus dans le périmètre confort   |
| `Approche – Sécurité` | ✅ oui   | approche intégrée au confort       |

### 🛑 Interdiction croisée

`Approche – Sécurité` est valide pour le confort
et **explicitement invalide** pour la sécurité.

Cette asymétrie est **intentionnelle et non négociable**.
Elle ne constitue pas une incohérence :
elle reflète des périmètres contractuellement distincts.

### ⚖️ Obligation de maintenance

Toute modification de ces listes :
- est une **évolution contractuelle**,
- impose une revue des capteurs de présence concernés,
- fait l'objet d'une entrée de changelog Arsenal.

---

## 🔌 Projection technique canonique

Chaque présence canonique est matérialisée
par **une entité unique**, point d'accès exclusif
pour les domaines consommateurs.

Cette section est une **référence technique courante**.
Elle est opposable dans l'état où elle se trouve,
et doit être mise à jour à chaque renommage ou restructuration.

### Entités canoniques en vigueur

| Présence canonique | Entité référente                          |
|--------------------|-------------------------------------------|
| Sécurité           | `binary_sensor.presence_famille_securite` |
| Confort            | `binary_sensor.presence_famille_unifiee`  |

### ⚖️ Règle d'usage

- Un domaine consommateur **ne consulte que l'entité canonique**
  qui lui est attribuée par ce contrat.
- Aucune logique métier ne peut lire directement
  un état `person.*` pour en dériver une présence.
- Toute duplication ou recalcul parallèle
  de la vérité de présence est **interdite**.

---

## 🔒 Invariants absolus

Les invariants suivants sont **non négociables** :

- la présence n'est **jamais décidée** par un domaine consommateur,
- la présence est **binaire et canonique** (`présent` / `absent`),
- la présence canonique peut admettre **plusieurs états techniques de projection**
  représentant un même état (`présent`),
  sans créer de nouvelle classe de présence,

- tout état technique supplémentaire (ex : "Maison – Sécurité") :
  - est un **sous-état de projection**,
  - ne modifie PAS la binarité canonique,
  - ne crée PAS une nouvelle présence contractuelle,

- aucune logique métier ne peut :
  - recalculer la présence,
  - la corriger localement,
  - l'interpréter différemment selon le contexte,
- sécurité et confort utilisent **des présences distinctes**,
- toute ambiguïté de présence est traitée **avant consommation**,

- la présence peut être exploitée avec des temporisations courtes,
  à condition qu'aucune écriture matérielle ne soit déclenchée directement,
  et que toute décision soit filtrée par une gouvernance centrale.

Tout comportement qui viole un invariant
est **non conforme**, même s'il est fonctionnel.

---

## 🛑 Interdictions formelles

Il est strictement interdit :

- de fusionner présence sécurité et présence confort,
- d'utiliser une présence "par défaut" faute de mieux,
- de déclencher une logique de sécurité
  sur une présence de confort,
- de déclencher une logique de confort
  sur une présence de sécurité,
- de créer une présence locale à un domaine métier,
- de dégrader la sémantique de la présence pour "simplifier",
- de lire un état `person.*` directement
  depuis un domaine consommateur.

---

## 🧠 Principe Arsenal

> La présence est un **contrat de vérité contextuelle**.
>
> Un domaine ne choisit pas ce qui l'arrange :
> il consomme le signal qui lui est contractuellement attribué.

---

## 🔁 Évolution du contrat

Toute évolution de ce contrat :

- est **explicite**,
- est **documentée**,
- fait l'objet :
  - d'une modification contractuelle,
  - d'une entrée de changelog Arsenal,
  - d'une validation humaine consciente.

Aucune évolution implicite n'est autorisée.

---

## 📌 Clause finale

Ce contrat :

- prime sur toute implémentation existante,
- prime sur toute logique métier,
- prime sur toute intuition "raisonnable".

Toute production qui ne s'y conforme pas
est **INVALIDE**.
