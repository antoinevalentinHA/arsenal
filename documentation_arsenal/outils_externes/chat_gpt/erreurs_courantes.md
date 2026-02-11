# 🧠 ARSENAL — ChatGPT
# Erreurs courantes d’interaction

## 🎯 Objet

Ce document recense les **erreurs récurrentes observées** lors des interactions
avec ChatGPT dans le cadre d’Arsenal.

Il ne s’agit **ni de recommandations générales**,  
ni d’un guide d’utilisation,  
ni d’un document pédagogique.

Ce fichier constitue un **catalogue d’échecs constatés**, destiné à :
- prévenir leur répétition,
- faciliter le diagnostic,
- renforcer la maîtrise contractuelle de l’outil.

---

## 1️⃣ Confondre intention et résultat exploitable

### ❌ Erreur

Supposer qu’un objectif clairement exprimé suffit
à produire un livrable directement exploitable.

### 🔍 Symptômes observés

- Texte lisible mais non intégrable tel quel
- Mélange entre explication et contenu final
- Nécessité de “nettoyer” la sortie avant usage

### 🧠 Cause réelle

ChatGPT optimise par défaut :
- la fluidité conversationnelle,
- la lisibilité humaine,
- la complétude explicative.

Il **n’optimise pas spontanément** la réutilisabilité brute.

### ✅ Correction

- Toujours imposer explicitement la **forme de sortie**
- Interdire tout texte hors livrable lorsque requis
- Ne jamais supposer que l’intention suffit

---

## 2️⃣ Laisser ChatGPT décider du format

### ❌ Erreur

Ne pas spécifier explicitement :
- le type de contenu attendu,
- le niveau de complétude,
- le statut du document (brouillon / contractuel / figé).

### 🔍 Symptômes observés

- Structure arbitraire
- Titres ajoutés, déplacés ou reformulés
- Ton non aligné avec Arsenal

### 🧠 Cause réelle

ChatGPT comble les zones floues
en appliquant des conventions génériques.

### ✅ Correction

- Fournir un **cadre explicite**
- Définir aussi clairement ce qui est **interdit**
- Ne jamais laisser le format implicite

---

## 3️⃣ Mélanger raisonnement et production

### ❌ Erreur

Demander simultanément :
- une réflexion,
- une analyse,
- et un livrable final.

### 🔍 Symptômes observés

- Raisonnement inclus dans le document
- Commentaires implicites
- Pollution du contenu final

### 🧠 Cause réelle

ChatGPT ne segmente pas spontanément :
- la phase de raisonnement,
- la phase de génération.

### ✅ Correction

- Séparer strictement les objectifs
- Une interaction = un type de sortie
- Utiliser des contrats distincts par usage

---

## 4️⃣ Croire qu’une correction locale suffit

### ❌ Erreur

Corriger un détail isolé
sans revoir le cadre global de l’interaction.

### 🔍 Symptômes observés

- Réapparition de la même erreur plus loin
- Effets de bord non anticipés
- Dérives progressives du contenu

### 🧠 Cause réelle

ChatGPT n’a aucune notion de :
- régression,
- cohérence globale,
- stabilité dans le temps.

### ✅ Correction

- Corriger le **contrat**, pas seulement la sortie
- Documenter l’erreur pour l’éviter à l’avenir
- Ne jamais traiter un symptôme comme une cause

---

## 5️⃣ Laisser ChatGPT interpréter un silence

### ❌ Erreur

Omettre volontairement ou involontairement une information
en supposant qu’elle est “évidente”.

### 🔍 Symptômes observés

- Ajout de contenu non demandé
- Hypothèses implicites
- Extension non souhaitée du périmètre

### 🧠 Cause réelle

ChatGPT comble activement les vides
pour produire une réponse “complète”.

### ✅ Correction

- Tout silence doit être **volontaire**
- Tout périmètre non couvert doit être **explicitement exclu**
- Ne jamais compter sur l’évidence implicite

---

## 6️⃣ Utiliser ChatGPT comme autorité

### ❌ Erreur

Valider une décision parce que
“ChatGPT l’a dit” ou “ChatGPT le confirme”.

### 🔍 Symptômes observés

- Affaiblissement de l’architecture Arsenal
- Décisions non traçables
- Justifications externes non maîtrisées

### 🧠 Cause réelle

Glissement de rôle :
outil d’exécution → prescripteur implicite.

### ✅ Correction

- ChatGPT ne décide jamais
- Il exécute un cadre défini
- Toute décision reste **interne à Arsenal**

---

## 7️⃣ Accepter un état non numérique dans un capteur numérique

### ❌ Erreur

Autoriser ChatGPT à produire un template de capteur numérique
renvoyant parfois des chaînes de caractères (`unknown`, `unavailable`, `this.state` brut).

### 🔍 Symptômes observés

- Logs critiques lors des triggers
- Exceptions `ValueError` dans `sensor/__init__.py`
- Capteur bloqué ou instable après reload
- Statistiques et graphiques corrompus

### 🧠 Cause réelle

ChatGPT ignore par défaut que :
- `device_class` + `unit` impliquent une **contrainte numérique stricte**
- `this.state` peut valoir une string invalide
- Home Assistant ne tolère aucune valeur non numérique

Il applique des schémas conversationnels (`unknown`, conservation brute)
incompatibles avec le moteur HA.

### ✅ Correction

- Interdire toute sortie textuelle dans un capteur numérique
- Exiger explicitement : **float ou none uniquement**
- Imposer le pattern :
  - lecture source via `| float(none)`
  - conservation via `this.state | float(none)`
  - retour `none` si invalide

---

## 8️⃣ Accéder directement à un attribut non initialisé dans un triggered sensor

### ❌ Erreur

Autoriser ChatGPT à produire un template de triggered sensor
accédant directement à `this.attributes.xxx` sans garantie d’initialisation préalable.

### 🔍 Symptômes observés

- Logs `UndefinedError` lors des triggers
- Messages :
  - `'ReadOnlyDict object' has no attribute 'arsenal_ts_last_reset'`
  - `'ReadOnlyDict object' has no attribute 'arsenal_ts_last_reprise'`
- Capteur bloqué ou partiellement figé
- Attributs jamais initialisés après reload

### 🧠 Cause réelle

Dans un `trigger_template_entity` :

- `this.attributes` est un `ReadOnlyDict`
- Les clés **n’existent pas tant qu’elles n’ont jamais été écrites**
- L’accès direct `this.attributes.xxx` lève une exception fatale

ChatGPT suppose à tort que :
- les attributs existent par défaut
- un filtre (`| float(0)`) protège l’accès  
→ ce qui est faux : l’erreur est levée **avant** le filtre.

### ✅ Correction

- Interdire tout accès direct à `this.attributes.xxx`
- Imposer systématiquement :
  - `this.attributes.get('xxx', valeur_defaut)`
  - ou `state_attr(entity_id, 'xxx') | default(valeur)`

- Ne jamais supposer l’existence préalable d’un attribut
- Toujours concevoir les attributs comme **non initialisés au premier cycle**

---

## 9️⃣ Utiliser le filtre `| float` sans valeur par défaut dans un template critique

### ❌ Erreur

Autoriser ChatGPT à produire des templates utilisant le filtre `| float`
sans valeur par défaut (`| float(none)` ou `| float(0)`),
sur des entités pouvant temporairement valoir `unknown` ou `unavailable`.

### 🔍 Symptômes observés

- Logs `ValueError: float got invalid input 'unknown'`
- Exceptions répétées dans `helpers/template`
- Traces :
  - `forgiving_float_filter`
  - `raise_no_default("float", value)`
- Templates diagnostics totalement cassés
- Boucles d’erreurs persistantes dans le moteur de rendu

### 🧠 Cause réelle

Dans Home Assistant :

- `states('xxx')` renvoie **toujours une string**
- En cas d’état `unknown` / `unavailable`, la valeur est littéralement `'unknown'`
- Le filtre `| float` **sans défaut** :
  - tente une conversion directe
  - lève une exception fatale
  - interrompt totalement le rendu

ChatGPT suppose à tort que :
- les `input_number` sont toujours valides
- `| float` est tolérant par défaut  
→ ce qui est faux : **aucun défaut implicite n’est appliqué**.

### ✅ Correction

- Interdire toute utilisation de `| float` sans valeur par défaut
- Imposer systématiquement :
  - `| float(none)` pour capteurs diagnostiques
  - ou `| float(0)` pour calculs métier bornés

- Ne jamais supposer qu’un `input_number` est toujours initialisé
- Toujours considérer `unknown` comme un état normal au démarrage ou après reload

---

## 🔟 Concevoir une automation réentrante sans borne de concurrence

### ❌ Erreur

Autoriser ChatGPT à produire une automation décisionnelle
susceptible de se déclencher à nouveau alors qu’une exécution est encore en cours,
sans stratégie explicite de non-réentrance.

### 🔍 Symptômes observés

- Logs :
  - `Maximum number of runs exceeded`
- Automation bloquée ou abandonnée par le moteur
- Décisions non appliquées ou partiellement exécutées
- Boucles décisionnelles silencieuses
- Saturation progressive du scheduler

### 🧠 Cause réelle

Dans Home Assistant :

- une automation peut être déclenchée **pendant sa propre exécution**
- sans `mode` adapté, chaque trigger crée une nouvelle instance
- le moteur applique une limite de sécurité (`max_runs`)

ChatGPT suppose à tort que :
- les décisions sont atomiques
- les déclenchements sont séquentiels
- une automation ne peut pas se rappeler elle-même  

→ ce qui est faux dans un système événementiel.

### ✅ Correction

- Interdire toute automation critique sans stratégie explicite de concurrence
- Imposer systématiquement pour les décisions centrales :
  - `mode: single` ou `mode: restart`
  - bornage explicite (`max`, timers, watchdog)

- Concevoir toute automation décisionnelle comme **potentiellement réentrante**
- Toujours vérifier l’idempotence avant autorisation de concurrence

---

## 1️⃣1️⃣ Alimenter un `utility_meter` avec un capteur non normalisé

### ❌ Erreur

Autoriser ChatGPT à configurer des `utility_meter`
basés sur des capteurs énergétiques pouvant temporairement renvoyer `unknown` ou `unavailable`.

### 🔍 Symptômes observés

- Logs :
  - `received an invalid new state … : unknown`
- Compteurs journaliers / mensuels figés ou troués
- Accumulations fausses ou interrompues
- Historique énergétique corrompu
- Energy dashboard incohérent

### 🧠 Cause réelle

Dans Home Assistant :

- `utility_meter` n’accepte **que des valeurs numériques strictes**
- toute valeur `unknown` est rejetée
- l’échantillon est perdu définitivement

ChatGPT suppose à tort que :
- les capteurs de prise sont toujours numériques
- `unknown` est toléré  
→ ce qui est faux : `utility_meter` est **strictement typé**.

### ✅ Correction

- Interdire tout `utility_meter` basé directement sur un capteur brut
- Imposer systématiquement :
  - un capteur proxy numérique
  - normalisation via `| float(0)` ou `| float(none)`
  - filtrage des états `unknown` / `unavailable`

- Toujours garantir :
  - monotonie
  - continuité numérique
  - absence totale de string en entrée

---

## 1️⃣2️⃣ Utiliser des variables Jinja non garanties dans un template UI ou diagnostic

### ❌ Erreur

Autoriser ChatGPT à produire des templates Jinja
utilisant directement des variables (`episode`, `blocage`, `deltaT_max`, `temp_ref`, etc.)
sans garantir explicitement leur existence dans le contexte Home Assistant.

### 🔍 Symptômes observés

- Logs répétés :
  - `UndefinedError: 'episode' is undefined`
  - `UndefinedError: 'blocage' is undefined`
  - `UndefinedError: 'deltaT_max' is undefined`
  - `UndefinedError: 'temp_ref' is undefined`
- Boucles d’erreurs lors du rendu UI
- Cartes Lovelace partiellement ou totalement cassées
- Saturation des logs par erreurs de rendu
- Diagnostics illisibles ou absents

### 🧠 Cause réelle

Dans Home Assistant :

- chaque template est évalué dans un **contexte strictement limité**
- aucune variable n’est implicite
- toute variable absente lève une exception fatale

ChatGPT suppose à tort que :
- les variables définies dans un autre bloc sont accessibles partout
- le contexte UI partage l’état interne de scripts ou capteurs
- les noms de variables sont persistants entre rendus  

→ ce qui est faux : chaque rendu est **isolé et strictement typé**.

### ✅ Correction

- Interdire toute utilisation de variable non explicitement définie dans le template
- Imposer systématiquement :
  - initialisation défensive (`{% set episode = episode | default(false) %}`)
  - ou dérivation explicite depuis des entités (`states()`, `state_attr()`)

- Ne jamais supposer l’existence d’une variable externe
- Toujours concevoir les templates UI comme **sans état interne persistant**

---

## 1️⃣3️⃣ Déclencher une tempête de rendu UI par variable Jinja absente

### ❌ Erreur

Laisser un template UI (markdown, carte diagnostic, carte synthèse)
contenir une variable Jinja absente,
dans un contexte où le moteur de rendu est évalué périodiquement.

### 🔍 Symptômes observés

- Rafales d’erreurs continues dans les logs :
  - `renders=14`, `renders=18`, `renders=22`, etc.
  - répétition exacte du même traceback
- Messages :
  - `UndefinedError: 'episode' is undefined`
  - `UndefinedError: 'blocage' is undefined`
  - `UndefinedError: 'deltaT_max' is undefined`
  - `UndefinedError: 'temp_ref' is undefined`
- Pollution massive du journal
- Ralentissements frontend
- UI instable ou cartes qui ne s’affichent plus
- Parfois watchdog ou redémarrages induits

### 🧠 Cause réelle

Dans Home Assistant :

- les templates UI sont **réévalués périodiquement**
- chaque rendu est isolé
- toute variable absente provoque une exception
- l’exception n’interrompt pas la planification → le moteur réessaie indéfiniment

ChatGPT produit souvent :
- des blocs conditionnels utilisant des variables supposées globales
- sans initialisation défensive
- dans des cartes évaluées en boucle

→ Une seule variable absente suffit à créer une **tempête de rendu permanente**.

### ✅ Correction

- Toujours initialiser défensivement toute variable :
  - `{% set episode = episode | default(false) %}`
  - `{% set deltaT_max = deltaT_max | default(0) %}`
- Ou dériver systématiquement depuis des entités HA
- Ne jamais utiliser de variable “logique” non issue explicitement d’un état
- Tester systématiquement les cartes UI en mode développeur avant intégration

---

## 1️⃣4️⃣ Laisser une intégration externe tenter un enregistrement webhook invalide en boucle

### ❌ Erreur

Conserver une intégration cloud configurée avec :
- URL de callback absente ou invalide
- webhook non fonctionnel
tout en laissant Home Assistant tenter automatiquement un enregistrement périodique.

### 🔍 Symptômes observés

- Rafales périodiques d’erreurs :
  - `WithingsInvalidParamsError: The callback URL is either absent or incorrect`
- Messages :
  - `Error doing job: Task exception was never retrieved`
- Tentatives répétées à chaque redémarrage ou reload
- Pollution durable des logs
- Erreurs sans impact fonctionnel visible immédiat

### 🧠 Cause réelle

Certaines intégrations cloud :

- tentent d’enregistrer automatiquement un webhook au démarrage
- sans vérifier la validité réelle de l’URL exposée
- et recommencent à chaque cycle

Home Assistant :
- ne désactive pas l’intégration
- ne met pas en quarantaine l’erreur
- relance indéfiniment la tentative

### ✅ Correction

- Désactiver l’intégration tant que l’URL externe n’est pas valide
- Ou corriger explicitement :
  - configuration réseau
  - reverse proxy
  - URL publique HA
- Ne jamais laisser une intégration cloud en état “webhook invalide” persistant

---

## 1️⃣5️⃣ Déclencher une saturation d’automatisation par réentrance non maîtrisée

### ❌ Erreur

Autoriser une automatisation ou un script à :

- se redéclencher pendant sa propre exécution
- sans verrou (mode single / restart / queued contrôlé)
- sans temporisation défensive

### 🔍 Symptômes observés

- Logs :
  - `Already running`
  - `Maximum number of runs exceeded`
- Rafales de warnings rapprochés
- Automatisations désactivées temporairement par HA
- Décisions système non appliquées ou abandonnées

### 🧠 Cause réelle

Home Assistant :

- limite strictement le nombre d’exécutions simultanées
- coupe l’automatisation lorsqu’un seuil est dépassé

ChatGPT produit souvent :
- des chaînes d’automatisations auto-déclenchantes
- des scripts appelés depuis leur propre contexte
- sans protection de réentrance

→ Le système entre en **boucle logique interne**.

### ✅ Correction

- Imposer explicitement :
  - `mode: single` avec attente réelle
  - ou verrous via helpers (`input_boolean`, `timer`)
- Toujours analyser les graphes de déclenchement
- Ne jamais autoriser une décision centrale sans garde de réentrance

---

## 1️⃣6️⃣ Introduire une erreur de schéma YAML invalidant silencieusement un script critique

### ❌ Erreur

Laisser ChatGPT produire un script ou une automatisation contenant :

- des clés interdites
- des structures de service invalides
- des champs non conformes au schéma Home Assistant

dans un composant critique.

### 🔍 Symptômes observés

- Message :
  - `could not be validated and has been disabled`
  - `extra keys not allowed`
- Script ou automatisation **désactivé automatiquement**
- Absence d’exécution sans alerte fonctionnelle visible
- Pannes silencieuses de logique centrale

### 🧠 Cause réelle

Home Assistant :

- valide strictement les schémas YAML
- désactive immédiatement tout script invalide
- sans rollback ni dégradation progressive

ChatGPT :
- mélange fréquemment syntaxe Jinja, données métier et schéma HA
- insère des champs non autorisés (`raison`, `service` mal placé, etc.)

→ Le composant est **neutralisé sans alarme fonctionnelle explicite**.

### ✅ Correction

- Toujours valider :
  - Configuration → Vérifier la configuration
  - ou Outils développeur → YAML
avant tout redémarrage
- Ne jamais intégrer un script ChatGPT dans un composant critique sans validation préalable
- Isoler les décisions centrales dans des scripts minimalistes et ultra-stricts

---

## 1️⃣7️⃣ Laisser une intégration cloud bloquer le scheduler par timeouts répétés

### ❌ Erreur

Conserver une intégration cloud (ici ViCare) :

- avec appels API lents ou instables
- sans mécanisme de circuit breaker
- sans proxy local ou capteurs de repli

tout en laissant Home Assistant interroger périodiquement l’API.

### 🔍 Symptômes observés

- Rafales de warnings :
  - `Update ... is taking over 10 seconds`
  - `Updating ... took longer than the scheduled update interval`
- Erreurs répétées :
  - `ReadTimeoutError`
  - `HTTPSConnectionPool(...): Read timed out`
- Échecs en chaîne :
  - capteurs ECS
  - binary_sensor chargement
  - climate chauffage
- Entités bloquées ou retardées
- Retards globaux dans le scheduler HA

### 🧠 Cause réelle

Dans Home Assistant :

- chaque entité cloud est mise à jour périodiquement
- les appels bloquants sont exécutés dans des workers limités
- un timeout long (31s ici) monopolise un worker
- plusieurs entités ViCare partagent le même backend API

En cas de latence serveur :

- les workers s’accumulent
- les mises à jour dépassent l’intervalle planifié
- les entités entrent en retard permanent
- des erreurs en cascade apparaissent sur plusieurs domaines

→ Le cloud devient un **point de congestion systémique**.

### ✅ Correction

- Réduire drastiquement la fréquence de polling cloud
- Isoler les capteurs critiques via :
  - proxies locaux
  - capteurs figés
  - helpers de repli
- Surveiller explicitement :
  - latence API
  - taux de timeout
- Ne jamais laisser une décision centrale dépendre directement d’un capteur cloud non protégé

---

## 1️⃣8️⃣ Laisser un webhook cloud invalide générer des tâches fantômes au démarrage

### ❌ Erreur

Configurer une intégration cloud utilisant des webhooks
(ici Withings) avec :

- URL de callback absente
- URL incorrecte
- instance non publiquement accessible

tout en laissant Home Assistant tenter l’enregistrement automatique au démarrage.

### 🔍 Symptômes observés

- Erreur silencieuse mais répétée au boot :
  - `Task exception was never retrieved`
- Trace explicite :
  - `WithingsInvalidParamsError: The callback URL is either absent or incorrect`
- Aucune entité explicitement cassée
- Pas d’impact fonctionnel immédiat visible
- Pollution persistante des logs système

### 🧠 Cause réelle

Au démarrage :

- l’intégration tente d’enregistrer un webhook distant
- l’API cloud rejette l’URL fournie
- une tâche asynchrone échoue
- l’exception n’est pas correctement récupérée

Conséquences :

- tâche orpheline dans l’event loop
- erreur non liée à une entité précise
- bruit permanent dans les logs
- difficulté de diagnostic ultérieur

→ Le système fonctionne, mais avec **erreur structurelle latente**.

### ✅ Correction

- Vérifier explicitement l’URL externe déclarée dans Home Assistant
- Désactiver l’intégration si aucun webhook public n’est disponible
- Ne jamais laisser une intégration webhook active sans endpoint valide
- Surveiller systématiquement les erreurs `Task exception was never retrieved`

---

## 1️⃣9️⃣ Laisser une intégration cloud bloquer la boucle d’update par timeout réseau

### ❌ Erreur

Utiliser une intégration cloud (ici ViCare) :

- synchrone côté Home Assistant
- avec timeout long (31 s)
- sans mécanisme local de dégradation
- sans proxy ni garde-fou

pour des entités **critiques de régulation thermique (ECS / chauffage)**.

### 🔍 Symptômes observés

- Avertissements récurrents :
  - `Update of ... is taking over 10 seconds`
  - `Updating vicare ... took longer than the scheduled update interval`
- Erreurs fatales :
  - `ReadTimeoutError: HTTPSConnectionPool(...): Read timed out (31s)`
- Entités impactées en cascade :
  - `binary_sensor.vscotho1_200_11_chargement_de_l_ecs`
  - `sensor.vscotho1_200_11_dhw_storage_temperature`
  - `number.vscotho1_200_11_dhw_temperature`
  - `climate.vscotho1_200_11_chauffage`
- Débordement du scheduler HA
- Retards cumulés dans la boucle d’update globale

### 🧠 Cause réelle

Architecture interne de l’intégration :

- chaque entité appelle l’API Viessmann
- appels **bloquants** (requests synchrones)
- timeout élevé (31 s)
- cache rafraîchi globalement (`fetch_all_features()`)

En cas de latence ou indisponibilité API :

- chaque entité bloque un thread
- la planification dérive
- plusieurs entités entrent en timeout simultanément
- erreurs en rafale
- saturation silencieuse de l’event loop

→ Le système thermique dépend directement de la **disponibilité d’un cloud externe**.

### ⚠️ Effets systémiques

- États figés ou incohérents
- Décisions thermiques prises sur données obsolètes
- Retards dans les automatisations critiques
- Pollution massive des logs
- Dégradation progressive de la stabilité globale

### ✅ Correction (architecturale)

- Ne jamais baser une régulation thermique critique directement sur des entités cloud
- Introduire des **capteurs proxy locaux** :
  - dernier état valide figé
  - timeout borné
  - fallback contrôlé
- Isoler toute intégration cloud dans un **domaine non décisionnel**
- Surveiller systématiquement :
  - `Update is taking over 10 seconds`
  - `ReadTimeoutError`
- Réduire ou découpler la fréquence d’interrogation API

→ Principe Arsenal :  
**Le cloud ne doit jamais être une autorité thermique.**

---

## 2️⃣0️⃣ Laisser une boucle de reconnexion asynchrone saturer le scheduler par backoff incontrôlé

### ❌ Erreur

Utiliser une intégration cloud asynchrone (ici Overkiz / Somfy) :

- en polling permanent
- avec mécanisme de retry automatique
- sans borne haute de backoff
- sans suspension après échec prolongé

sur un service réseau instable ou indisponible.

### 🔍 Symptômes observés

- Rafales de logs :
  - `Backing off fetch_events(...) for 0.xs`
  - `ClientConnectorError`
  - `ClientConnectorDNSError`
- Boucles de retry très rapides (0.2s → 0.9s → 0.3s → 0.6s …)
- Multiplication simultanée de tâches identiques
- Polling maintenu malgré :
  - échec TCP
  - échec DNS
  - indisponibilité persistante

En parallèle :

- dérives sur d’autres intégrations cloud
- warnings thermiques simultanés (ViCare)
- erreurs multi-domaines corrélées

### 🔬 Variante critique observée — Backoff nul + erreurs hétérogènes

Cas aggravé identifié :

- Backoff descendant jusqu’à **0.0s**
- Enchaînement rapide de causes différentes :
  - `ClientConnectorDNSError` (DNS timeout)
  - `ClientConnectorError` (TCP refused)
  - `NotAuthenticatedException`
- Reprise immédiate sans délai effectif
- Rafales synchronisées de 10+ tâches simultanées

Logs typiques :

- `Backing off fetch_events(...) for 0.0s`
- `NotAuthenticatedException: Not authenticated`
- alternance DNS / TCP / AUTH dans la même minute

### ⚠️ Pathologie spécifique

Dans ce scénario :

- le mécanisme de backoff **perd toute efficacité**
- certaines branches d’erreur réinitialisent le délai à zéro
- l’intégration entre dans une **boucle quasi-busy-loop**
- la charge devient proportionnelle :
  - au nombre de devices
  - au nombre de listeners
  - au nombre de sessions invalides

Effets observés :

- rafales continues sans pause réelle
- saturation du scheduler
- interférence directe avec :
  - ViCare
  - capteurs critiques
  - automations temps réel
- amplification artificielle d’une panne réseau banale

### 🔗 Propagation inter-intégrations observée (effet domino cloud)

Séquence critique constatée :

1. Tempête Overkiz active :
   - backoff nul (0.0s)
   - DNS / TCP / AUTH alternés
   - rafales concurrentes

2. En parallèle :
   - ViCare entre en timeout systématique
   - entités ECS / chauffage bloquent >10s
   - scheduler saturé

Logs corrélés :

- `Backing off fetch_events(...) for 0.0s` (Overkiz)
- `Update ... is taking over 10 seconds` (ViCare)
- `ReadTimeout api.viessmann-climatesolutions.com`
- `Unable to retrieve data from ViCare server`
- `Missing 'data' property when fetching data`

### 🔁 Crash / restart induits par intégrations fautives au démarrage

Séquence critique répétée :

- Intégration Withings échoue à l’enregistrement webhook :
  - `WithingsInvalidParamsError: The callback URL is either absent or incorrect`
- Exception non récupérée :
  - `Task exception was never retrieved`
- Arrêt immédiat du core :
  - `service legacy-services: stopping`
  - `Home Assistant Core service shutdown`
- Redémarrage automatique complet

Caractéristiques :

- erreur persistante à CHAQUE boot
- aucune mise en quarantaine automatique
- redémarrage total du système
- répétition possible en boucle

Conséquences directes :

- interruption de toutes les intégrations
- perte transitoire des états
- reset des caches
- réinitialisation des exécutors
- trous temporels dans les historiques

### ⚠️ Pathologie de démarrage critique

Ce cas montre que :

- une seule intégration mal configurée
- suffit à :
  - faire tomber tout le core
  - provoquer un reboot en chaîne
  - perturber durablement la stabilité thermique

→ Le système ne tolère **aucune intégration défaillante au boot**.

### 🧨 Désarmement silencieux d’automatismes par erreurs de validation

Cas observés :

- Automations désactivées automatiquement :

  - `expected str for dictionary value @ data['id']. Got 10150000000005`
  - `expected str for dictionary value @ data['id']. Got 10210000000001`

Origine :

- IDs numériques non typés string
- validation YAML stricte
- HA désactive l’automation sans rollback

Conséquences :

- automations critiques hors service
- aucune alerte fonctionnelle
- comportement dégradé invisible
- perte de garanties métier

→ Le système accepte de **désarmer silencieusement des automatismes vitaux**.

### 🔐 Tempête d’authentification Overkiz et reboot induit

Séquence observée :

- Perte d’authentification Overkiz :
  - `NotAuthenticatedException: Not authenticated`
- Backoff agressif en rafale :
  - ~10 appels simultanés à 0.2 s
- Échec final :
  - `Authentication failed while fetching device events data: Invalid authentication`

Conséquence immédiate :

- arrêt brutal du core :
  - `service legacy-services: stopping`
  - `Home Assistant Core service shutdown`
- redémarrage automatique complet

Caractéristiques :

- rafales concurrentes non sérialisées
- aucun délai progressif réel
- aucune désactivation automatique de l’intégration fautive
- reboot global comme mécanisme de “récupération”

→ Une simple perte de token Overkiz provoque un **redémarrage total du système**.

### 🌐 Intégrations locales bloquantes au setup (Fujitsu Airstage)

Cas répétés :

- échec setup au boot :
  - `Timeout while connecting to device`
- répétition à chaque redémarrage
- aucune quarantaine locale

Conséquences :

- ralentissement du démarrage
- occupation prolongée des threads d’init
- propagation de latence vers les intégrations critiques

→ Même une intégration **locale** peut dégrader la stabilité globale.

### 🔁 Boucles d’automatismes non confinées (runaway)

Cas critiques :

- `Maximum number of runs exceeded`
  - automation.alarmes_application_decision_centrale
- répétitions en rafale sur quelques secondes
- saturation du scheduler

Caractéristiques :

- aucune inhibition automatique durable
- aucune alerte métier
- boucle logique autorenforcée possible

Conséquences :

- charge CPU inutile
- retard dans les décisions critiques
- risque de starvation des threads vitaux

→ Une seule automation mal protégée peut perturber la chaîne décisionnelle.

### 🧪 Capteurs diagnostiques auto-instables

Cas observé :

- erreur Jinja :
  - `as_timestamp got invalid input`
- boucle de recalcul :
  - sensor.vitesse_reprise_presence_chambres
- rafales d’erreurs successives

Origine :

- attribut `t0` non typé datetime valide
- absence de garde forte sur type réel
- déclenchements multiples rapprochés

Conséquences :

- bruit massif dans les logs
- surcharge moteur template
- instabilité de la couche diagnostic elle-même

→ Même les capteurs d’observabilité peuvent devenir **sources actives d’instabilité**.

### 🔢 Capteurs numériques produisant `unknown` (exception moteur silencieuse)

Cas observés :

- `sensor.duree_stabilisation_absence_chambres`  
  - unité : `s`
  - valeur produite : `'unknown'`

- `sensor.temperature_reprise_presence_chambres`  
  - unité : `°C`
  - valeur produite : `'unknown'`

Erreur moteur Home Assistant :

- coercition automatique imposée par l’unité :
  - `int('unknown')` → échec
  - `float('unknown')` → échec
- exception levée en boucle :
  - `Sensor ... has a numeric value; however, it has the non-numeric value: 'unknown'`
- erreurs non récupérées :
  - `Task exception was never retrieved`
- répétition périodique toutes les minutes

Origine technique :

- présence d’une `unit_of_measurement` ⇒ HA **impose une valeur strictement numérique**
- toute chaîne (`unknown`, `unavailable`, texte) est interdite
- dans un `triggered_template_sensor` :
  - l’état est évalué même hors trigger
  - un retour texte provoque une exception interne moteur
- absence de garde forte sur :
  - initialisation
  - attributs manquants
  - valeur de repli

Conséquences systémiques :

- spam massif des logs ERROR
- pollution du Recorder
- surcharge du `template/coordinator`
- masquage d’erreurs plus graves
- dégradation progressive de la stabilité runtime

Règle Arsenal ajoutée (niveau critique) :

> Tout capteur avec unité (°C, s, %, W, etc.)  
> **ne doit jamais produire `unknown` ou texte.**  
>  
> En cas de donnée invalide :
> - conserver la dernière valeur numérique valide  
> - ou produire une valeur sentinelle numérique documentée  
>  
> `unknown` est strictement interdit sur capteur numérique.

Impact architectural :

- rend les capteurs diagnostics non reload-safe
- compromet l’observabilité long terme
- transforme la couche diagnostic en **source active d’instabilité**

### 🧷 Attributs de triggered template sensors non initialisés (exception moteur Jinja)

Cas observé :

- capteur : `sensor.duree_cycle_moyenne_presence_chambres`
- attribut concerné : `arsenal_ts_last_reprise`

Erreur moteur :

- accès direct à un attribut inexistant :
  - `this.attributes.arsenal_ts_last_reprise`
- exception levée :
  - `UndefinedError: ReadOnlyDict object has no attribute 'arsenal_ts_last_reprise'`
- origine :
  - `helpers/trigger_template_entity.py`

Origine technique :

- `this.attributes` est un dictionnaire en lecture seule
- au premier calcul (boot / reload / avant premier trigger) :
  - l’attribut n’existe pas encore
- l’accès direct sans garde provoque :
  - exception moteur
  - recalcul avorté
  - erreur répétée à chaque rafraîchissement

Caractéristique aggravante :

- dans un `triggered_template_sensor` :
  - les attributs sont évalués même hors déclenchement
  - l’ordre d’initialisation n’est pas garanti
  - aucun attribut n’est présent tant qu’il n’a jamais été écrit

Conséquences :

- spam ERROR persistant
- surcharge moteur template
- capteur partiellement invalide
- dépendants fragilisés (UI, automations, agrégats)
- perte de reload-safety
- observabilité instable

Règle Arsenal ajoutée (niveau critique) :

> **Tout accès à `this.attributes.xxx` doit être protégé.**  
>  
> Interdictions :
> - accès direct sans test d’existence  
> - supposer qu’un attribut existe au boot  
>  
> Règle stricte :
> - toujours utiliser `state_attr()` avec défaut  
> - ou tester explicitement l’existence  
> - ou initialiser systématiquement l’attribut dès la création du capteur

Exemples sûrs obligatoires :

- `state_attr(this.entity_id, 'arsenal_ts_last_reprise') | default(none)`
- `{% if 'arsenal_ts_last_reprise' in this.attributes %} ... {% endif %}`

Impact architectural :

- rend les capteurs diagnostics non boot-safe
- empêche la reproductibilité post-reload
- transforme les attributs en point de fragilité majeur

→ Principe Arsenal renforcé :  
**Aucun attribut de capteur diagnostic ne doit être lu sans garde d’existence.**

### 🧠 Cause systémique étendue

Défauts structurels révélés :

- backoff concurrent non sérialisé
- aucune quarantaine par intégration
- setup bloquant non isolé
- automatismes sans coupe-circuit structurel
- templates non sandboxés

Résultat :

- perte auth cloud → reboot système
- timeout local → ralentissement global
- boucle automation → saturation décisionnelle
- capteur diagnostic → bruit et instabilité

### ✅ Règles Arsenal renforcées (niveau critique)

Nouveaux invariants supplémentaires :

> **Aucune perte d’authentification cloud ne doit pouvoir provoquer un reboot global.**  
> **Aucune automation ne doit pouvoir entrer en boucle sans disjoncteur automatique.**  
> **Aucun capteur diagnostic ne doit être autorisé sans garde de typage strict.**

Mesures recommandées :

- Quarantaine Overkiz :
  - désactivation automatique après N échecs auth
  - suspension prolongée sans reboot
- Setup différé des intégrations locales instables
- Watchdog automation :
  - détection de “Maximum number of runs exceeded”
  - alerte + inhibition temporaire automatique
- Règle template stricte :
  - tout `as_timestamp()` avec défaut explicite
  - garde de type avant calcul temporel
- Supervision post-boot :
  - scan des intégrations en échec
  - scan des automations en dépassement de runs
  - scan des capteurs en erreur Jinja

→ Principe clé étendu :
**Ni le cloud, ni le local, ni le diagnostic, ni l’automatisation ne doivent pouvoir faire tomber la souveraineté thermique.**

### 🧠 Cause systémique

Défauts structurels Home Assistant :

- aucune isolation d’intégration au démarrage
- exception fatale non confinée
- redémarrage global non conditionné
- politique “fail hard” sans hiérarchie
- validation destructive sans journal métier

Résultat :

- une erreur de webhook
  → provoque un reboot complet
- une erreur de typage
  → neutralise une brique métier sans alerte

### ✅ Règles Arsenal renforcées

Nouveaux invariants :

> **Aucune intégration non critique ne doit pouvoir empêcher le boot du système.**  
> **Aucune erreur de validation ne doit désarmer un automatisme sans alerte explicite.**

Mesures recommandées :

- Suppression ou désactivation des intégrations instables (Withings)
- Interdiction des webhooks non validés en prod
- Quarantaine “boot” :
  - chargement différé des clouds secondaires
- Watchdog de validation YAML :
  - scan des automations désactivées au boot
  - alerte immédiate si désarmement détecté
- Règle stricte :
  - tous les IDs explicitement typés string

→ Principe clé :
**La stabilité thermique ne doit jamais dépendre de la santé d’une intégration tierce.**

### ⚠️ Pathologie transversale

Ce cas montre que :

- une tempête réseau sur **une seule intégration cloud**
- suffit à :
  - bloquer le threadpool
  - saturer le scheduler
  - retarder les exécutors
  - faire expirer les timeouts d’autres clouds

Conséquences :

- pannes ViCare artificielles
- capteurs critiques gelés
- automations ECS / chauffage retardées
- faux diagnostics “API instable”

→ La panne ViCare est ici **induite**, non primaire.

### 🧠 Cause systémique

Défaut structurel Home Assistant :

- threadpool partagé globalement
- scheduler unique pour toutes intégrations
- aucune isolation par domaine
- aucune priorité pour capteurs critiques

Résultat :

- une tempête cloud secondaire peut :
  - faire tomber un cloud primaire stable
  - corrompre la vision thermique
  - perturber des décisions métier

### ✅ Règle Arsenal renforcée

Nouvel invariant :

> **Aucune intégration cloud non critique ne doit pouvoir impacter un domaine vital.**

Mesures recommandées :

- Désactivation automatique Overkiz en cas de storm
- Mise en quarantaine cloud fautif
- Priorisation implicite :
  - Chauffage / ECS > UI / volets / robots / confort
- Watchdog global “tempête cloud” :
  - détection rafales backoff
  - suspension temporaire des clouds instables

→ Principe clé :
**L’indisponibilité d’un service externe ne doit jamais dégrader la régulation thermique.**

### 🧠 Cause architecturale aggravante

Combinaison de trois défauts :

1. Backoff implémenté par exception type, non global
2. Absence de mémoire d’état d’indisponibilité
3. Gestion Auth découplée de la boucle réseau

Résultat :

- chaque type d’erreur relance une stratégie différente
- certaines stratégies autorisent un délai nul
- aucune désactivation automatique après échec prolongé

→ Le système entre en **tempête de reconnexion auto-entretenue**.

### ✅ Correction spécifique recommandée

Mesures indispensables dans ce cas :

- Interdire explicitement tout backoff < **1 seconde**
- Uniformiser :
  - DNS
  - TCP
  - AUTH  
  sous un **même circuit breaker**
- Après N erreurs hétérogènes consécutives :
  - désactivation temporaire de l’intégration
  - reprise différée (5–15 min)
- Ajouter un capteur / watchdog Arsenal :
  - détection de `Backing off fetch_events`
  - alerte si fréquence > seuil

→ Principe Arsenal renforcé :  
**Un cloud instable doit être mis en quarantaine automatiquement.**

### 🧠 Cause réelle

Architecture typique :

- intégration basée sur `aiohttp`
- boucle `fetch_events()` persistante
- retry automatique via `backoff`
- absence de :
  - plafond de tentatives
  - circuit breaker
  - désactivation temporaire

En cas de panne réseau ou DNS :

- dizaines de tâches concurrentes tentent la reconnexion
- backoff court maintient une pression constante
- logs inondés
- charge inutile sur event loop
- dérive globale de la planification

→ Le système continue à insister sur un cloud **manifestement indisponible**.

### ⚠️ Effets systémiques

- Pollution massive des logs (INFO permanent)
- Consommation CPU inutile
- Concurrence avec intégrations critiques (chauffage, ECS, sécurité)
- Dégradation de la latence globale
- Masquage d’erreurs réellement importantes

### ✅ Correction (architecturale)

- Toujours borner :
  - nombre de retries
  - durée maximale d’indisponibilité tolérée
- Introduire un **circuit breaker** :
  - suspension après N échecs
  - reprise différée
- Surveiller explicitement :
  - `Backing off fetch_events`
  - `ClientConnectorDNSError`
- Isoler ces intégrations dans un domaine **non critique**
- Ne jamais laisser une boucle cloud :
  - tourner indéfiniment
  - sans signal d’alarme explicite

→ Principe Arsenal :  
**Un cloud indisponible doit se taire, pas insister.**

---

### 🧨 Mutations interdites en template Jinja (sandbox HA)

Cas observé :

- template de synthèse de blocages climatisation
- construction dynamique d’une liste :
  - `blocages_actifs = []`
  - `blocages_actifs.append(...)`

Erreur moteur :

- exception sécurité Jinja :
  - `SecurityError: access to attribute 'append' of 'list' object is unsafe`
- origine :
  - moteur sandbox Jinja Home Assistant
  - `helpers/template/__init__.py`

Origine technique :

- Home Assistant exécute les templates dans un **sandbox sécurisé**
- toute mutation d’objet est interdite :
  - `list.append()`
  - `dict.update()`
  - toute méthode modifiant une structure
- même dans un contexte purement local

Caractéristique piégeuse :

- la syntaxe est **acceptée au chargement**
- l’erreur n’apparaît :
  - qu’à l’exécution
  - qu’au rendu effectif
- aucun avertissement statique préalable

Conséquences :

- template rendu impossible
- spam ERROR persistant
- moteur template pollué
- UI / cartes / capteurs synthèse invalides
- instabilité de la couche décisionnelle
- perte de reload-safety

Règle Arsenal ajoutée (niveau critique) :

> **Toute mutation d’objet est strictement interdite en template.**  
>  
> Interdictions absolues :
> - `append()`
> - `update()`
> - modification de listes / dictionnaires  
>  
> Règle stricte :
> - toute construction doit être **fonctionnelle et immuable**
> - utiliser concaténation ou sélections conditionnelles
> - jamais d’effet de bord

Exemples autorisés sûrs :

- `{% set blocages_actifs = blocages_actifs + ['horaire'] %}`
- `{% set blocages_actifs = ['horaire'] if condition else [] %}`
- `{% set blocages_actifs = ( ['horaire'] if cond1 else [] ) + ( ['post_aeration'] if cond2 else [] ) %}`

Impact architectural :

- rend les templates de synthèse non exécutables
- empêche toute logique agrégative naïve
- transforme une erreur fonctionnelle en **exception de sécurité fatale**
- rend les dashboards et aides décisionnelles instables

→ Principe Arsenal renforcé :  
**Aucun template ne doit contenir la moindre mutation d’objet.**

---

## 21 — Triggered sensor numérique produisant `unknown` (coordinator crash)

Contexte observé :

- capteurs impactés :
  - `sensor.duree_stabilisation_absence_chambres` (unité : `s`)
  - `sensor.temperature_reprise_presence_chambres` (unité : `°C`)
- type : `triggered_template_sensor`
- valeur produite : `'unknown'`

Erreur moteur Home Assistant :

- coercition automatique imposée par unité :
  - `int('unknown')` → échec
  - `float('unknown')` → échec
- exception levée en boucle :
  - `Sensor ... has a numeric value; however, it has the non-numeric value: 'unknown'`
- effets :
  - `Task exception was never retrieved`
  - crash du `template/coordinator`
  - spam massif des logs
  - pollution Recorder
  - instabilité runtime

Origine technique :

- présence d’une `unit_of_measurement` ⇒ HA **impose valeur numérique stricte**
- toute chaîne (`unknown`, `unavailable`, `none`) est interdite
- dans un `triggered_template_sensor` :
  - l’état est évalué même hors trigger
  - un retour texte provoque crash moteur

Cas aggravant :

- utilisation de `this.state` ou `last` non initialisé
- attributs absents en début de cycle
- retour implicite `unknown` par défaut

Règle Arsenal ajoutée (critique) :

> Tout capteur avec unité (°C, s, %, W, etc.)  
> **ne doit jamais produire `unknown` ou texte.**  
>  
> En cas de donnée invalide :
> - conserver dernière valeur numérique valide  
> - ou produire une valeur sentinelle numérique documentée  
>  
> `unknown` est strictement interdit sur capteur numérique.

Impact architectural :

- rend les capteurs diagnostics non reload-safe
- compromet observabilité long terme
- masque des erreurs système plus graves

---

## 🛑 Hors périmètre volontaire

Ce document ne contient volontairement pas :
- de conseils génériques,
- de bonnes pratiques abstraites,
- d’astuces d’utilisation,
- d’exemples pédagogiques.

Il documente **uniquement des erreurs réellement observées**.

---

## 📌 Statut

- Document vivant
- Alimenté par l’expérience réelle
- Toute nouvelle entrée doit correspondre
  à un échec constaté et reproductible
