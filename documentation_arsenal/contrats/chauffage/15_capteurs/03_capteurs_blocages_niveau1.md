# ==========================================================
# 🧠 ARSENAL — CONTRAT CAPTEURS DE BLOCAGES ABSOLUS NIVEAU 1
#     Immunité thermique — Frontières physiques et apports exogènes
# ----------------------------------------------------------
# Domaine : Chauffage / Blocages absolus
# Couche  : NIVEAU 1 — Priorité hiérarchique maximale
# Statut  : STRUCTURANT — FRONTIÈRE DE SÉCURITÉ CRITIQUE
# ==========================================================

## 🎯 Rôle global

Définir la **COUCHE DES SIGNAUX DE BLOCAGE ABSOLUS DU MOTEUR THERMIQUE**.

Cette couche regroupe exclusivement :

- des **CAPTEURS DE FRONTIÈRE NIVEAU 1 FINAUX**
- des **CAPTEURS STRUCTURANTS INDIRECTS DE DÉTECTION**

Ces capteurs détectent des **conditions physiques ou causales d'interdiction thermique non négociables**, notamment :

- ouverture de l'enveloppe thermique
- épisodes d'aération qualifiés
- apports thermiques externes non pilotés
- dynamiques thermiques anormales persistantes

Ces signaux constituent des **CAUSES D'INTERDICTION PRIORITAIRES** qui écrasent systématiquement :

- toute décision centrale
- toute autorisation d'exécution
- toute calibration thermique
- toute tentative de relance du chauffage

---

## 🧱 Frontière d'autorité protégée

**IMMUNITÉ THERMIQUE DU MOTEUR CHAUFFAGE**

Cette couche garantit que le moteur thermique :

- ne chauffe jamais en présence d'un apport concurrent
- ne chauffe jamais enveloppe ouverte
- ne calibre jamais sur des données polluées
- ne relance jamais dans un contexte physiquement invalide

---

## 🧭 Hiérarchie interne

La couche distingue strictement deux types de capteurs.

### 1️⃣ Capteurs de frontière NIVEAU 1

Ces capteurs :

- produisent directement un **blocage thermique absolu**
- constituent la **source normative finale consommée par la décision centrale**
- sont consommés par les mécanismes décrits dans `40_blocages.md`

### 2️⃣ Capteurs structurants indirects

Ces capteurs :

- détectent des signatures physiques ou dynamiques
- **n'induisent jamais de blocage direct**
- alimentent exclusivement des **frontières NIVEAU 1 finales explicitement documentées**

Un capteur structurant indirect ne doit jamais :

- déclencher directement un blocage
- être utilisé comme condition d'autorisation
- être consommé hors d'une frontière NIVEAU 1 documentée

Les capteurs structurants indirects ne doivent jamais être consommés
directement par une automatisation ou un mécanisme métier.
Ils doivent toujours transiter par une **frontière NIVEAU 1 finale**
explicitement documentée.
Toute consommation doit rester confinée aux mécanismes normatifs explicitement documentés.

Les **frontières NIVEAU 1 finales** constituent les seules autorités
capables de produire un blocage absolu.
Toute nouvelle frontière doit être explicitement documentée
dans cette couche avant d'être consommée ailleurs dans le système.

---

## ⛔ Interdictions cardinales (couche entière)

Les capteurs de cette couche :

- ne décident jamais d'un mode thermique
- ne participent jamais à la table de décision
- n'autorisent jamais une exécution
- ne modifient jamais une consigne
- n'écrivent jamais d'offset
- ne produisent jamais de calibration thermique
- ne déclenchent jamais d'action matérielle directe
- ne reçoivent jamais d'écriture externe (read-only logique)

---

## 🔒 Garanties exigées

Les capteurs de cette couche doivent garantir :

- **priorité hiérarchique absolue** sur toute autre couche
- valeurs binaires pures lorsque requis (`on / off`)
- détection déterministe et robuste
- indépendance totale vis-à-vis des décisions et paramètres
- fonctionnement **reload-safe / restart-safe / runtime-safe**
- absence totale d'effet de bord
- absence de dépendance à toute décision, consigne, offset ou mode thermique
  provenant des couches décisionnelles
- absence de dépendance circulaire avec les mécanismes de décision
  ou les capteurs produits par ces mécanismes

---

## 🛡 Doctrine de sûreté

La couche NIVEAU 1 privilégie volontairement la **stabilité systémique**.

Un **faux positif de blocage N1** constitue un risque majeur,
car il peut empêcher illégitimement le fonctionnement du chauffage.

Un **faux négatif ponctuel** peut être temporairement absorbé par les mécanismes
généraux de régulation, mais reste indésirable dès lors qu'il autorise une chauffe
dans un contexte physiquement invalide ou pollue les diagnostics thermiques.

Les capteurs de cette couche doivent donc privilégier :

- la **robustesse de détection**
- la **résistance aux faux positifs**
- la **stabilité temporelle**

plutôt qu'une sensibilité maximale.

La régulation thermique principale du système doit rester cohérente
même en l'absence temporaire ou permanente des capteurs de cette couche.
Cette couche **protège** la régulation — elle ne la gouverne pas.

---

## 🔗 Autorités aval autorisées

Les capteurs NIVEAU 1 peuvent être consommés par :

- `40_blocages.md` (mécanismes de blocage thermique)
- la décision centrale chauffage
- les pipelines normatifs d'aération
- l'invalidation des cycles thermiques
- les mécanismes de protection des modèles inertiels

Ces capteurs ne doivent jamais être consommés directement par
des automatisations applicatives hors des mécanismes listés ci-dessus.

Tout usage applicatif doit consommer exclusivement les **frontières NIVEAU 1 finales**
et jamais les capteurs structurants intermédiaires ou dérivés.

Toute consommation hors de ces mécanismes constitue une **violation contractuelle**.

---

## ⚠️ Risques systémiques surveillés

- faux positifs bloquant indûment le système
- faux négatifs autorisant une chauffe illégitime
- oscillations si hystérésis affaiblie
- contournement dans les automatisations
- pollution des modèles thermiques

---

## 📂 Capteurs de la couche

Les capteurs NIVEAU 1 et les capteurs structurants indirects sont documentés individuellement dans :

`03_capteurs_blocages_niveau1/`

Chaque fichier décrit :

- le rôle du capteur
- ses dépendances amont
- ses garanties
- ses interdictions d'usage
- ses consommateurs contractuels

### Frontières NIVEAU 1 finales

- `binary_sensor.fenetre_ouverte_maison_avec_delai`
- `binary_sensor.poele_en_fonction`

### Capteurs structurants indirects

- `binary_sensor.fenetre_ouverte_maison`
- `binary_sensor.signature_thermique_poele`
- `binary_sensor.presence_humaine_sejour`

### Capteurs structurants indirects — briques numériques dérivées

Ces capteurs représentent des **mesures physiques transformées
ou agrégées dans le temps** (fenêtres de moyenne, dérivées, deltas).
Ils ne constituent jamais une autorité de blocage directe.

- `sensor.sejour_delta_30min`
- `sensor.sejour_delta_60min`
- `sensor.sejour_co2_delta_30min`

### Canons de stabilisation d'orchestration

Ces capteurs fournissent des signaux stables pour l'orchestration aval.
Ils ne produisent aucun blocage direct et ne constituent pas des frontières N1.

- `binary_sensor.fenetres_maison_fermees_stable`

---

## 🔒 Statut d'autorité

**FRONTIÈRE D'IMMUNITÉ THERMIQUE ABSOLUE**

Toute violation des règles de cette couche constitue un **RISQUE SYSTÉMIQUE MAJEUR** pour le moteur thermique.

# ==========================================================
