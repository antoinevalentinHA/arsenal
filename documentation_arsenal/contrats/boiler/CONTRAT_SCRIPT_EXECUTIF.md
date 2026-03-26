# ARSENAL — Contrat d'exécution transactionnelle · Script exécutif MQTT — Boiler Bridge

**Composant :** `arsenal-ha`
**Version :** v1.1
**Scope :** Script exécutif Home Assistant publiant une commande MQTT transactionnelle vers `arsenal-boiler-bridge`
**Dépendances :**
- `arsenal-boiler-bridge` v0.4.3
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

### 4.4 Unicité locale

Aucune seconde instance du même script ne doit manipuler le même `request_helper` simultanément.

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

### 7.4 Attente

Le script ouvre une attente bornée sur `topic_ack`, avec corrélation stricte sur `request_id`.

Il ignore : tout ACK sans `request_id`, tout ACK de `request_id` différent, tout ACK reçu bridge offline, tout ACK `accepted` comme état final.

### 7.5 Conclusion

Le premier ACK terminal corrélé parmi `applied`, `rejected`, `timeout` clôture la transaction.

### 7.6 Nettoyage

Quel que soit le résultat terminal : suppression du `request_id` dans `request_helper`, nettoyage des états transitoires, retour à `idle`.

**Invariant : aucune transaction fantôme.**

---

## 8. Interprétation des ACK par le script

### 8.1 `accepted`

Autorisé comme signal transitoire. Jamais terminal. Jamais propagé comme succès. Peut être ignoré purement et simplement.

### 8.2 `applied`

Actions obligatoires : conclure en succès, autoriser l'écriture mémoire souveraine aval, exposer le résultat terminal `applied`, nettoyer.

### 8.3 `rejected`

Actions obligatoires : conclure en échec explicite, journaliser la `reason`, interdire toute écriture mémoire métier, nettoyer.

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

---

## 11. ACK tardifs, dupliqués, résiduels

Le script doit ignorer strictement :

- **ACK tardif** : reçu après clôture locale de la transaction.
- **ACK dupliqué** : reçu après consommation d'un premier ACK terminal pour le même `request_id`.
- **ACK résiduel** : reçu après reboot / reconnexion, sans transaction active correspondante.

---

## 12. Retry

Le script exécutif ne décide pas librement du retry.

**Autorisé :** uniquement sur `timeout`, et seulement si une stratégie métier amont l'autorise explicitement.

**Interdit :** retry sur `rejected`, retry infini, retry avec réutilisation du même `request_id`.

Le script expose `timeout` comme résultat — c'est la couche amont qui arbitre.

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

## Lecture pratique

Pour Arsenal, ce contrat impose un pattern unique :

```
précheck → armement → publish → attente corrélée → conclusion terminale → nettoyage
```

Pas d'autre modèle. Pas de "petit script rapide". Pas de raccourci.
