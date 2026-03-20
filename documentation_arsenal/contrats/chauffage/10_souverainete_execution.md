# Arsenal — Contrat Normatif Fondateur
## Chauffage — Souveraineté d'Exécution (V3 Pro)

---

**Statut :** Contrat normatif fondateur — Gouvernance d'exécution

**Autorité :**
Ce document définit les règles de souveraineté d'exécution du sous-système Chauffage Arsenal.

Il formalise :
- qui est autorisé à exécuter une action ;
- dans quel périmètre ;
- sous quelle autorité ;
- avec quelles garanties ;
- et avec quelles interdictions absolues.

Il est opposable à toute implémentation : scripts d'application, automatisations matérielles,
adaptateurs locaux, commandes UI.

Subordonné à :
`/homeassistant/documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md`

---

## 1. Objet du contrat

Ce contrat définit la **souveraineté d'exécution** du sous-système Chauffage.

Il formalise :

- les niveaux d'autorité d'exécution ;
- la séparation stricte décision / application / validation / matériel ;
- les règles d'appel légitimes ;
- les interdictions formelles d'accès direct ;
- les garanties transactionnelles d'exécution.

Ce contrat garantit que :

> **AUCUNE ACTION MATÉRIELLE NE PEUT ÊTRE EXÉCUTÉE SANS DÉCISION CENTRALE,
> CHAÎNE D'APPLICATION OFFICIELLE ET VALIDATION EXPLICITE D'EXÉCUTION.**

---

## 2. Principe de souveraineté

Principe cardinal :

> **Le moteur Chauffage Arsenal est l'autorité souveraine de référence
> sur toute intention, toute décision et toute exécution thermique légitime.**

Cela implique :

- aucune entité externe ne produit de décision métier ;
- aucune UI ne produit d'ordre matériel autonome ;
- aucun adaptateur matériel n'est autorité décisionnelle ;
- aucun script n'est habilité à décider hors moteur ;
- aucune action n'est considérée comme réussie sans validation explicite.

Toute action matérielle légitime doit être :

- décidée par la Décision Centrale ;
- mémorisée comme décision de référence ;
- transmise par la couche d'application ;
- exécutée via l'adaptateur matériel officiel ;
- validée par un retour d'exécution explicite.

La souveraineté est donc définie comme :

> **Souveraineté par autorité décisionnelle
> et validation transactionnelle de l'exécution.**

---

## 3. Couches d'autorité d'exécution

L'architecture est structurée en **quatre couches d'autorité d'exécution**.

---

### 3.1 Couche Décisionnelle — Autorité suprême

**Rôle :**
- produire une décision explicite ;
- choisir un régime cible ;
- refuser toute action illégitime.

**Entités autorisées :**
- `script.chauffage_decision_centrale`
- moteurs décisionnels dérivés.

**Interdictions :**
- aucun accès matériel ;
- aucune écriture de consigne directe ;
- aucune interaction directe avec l'adaptateur.

---

### 3.2 Couche d'Autorisation — Intention thermique

**Rôle :**
- produire une intention autorisée ;
- décrire l'état thermique local ;
- proposer sans imposer.

**Entités autorisées :**
- `sensor.chauffage_autorisation_cible`
- capteurs d'intention thermique.

**Interdictions :**
- aucune décision ;
- aucune action ;
- aucun pilotage ;
- aucune lecture matérielle.

#### Autorisations contextuelles automatiques

Certaines autorisations thermiques peuvent être produites automatiquement par des mécanismes
contextuels légitimes, sans constituer une décision ni une action d'exécution.

Caractéristiques cardinales :

- ne produisent jamais d'ordre matériel ;
- ne déclenchent aucune exécution ;
- n'interagissent avec aucun adaptateur ;
- se limitent exclusivement à la couche d'autorisation.

Mécanismes reconnus : inhibition géofencing, pré-confort retour vacances.

Règles cardinales :

- ces mécanismes n'ont aucun droit d'accès aux couches d'application ou matérielle ;
- ils ne peuvent agir que par modification d'un helper d'autorisation reconnu ;
- ils ne peuvent jamais appeler un script d'exécution ni un adaptateur.

Toute interaction directe avec la chaîne d'exécution constitue une rupture de souveraineté.

---

### 3.3 Couche d'Application — Exécution logique

**Rôle :**
- traduire une décision en commande exécutable ;
- préparer la transaction d'exécution ;
- gérer la sérialisation et les transitions ;
- produire la traçabilité ;
- attendre un résultat explicite d'exécution.

**Entités autorisées :**
- `script.chauffage_appliquer_consigne`
- scripts d'application thermique.

**Garanties :**
- idempotence ;
- sérialisation ;
- protection anti-rebond ;
- vérification préalable d'état ;
- corrélation de commande (`request_id`) ;
- absence de succès implicite.

**Interdictions :**
- aucune décision autonome ;
- aucun arbitrage ;
- aucun contournement hiérarchique ;
- aucune validation implicite.

---

### 3.4 Couche Matérielle — Adaptateur d'exécution

**Rôle :**
- transmettre une commande validée par la couche d'application ;
- interfacer avec le matériel via l'adaptateur local officiel (boiler bridge) ;
- exposer les retours d'exécution ;
- n'exécuter aucune logique métier.

**Entités autorisées :**
- boiler bridge ;
- canal de transport MQTT ;
- mécanismes d'exposition des retours d'exécution ;
- adaptateurs locaux chauffage.

**Interdictions absolues :**
- aucune logique métier ;
- aucune décision locale ;
- aucune initiative autonome ;
- aucune correction implicite ;
- aucune réinterprétation de l'intention Arsenal.

---

## 4. Interdictions fondamentales

Il est **strictement interdit** :

- de publier une commande matérielle hors chaîne officielle ;
- d'émettre une action sans décision centrale préalable ;
- de modifier une consigne depuis l'UI par accès direct matériel ;
- de contourner le boiler bridge ;
- de créer une automatisation matérielle autonome ;
- de considérer une commande comme réussie sans validation explicite ;
- de déclencher une chauffe par seuil direct ;
- de produire une logique métier dans la couche matérielle.

Toute violation constitue :

- une rupture de souveraineté ;
- une dérive d'architecture ;
- une perte de gouvernance.

---

## 5. Gouvernance d'exécution

**Principes :**

- l'adaptateur matériel local est passif ;
- il ne décide jamais ;
- il ne constitue jamais une autorité métier ;
- il reste toujours subordonné au moteur Arsenal.

**Règles :**

- toute commande est initiée par un script d'application autorisé ;
- toute commande doit être traçable et corrélée (`request_id`) ;
- toute commande doit attendre un retour d'exécution explicite ;
- toute commande doit être clôturée par un statut explicite : `applied`, `rejected` ou `timeout` ;
- tout échec d'exécution doit être diagnostiquable.

**Objectifs :**

- garantir l'exécution locale et souveraine ;
- éviter tout contournement matériel ;
- supprimer toute réussite supposée.

---

## 6. UI, commandes manuelles et exceptions

**Règles cardinales :**

- aucune carte UI ne pilote directement le chauffage ;
- toute action utilisateur passe par un helper ou un script autorisé ;
- toute commande manuelle est réinterprétée par la Décision Centrale.

**Cas autorisés :**

- forçage confort via `input_boolean.mode_confort_chauffage` ;
- désactivation système via helpers de gouvernance ;
- modes maison officiels.

**Cas interdits :**

- slider thermostat direct ;
- carte climate interactive ;
- script UI appelant un adaptateur directement ;
- automatisation utilisateur hors moteur.

---

## 6 bis. Diagnostic d'échec d'exécution

Le sous-système Chauffage Arsenal traite tout retour d'exécution comme une information
contractuelle. Aucune commande n'est considérée comme appliquée sans confirmation explicite.

### Principe fondamental

La divergence critique à surveiller est :

    commande émise ≠ application validée

L'échec correspond à :
- rejet explicite par l'adaptateur (`rejected`) ;
- absence d'ACK dans le délai contractuel (`timeout`).

Ce mécanisme repose sur une séparation stricte entre :

- **émission de commande** (couche d'application) ;
- **réception du retour d'exécution** (couche matérielle) ;
- **qualification du résultat** (lecture pure, non décisionnelle).

Aucune décision thermique n'est produite dans ce cadre.
La Décision Centrale demeure l'unique autorité thermique.

### États de retour reconnus

| État ACK   | Signification                              | Action Arsenal                          |
|------------|--------------------------------------------|-----------------------------------------|
| `applied`  | Commande exécutée et confirmée             | État validé, traçabilité produite       |
| `rejected` | Commande refusée par l'adaptateur          | Échec qualifié, alerte diagnostic       |
| `timeout`  | Absence de retour dans le délai contractuel| Échec qualifié, alerte diagnostic       |

### Interdictions structurelles

Ce mécanisme est strictement interdit de :

- produire une décision thermique ;
- réévaluer une hiérarchie ;
- modifier `input_select.chauffage_dernier_mode_decide` ;
- intégrer une logique métier (présence, seuil, blocage, hystérésis) ;
- supposer un succès en l'absence d'ACK.

### Statut architectural

Ce mécanisme constitue un **invariant de validation transactionnelle**, garantissant :

- l'absence de succès implicite ;
- la traçabilité complète de toute exécution ;
- la détection déterministe de tout échec d'application.

La Décision Centrale Chauffage demeure **l'autorité unique de décision thermique**.
Toute autre couche lui est strictement subordonnée.

---

## 7. Traçabilité et audit d'exécution

Toute action matérielle doit produire :

- une décision traçable ;
- une raison métier explicite ;
- une commande identifiable (`request_id`) ;
- un retour d'exécution explicite (`applied` / `rejected` / `timeout`) ;
- un état final qualifié.

**Règles :**

- aucune action silencieuse ;
- aucune action non justifiée ;
- aucune transition invisible ;
- aucune réussite implicite.

**Objectifs :**

- auditabilité complète ;
- diagnostic simplifié ;
- compréhension humaine permanente.

---

## 8. Invariants de souveraineté

Invariants absolus :

- une seule source de décision ;
- une seule chaîne d'exécution officielle ;
- aucun accès direct matériel ;
- aucune action sans décision préalable ;
- aucune action sans validation explicite ;
- aucune UI souveraine ;
- aucune logique métier dans l'adaptateur matériel.

Toute violation constitue :

- une perte de contrôle système ;
- une rupture de gouvernance ;
- un risque énergétique majeur ;
- une dette architecturale critique.

---

## 9. Dépendances contractuelles

Ce contrat est subordonné à :
- `00_gouvernance_chauffage.md`

Il est fondation de :
- `30_decision_centrale.md`
- `40_blocages.md`
- `60_absence_inhibition_geofencing.md`
- `70_autorisation_thermostat.md`
- `80_table_decision_canonique.md`

Il gouverne directement :

- tous les scripts d'application chauffage ;
- toute commande vers l'adaptateur matériel officiel ;
- toute interaction UI chauffage ;
- toute automatisation d'exécution ;
- tout mécanisme de validation d'exécution.

---

## 10. Portée et stabilité

Ce contrat est :

- fondateur dans l'architecture Arsenal ;
- stable long terme ;
- modifié uniquement lors d'évolutions majeures ;
- versionné explicitement ;
- opposable à toute implémentation.

Il constitue la **charte de souveraineté d'exécution officielle du Chauffage Arsenal V3 Pro**.