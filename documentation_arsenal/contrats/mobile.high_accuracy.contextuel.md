# CONTRAT `mobile.high_accuracy.contextuel` — v2.1

**Statut :** Draft — à valider avant implémentation  
**Domaine :** Infrastructure mobile / Perception  
**Portée :** Pilotage contextuel de la précision de localisation via Companion App

---

## 0. Périmètre d'application

Ce contrat s'applique à toute personne disposant :

- d'une entité `person.*` exploitable dans Arsenal
- d'un helper `input_text.telephone_*_notify` correctement configuré
- d'un téléphone mobile équipé de l'application Home Assistant Companion

Sont explicitement hors périmètre : tablettes, visiteurs temporaires sans intégration mobile, appareils non Companion.

---

## 1. Objet

Ce contrat définit les règles de pilotage du mode High Accuracy des téléphones mobiles via l'application Companion Home Assistant.

Il encadre :

- l'usage des commandes Companion (`high_accuracy`, `update_sensors`)
- leur déclenchement contextuel
- leur intégration dans l'architecture Arsenal

Objectif :

> Améliorer la réactivité de détection de présence lors du retour domicile, sans dégrader la sécurité ni l'autonomie des appareils.

---

## 2. Positionnement architectural

**Couche** : Infrastructure mobile — Companion

**Rôle** : levier de qualité de perception, sans intervention dans la décision métier

**Chaîne** :

```
Automation métier (contexte)
        │
        ▼
Scripts Core Mobile (exécution)
        │
        ▼
Companion App (téléphone)
        │
        ▼
Capteurs de présence (GPS / Wi-Fi)
```

---

## 3. Principe fondamental

> Le mode High Accuracy est un amplificateur de perception contextuel.  
> Il ne constitue ni une preuve, ni une décision, ni un état métier.

Conséquences :

- il améliore la qualité du signal
- il ne garantit aucun résultat
- il ne doit jamais être utilisé comme condition logique

---

## 4. Invariants

| ID  | Invariant |
|-----|-----------|
| I-1 | Aucune automation métier ne cible directement un `notify.mobile_app_*` |
| I-2 | Toute commande Companion passe exclusivement par les scripts Core Mobile |
| I-3 | Activation strictement événementielle — sur entrée dans la zone, jamais sur état statique |
| I-4 | Aucun mécanisme de retry, watchdog ou ACK n'est autorisé |
| I-5 | L'échec d'une commande mobile ne déclenche aucun contournement logique |
| I-6 | Le High Accuracy ne constitue jamais un état exploitable métier |
| I-7 | Le désarmement automatique ne consulte jamais l'état du High Accuracy ni le succès supposé d'une commande Companion |
| I-8 | Aucune duplication de calcul géographique en template |

---

## 5. Infrastructure concernée

### Scripts Core Mobile

#### `script.mobile_high_accuracy_on`

- Active le mode High Accuracy sur une cible dynamique
- Pure exécution — ne décide pas du contexte
- Aucun retry, aucun ACK

#### `script.mobile_high_accuracy_off`

- Désactive le mode High Accuracy sur une cible dynamique
- Pure exécution

#### `script.mobile_update_sensors`

- Force une remontée immédiate des capteurs
- Best-effort uniquement
- Aucun ACK attendu, aucune garantie de résultat

### Capteurs d'infrastructure

| Entité | Sémantique |
|--------|------------|
| `binary_sensor.approche_securite_antoine` | `on` si `person.antoine` est dans `zone.approche_securite`, `off` sinon |
| `binary_sensor.approche_securite_constance` | `on` si `person.constance` est dans `zone.approche_securite`, `off` sinon |

**Règle** : ces capteurs sont des projections d'infrastructure pure. Ils ne constituent ni une présence canonique, ni une décision, ni une autorisation métier. Ils ne doivent pas être consommés par des domaines métier (chauffage, sécurité, présence canonique).

### Timer d'infrastructure

| Entité | Rôle |
|--------|------|
| `timer.high_accuracy_securite` | Borne la durée maximale d'activation du High Accuracy — déclenche la désactivation en cas de non-résolution |

La durée de ce timer doit être cohérente avec un temps d'approche réel du domicile. Une valeur excessive constitue une mauvaise implémentation du contrat.

---

## 6. Référentiels géographiques Arsenal

Arsenal repose sur plusieurs zones géographiques distinctes aux rôles non interchangeables :

| Zone | Rôle | Nature |
|------|------|--------|
| `zone.home` | Confort — chauffage, présence large | Large |
| `zone.maison_securite` | Sécurité — désarmement, présence sécuritaire | Précise |
| `zone.approche_securite` | Infrastructure — déclenchement High Accuracy | Dédiée |

Le présent contrat :

- ne redéfinit pas ces zones
- ne modifie pas leur rôle
- ne suppose pas leur interchangeabilité

### Justification de zone.approche_securite

`zone.home` est trop large — elle peut inclure des zones de vie fréquentes (lieu de travail, commerces), entraînant des activations parasites.

`zone.maison_securite` peut être trop petite — elle risque d'activer le High Accuracy trop tard pour améliorer la remontée de présence.

Aucune zone métier existante ne satisfait simultanément les contraintes d'anticipation et de pertinence. `zone.approche_securite` est introduite à cet effet exclusif.

---

## 7. Conditions d'activation

Le High Accuracy est activé, **par personne**, si :

- `alarm_control_panel.alarme_maison` = `armed_away`
- ET événement d'entrée dans `zone.approche_securite`

L'activation est déclenchée sur un événement d'entrée dans `zone.approche_securite`, et jamais sur un état statique de présence dans cette zone. Une implémentation ne doit pas activer le High Accuracy au démarrage ou au rechargement sur la seule base d'un état déjà égal à `home`.

---

## 8. Conditions de désactivation

Le High Accuracy est désactivé si :

- l'alarme est désarmée
- ou `timer.high_accuracy_securite` expire

La désactivation est appliquée globalement à toutes les cibles lorsque la condition de désactivation est remplie.

> La durée de `timer.high_accuracy_securite` doit rester courte — de l'ordre de quelques minutes — et cohérente avec un temps d'approche réel du domicile. Une durée excessive constitue une mauvaise implémentation du contrat.

Chronologie nominale attendue :

```
extérieur → entrée zone.approche_securite → High Accuracy ON + timer start
        → entrée zone.maison_securite → présence détectée → désarmement → High Accuracy OFF
```

### Clause fausse approche (hors périmètre v2.1)

La gestion du cas "sortie de zone.approche_securite sans retour domicile" (demi-tour, fausse approche) n'est pas traitée explicitement en v2.1. Le timeout défensif de `timer.high_accuracy_securite` en limite les effets de consommation. Un mécanisme d'état dédié fera l'objet d'un avenant si le besoin est confirmé en production.

---

## 9. Dimensionnement de zone.approche_securite

Le rayon de `zone.approche_securite` doit être déterminé empiriquement pour garantir :

- une activation assez précoce pour améliorer la remontée de présence
- sans inclure durablement des zones de vie fréquentes non liées au retour domicile

Contraintes de dimensionnement :

- le rayon doit être supérieur à celui de `zone.maison_securite`
- le rayon doit rester strictement inférieur à celui de `zone.home` dès lors que `zone.home` inclut des zones de vie fréquentes
- un rayon inférieur à 150 m est une mauvaise implémentation du contrat

Le dimensionnement optimal ne peut pas être purement théorique. Il doit être validé par observation des activations réelles, mesure empirique des temps d'arrivée, et ajustement progressif du rayon.

---

## 10. Interdictions explicites

| Interdit | Justification |
|----------|---------------|
| Cibler directement `notify.mobile_app_*` | violation I-1 |
| Contourner les scripts Core Mobile | violation I-2 |
| Activer sur état statique ou au boot/reload | violation I-3 |
| Activer en continu tant que l'alarme est armée | violation I-3 |
| Utiliser `zone.home` comme déclencheur du High Accuracy | détournement de rôle métier, activation parasite probable |
| Utiliser `zone.maison_securite` comme déclencheur du High Accuracy | détournement de rôle métier, activation trop tardive probable |
| Utiliser `zone.approche_securite` dans une logique métier de chauffage, climatisation, sécurité ou présence canonique | contamination infrastructure → métier |
| Consommer `binary_sensor.approche_securite_*` dans un domaine métier | violation §5 — capteurs d'infrastructure uniquement |
| Ajouter retry / watchdog | violation I-4 |
| Conditionner un désarmement au succès supposé d'une commande Companion | violation I-7 |
| Configurer `timer.high_accuracy_securite` avec une durée excessive | dérive batterie, mauvaise implémentation |
| Dupliquer la logique géographique en template | violation I-8 |

---

## 11. Effet attendu

- Activation anticipée mais pertinente
- Réduction drastique des activations inutiles
- Amélioration du taux de désarmement automatique
- Impact batterie maîtrisé, borné par `timer.high_accuracy_securite`
- Zones métier existantes intactes dans leur rôle et leur périmètre

---

## 12. Clause de non-garantie

> Le mode High Accuracy est un mécanisme probabiliste d'amélioration de perception.  
> Il ne garantit ni la détection, ni le délai de remontée des capteurs.

En conséquence :

- le délai d'entrée reste le seul filet de sécurité temporel du domaine alarme
- la décision centrale reste l'unique autorité de désarmement automatique
- aucune logique de compensation ne peut être introduite sur la base d'un échec présumé de ce mécanisme

---

## 13. Relations avec les autres contrats

| Contrat | Relation |
|---------|----------|
| `presence.security.individual` | Consommateur aval — ce contrat améliore la qualité des signaux exploités |
| `alarme.decision_centrale` | Non altéré — le désarmement reste gouverné exclusivement par la décision centrale |
| Architecture mobile Companion | Dépendance d'exécution — scripts Core Mobile uniquement |

Ce contrat n'altère aucun des contrats listés.

---

## 14. Classification

| Attribut | Valeur |
|----------|--------|
| Type | Contrat d'infrastructure contextuelle |
| Niveau | Intermédiaire (entre perception et métier) |
| Stabilité attendue | Élevée |
| Fréquence d'évolution | Faible |
