# ==========================================================
# 🧠 ARSENAL — NOTE D’AUDIT / PROPOSITION CIBLÉE
#     Ouvertures — Capteur hybride "avec délai" (Étage)
# ----------------------------------------------------------
# Statut :
#   Proposition ARCHI + correctif minimal (sans déploiement forcé)
#
# Objet :
#   Clarifier une ambiguïté de couche (structure vs qualification)
#   qui produit des effets de bord sur les consommateurs (M5/M6).
# ==========================================================


## 1) 🎯 PROBLÈME (constat précis)

### 1.1 Signal hybride détecté

Le capteur :

- `binary_sensor.fenetre_ouverte_etage_avec_delai`

(mis en œuvre dans `homeassistant/11_template_sensors/ouvertures/delai/etage.yaml`)

retourne `on` si :

- une fenêtre ENFANT est ouverte **immédiatement**
  (`binary_sensor.contact_chambre_arnaud` ou `binary_sensor.contact_chambre_matthieu`)
  **OU**
- une fenêtre PARENTS est ouverte **après qualification du délai**
  (`binary_sensor.fenetre_chambre_parents_ouverte_avec_delai == on`)

=> Un seul état binaire mélange deux sémantiques :
- **immediate / instantané** (N1/N2)
- **confirmé après temporisation** (canon temporel)

### 1.2 Propagation de l’ambiguïté (effet en chaîne)

Ce signal hybride est ensuite utilisé par :

- `homeassistant/11_template_sensors/ouvertures/delai/global.yaml`
  (agrégation de niveau “maison”)
  via :
  - `entree_open` (immédiat)
  - `sejour_ok` (confirmé délai)
  - `etage_ok` (hybride)

=> Le capteur “maison avec délai” hérite de la même ambiguïté.

### 1.3 Effet observable sur les consommateurs (ex: pipeline aération)

Dès qu’un consommateur (ex. M5/M6) déclenche sur un *edge* (OFF→ON / ON→OFF)
de ce signal composite, il ne peut pas distinguer :

- un `ON` issu d’une ouverture **immédiate**
- un `ON` issu d’une ouverture **confirmée après délai**

=> Résultat typique :
- des suspensions / reprises (M5/M6) déclenchées “trop tôt” (sur ouverture légitime),
- ou des transitions difficiles à stabiliser lors de consolidation des capteurs,
- ou des effets de bord lors de modifications de la couche Ouvertures.

Ce comportement n’est pas un bug du pipeline aération : c’est une **ambiguïté de couche**.


---


## 2) 📜 ANALYSE CONTRACTUELLE (justification)

Références directes au **Contrat Ouvertures** :

### 2.1 Séparation stricte des couches
Le contrat impose une séparation stricte entre :
- événement physique (N0),
- état normalisé (N1),
- état agrégé (N2),
- canons (stabilisation locale),
- fait métier qualifié,
- restitution UI.

### 2.2 Invariants pertinents
- **N2** : “agrège sans interpréter” ; pas de temporisation, pas de qualification.
- **Canons** : stabilisation temporelle localisée, sans qualification métier.
- **Timers** : définissent le temps, n’interprètent rien.
- **Faits métier** : posés explicitement (helpers), sans effet de bord.
- **UI** : lecture seule, peut agréger pour lisibilité, mais ne doit pas servir de signal décisionnel ambigu.

### 2.3 Violation constatée (au niveau de l’usage)
Le capteur `fenetre_ouverte_etage_avec_delai` est acceptable **comme capteur UI**
(composite pour lisibilité), mais devient **non conforme** dès qu’il sert de signal
à un moteur externe (chauffage / aération / alarme) car :

- il ne respecte plus une sémantique monocouche,
- il mélange instantané et confirmé dans un même état,
- il rend les edges non interprétables.

=> Le contrat n’interdit pas un composite UI ; il interdit implicitement
qu’un composite UI serve de pivot d’orchestration.


---


## 3) 🧱 SOLUTION PROPOSÉE (minimaliste, posée, sans refonte)

### 3.1 Principe
Restaurer la pureté des signaux en séparant explicitement :

1) **signal instantané (sans délai)** — “ça vient de s’ouvrir”
2) **signal confirmé (avec délai)** — “c’est réellement ouvert après grâce”

et ne conserver le composite que pour l’UI.

### 3.2 Capteurs à créer (1 à 2 maximum)

#### A) Capteur métier “Étage — sans délai”
Créer un nouveau binary_sensor (sémantique pure immédiate) :

- `binary_sensor.fenetre_ouverte_etage_sans_delai`

Rôle :
- `on` si une fenêtre enfant est ouverte immédiatement
  (base N1 : `contact_*`)

#### B) Capteur métier “Étage — avec délai confirmé”
Créer un second binary_sensor (sémantique pure confirmée) :

- `binary_sensor.fenetre_ouverte_etage_avec_delai_confirmee`

Rôle :
- `on` si une ouverture “avec délai” de l’étage est confirmée
  (actuellement : `binary_sensor.fenetre_chambre_parents_ouverte_avec_delai`)

### 3.3 Conservation du capteur composite existant (UI)
Conserver tel quel :

- `binary_sensor.fenetre_ouverte_etage_avec_delai`

Mais le reclassifier mentalement comme :
- **UI only / diagnostic**, interdit comme déclencheur métier.

=> Aucun besoin de casser l’UI existante.

### 3.4 Ajustement du global (maison) : signal métier vs signal UI
Dans `homeassistant/11_template_sensors/ouvertures/delai/global.yaml` :

- créer (ou exposer) un signal “maison bloquante” fondé sur les capteurs métier purs :

  `maison_bloquante =`
  - entrée immédiate
  - séjour confirmé
  - étage sans délai
  - étage confirmé

Et conserver, si désiré :
- le capteur global composite existant comme “UI”.

### 3.5 Re-câblage des consommateurs (M5/M6)
Principe contractuel :
- M5/M6 ne doivent écouter que des signaux métier interprétables.

Cible :
- M5 = déclenchement uniquement sur **réouverture bloquante confirmée**
- M6 = reprise uniquement sur **fin de réouverture bloquante confirmée** (avec stabilité)

Donc :
- ne plus déclencher M5/M6 sur `fenetre_ouverte_etage_avec_delai` (composite)
- déclencher sur le signal métier (maison_bloquante, ou équivalent)

NB : Ce document propose la direction ; l’audit suivant déterminera le point exact
où M5/M6 consomment aujourd’hui le signal composite et la correction minimale.


---


## 4) ✅ BÉNÉFICES ATTENDUS (sans promesse abusive)

- Edges redevenus interprétables (instantané ≠ confirmé).
- Réduction des comportements “bizarres” lors des modifications de capteurs.
- Respect strict des invariants contractuels (séparation couches).
- UI inchangée (si on conserve les composites UI).
- Correction localisée : 1–2 capteurs + un ajustement global + re-câblage M5/M6 ciblé.


---


## 5) 🔎 PÉRIMÈTRE DE L’AUDIT À POURSUIVRE (après cette note)

Objectif : confirmer précisément, dans l’implémentation actuelle :

1) Quel capteur global est consommé par :
   - le pipeline aération (M5/M6),
   - le chauffage (blocage / guards),
   - l’alarme (si concerné).

2) Vérifier que les capteurs “avec délai” (séjour/parents) sont bien des canons
   (stabilisation locale) et non des faits métier (helpers), conformément au contrat.

3) Vérifier la cohérence des triggers :
   - pas de dépendance à des composites UI,
   - pas de transitions ambiguës (ON/OFF) utilisées comme signaux décisionnels.

Fin de note.