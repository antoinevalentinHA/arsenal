# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF
#     Batteries des capteurs
# ==========================================================

## 📌 Statut

- **Contrat normatif et opposable**
- Domaine : **Transversal / Fiabilité des capteurs**
- Version : v1.0 (initiale)
- Portée : Arsenal v8.x+

Ce contrat définit les règles strictes de **gouvernance, supervision et maintenance**
des batteries des capteurs utilisés dans le système Arsenal.

Il constitue la **référence normative unique** pour toute évolution liée :

- au périmètre des capteurs sur batterie,
- à la détection de batteries critiques,
- à la supervision UI,
- à la notification de maintenance,
- et aux invariants système associés.

---

## 🎯 Objet du contrat

Ce contrat définit :

- le **périmètre canonique** des batteries surveillées,
- la **définition normative d’une batterie critique**,
- les **invariants système** associés,
- la **discipline de notification** de maintenance,
- la **sémantique des alertes critiques**,
- et les **interdits structurels**.

Il ne définit PAS :

- les stratégies de remplacement,
- la fréquence physique de changement de piles,
- la calibration des capteurs,
- ni aucune décision fonctionnelle basée sur un niveau de batterie.

---

## 🧱 Périmètre couvert

Le périmètre des batteries surveillées est défini **exclusivement** par :

- `group.batteries`

Ce groupe constitue la **source UNIQUE et canonique** de la liste des entités
dont le niveau de batterie est pris en compte par le système.

Il peut inclure :

- capteurs Zigbee,
- capteurs Netatmo,
- périphériques SwitchBot,
- équipements sécurité,
- capteurs atelier.

Aucun autre périmètre n’est autorisé.

---

## 🔗 Source de périmètre canonique

### Entité de référence

- `group.batteries`

Règle normative :

> Toute logique système liée aux batteries  
> DOIT dériver exclusivement de `group.batteries`.

Interdits :

- 🚫 Liste codée en dur dans un template  
- 🚫 Duplication de périmètre dans un autre capteur  
- 🚫 Sélection partielle non documentée  

---

## ⚙️ Définition normative d’une batterie critique

Une batterie est considérée comme **critique** si et seulement si :

- son état est **numérique**,  
- et sa valeur est **strictement inférieure à 28 %**.

Formellement :

  batterie critique ⇔ état numérique ∧ valeur < 28

Conséquences normatives :

| Cas                   | Interprétation           |
|-----------------------|--------------------------|
| valeur ≥ 28           | batterie acceptable      |
| valeur < 28           | batterie critique        |
| unknown / unavailable | **exclu de l’invariant** |

Les états :

- `unknown`  
- `unavailable`  
- non numériques  

ne déclenchent **pas** une alerte batterie critique par défaut.

---

## 🧠 Invariant système principal

### Entité

- `binary_sensor.batterie_a_remplacer`

### Rôle

Matérialiser l’invariant :

> **"Aucune batterie critique ne doit être ignorée par le système."**

### Définition

Ce binaire est :

- ON  → s’il existe **au moins une** batterie critique dans `group.batteries`  
- OFF → sinon  

Il est dérivé exclusivement de :

- `expand('group.batteries')`

Règles normatives :

- Il s’agit d’un **invariant de maintenance**.
- Il ne déclenche **aucune décision fonctionnelle**.
- Il est utilisé uniquement pour :
  - supervision système,
  - alerte utilisateur,
  - diagnostic.

---

## 📊 Mesure agrégée de maintenance

### Entité

- `sensor.batteries_faibles`

### Rôle

Fournir une **mesure agrégée de maintenance** :

- état principal :
  - nombre total de batteries critiques,
- attribut `faibles` :
  - liste détaillée des entités concernées
    avec leur niveau (%) restant.

### Définition normative

Ce capteur est dérivé exclusivement de :

- `group.batteries`

Il applique :

- le même **seuil normatif de 28 %**,  
- les mêmes règles d’exclusion :
  - `unknown`, `unavailable`, non numériques ignorés.

Règles normatives :

- Il ne déclenche **aucune action directe**.
- Il n’est utilisé que pour :
  - diagnostic,
  - information utilisateur,
  - alimentation des notifications disciplinées.

Interdits :

- 🚫 Liste codée en dur d’entités batterie  
- 🚫 Décision fonctionnelle basée sur ce capteur  

---

## 🩺 Intégration dans les Systèmes critiques

L’état batterie est intégré dans le panneau :

> 🩺 **Systèmes critiques**

via :

- `binary_sensor.batterie_a_remplacer`
- template UI : `carte_alerte_binaire_critique`

Règles normatives :

- L’alerte batterie est une **alerte critique de même rang** que :
  - coupure secteur,
  - réseau Zigbee dégradé,
  - automatisations désactivées.

- Elle est :
  - 🔴 rouge si `on`,
  - 🟢 verte si `off`,
  - ⚪ grise si indéterminée.

Interdits :

- 🚫 Autre template UI  
- 🚫 Autre sémantique couleur  
- 🚫 Toute action directe depuis cette carte  

---

## 🔁 Discipline temporelle des notifications

### Principe

Toute anomalie batterie persistante doit être notifiée :

- **au plus une fois par jour**,  
- et **au moins une fois par jour** tant qu’elle n’est pas résolue.

### Verrou de discipline

- `input_boolean.batteries_notifiees`

Sémantique :

| État | Sens                                          |
|------|-----------------------------------------------|
| OFF  | aucune notification envoyée aujourd’hui       |
| ON   | au moins une notification envoyée aujourd’hui |

Ce helper est un **verrou de discipline temporelle**, et non un état métier.

Il est :

- activé lors de l’envoi d’une notification,
- réinitialisé quotidiennement par une automation dédiée.

---

## 🔔 Orchestration de notification

### Automation quotidienne

- `Batteries faibles - Notification quotidienne`

Règles normatives :

- Déclenchement :
  - variation de `sensor.batteries_faibles`
- Conditions :
  - compteur > 0  
  - `input_boolean.batteries_notifiees == off`
- Comportement :
  - délégation de l’envoi à un script centralisé,
  - activation du verrou journalier.

Interdits :

- 🚫 Notification par polling périodique  
- 🚫 Notification sans discipline temporelle  
- 🚫 Notification directe depuis une autre automation  

---

## 🔔 Script de restitution utilisateur

### Entité

- `script.notification_batteries_faibles`

### Rôle

Script **UNIQUE** de restitution utilisateur concernant les batteries faibles.

Ce script :

- dépend exclusivement de :
  - `sensor.batteries_faibles`
- lit uniquement :
  - l’attribut `faibles`,
- génère un message :
  - lisible,
  - stable,
  - sans bruit inutile.

Règles normatives :

- Il ne :
  - scanne aucun capteur,
  - ne fixe aucun seuil,
  - ne prend aucune décision,
  - ne dépend d’aucune intégration matérielle.

Il est un **script de restitution pure**.

Interdits :

- 🚫 Ajouter une logique de détection dans ce script  
- 🚫 Envoyer une notification batterie sans passer par ce script  

---

## 🔄 Réinitialisation quotidienne

Une automation dédiée :

- réinitialise `input_boolean.batteries_notifiees`  
- tous les jours à **00:00:00**

Cette automation :

- ne détecte aucune anomalie,
- ne notifie pas,
- ne décide rien,
- lève uniquement le verrou temporel.

---

## 🧠 Sémantique des alertes critiques

Toute alerte batterie critique doit respecter :

- template : `carte_alerte_binaire_critique`
- sémantique :

| État  | Couleur | Sens          |
|-------|---------|---------------|
| on    |   🔴    | Alerte active |
| off   |   🟢    | OK            |
| autre |   ⚪    |Indéterminé    |

Interdits :

- 🚫 Action utilisateur directe  
- 🚫 Pilotage matériel  
- 🚫 Déclenchement fonctionnel  

Les alertes batteries sont **strictement de supervision**.

---

## 🚫 Interdits structurels

Il est strictement interdit de :

- utiliser un niveau de batterie comme condition de décision métier,
- déclencher une action fonctionnelle sur batterie faible,
- dupliquer la liste des batteries ailleurs que dans `group.batteries`,
- maintenir une liste codée en dur dans un template batterie,
- déclencher une notification sans passer par :
  - `sensor.batteries_faibles`
  - puis `script.notification_batteries_faibles`,
- modifier `input_boolean.batteries_notifiees` hors :
  - de l’automation de notification,
  - de l’automation de reset quotidien,
- afficher une alerte batterie hors du panneau Systèmes critiques.

---

## 🔁 Cycle de maintenance normatif

Le cycle attendu est :

  Batterie critique détectée
        ↓ 
  sensor.batteries_faibles > 0
        ↓ 
  binary_sensor.batterie_a_remplacer = ON
        ↓ 
  Alerte Systèmes critiques
        ↓ 
  Automation notification quotidienne
        ↓ 
  script.notification_batteries_faibles
        ↓ 
  Notification utilisateur
        ↓ 
  Maintenance physique
        ↓ 
  Retour à OFF

Ce cycle constitue le **cycle MCO batterie de référence**.

---

## 📌 Conclusion

Le sous-système Batteries est un **sous-système de sûreté de fonctionnement**.

Il garantit :

- un inventaire unique (`group.batteries`),
- une mesure agrégée fiable (`sensor.batteries_faibles`),
- un invariant robuste (`binary_sensor.batterie_a_remplacer`),
- une alerte critique cohérente,
- une discipline stricte de notification,
- une restitution utilisateur centralisée.

Toute évolution future DOIT respecter ce contrat.