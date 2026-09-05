# 🧠 ARSENAL — AMENDEMENT NORMATIF · CHAUFFAGE — DÉCISION CENTRALE · Amendement : garde d'exécution composée
#
# 📌 STATUT :
#   AMENDEMENT au contrat central [`30_decision_centrale.md`](30_decision_centrale.md)
#   PORTÉE : §7 — Garde d'exécution — Disponibilité du système
#   NIVEAU : structurant — conditionne toute exécution descendante
#
# 🎯 OBJET :
#   Le §7 évalue la disponibilité du système d'exécution VIA UN SEUL SIGNAL,
#   `binary_sensor.boiler_bridge_online`. Ce signal ne suffit plus.
#
#   Trois effets normatifs :
#     1. faire de la disponibilité une garde COMPOSÉE, et non un signal unique ;
#     2. la qualifier PAR RÔLE et non globalement ;
#     3. DÉCIDER les deux seuils d'âge, et les motiver.
#
#   Cet amendement ne produit AUCUN patch runtime. Il ouvre le recâblage,
#   il ne l'exécute pas.
#
# 🔒 AUTORITÉ :
#   Opposable à toute implémentation de la garde d'exécution du domaine
#   chauffage et du domaine ECS.
#
# ----------------------------------------------------------
# 🧱 SUBORDINATION
#
#   Subordonné à :
#     • [00_gouvernance_chauffage.md](00_gouvernance_chauffage.md)
#     • [30_decision_centrale.md](30_decision_centrale.md)
#
#   Cohérent avec :
#     • [30_decision_centrale__amendement.md](30_decision_centrale__amendement.md)
#     • [10_souverainete_execution.md](10_souverainete_execution.md)
#
#   S'appuie sur, sans s'y subordonner :
#     • `architecture/chauffage/migration_boiler_bridge_vers_boilerack.md`
#     • `architecture/chauffage/interface_ha_boiler_bridge.md`
#
# ----------------------------------------------------------

---

## 1. Ce que le §7 disait, et pourquoi cela ne tient plus

Le contrat central énonce :

> *« La disponibilité du système d'exécution est une condition préalable à toute
> exécution descendante. Elle est évaluée via `binary_sensor.boiler_bridge_online`. »*

**Ce signal seul ne suffit plus, et la raison est structurelle.**

L'écrivain souverain **n'implémente aucune politique de reconnexion**. Après une
déconnexion inattendue, son testament fait passer le retenu `bridge/online` à
`offline` ; **s'il se reconnecte de lui-même, il ne le voit pas**, et le retenu
**restera `offline` alors que le service est vivant**, jusqu'à son prochain
démarrage.

> **Une garde fondée sur ce seul signal produirait un refus DURABLE sur un
> système parfaitement disponible.** Ce n'est pas un incident : c'est un faux
> négatif permanent, et il bloquerait toute exécution descendante sans que rien
> ne soit en panne.

**Symétriquement**, `online` demeure un signal **négatif fiable** : un `offline`
franc reste un motif légitime de refus.

---

## 2. La garde devient COMPOSÉE, et elle est qualifiée PAR RÔLE

**Le §7 est amendé comme suit.**

La disponibilité du système d'exécution **pour un rôle donné** est établie si, et
seulement si, les **quatre** conditions suivantes sont réunies :

| # | Condition | Nature |
|---|---|---|
| **1** | `<prefix>/bridge/online` vaut `online` | **nécessaire, jamais suffisante** |
| **2** | l'instantané `<prefix>/bridge/telemetry_status` porte un `ts` **d'âge inférieur ou égal au seuil du §3** | vivacité de la publication |
| **3** | `chain.status` vaut **`ok`** — ni `degraded`, ni `unavailable` | santé de la chaîne de lecture |
| **4** | `measurements[<rôle>].fresh` vaut **vrai** | fraîcheur de la grandeur commandée |

**La qualification est PAR RÔLE.** Une chaîne saine n'autorise pas à commander
un rôle dont la mesure est périmée : la condition 4 est **individuelle**, et
c'est délibéré.

**Les règles du §7 demeurent inchangées** : la garde ne participe pas à la
décision métier · elle conditionne uniquement la capacité d'exécution · elle est
évaluée **après** finalisation complète de `desired_mode` et `reason` · elle est
**non contournable**. Une décision valide peut donc être produite et non
exécutée.

> **`measurements[<rôle>].fresh` est une valeur normative de la surface amont**,
> définie comme `age_s ≤ 3 × période` de la mesure. **Arsenal la lit, il ne la
> recalcule pas.**

---

## 3. Les deux seuils d'âge — DÉCISION, et sa motivation

> **Ces deux seuils ne sont déduits d'aucun code.** La surface amont publie une
> période et un instant ; **elle ne publie aucune tolérance**. Le seuil est donc
> une **décision d'Arsenal**, et la voici.

### 3.1 Décision

| Signal | Seuil d'âge | Valeur courante |
|---|---|---|
| `<prefix>/bridge/telemetry_status` — champ `ts` | **3 × la période d'instantané** | **90 s** |
| `<prefix>/bridge/heartbeat` | **3 × la période de battement** | **90 s** |

**Le seuil est exprimé en MULTIPLE DE PÉRIODE, pas en secondes.** Les deux
périodes valent aujourd'hui 30 s et sont configurables : figer `90` en dur
rendrait la garde fausse au premier réglage.

### 3.2 Pourquoi trois périodes, et pas deux

**Le battement est publié en QoS 0 et n'est pas retenu.** Il **peut donc être
perdu sans que rien ne soit en panne** : c'est une propriété du transport, pas un
symptôme.

- **Deux périodes** ne toléreraient **qu'une seule perte**. Un unique battement
  égaré bloquerait toute exécution descendante — un refus provoqué par le
  transport, non par l'indisponibilité.
- **Trois périodes** tolèrent **deux pertes consécutives**. C'est la marge
  minimale qui rende la garde insensible à un aléa de transport isolé.

**Le facteur trois n'est pas emprunté au code : il est CHOISI**, et il l'est pour
une seconde raison — c'est déjà le facteur que la surface amont applique à sa
propre notion de fraîcheur. **Retenir un autre facteur pour la même famille de
signal serait arbitraire**, et rendrait le corpus plus difficile à tenir.

### 3.3 Ce que ce seuil n'est pas

**Il ne remplace pas le seuil de dégradation de 60 s** porté par la santé dérivée
de l'interface d'intégration. Les deux coexistent **et ne mesurent pas la même
chose** :

| | Objet | Effet |
|---|---|---|
| **60 s** | qualifier une **dégradation** | signal de diagnostic |
| **90 s** | qualifier une **incapacité à commander** | **garde bloquante** |

> **Une garde doit être PLUS tolérante qu'un diagnostic.** Aligner la garde sur
> le seuil de dégradation ferait refuser des commandes dès le premier signe de
> faiblesse, alors que le système est encore parfaitement capable d'exécuter.

---

## 4. Vocabulaire — matcher la projection publique

`chain.status` vaut **`ok`**, **`degraded`** ou **`unavailable`** : trois états,
pas davantage.

`chain.cause` et `last_result` partagent un **même vocabulaire public** :
`daemon_unreachable`, **`unsupported_command`**, `timeout`, `unusable_output`,
`transport_error` — `chain.cause` valant `null` **si et seulement si**
`chain.status` vaut `ok`.

> **`unknown_command` est un état INTERNE de la surface amont, et n'apparaît
> jamais sur le fil.** Toute implémentation **MUST** matcher la projection
> publique, jamais les états internes : un gabarit comparant à
> `unknown_command` ne s'apparierait à aucune valeur émise et **échouerait en
> silence**.

---

## 5. Ce que cet amendement ne fait pas

Il **n'exécute aucun recâblage** · **ne modifie aucun capteur, script, retry,
interface ou CI** · **ne renomme aucune entité** · **n'en crée aucune** ·
**ne touche pas à la surface `guard/*`**, qui demeure vivante et inchangée ·
**ne touche pas au ping ICMP d'hôte**, indépendant du transport MQTT ·
**n'impose rien à la surface amont**.

**Il lève un verrou normatif, et rien d'autre.**

---

## 6. Réserves

1. **Les deux seuils sont une décision, pas une mesure.** Ils n'ont **jamais été
   éprouvés en régime réel**, et une observation ultérieure pourra les rouvrir.
2. **La limite de reconnexion de la surface amont n'est pas corrigée** par cet
   amendement : elle est **contournée**. La corriger relèverait de l'amont.
3. **La garde composée n'a pas encore d'implémentation.** Elle est normative ;
   elle n'est pas en service.
