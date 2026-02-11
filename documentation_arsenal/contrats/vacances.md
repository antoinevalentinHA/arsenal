# 🏖️ CONTRAT ARSENAL — MODE VACANCES

## 1. Objet du contrat

Le **mode Vacances** définit un **contexte global d’absence prolongée**.
Il permet au système Home Assistant Arsenal d’adapter son comportement
en garantissant **sobriété, sécurité et cohérence**, sans jamais introduire
de décisions implicites ou incontrôlées.

Ce contrat formalise :
- ce que signifie *être en vacances* pour le système,
- comment cette situation est détectée,
- quelles en sont les implications,
- et ce que le mode Vacances **ne fait volontairement pas**.

---

## 2. Principe fondamental

> **Vacances ≠ intention seule**  
> **Vacances = intention + absence réelle**

Le système distingue strictement :
- l’**intention utilisateur** (*mode_maison = Vacances*),
- la **réalité terrain** (présence humaine effective).

Le mode Vacances n’est considéré comme **effectif** que si **toutes les
conditions métier sont réunies simultanément**.

---

## 3. Sources d’information

### 3.1 Intention utilisateur

- `input_select.mode_maison`

Valeur attendue :
- `Vacances`

Cette entité **exprime uniquement l’intention**.
Elle ne déclenche aucune action directe à elle seule.

---

### 3.2 Réalité terrain

- `binary_sensor.presence_famille_unifiee`
- `input_boolean.visite_en_cours`

Ces entités représentent la **réalité humaine effective** dans le logement.

---

## 4. Décision métier Vacances

### 4.1 Capteur de décision finale

- `binary_sensor.vacances_actives`

#### Règle de calcul

Le mode Vacances est **effectif** si et seulement si :

- `mode_maison = Vacances`
- **ET** aucune présence famille détectée
- **ET** aucune visite en cours

Ce capteur constitue :
- la **vérité métier unique** du mode Vacances,
- une décision **pure, déterministe, stateless**,
- tolérante aux redémarrages Home Assistant.

Il :
- ❌ ne déclenche aucune action,
- ❌ ne pilote aucun équipement.

---

### 4.2 Capteur explicatif

- `sensor.vacances_raison`

Ce capteur fournit une **justification déterministe** de l’état Vacances,
selon une priorité stricte :

1. Mode maison non positionné sur Vacances
2. Présence famille détectée
3. Visite en cours
4. Vacances actives

Il garantit :
- une **lecture explicable** du système,
- une traçabilité claire en UI et en diagnostic.

---

## 5. Implications fonctionnelles

Lorsque `binary_sensor.vacances_actives = on`, le système peut :

- Autoriser des comportements spécifiques (ex. désinfection ECS au retour)
- Adapter certains sous-systèmes **via leurs propres contrats**
  (chauffage, ECS, éclairage, etc.)

⚠️ **Important** :  
Le mode Vacances **n’impose jamais directement** :
- une consigne,
- un arrêt,
- une activation d’équipement.

Toute action reste **déduite localement** par les sous-systèmes concernés,
selon leurs propres règles et garde-fous.

---

## 6. Ce que le mode Vacances ne fait pas

Par conception, le mode Vacances :

- ❌ ne force pas le chauffage en réduit
- ❌ ne coupe pas arbitrairement l’ECS
- ❌ ne déclenche pas d’automatisme caché
- ❌ ne dépend pas d’un horaire
- ❌ ne repose pas sur des temporisations implicites

Il **n’est pas un scénario**,  
il est un **contexte métier global**.

---

## 7. Interface utilisateur (UI Arsenal)

Le mode Vacances est exposé en UI via :

### 7.1 Templates dédiés

- `carte_vacances_decision`  
  Lecture de la décision réelle (Vacances actives / inactives)

- `carte_vacances_justification`  
  Lecture explicative de la raison métier

Ces cartes sont :
- en lecture seule,
- alignées visuellement et cognitivement avec le chauffage,
- sans aucune logique embarquée.

---

## 8. Robustesse et garanties

Le contrat Vacances garantit :

- Une décision **réversible à tout moment**
  (retour temporaire à la maison, visite, etc.)
- Une reprise automatique et cohérente du système
- L’absence totale d’effet de bord
- Une compréhension immédiate de l’état global

---

## 9. Statut du contrat

- ✔ Implémenté
- ✔ Testé en conditions réelles
- ✔ Intégré en UI
- ✔ Documenté
- ✔ Stable

👉 **Contrat Vacances validé et clos.**

---
