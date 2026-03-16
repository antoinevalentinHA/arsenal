# Arsenal — Architecture thermique & migration chaudière

**Remplacement ViCare par Optolink / KM-Bus**
Version : v4 | Date : 13/03/2026

---

## 1. Objectif

Ce document décrit :

1. l'architecture thermique actuelle du système Arsenal
2. les dépendances à ViCare
3. la stratégie de migration vers lecture et pilotage locaux de la chaudière
4. l'analyse des registres Optolink nécessaires

**Objectifs de la migration :**
- suppression de la dépendance cloud
- réduction de la latence
- robustesse accrue
- conservation intégrale de la logique Arsenal

> **Principe fondamental :** La migration ne modifie aucune logique métier. Elle remplace uniquement la source matérielle chaudière.

---

## 2. Architecture thermique Arsenal

Le système thermique Arsenal repose sur trois couches.

### 2.1 Couche matériel chaudière

**Architecture actuelle**

```
Chaudière Viessmann
        │
        ▼
     ViCare Cloud
        │
        ▼
Home Assistant — intégration ViCare
```

**Architecture cible**

```
Chaudière Viessmann
        │
        ▼
    Optolink / KM-Bus
        │
        ▼
Home Assistant — intégration locale
```

### 2.2 Couche abstraction Arsenal

Arsenal n'utilise jamais directement les entités ViCare. Une couche de capteurs template robustes assure la translation.

```
Sources chaudière
        │
        ▼
Capteurs template Arsenal
        │
        ▼
Scripts / Automatisations
        │
        ▼
Décision thermique
```

Cette abstraction rend la migration quasi transparente.

### 2.3 Couche décision thermique

Arsenal possède un moteur décisionnel séparé : chauffage, ECS, sécurité thermique, supervision.

La chaudière est traitée comme un **actionneur externe**.

---

## 3. Capteurs structurants Arsenal

Ces entités constituent **le contrat interne du système**. Elles ne doivent **pas être modifiées**.

**Chauffage**

```
sensor.programme_chauffage
sensor.chauffage_consigne_confort_local
sensor.chauffage_consigne_reduced_local
sensor.temperature_chaudiere_locale
binary_sensor.bruleur_physique_local
```

**ECS**

```
sensor.ecs_consigne_chaudiere_securisee
sensor.ecs_temperature_ballon_securisee
```

---

## 4. Architecture fonctionnelle ECS

Le système ECS repose sur deux capteurs fondamentaux.

**Flux consigne ECS**

```
Consigne ECS chaudière
        │
        ▼
sensor.ecs_consigne_chaudiere_securisee
        │
        ├── gardien consigne
        ├── watchdog ECS
        ├── sécurité rebond thermique
        └── logique ECS
```

**Flux température ballon**

```
Température ballon ECS
        │
        ▼
sensor.ecs_temperature_ballon_securisee
        │
        ├── détection fin de chauffe
        ├── calcul delta thermique
        ├── gestion boost
        └── logique ECS
```

---

## 5. Architecture chauffage

Le chauffage repose sur trois capteurs structurants.

```
sensor.programme_chauffage
sensor.chauffage_consigne_confort_local
sensor.chauffage_consigne_reduced_local
        │
        ├── scripts chauffage
        ├── correction courbe
        └── décision thermique centrale
```

---

## 6. Scripts chaudière (7)

```
\data\09_scripts\chauffage\consignes\confort.yaml
\data\09_scripts\chauffage\consignes\reduit.yaml
\data\09_scripts\chauffage\courbe_de_chauffe\application_parallele.yaml
\data\09_scripts\chauffage\courbe_de_chauffe\application_pente.yaml
\data\09_scripts\chauffage\synchro_consignes\confort.yaml
\data\09_scripts\chauffage\synchro_consignes\reduit.yaml
\data\09_scripts\ecs\cycle.yaml
```

Ces scripts représentent **l'interface d'écriture chaudière**. Ils seront les seuls modifiés lors de la migration (remplacement des appels de service ViCare).

---

## 7. Automatisations liées à la chaudière (6)

```
\data\10_automations\ecs\consigne_10\watchdog.yaml
\data\10_automations\ecs\consigne_10\gardien_consigne_reduite.yaml
\data\10_automations\ecs\consigne_10\applique_consigne_post_delai.yaml
\data\10_automations\ecs\consigne_10\verification_post_delai.yaml
\data\10_automations\panne\electricite\desactivation_mode_panne.yaml
\data\10_automations\chauffage\courbe_de_chauffe\correction_demarrage.yaml
```

Rôles : sécurité ECS, cohérence thermique, sortie de mode panne, corrections chaudière.
Ces automatisations restent **inchangées** après migration.

---

## 8. Primitives chaudière réellement utilisées

Arsenal utilise seulement **7 primitives chaudière**.

**Écriture**

| Fonction Arsenal | Action chaudière | Priorité |
|---|---|---|
| changer programme chauffage | set preset | haute |
| consigne confort | set comfort temperature | haute |
| consigne réduit | set reduced temperature | haute |
| pente courbe chauffe | set slope | moyenne |
| parallèle courbe chauffe | set parallel shift | moyenne |
| consigne ECS | set DHW temperature | haute |
| déclenchement ECS | trigger one-shot | haute |

**Lecture**

| Information | Entité ViCare actuelle | Usage Arsenal |
|---|---|---|
| programme chauffage | `climate` → attr `active_vicare_program` | décision thermique |
| consigne confort | `number.vscotho1_200_11_temperature_de_confort` | synchronisation |
| consigne réduit | `number.vscotho1_200_11_reduced_temperature` | synchronisation |
| température départ | `sensor.vscotho1_200_11_supply_temperature` | diagnostics |
| température ballon | `sensor.vscotho1_200_11_dhw_storage_temperature` | logique ECS |
| état brûleur | `binary_sensor.vscotho1_200_11_bruleur` | supervision |

---

## 9. Correspondances ViCare → Arsenal

| Capteur Arsenal | Source ViCare actuelle |
|---|---|
| `sensor.programme_chauffage` | `climate.vscotho1_200_11_chauffage` → `active_vicare_program` |
| `sensor.chauffage_consigne_confort_local` | `number.vscotho1_200_11_temperature_de_confort` |
| `sensor.chauffage_consigne_reduced_local` | `number.vscotho1_200_11_reduced_temperature` |
| `sensor.temperature_chaudiere_locale` | `sensor.vscotho1_200_11_supply_temperature` |
| `binary_sensor.bruleur_physique_local` | `binary_sensor.vscotho1_200_11_bruleur` |
| `sensor.ecs_consigne_chaudiere_securisee` | `number.vscotho1_200_11_dhw_temperature` |
| `sensor.ecs_temperature_ballon_securisee` | `sensor.vscotho1_200_11_dhw_storage_temperature` |

---

## 10. Analyse des registres Optolink nécessaires

Cette section traduit les besoins fonctionnels Arsenal en objets/points de données chaudière. Les types d'objets sont stables entre modèles ; les adresses exactes peuvent varier selon firmware (Vitotronic/Vitodens).

### 10.1 Données chauffage

**Programme chauffage**

Utilisé par : `sensor.programme_chauffage`, `binary_sensor.chauffage_actif`

| Valeur chaudière | Traduction Arsenal |
|---|---|
| comfort / normal | Confort |
| sleep / reduced | Eco |

```
Objet : heating_circuit.mode  /  heating.program
Type  : enum
```

---

**Consigne confort**

Utilisé par : `sensor.chauffage_consigne_confort_local`, `script.chauffage_appliquer_consigne_confort`

```
Objet : heating_circuit.comfort_temperature
Type  : float (°C)
```

---

**Consigne réduit**

Utilisé par : `sensor.chauffage_consigne_reduced_local`, `script.chauffage_appliquer_consigne_reduite`

```
Objet : heating_circuit.reduced_temperature
Type  : float (°C)
```

---

**Courbe de chauffe — pente**

Utilisé par : `script.chauffage_appliquer_pente`, `automation.correction_demarrage`

```
Objet : heating_curve.slope
Type  : float
```

---

**Courbe de chauffe — parallèle**

Utilisé par : `script.chauffage_appliquer_parallele`

```
Objet : heating_curve.parallel_shift
Type  : float (°C)
```

---

### 10.2 Données ECS

**Consigne ECS**

Utilisé par : `sensor.ecs_consigne_chaudiere_securisee`, watchdog ECS, cycle ECS

```
Objet : dhw.temperature_setpoint
Type  : float (°C)
```

---

**Température ballon ECS**

Utilisé par : `sensor.ecs_temperature_ballon_securisee`, cycle ECS, calcul delta thermique

```
Objet : dhw.storage_temperature
Type  : float (°C) — lecture seule
```

---

### 10.3 Télémétrie chaudière

**Température départ chauffage**

Utilisé par : `sensor.temperature_chaudiere_locale`

```
Objet : boiler.supply_temperature
Type  : float (°C) — lecture seule
```

---

**État brûleur**

Utilisé par : `binary_sensor.bruleur_physique_local`, diagnostics chauffage

```
Objet : boiler.burner_state
Type  : bool  (0 = off / 1 = on)
```

---

### 10.4 Liste finale des objets nécessaires

**Lecture (6 objets)**

```
heating_circuit.mode
heating_circuit.comfort_temperature
heating_circuit.reduced_temperature
boiler.supply_temperature
dhw.storage_temperature
boiler.burner_state
```

**Écriture (7 objets)**

```
heating_circuit.mode
heating_circuit.comfort_temperature
heating_circuit.reduced_temperature
heating_curve.slope
heating_curve.parallel_shift
dhw.temperature_setpoint
dhw.one_time_charge
```

**Total : 13 objets chaudière distincts.**

> Toute interface Optolink capable d'exposer ces 13 points est compatible avec Arsenal.

---

## 11. Compatibilité interfaces Optolink

Exemples d'intégrations pouvant fournir ces données :

- EMS-ESP
- ebusd
- vitotronic-optolink
- vitoconnect local bridge

---

## 12. Données chaudière nécessaires — vue synthétique

| Donnée | Objet Optolink | Entité cible (exemple) | Mode |
|---|---|---|---|
| programme chauffage | `heating_circuit.mode` | `sensor.boiler_heating_program` | R/W |
| consigne confort | `heating_circuit.comfort_temperature` | `number.boiler_comfort_temp` | R/W |
| consigne réduit | `heating_circuit.reduced_temperature` | `number.boiler_reduced_temp` | R/W |
| pente courbe chauffe | `heating_curve.slope` | `number.boiler_curve_slope` | W |
| parallèle courbe chauffe | `heating_curve.parallel_shift` | `number.boiler_curve_shift` | W |
| consigne ECS | `dhw.temperature_setpoint` | `number.boiler_dhw_setpoint` | R/W |
| déclenchement ECS | `dhw.one_time_charge` | `button.boiler_dhw_oneshot` | W |
| température départ | `boiler.supply_temperature` | `sensor.boiler_supply_temperature` | R |
| température ballon | `dhw.storage_temperature` | `sensor.boiler_dhw_temperature` | R |
| état brûleur | `boiler.burner_state` | `binary_sensor.boiler_burner_state` | R |

---

## 13. Cartographie flux Arsenal

```
Chaudière
   │
   ▼
Optolink / KM-Bus
   │
   ▼
Capteurs bruts locaux
   │
   ▼
Template Sensors Arsenal
   │
   ├── chauffage
   │   ├── programme
   │   ├── consigne confort
   │   ├── consigne reduced
   │   ├── température chaudière
   │   └── état brûleur
   │
   └── ECS
       ├── consigne chaudière
       └── température ballon
```

---

## 14. Plan de migration

### Étape 1 — Installation interface

Installer l'interface Optolink / KM-Bus entre la chaudière Viessmann et le réseau local.

### Étape 2 — Intégration Home Assistant

Options possibles :
- EMS-ESP
- ebusd
- optolink HA
- vitotronic integrations

### Étape 3 — Création des capteurs bruts locaux

Créer les 10 entités locales brutes correspondant aux objets Optolink :

```yaml
sensor.boiler_supply_temperature       # boiler.supply_temperature
sensor.boiler_dhw_temperature          # dhw.storage_temperature
binary_sensor.boiler_burner_state      # boiler.burner_state
sensor.boiler_heating_program          # heating_circuit.mode
number.boiler_comfort_temp             # heating_circuit.comfort_temperature
number.boiler_reduced_temp             # heating_circuit.reduced_temperature
number.boiler_curve_slope              # heating_curve.slope
number.boiler_curve_shift              # heating_curve.parallel_shift
number.boiler_dhw_setpoint             # dhw.temperature_setpoint
button.boiler_dhw_oneshot              # dhw.one_time_charge
```

### Étape 4 — Adaptation des template sensors Arsenal

Remplacer la source dans chaque capteur structurant. Les 7 capteurs sont les seuls fichiers à modifier.

Exemple — `sensor.ecs_temperature_ballon_securisee` :

```yaml
# avant
sensor.vscotho1_200_11_dhw_storage_temperature

# après
sensor.boiler_dhw_temperature
```

### Étape 5 — Adaptation des scripts d'écriture

Remplacer les appels de service ViCare dans les 7 scripts par ceux de l'intégration locale.

### Étape 6 — Tests fonctionnels

**Chauffage :** mode confort / eco / modification consigne / correction courbe

**ECS :** déclenchement cycle / montée température / watchdog / gardien consigne

---

## 15. Validation

**Chauffage**

| Test | Critère de succès |
|---|---|
| changement mode confort / eco | `sensor.programme_chauffage` mis à jour |
| modification consigne confort | `sensor.chauffage_consigne_confort_local` correct |
| modification consigne réduit | `sensor.chauffage_consigne_reduced_local` correct |
| correction courbe chauffe | pente et parallèle appliqués |

**ECS**

| Test | Critère de succès |
|---|---|
| déclenchement cycle | cycle ECS lancé |
| atteinte température ballon | `sensor.ecs_temperature_ballon_securisee` correct |
| gardien consigne 10°C | watchdog actif et fonctionnel |
| watchdog fin de cycle | automatisation terminée correctement |

---

## 16. Stratégie rollback

- Garder ViCare actif pendant toute la durée de la migration
- Basculer uniquement les sources des capteurs template
- Rollback possible **immédiatement** à tout moment

---

## 17. Périmètre de migration

| Type | Nombre |
|---|---|
| Scripts | 7 |
| Automatisations | 6 |
| Capteurs structurants | 7 |
| UI | 1 |
| **Total fichiers** | **21** |
| **Objets chaudière nécessaires** | **13** |

Migration : **limitée, maîtrisée et entièrement cartographiée.**

---

## Conclusion

Arsenal possède déjà une architecture idéale pour une migration locale :
- séparation logique / matériel
- capteurs robustes
- scripts idempotents
- sécurités indépendantes du cloud

Arsenal utilise un **sous-ensemble très réduit des capacités chaudière** — 13 objets distincts sur l'ensemble du protocole Optolink.

La migration vers Optolink consiste uniquement à **réalimenter les capteurs structurants avec des données locales**. Aucune modification de la logique Arsenal n'est nécessaire.
