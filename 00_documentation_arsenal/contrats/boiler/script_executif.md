# ARSENAL — Contrat d'exécution transactionnelle · Script exécutif MQTT — Boiler Bridge

**Composant :** `arsenal-ha`
**Version :** v1.3
**Scope :** Script exécutif Home Assistant publiant une commande MQTT transactionnelle vers `arsenal-boiler-bridge`
**Dernière mise à jour :** 2026-03-27
**Dépendances :**
- `arsenal-boiler-bridge` v0.5
- Contrat HA de consommation ACK v1.2

---

## 1. Rôle

Ce script constitue la frontière exécutive canonique entre Home Assistant et le boiler bridge.

Il a pour unique responsabilité de :

- préparer une transaction valide,
- publier la commande MQTT,
- ouvrir une attente corrélée,
- conclure la transaction sur ACK terminal,
- restituer un résultat exploitable au reste d'Arsenal.

Il est strictement exécutif : aucune décision métier, aucune heuristique, aucune validation par télémétrie, aucune reconstruction locale du succès.

---

## 2. Principe cardinal

> Le script n'exécute pas une commande parce qu'il publie un message.
> Le script n'exécute réellement que lorsqu'il obtient un ACK terminal corrélé.

Conséquences :

- `publier` ≠ exécuter
- `accepted` ≠ succès
- télémétrie cohérente ≠ succès
- `applied` corrélé = seul succès

---

## 3. Entrées contractuelles

Le script reçoit **obligatoirement** :

| Paramètre | Description |
|-----------|-------------|
| `topic_command` | Topic MQTT de publication de la commande |
| `topic_ack` | Topic MQTT d'écoute de l'ACK |
| `value` | Valeur à appliquer, déjà validée par la couche amont |
| `request_helper` | Helper de corrélation dédié à cette transaction |
| `timeout_local` | Délai d'attente local (voir §3.1) |
| `source` | Identifiant de la source émettrice, non vide |

Le script peut recevoir **facultativement** : metadata métier, `reason_helper`, `status_helper`, `result_target`.

### 3.1 Contraintes

- `topic_command` et `topic_ack` doivent être explicitement fournis.
- `request_helper` doit être dédié à une seule transaction logique.
- `timeout_local` doit respecter `timeout_local > timeout_bridge`, avec `timeout_bridge = 10 s` côté bridge — cohérent avec la recommandation de 12 à 15 s du contrat HA.
- `source` doit être non vide.

---

## 4. Préconditions obligatoires

Le script ne peut démarrer que si toutes les conditions suivantes sont vraies.

### 4.1 Bridge disponible

```
boiler/bridge/online == "online"
```

au moment du départ de la transaction, conformément au contrat HA.

### 4.2 Aucune transaction résiduelle

Le helper `request_helper` doit être vide ou explicitement nettoyé.

### 4.3 Paramètre exécutable

La valeur transmise au script doit déjà être conforme au contrat métier amont : bornes, type attendu, sémantique métier.

> Le script exécutif ne décide pas si la valeur est pertinente. Il exécute seulement une valeur déjà autorisée par la couche amont.

À partir de `arsenal-boiler-bridge` v0.5, le bridge valide strictement les bornes physiques **et le pas** des paramètres de courbe avant toute émission boiler (voir §8.3 et §18). Une valeur hors bornes ou hors pas produit un ACK `rejected` avec une `reason` spécifique. Ces cas signalent un bug de pipeline Arsenal amont — ils ne doivent jamais se produire en production nominale.

La couche décision Arsenal est contractuellement responsable d'émettre des valeurs conformes aux bornes et au pas physiques avant d'invoquer ce script.

### 4.4 Unicité locale

Aucune seconde instance du même script ne doit manipuler le même `request_helper` simultanément.

### 4.5 Synchronisation temporelle (NTP)

Home Assistant et `arsenal-boiler-bridge` doivent être synchronisés sur une source NTP commune.

**Dérive maximale tolérée : 2 secondes.**

> Sans cette précondition, les champs `ts` et `expires_at` des payloads de commande peuvent être évalués de façon incohérente côté bridge, produisant des rejets `expired` erronés ou des fenêtres d'expiration imprévues. Ces dégradations sont silencieuses et difficiles à diagnostiquer.

Cette précondition est une exigence d'infrastructure. Elle n'est pas vérifiable à chaque transaction — elle doit être garantie par la configuration système (NTP actif sur HA et sur le Pi).

---

## 5. Sorties contractuelles

Le script doit conclure par un statut terminal unique parmi : `applied`, `rejected`, `timeout`, `aborted`.

### 5.1 Sémantique

| Statut | Signification |
|--------|--------------|
| `applied` | Exécution confirmée par ACK corrélé |
| `rejected` | Refus explicite via ACK corrélé |
| `timeout` | Aucun ACK terminal corrélé dans le délai |
| `aborted` | Impossibilité de démarrer la transaction localement avant publication valide |

> `aborted` est un statut local HA. Il ne remplace pas un ACK bridge — il décrit un échec d'entrée dans la transaction.

**Table exhaustive des cas :**

| Situation | Statut | Retry autorisé |
|-----------|--------|----------------|
| Bridge offline au départ de la transaction | `aborted` | Non — attendre retour bridge |
| `request_helper` non vide au départ | `aborted` | Non — investiguer transaction précédente |
| Vérification post-écriture helper échouée (§7.2) | `aborted` | Non — investiguer concurrence |
| Échec de publication MQTT (erreur réseau ou broker) | `aborted` | Selon stratégie amont |
| Aucun ACK terminal reçu dans `timeout_local` | `timeout` | Oui — si autorisé par stratégie amont (§12) |
| Bridge passé offline pendant `pending` | `timeout` | **Non** — voir §10 |

---

## 6. Machine d'état du script

### 6.1 États internes

| État | Description |
|------|-------------|
| `idle` | Aucun travail en cours |
| `precheck` | Validation des préconditions |
| `armed` | `request_id` généré et helper préparé |
| `published` | Commande MQTT publiée |
| `pending` | Attente ACK corrélé |
| `applied` | Succès |
| `rejected` | Refus explicite |
| `timeout` | Délai dépassé |
| `aborted` | Annulation locale avant publication exploitable |
| `cleanup` | Nettoyage terminal |

### 6.2 Graphe nominal

```
idle → precheck → armed → published → pending → applied → cleanup → idle
```

### 6.3 Graphes d'échec

```
idle → precheck → aborted → cleanup → idle
idle → precheck → armed → published → pending → rejected → cleanup → idle
idle → precheck → armed → published → pending → timeout → cleanup → idle
```

---

## 7. Séquence canonique

### 7.1 Précheck

Le script vérifie `online == "online"`, l'absence de transaction résiduelle, et la cohérence minimale des paramètres.

Si échec : statut `aborted`, aucune publication, nettoyage, sortie.

### 7.2 Armement transactionnel

Le script génère un `request_id` UUID v4 unique, l'écrit immédiatement dans `request_helper`, et initialise les éventuels helpers de statut locaux.

> **Ordre strict :** l'écriture du `request_id` dans `request_helper` doit être atomique et immédiate — avant toute publication MQTT. Cette contrainte garantit qu'aucun ACK ne peut être reçu sans contexte de corrélation actif, prévenant le cas — rare mais réel — d'un ACK ultra-rapide arrivant avant l'écriture du helper et ignoré faute de contexte.

> **Vérification post-écriture obligatoire :** Home Assistant ne garantit pas l'atomicité des écritures de helpers au sens système. Une race condition reste possible en cas de mauvaise configuration ou d'instance concurrente. Le script **doit vérifier immédiatement après écriture** que `request_helper == request_id` attendu.
>
> Si la vérification échoue : statut `aborted`, aucune publication, nettoyage, sortie. Ne pas poursuivre avec un contexte de corrélation non fiable.

### 7.3 Publication

Le script publie sur `topic_command` un payload conforme au contrat bridge :

```json
{
  "request_id": "<uuid-v4>",
  "ts": "<ISO8601-UTC>",
  "expires_at": "<ISO8601-UTC>",
  "source": "<source>",
  "value": "<value>"
}
```

En JSON UTF-8 compact, conforme au format bridge.

- QoS = 1 (au minimum)
- retain = false

### 7.4 Attente

Le script ouvre une attente bornée sur `topic_ack`, avec corrélation stricte sur `request_id`.

Il ignore : tout ACK sans `request_id`, tout ACK de `request_id` différent, tout ACK reçu bridge offline, tout ACK `accepted` comme état final.

### 7.5 Conclusion

Le premier ACK terminal corrélé parmi `applied`, `rejected`, `timeout` clôture la transaction.

### 7.6 Nettoyage

Quel que soit le résultat terminal : suppression du `request_id` dans `request_helper`, nettoyage des états transitoires, retour à `idle`.

Échec de nettoyage → journalisation obligatoire + état critique

**Invariant : aucune transaction fantôme.**

---

## 8. Interprétation des ACK par le script

### 8.1 `accepted`

Autorisé comme signal transitoire. Jamais terminal. Jamais propagé comme succès. Peut être ignoré purement et simplement.

> **Note v0.5 :** `arsenal-boiler-bridge` v0.5 ne met plus `accepted` en cache de déduplication. Un duplicat MQTT reçu pendant la fenêtre d'exécution ne recevra donc plus `accepted` en replay — il ne recevra aucune réponse jusqu'à l'état final (`applied`, `rejected`, `timeout`). Ce comportement est conforme : `accepted` reste transitoire et le consommateur ne doit jamais l'attendre comme confirmation.

### 8.2 `applied`

Actions obligatoires : conclure en succès, autoriser l'écriture mémoire souveraine aval, exposer le résultat terminal `applied`, nettoyer.

### 8.3 `rejected`

Actions obligatoires : conclure en échec explicite, journaliser la `reason`, interdire toute écriture mémoire métier, nettoyer.

À partir de `arsenal-boiler-bridge` v0.5, les commandes de courbe de chauffe (`set_curve_shift`, `set_curve_slope`) peuvent produire des `reason` granulaires. Leur sémantique diagnostique est normative :

| `reason` | Origine | Diagnostic Arsenal |
|----------|---------|--------------------|
| `invalid_payload` | Payload malformé, champs manquants, types invalides | Bug de construction du payload côté HA |
| `expired` | `expires_at` dépassé à la réception | Latence réseau ou horloge désynchronisée |
| `invalid_type` | Valeur non numérique, NaN, Inf, bool | Bug de type côté couche décision Arsenal |
| `invalid_value_out_of_range` | Valeur hors bornes physiques chaudière | Bug de validation côté couche décision Arsenal — valeur non bornée avant émission |
| `invalid_step` | Valeur non conforme au pas physique (slope: 0.1 / shift: entier) | Bug de granularité côté couche décision Arsenal |
| `bridge_unavailable` | Écriture vclient échouée | Problème bridge/vcontrold, non lié à la valeur |

> `invalid_type`, `invalid_value_out_of_range` et `invalid_step` signalent **invariablement un bug de pipeline Arsenal amont**. Ils ne doivent jamais apparaître en production nominale. Leur occurrence doit déclencher une investigation de la couche décision émettrice, et non un retry.

### 8.4 `timeout`

Actions obligatoires : conclure en échec temporel, autoriser éventuellement un retry amont si prévu, nettoyer.

---

## 9. Règles strictes de corrélation

Le script ne doit exploiter un ACK que si les quatre conditions suivantes sont vraies :

```
ack.request_id == request_id_attendu
AND bridge_online == "online"
AND transaction_locale == pending
AND ack.status ∈ {applied, rejected, timeout}
```

Sinon : ACK ignoré strictement.

---

## 10. Rupture de session bridge

Si `boiler/bridge/online` passe à `offline` pendant `pending` :

- la transaction est immédiatement considérée comme interrompue,
- le script conclut en `timeout` fonctionnel,
- tout ACK ultérieur est ignoré.

**Distinction normative : incertitude vs interruption certaine**

| Situation | Nature réelle | Statut | Retry |
|-----------|--------------|--------|-------|
| Aucun ACK reçu dans le délai, bridge toujours online | Incertitude — état boiler inconnu | `timeout` | Autorisé si stratégie amont le prévoit |
| Bridge passé offline pendant `pending` | Interruption certaine — commande non exécutée | `timeout` | **Interdit** |

> Ces deux cas produisent le même statut terminal `timeout`, mais leur sémantique opérationnelle est différente. Le script **doit exposer l'état du bridge au moment de la clôture** à la couche amont (via helper ou contexte de résultat) pour lui permettre de distinguer les deux situations et d'arbitrer correctement le retry.

**Règle normative :** `timeout` avec bridge offline au moment de la clôture → **retry interdit**. La couche amont est responsable de lire l'état bridge avant de décider un éventuel retry.

---

## 11. ACK tardifs, dupliqués, résiduels

Le script doit ignorer strictement :

- **ACK tardif** : reçu après clôture locale de la transaction.
- **ACK dupliqué** : reçu après consommation d'un premier ACK terminal pour le même `request_id`.
- **ACK résiduel** : reçu après reboot / reconnexion, sans transaction active correspondante.

---

## 12. Retry

Le script exécutif ne décide pas librement du retry.

**Autorisé :** uniquement sur `timeout` avec bridge online au moment de la clôture, et seulement si une stratégie métier amont l'autorise explicitement.

**Interdit :**
- retry sur `rejected` — le bridge a refusé explicitement, retenter la même valeur produirait le même résultat
- retry sur `timeout` avec bridge offline au moment de la clôture (§10)
- retry infini ou non borné
- retry avec réutilisation du même `request_id`

**Règle normative — nouveau `request_id` obligatoire :**

> Tout retry doit générer un **nouveau `request_id` UUID v4**. La réutilisation d'un `request_id` existant est strictement interdite.
>
> Le bridge maintient un cache de déduplication par `request_id`. Réutiliser un identifiant déjà traité peut produire un replay de l'ACK précédent (potentiellement `timeout` ou `rejected`) sans nouvelle tentative d'écriture boiler. Le comportement résultant est imprévisible et non conforme.

Le script expose `timeout` comme résultat — c'est la couche amont qui arbitre, en tenant compte de l'état bridge (§10).

---

## 13. Écriture mémoire et helpers souverains

Le script exécutif ne doit écrire une mémoire métier, un helper souverain, ou un état durable que si `resultat_terminal == applied`.

**Interdictions absolues :** écrire sur `accepted`, écrire sur télémétrie cohérente, écrire sur simple publication MQTT, écrire sur absence d'erreur apparente.

---

## 14. Journalisation minimale

La journalisation du script exécutif doit rester exceptionnelle, ciblée et non bavarde.

Le script n'a pas vocation à produire une trace narrative de son déroulement. La transaction est déjà observable par le `request_id`, les ACK MQTT, et les éventuels helpers techniques dédiés.

### 14.1 Journalisation autorisée

Uniquement pour :

- échec de précondition locale (`aborted`)
- `rejected`
- `timeout`
- anomalie interne empêchant une conclusion normale

### 14.2 Journalisation non requise

Le script n'a pas à journaliser : début de transaction, publication nominale, réception de `accepted`, réussite `applied` (sauf exigence explicite d'observabilité locale).

### 14.3 Principe directeur

> En nominal, le script exécute et se tait.
> Il ne parle que si la transaction échoue, dévie, ou ne peut pas être engagée proprement.

### 14.4 Contenu minimal en cas de journalisation

Si une journalisation est émise, elle se limite à : nature de l'échec, `request_id` si disponible, domaine / action, `reason` si connue.

Aucune journalisation verbeuse pas-à-pas n'est conforme.

---

## 15. Invariants non négociables

| Réf | Invariant |
|-----|-----------|
| 15.1 | **Unicité** — un script = une transaction = un `request_id` |
| 15.2 | **Clôture** — toute transaction ouverte se clôture par `applied`, `rejected`, `timeout` ou `aborted` |
| 15.3 | **Nettoyage** — aucune sortie terminale sans nettoyage de `request_helper` |
| 15.4 | **Vérité d'exécution** — aucune exécution reconnue sans `applied` corrélé |
| 15.5 | **Pas d'inférence** — le script n'utilise jamais la télémétrie comme preuve d'exécution |
| 15.6 | **Pas de concurrence sauvage** — deux transactions ne partagent jamais simultanément le même helper de corrélation |
| 15.7 | **Vérification post-écriture** — le script vérifie que `request_helper == request_id` immédiatement après écriture ; échec → `aborted` sans publication |
| 15.8 | **Synchronisation temporelle** — HA et boiler bridge sont synchronisés NTP avec une dérive < 2s ; sans cette garantie, les rejets `expired` peuvent être erronés et indétectables |
| 15.9 | **Retry avec nouveau `request_id`** — tout retry génère un nouvel UUID v4 ; la réutilisation d'un `request_id` est strictement interdite |

---

## 16. Anti-patterns explicitement interdits

- Publier puis supposer le succès sans ACK
- Conclure sur `accepted`
- Conclure sur variation de télémétrie
- Réutiliser un `request_id`
- Laisser un `request_helper` sale
- Déclencher un retry dans une boucle non bornée
- Lancer le script alors que `online ≠ "online"`
- Consommer un ACK sans corrélation stricte

---

## 17. Invariant global

> Le script exécutif transactionnel est conforme uniquement si :
>
> - il ouvre une transaction avec `request_id` unique,
> - il attend un ACK terminal corrélé,
> - il ne reconnaît le succès qu'en présence de `applied`,
> - il nettoie systématiquement sa corrélation locale,
> - il ignore tout signal non terminal, tardif, dupliqué ou hors ligne.

---

## 18. Bornes et pas physiques — paramètres de courbe (v0.5)

Ces valeurs sont normatives et opposables à toute couche émettrice Arsenal.  
Source : [`mqtt.md`](../../outils_externes/boiler_pi/mqtt.md) §5.3 et §5.4 / `arsenal-boiler-bridge` v0.4.3.

| Paramètre | Commande | Bornes | Pas | Type émis |
|-----------|----------|--------|-----|-----------|
| Pente courbe | `set_curve_slope` | [0.2 ; 3.5] | 0.1 | float (`round(1)`) |
| Parallèle courbe | `set_curve_shift` | [-13 ; 40] | 1 | int (entier strict) |

Toute valeur transmise à ce script pour ces commandes doit satisfaire simultanément :
- appartenir aux bornes ci-dessus,
- être conforme au pas (multiple exact de 0.1 pour la pente, entier pour le parallèle),
- être du type attendu.

Un échec sur l'un de ces critères produit un ACK `rejected` avec `reason` `invalid_value_out_of_range` ou `invalid_step` (voir §8.3). Ces cas sont des bugs Arsenal, pas des comportements bridge.

---

## Lecture pratique

Pour Arsenal, ce contrat impose un pattern unique :

```
précheck → armement → publish → attente corrélée → conclusion terminale → nettoyage
```

Pas d'autre modèle. Pas de "petit script rapide". Pas de raccourci.
