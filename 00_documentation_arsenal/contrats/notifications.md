# 🧠 ARSENAL — CONTRAT NORMATIF · NOTIFICATIONS

## 🎯 OBJET DU CONTRAT

Ce contrat définit le **cadre normatif global** de conception,
d’utilisation et d’interprétation des **notifications dans Arsenal**.

Il établit :

- la **distinction fondamentale** entre les types de notifications,
- leur **statut informationnel** (état vs événement),
- leur **cycle de vie attendu**,
- leurs **invariants de cohérence UI**,
- leur **non-substitution** aux autres mécanismes Arsenal
  (logbook, dashboards, diagnostics).

Ce contrat a vocation à être **enrichi progressivement**.  
Il constitue une **référence structurante**, destinée à aligner
l’ensemble du système sur un modèle cohérent et durable.

---

## 🧱 PÉRIMÈTRE COUVERT

Le présent contrat couvre :

- les **notifications éphémères** (mobiles),
- les **notifications persistantes**,
- leur rôle dans la restitution de l’état du système,
- leur articulation avec :
  - l’UI,
  - le logbook,
  - les automatisations décisionnelles.

Il ne couvre pas :

- le design graphique des notifications,
- les mécanismes techniques spécifiques aux plateformes mobiles,
- la hiérarchisation des priorités visuelles (traitée ailleurs),
- les stratégies de regroupement ou d’agrégation futures.

---

## 🧠 PRINCIPE FONDAMENTAL

Dans Arsenal :

> **Une notification n’est jamais neutre.**

Elle est soit :

- la **trace d’un événement**,
- soit la **projection d’un état courant**.

Toute confusion entre ces deux natures est **architecturalement invalide**.

---

## 🔔 TYPOLOGIE DES NOTIFICATIONS

### 1️⃣ Notification éphémère (mobile)

La notification éphémère est :

- **temporaire**,
- **événementielle**,
- destinée à attirer l’attention à un instant donné.

Elle sert à signaler :

- un changement notable,
- une action utilisateur pertinente,
- une information ponctuelle.

Caractéristiques :

- elle **peut disparaître sans laisser de trace**,
- elle **ne représente jamais un état durable**,
- elle **ne fait pas autorité** sur la situation courante.

👉 Une notification éphémère **n’est pas un état**.

#### 🏷️ Titre mobile — Emoji obligatoire

Toute notification mobile émise via le canal central — `script.notification_envoyer`,
`script.notification_envoyer_famille`, `script.notification_envoyer_avance` — doit
fournir un champ `titre:` commençant par un **emoji de domaine**, au même titre
qu’une notification persistante.

Cette règle prolonge au canal mobile le format normatif défini plus bas
(§ « FORMAT NORMATIF DES NOTIFICATIONS ») : l’emoji de tête identifie le domaine
fonctionnel sur l’écran de verrouillage, sans dépendre du message ni du contexte
d’appel.

Sont non conformes :

- un `titre:` sans emoji initial,
- un `titre:` commençant par une lettre, même accentuée.

Exception explicite : un `titre:` entièrement dynamique (template Jinja `{{ … }}`)
ne peut pas être vérifié statiquement ; sa conformité relève de l’automatisation
émettrice. C’est la même tolérance que pour les titres persistants dynamiques.

Exemples conformes :

- `👶 Matthieu`
- `🔋 Audi A3 e-tron`
- `🚨 Badge inconnu`

---

### 2️⃣ Notification persistante

La notification persistante est :

- **durable tant que l’état qu’elle représente est vrai**,
- **décisionnelle**,
- considérée comme une **projection UI de l’état métier courant**.

Elle sert à exposer :

- une situation active,
- un contexte en cours,
- un état saillant nécessitant une lisibilité continue.

👉 Une notification persistante **n’est jamais un historique**.

#### 🏷️ Titre persistant — Emoji obligatoire

Toute notification créée via `persistent_notification.create`
doit posséder un titre commençant par un **emoji de domaine**.

Cette règle est obligatoire car la notification persistante est une
projection UI durable de l’état métier courant : son domaine doit être
identifiable immédiatement, sans dépendre du texte long ni du contexte
d’appel.

Format minimal obligatoire :

> **<emoji> <Titre lisible>**

Sont non conformes :

- un titre sans emoji initial,
- un titre commençant par une lettre, même accentuée,
- un titre commençant par un symbole non fonctionnel,
- un titre dynamique dont la conformité ne peut pas être vérifiée
  explicitement.

Exemples conformes :

- `💨 Aération conseillée – RDC`
- `🔥 Chauffage – Mode Confort`
- `🚿 ECS – Bouclage actif`

---

----------------------------------------------------------
🔀 CANAUX AUTORISÉS SELON LA NATURE INFORMATIONNELLE
----------------------------------------------------------

Cette section définit la **correspondance normative obligatoire**
entre :

- la nature informationnelle d’une notification (état / événement),
- et les **canaux de restitution autorisés** dans Arsenal.

Elle constitue une règle **structurante transverse**.

---

## 🔹 Principe fondamental de canal

Dans Arsenal :

- un **état** se restitue par un **canal persistant**,
- un **événement** se restitue par un **canal éphémère**.

Toute inversion de ce principe constitue :

> une **violation sémantique**,  
> une **dette cognitive**,  
> et une **erreur d’architecture UI**.

---

## 🟦 États métier → canal persistant obligatoire

Tout état métier durable :

- décision thermique,
- mode actif,
- contexte courant,
- situation prolongée,

doit être notifié :

- exclusivement par **notification persistante**,
- unique par état,
- recalculable à partir du seul état courant.

Il est **strictement interdit** :

- d’envoyer un push mobile pour un état durable,
- d’utiliser une notification éphémère pour représenter un état.

Exemples normatifs :

- 💨 Aération conseillée – RDC  
- 🔥 Chauffage – Mode Confort  
- 🚿 ECS – Bouclage actif  

Canal autorisé :
- notification persistante uniquement

Canal interdit :
- notification mobile

---

## 🟥 Événements opérationnels → canal mobile autorisé

Tout événement ponctuel :

- action humaine attendue,
- situation transitoire,
- risque immédiat,
- oubli utilisateur,
- alerte temporelle,

peut être notifié par :

- notification éphémère (mobile),
- éventuellement doublée d’un persistant secondaire.

Exemples normatifs :

- fenêtre ouverte trop longtemps  
- fermeture demandée  
- oubli nocturne  
- alarme déclenchée  

Canal autorisé :
- notification mobile prioritaire

Canal persistant :
- optionnel
- uniquement si un état durable en découle

---

## ⛔ Interdictions structurantes

Il est strictement interdit que :

- un état durable génère une notification mobile,
- un événement soit représenté par un persistant sans état associé,
- un push mobile remplace un persistant décisionnel,
- une notification mobile soit utilisée comme vue d’état.

---

## 🧠 Clause d’alignement obligatoire

Toute nouvelle notification Arsenal doit être validée selon :

1. Nature informationnelle :
   - état  
   - événement  

2. Canal autorisé correspondant :
   - persistant si état  
   - mobile si événement  

Toute notification ne respectant pas cette correspondance est :

> contractuellement invalide
> et candidate à refactor immédiat.

---

## 📌 Portée

Cette règle s’applique à l’ensemble des domaines :

- Chauffage  
- Aération  
- ECS  
- Énergie  
- Sécurité  
- Mobilité  
- Présence  

Elle constitue une **frontière sémantique majeure** de l’architecture Arsenal.

---

## 🧠 STATUT INFORMATIONNEL

### 🔹 Notification persistante = ÉTAT

Une notification persistante :

- décrit **exclusivement un état présent**,
- n’a **aucune valeur** une fois cet état devenu faux,
- ne doit **jamais survivre** à la disparition de l’état.

Deux comportements normatifs sont autorisés :

#### 🔁 Remplacement explicite
- un état A devient faux,
- un état B devient vrai,
- la notification persistante A est **disqualifiée**,
- la notification persistante B la **remplace**.

#### 📴 Extinction naturelle
- l’état devient faux,
- aucun nouvel état ne le remplace,
- la notification persistante est **supprimée**.

---

### 🔹 Notification éphémère = ÉVÉNEMENT

Une notification éphémère :

- signale qu’**un fait s’est produit**,
- peut être ignorée sans perte de cohérence,
- ne doit jamais être utilisée pour représenter un état durable.

---

## 🚫 INTERDICTIONS TEMPORELLES & ÉVÉNEMENTS DÉGUISÉS (PERSISTANT)

Cette section complète et précise le cadre normatif applicable
aux **notifications persistantes**, afin d’éliminer toute ambiguïté
entre **état courant** et **événement passé**.

---

### ⛔ Interdiction de référence au passé

Une notification persistante **ne doit contenir aucune information temporelle**.

Sont strictement interdits :

- timestamps (date, heure, `now()`, durée écoulée),
- compteurs, numéros de tentative ou d’occurrence,
- références à une action passée ou à un résultat,
- formulations de type :
  - « vient de… »
  - « a été… »
  - « relancé »
  - « échoué »
  - « tentative n°X »

👉 Toute notification persistante décrivant un fait passé
est considérée comme **sémantiquement invalide**.

---

### 🔁 Test de recalculabilité forte (obligatoire)

Toute notification persistante doit satisfaire le test suivant :

> Après un redémarrage complet de Home Assistant,
> sans log, sans historique, sans mémoire implicite,
> la notification doit pouvoir être **recréée correctement**
> à partir du **seul état courant**.

Si la notification dépend :

- d’un événement antérieur,
- d’un succès ou d’un échec passé,
- d’une action utilisateur,
- d’un compteur ou d’une tentative,

👉 elle est **contractuellement interdite**.

---

### ❌ Événement déguisé (violation contractuelle)

Est qualifiée **d’événement déguisé** toute notification persistante qui :

- est déclenchée par une action ou une transition,
- confirme un succès ou un échec,
- décrit un changement passé,
- ne possède pas de condition d’extinction explicite,
- ne peut pas être recalculée sans historique.

Un événement déguisé constitue :

> une **dette sémantique UI**
> et une **violation du contrat Notifications Arsenal**.

---

### 🧠 Vitalité & charge cognitive

Tout état candidat à une notification persistante
doit être évalué selon sa **vitalité informationnelle** :

- 🟥 **Vital**  
  L’état doit rester visible tant qu’il est vrai.
- 🟧 **Non vital**  
  L’état est réel mais peut disparaître sans conséquence.
- ❓ **Indéterminé**  
  Requiert une décision métier explicite.

👉 Un état **non vital** ou **indéterminé**
n’est **pas éligible par défaut**
à une notification persistante.

---

### 🧾 Clause de conformité rétroactive

Toute notification persistante existante
doit pouvoir être justifiée
au regard du présent contrat.

À défaut :

- elle peut être **techniquement fonctionnelle**,
- mais est considérée comme **architecturalement invalide**.

---

## 🔄 CYCLE DE VIE NORMATIF (PERSISTANT)

Pour une notification persistante :

1. **Apparition**
   - l’état devient vrai,
   - la notification est affichée.

2. **Maintien**
   - l’état reste vrai,
   - la notification reste visible.

3. **Disqualification ou extinction**
   - l’état devient faux,
   - la notification est remplacée ou supprimée.

👉 Il est interdit de conserver une notification persistante
dont l’état n’est plus valide.

---

## 🏷️ IDENTITÉ & UNICITÉ

Une notification persistante :

- est **unique par état métier**,
- ne doit **jamais être empilée**,
- peut être identifiée par un identifiant stable
  lorsqu’un remplacement est requis.

Il est interdit :

- d’avoir plusieurs notifications persistantes
  représentant le **même état**,
- d’utiliser une notification persistante
  comme journal d’événements.

---

## 🧠 SÉMANTIQUE IMPOSÉE

- Le **titre**, l’**alias** et l’**identité** d’une notification persistante
  décrivent **l’état**, jamais l’action.
- Les **actions suggérées** (ouvrir, fermer, activer, désactiver) :
  - sont contextuelles,
  - figurent uniquement dans le **contenu du message**,
  - ne définissent jamais l’identité de la notification.

---

## 🧾 FORMAT NORMATIF DES NOTIFICATIONS

Cette section définit le **format obligatoire** de toute notification Arsenal,
qu’elle soit **éphémère** ou **persistante**.

Elle vise à garantir :

- une **identification immédiate du domaine fonctionnel**,
- une **lecture homogène dans l’UI**,
- une **cohérence transverse** entre tous les sous-systèmes.

---

### 🏷️ Titre — Format imposé

Toute notification Arsenal **doit** posséder un titre conforme au format suivant :

> **<emoji> <Domaine> – <État ou situation>**

Pour les notifications persistantes, cette règle s’applique
obligatoirement à chaque appel `persistent_notification.create`.

Règles obligatoires :

- le titre commence **toujours par un emoji de domaine**,
- l’emoji est placé en tout début de titre,
- l’emoji est suivi d’un espace,
- l’emoji identifie le **domaine fonctionnel principal**,
- le titre décrit un **état** ou une **situation**, jamais une action,
- le séparateur canonique est : `–` (tiret demi-cadratin).

Exemples normatifs :

- `💨 Aération conseillée – RDC`  
- `🔥 Chauffage – Mode Confort`  
- `🚿 ECS – Bouclage actif`  
- `🛡️ Alarme – Mode Visite`  
- `🔋 Énergie – Batterie faible`  

Sont interdits dans le titre :

- verbes d’action (`démarrage`, `relance`, `arrêt`, `tentative`),
- références temporelles,
- confirmations de succès ou d’échec,
- formulations événementielles.

👉 Le titre **désigne un état**, jamais un fait passé.

---

### 📝 Message — Règles de contenu

Le corps du message :

- décrit la **situation courante**,
- peut préciser :
  - la valeur cible,
  - la raison métier,
  - le contexte décisionnel,
- peut contenir des **actions suggérées**,
- ne doit jamais définir l’identité de la notification.

Exemples normatifs :

**Notification persistante**

---

## 🛡️ ROBUSTESSE & COHÉRENCE

Le système de notifications doit garantir :

- absence de notification persistante orpheline,
- cohérence après reload YAML,
- recalcul possible à partir du seul état courant,
- absence de dépendance à un historique implicite.

Une notification persistante est considérée comme :

> une **vue synthétique**,  
> pas comme une source de vérité.

---

## 🛑 INVARIANTS ABSOLUS

Il est strictement interdit que :

- une notification persistante subsiste
  alors que l’état qu’elle représente est faux,
- une notification persistante décrive un événement passé,
- une notification éphémère soit utilisée
  pour maintenir un état,
- une notification remplace un dashboard ou un diagnostic,
- une notification décide à la place du système métier.

---

## 📌 PORTÉE CONTRACTUELLE

Ce contrat constitue la **référence normative transverse**
pour tout usage des notifications dans Arsenal.

Tout sous-système (chauffage, aération, énergie, mobilité, sécurité, etc.)
souhaitant utiliser des notifications persistantes
doit s’aligner sur les principes définis ici.

Toute extension devra :

- respecter ce socle,
- être explicitement documentée,
- ne jamais contredire les principes fondamentaux.

---

## ✅ STATUT

- Contrat normatif : **ACTIF**
- Domaine : **Notifications**
- Évolutivité : **PRÉVUE**
- Rôle : **STRUCTURANT**

# ==========================================================