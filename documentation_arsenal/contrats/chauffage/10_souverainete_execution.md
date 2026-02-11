# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF FONDATEUR
#     CHAUFFAGE — SOUVERAINETÉ D’EXÉCUTION (V3 PRO)
# ==========================================================
#
# 📌 STATUT :
#   CONTRAT NORMATIF FONDATEUR — GOUVERNANCE D’EXÉCUTION
#
# 🔒 AUTORITÉ :
#   Ce document définit les règles de **souveraineté d’exécution**
#   du sous-système Chauffage Arsenal.
#
#   Il formalise :
#     • qui est autorisé à exécuter une action,
#     • dans quel périmètre,
#     • sous quelle autorité,
#     • avec quelles garanties,
#     • et avec quelles interdictions absolues.
#
#   Il est OPPOSABLE à toute implémentation :
#     • scripts d’application,
#     • automatismes matériels,
#     • intégrations cloud,
#     • appels directs ViCare,
#     • commandes UI.
#
#   Subordonné à :
#     /homeassistant/documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#
# ==========================================================


# ----------------------------------------------------------
# 🎯 1. OBJET DU CONTRAT
# ----------------------------------------------------------

Ce contrat définit la **souveraineté d’exécution** du sous-système Chauffage.

Il formalise :

- les niveaux d’autorité d’exécution,
- la séparation stricte décision / application / matériel,
- les règles d’appel légitimes,
- les interdictions formelles d’accès direct,
- la protection contre les dérives API et UI.

Ce contrat garantit que :

> 🧠 **AUCUNE ACTION MATÉRIELLE NE PEUT ÊTRE EXÉCUTÉE  
> SANS PASSER PAR LE CERVEAU ARSENAL**

---

# ----------------------------------------------------------
# 🧠 2. PRINCIPE DE SOUVERAINETÉ
# ----------------------------------------------------------

Principe cardinal :

> 🔒 **Le moteur Chauffage Arsenal est l’autorité souveraine  
> de référence sur toute intention et toute décision thermique.**

Cela implique :

- aucune entité externe ne produit de décision métier,
- aucune UI ne produit d’ordre matériel autonome,
- aucune intégration cloud n’est autorité décisionnelle,
- aucun script n’est habilité à décider hors moteur.

Cependant :

- des dérives matérielles peuvent être injectées passivement,
- des synchronisations cloud peuvent modifier l’état réel,
- des redémarrages HA peuvent produire des incohérences transitoires.

Dans ces cas :

> 🧠 **Arsenal conserve la souveraineté par restauration de cohérence**,  
> et non par interdiction absolue d’injection externe.

Toute action matérielle légitime doit être :

- décidée par la Décision Centrale,
- mémorisée comme décision de référence,
- transmise par la couche d’application,
- exécutée par un adaptateur matériel,
- restaurée si nécessaire par une garde de cohérence.

La souveraineté est donc définie comme :

> 🔒 **Souveraineté par autorité décisionnelle  
> et restauration défensive de l’état matériel.**

---

# ----------------------------------------------------------
# 🧱 3. COUCHES D’AUTORITÉ D’EXÉCUTION
# ----------------------------------------------------------

L’architecture est structurée en **quatre couches souveraines**.

## 3.1 Couche Décisionnelle (Autorité suprême)

Rôle :

- produire une décision explicite,
- choisir un régime cible,
- refuser toute action illégitime.

Entités autorisées :

- `script.chauffage_decision_centrale`
- moteurs décisionnels dérivés.

Interdictions :

- aucun accès matériel,
- aucun appel ViCare,
- aucune écriture de consigne,
- aucune interaction directe.

---
## 3.2 Couche d’Autorisation (Intention thermique)

Rôle :

- produire une intention autorisée,
- décrire l’état thermique local,
- proposer sans imposer.

Entités autorisées :

- `sensor.chauffage_autorisation_cible`
- capteurs d’intention thermique.

---

### Autorisations contextuelles automatiques

Certaines autorisations thermiques peuvent être produites automatiquement
par des mécanismes contextuels légitimes, sans constituer une décision
ni une action d’exécution.

Caractéristiques cardinales :

- ne produisent jamais d’ordre matériel,
- ne déclenchent aucune exécution,
- n’interagissent avec aucune intégration,
- se limitent exclusivement à la couche d’autorisation.

Mécanismes reconnus :

- inhibition géofencing,
- pré-confort retour vacances.

Règles cardinales :

- ces mécanismes n’ont aucun droit d’accès aux couches d’application ou matérielle,
- ils ne peuvent agir que par modification d’un helper d’autorisation reconnu,
- ils ne peuvent jamais appeler un script d’exécution ni une intégration.

Toute interaction directe avec la chaîne d’exécution constitue une rupture de souveraineté.

---

Interdictions :

- aucune décision,
- aucune action,
- aucun pilotage,
- aucune lecture matérielle.

---

## 3.3 Couche d’Application (Exécution logique)

Rôle :

- traduire une décision en ordre logique,
- appliquer des consignes abstraites,
- gérer les transitions,
- produire la traçabilité.

Entités autorisées :

- `script.chauffage_consigne_confort`
- `script.chauffage_consigne_reduite`
- scripts d’application thermique.

Garanties :

- idempotence,
- sérialisation,
- protection anti-rebond,
- vérification d’état avant action.

Interdictions :

- aucune décision autonome,
- aucun arbitrage,
- aucun contournement hiérarchique.

---

## 3.4 Couche Matérielle (Adaptateurs & Intégrations)

Rôle :

- transmettre un ordre validé,
- interfacer avec ViCare,
- appliquer physiquement une consigne.

Entités autorisées :

- intégration ViCare,
- adaptateurs locaux chauffage,
- scripts proxy matériel.

Interdictions absolues :

- aucune logique métier,
- aucune décision locale,
- aucune initiative autonome,
- aucune correction implicite.

---

# ----------------------------------------------------------
# 🔒 4. INTERDICTIONS FONDAMENTALES
# ----------------------------------------------------------

Il est STRICTEMENT INTERDIT :

- d’appeler ViCare hors couche d’application,
- de modifier une consigne depuis l’UI,
- de piloter un thermostat directement,
- de créer une automatisation matérielle autonome,
- d’écrire un programme chauffage sans décision centrale,
- de déclencher une chauffe par seuil direct.

Toute violation constitue :

- une rupture de souveraineté,
- une dérive d’architecture,
- un risque de pompage API,
- une perte de gouvernance.

---

# ----------------------------------------------------------
# 🧠 5. GOUVERNANCE DES APPELS VI CARE
# ----------------------------------------------------------

Principes :

- ViCare est un **adaptateur matériel passif**,
- ViCare ne décide jamais,
- ViCare n’est jamais une autorité métier,
- ViCare est toujours subordonné au moteur Arsenal.

Règles :

- tout appel ViCare est initié par un script d’application,
- aucun appel périodique n’est autorisé sans nécessité métier,
- toute correction ViCare est contrôlée par Arsenal,
- toute dérive API est auditée.

Objectifs :

- réduire drastiquement les requêtes API,
- éviter les conflits cloud / local,
- garantir la souveraineté locale.

---

# ----------------------------------------------------------
# 🧩 6. UI, COMMANDES MANUELLES & EXCEPTIONS
# ----------------------------------------------------------

Règles cardinales :

- aucune carte UI ne pilote directement le chauffage,
- toute action utilisateur passe par un helper ou un script autorisé,
- toute commande manuelle est réinterprétée par la Décision Centrale.

Cas autorisés :

- forçage confort via `input_boolean.mode_confort_chauffage`,
- désactivation système via helpers de gouvernance,
- modes maison officiels.

Cas interdits :

- slider thermostat direct,
- carte climate interactive,
- script UI appelant ViCare,
- automatisation utilisateur hors moteur.

---

# ----------------------------------------------------------
# 🛡️ 6 bis. GARDE DE COHÉRENCE POST-MATÉRIELLE
# ----------------------------------------------------------

Le sous-système Chauffage Arsenal tolère l’existence de :

- synchronisations cloud ViCare,
- redémarrages Home Assistant,
- mises à jour matérielles,
- dérives passives de programme.

Ces événements peuvent produire :

- une divergence entre l’état matériel réel,
- et la dernière décision officiellement exécutée par Arsenal.

Dans ce cas :

- aucune décision thermique n’est produite,
- aucune hiérarchie n’est réévaluée,
- aucune autorisation n’est recalculée.

Un mécanisme défensif spécialisé est autorisé :

> 🧠 **GARDE DE COHÉRENCE POST-MATÉRIELLE**

---

## 🎯 Principe fondamental

Le mécanisme repose sur une séparation stricte entre :

- **détection de divergence** (lecture pure, qualifiée),
- **correction matérielle** (action défensive),
- **décision thermique** (strictement interdite).

Aucune décision n’est jamais prise dans ce cadre.  
La Décision Centrale demeure l’unique autorité thermique.

---

## 🧩 Architecture de référence

La garde de cohérence est désormais structurée en deux couches distinctes :

### 1️⃣ Détection qualifiée d’incohérence (lecture pure)

Un capteur métier dédié assure la détection déterministe de toute divergence :

- `binary_sensor.chauffage_incoherence_vicare_decision`

Rôle :

- comparer :
  - le programme réel ViCare (`sensor.programme_chauffage`)
  - la dernière consigne souveraine Arsenal (`input_select.chauffage_dernier_mode_decide`)
- qualifier une incohérence effective et stable

Propriétés cardinales :

- neutralisé si API indisponible  
- neutralisé si application matérielle en cours  
- ignore états Inconnu / unknown / unavailable  
- anti-rebond temporel intégré  
- lecture pure, non historisée  

Ce capteur constitue :

> 🧠 **LA SOURCE UNIQUE DE VÉRITÉ DE DIVERGENCE POST-MATÉRIELLE**

---

### 2️⃣ Correction défensive de cohérence

Une automation spécialisée est autorisée :

- `10240000000004 — Réalignement ViCare HA`

Déclenchement exclusif :

- sur transition `off → on` de  
  `binary_sensor.chauffage_incoherence_vicare_decision`
- ou sur stabilisation de Home Assistant (`input_boolean.systeme_stable`)

Rôle :

- restaurer strictement l’état matériel décidé,
- sans jamais recalculer ni réévaluer quoi que ce soit.

---

## 🚫 Interdictions structurelles

Ce mécanisme est strictement interdit de :

- produire une décision thermique,
- réévaluer une hiérarchie,
- modifier `input_select.chauffage_dernier_mode_decide`,
- appeler directement `climate.*`,
- intégrer une logique métier (présence, seuil, blocage, hystérésis),
- se déclencher autrement que par incohérence qualifiée ou redémarrage.

---

## 🛡️ Statut architectural

Ce mécanisme constitue :

> 🛡️ **UN INVARIANT DÉFENSIF DE SOUVERAINETÉ POST-MATÉRIELLE**  
> garantissant :

- l’alignement durable entre décision et matériel,
- l’immunité aux dérives cloud passives,
- l’absence totale de dépendance décisionnelle à ViCare,
- la restauration systématique et déterministe de l’état souverain.

La Décision Centrale Chauffage demeure :

> 🧠 **L’AUTORITÉ UNIQUE DE DÉCISION THERMIQUE**  
toute autre couche étant strictement subordonnée.

---

# ----------------------------------------------------------
# 🔁 7. TRAÇABILITÉ & AUDIT D’EXÉCUTION
# ----------------------------------------------------------

Toute action matérielle doit produire :

- une décision traçable,
- une raison métier explicite,
- un logbook lisible,
- un état final cohérent.

Règles :

- aucune action silencieuse,
- aucune action non justifiée,
- aucune transition invisible.

Objectifs :

- auditabilité complète,
- diagnostic simplifié,
- compréhension humaine permanente.

---

# ----------------------------------------------------------
# 🧱 8. INVARIANTS DE SOUVERAINETÉ
# ----------------------------------------------------------

Invariants absolus :

- une seule source de décision,
- une seule chaîne d’exécution,
- aucun accès direct matériel,
- aucune initiative cloud,
- aucune action sans décision préalable,
- aucune UI souveraine.

Toute violation constitue :

- une perte de contrôle système,
- une rupture de gouvernance,
- un risque énergétique majeur,
- une dette architecturale critique.

---

# ----------------------------------------------------------
# 🧠 9. DÉPENDANCES CONTRACTUELLES
# ----------------------------------------------------------

Ce contrat est :

- subordonné à :
  - `00_gouvernance_chauffage.md`

- fondation de :
  - `30_decision_centrale.md`
  - `40_blocages.md`
  - `60_absence_inhibition_geofencing.md`
  - `70_autorisation_thermostat.md`
  - `80_table_decision_canonique.md`

Il gouverne directement :

- tous les scripts d’application chauffage,
- tous les appels ViCare,
- toute interaction UI chauffage,
- toute automatisation matérielle.

---

# ----------------------------------------------------------
# 📌 10. PORTÉE & STABILITÉ
# ----------------------------------------------------------

Ce contrat est :

- fondateur dans l’architecture Arsenal,
- stable long terme,
- modifié uniquement lors d’évolutions majeures,
- versionné explicitement,
- opposable à toute implémentation.

Il constitue la **charte de souveraineté d’exécution officielle  
du Chauffage Arsenal V3 PRO**.

# ==========================================================