# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF FORMEL
#     CHAUFFAGE — TABLE DE DÉCISION CANONIQUE (V3 PRO)
# ==========================================================
#
# 📌 STATUT :
#   CONTRAT NORMATIF FORMEL — SPÉCIFICATION ULTIME DE DÉCISION
#
# 🔒 AUTORITÉ :
#   Ce document définit la TABLE DE DÉCISION CANONIQUE
#   du sous-système Chauffage Arsenal.
#
#   Il constitue la RÉFÉRENCE FORMELLE UNIQUE décrivant,
#   pour chaque combinaison de contextes, la décision thermique autorisée.
#
#   Il est OPPOSABLE à toute implémentation :
#     • scripts,
#     • automatismes,
#     • moteurs de règles,
#     • refactors futurs.
#
#   Toute divergence entre ce contrat et le comportement réel
#   constitue une erreur critique de conception.
#
#   Subordonné à :
#     /documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#
#   Implémenté par :
#     /documentation_arsenal/contrats/chauffage/30_decision_centrale.md
#
# ==========================================================


# ----------------------------------------------------------
# 🎯 1. OBJET DU CONTRAT
# ----------------------------------------------------------

Ce contrat définit la **table de décision canonique** du Chauffage Arsenal.

Il formalise :

- l’ensemble des cas décisionnels légitimes,
- leur ordre hiérarchique strict,
- les états finaux autorisés,
- les interdictions explicites,
- les règles d’abstention,
- la cohérence globale du moteur.

Ce document est la **spécification finale opposable**  
du comportement décisionnel du système Chauffage V3 PRO.

---

# ----------------------------------------------------------
# 🧠 2. PRINCIPES GÉNÉRAUX DE LA TABLE
# ----------------------------------------------------------

Principes structurants :

- la table est évaluée de haut en bas,
- la première règle applicable est souveraine,
- aucune règle ultérieure ne peut être évaluée,
- toute décision est déterministe,
- aucun cas implicite n’est autorisé.

Règles cardinales :

- tout cas non listé est interdit,
- toute ambiguïté est une erreur,
- toute absence de règle produit une abstention.

---

# ----------------------------------------------------------
# ⚖️ 3. AXES D’ÉVALUATION OFFICIELS
# ----------------------------------------------------------

Chaque ligne de la table est évaluée selon les axes suivants :

### 3.1 Blocages hiérarchiques

- chauffage autorisé système
- fenêtres ouvertes
- aération en cours / bloquée
- poêle actif / mémoire poêle
- mode maison Vacances

### 3.2 Régime global

- présence
- absence
- vacances

### 3.3 Autorisation thermique locale

Valeurs possibles :

- `comfort`
- `neutre`
- `reduced`

---

### Autorisations forcées amont

Certaines valeurs d’autorisation peuvent être produites
par des mécanismes amont non thermiques.

Sources reconnues :

- **override opérateur** via `mode_confort_chauffage`,
- inhibition géofencing,
- pré-confort retour vacances.

Règles cardinales :

- `mode_confort_chauffage` constitue une **commande opérateur souveraine**.
- Lorsqu’il est actif, il est équivalent à l’exécution manuelle
  du script de passage en mode confort.
- Il impose la décision finale `comfort` indépendamment
  des blocages hiérarchiques et des règles d’abstention.
- Il est évalué **avant** toute application de la table décisionnelle standard.
- Il ne contourne jamais les sécurités matérielles hors périmètre Arsenal.

- Les sources **inhibition géofencing** et **pré-confort retour vacances**
  ne constituent pas des overrides.
- Elles sont évaluées strictement comme une autorisation `comfort` standard
  et restent intégralement soumises :
  - aux blocages hiérarchiques,
  - au régime global,
  - aux règles d’absence / vacances,
  - aux cas interdits formels.

### 3.4 Inhibition géofencing

- inactive
- active

### 3.5 État actuel du programme

- `comfort`
- `reduced`
- `unknown`

---

# ----------------------------------------------------------
# 🧱 4. PRIORITÉ ABSOLUE — BLOCAGES
# ----------------------------------------------------------

Exception souveraine :

Lorsque `input_boolean.mode_confort_chauffage` est actif,
la présente section n’est pas évaluée.
La décision finale imposée est `comfort`.

Hors override opérateur, les règles ci-dessous s’appliquent strictement.

---

| Ordre | Blocage actif                               | Décision finale | Justification |
|-------|---------------------------------------------|-----------------|---------------|
| 1     | Chauffage non autorisé système              | Abstention      | Interdiction système (hors override opérateur) |
| 2     | Fenêtre ouverte                             | `reduced`       | Chauffe vers l’extérieur interdite |
| 3     | Aération en cours                           | `reduced`       | Respect inertie et purge thermique |
| 4     | Blocage post-aération                       | `reduced`       | Interdiction reprise prématurée |
| 5     | Blocage poêle événementiel actif (timer)    | `reduced`       | Verrou de sûreté temporisé poêle |
| 6     | Mode maison = Vacances                      | `reduced`       | Sobriété maximale imposée |

Règles :

- hors override opérateur, toute autorisation est ignorée,
- toute inhibition géofencing est annulée,
- les blocages ci-dessus sont souverains en régime automatique,
- l’override utilisateur constitue l’unique exception autorisée.

---

# ----------------------------------------------------------
# 🌡️ 5. RÉGIME PRÉSENCE — TABLE PRINCIPALE
# ----------------------------------------------------------

Contexte :  
- override opérateur inactif  
- aucun blocage actif  
- régime = présence  

| Autorisation cible | Programme actuel | Décision finale | Règle |
|-------------------|------------------|-----------------|-------|
| `comfort`         | `reduced`        | `comfort`       | Besoin thermique avéré |
| `comfort`         | `comfort`        | Abstention      | Déjà en confort |
| `neutre`          | `comfort`        | Abstention      | Confort suffisant |
| `neutre`          | `reduced`        | Abstention      | Sobriété maintenue |
| `reduced`         | `comfort`        | `reduced`       | Fin de besoin / sobriété |
| `reduced`         | `reduced`        | Abstention      | Déjà en reduced |

Règles cardinales :

- `neutre` produit toujours une abstention,
- aucune oscillation `comfort ↔ reduced` n’est autorisée sans justification thermique,
- cette table n’est jamais évaluée lorsque `mode_confort_chauffage` est actif.

---

# ----------------------------------------------------------
# 🔁 6. RÉGIME ABSENCE — TABLE PRINCIPALE
# ----------------------------------------------------------

Contexte :  
- override opérateur inactif  
- aucun blocage actif  
- régime = absence  
- inhibition géofencing inactive  

| Autorisation | Programme actuel | Décision finale | Règle |
|--------------|------------------|-----------------|-------|
| `comfort`    | `reduced`        | Abstention      | Confort interdit en absence |
| `comfort`    | `comfort`        | `reduced`       | Retour sobriété |
| `neutre`     | `comfort`        | `reduced`       | Fin confort absence |
| `neutre`     | `reduced`        | Abstention      | Sobriété normale |
| `reduced`    | `comfort`        | `reduced`       | Forçage sobriété |
| `reduced`    | `reduced`        | Abstention      | État nominal absence |

Règle cardinale :

> ⚠️ En régime automatique d’absence, toute recherche de confort
> est interdite hors inhibition géofencing.

---

### Autorisations forcées en absence

En régime **Vacances effectif** (au sens strict : `binary_sensor.vacances_actives = on`),
hors override opérateur, toute autorisation `comfort`
produite :

- par pré-confort retour vacances,
- par mécanisme amont non utilisateur,

est traitée comme une autorisation locale standard
et soumise intégralement aux règles suivantes :

- sans inhibition géofencing active :
  - toute autorisation `comfort` produit une abstention,
  - aucun passage en confort n’est autorisé.

Note :

Le forçage utilisateur via `mode_confort_chauffage`
ne relève pas de la présente section.
Il constitue un override souverain et impose `comfort`
indépendamment du régime Vacances.

Règle absolue :

> ⚠️ Le pré-confort retour vacances ne peut JAMAIS
> produire une décision de confort en absence réelle
> hors inhibition géofencing explicitement active.

---

# ----------------------------------------------------------
# 🧠 7. ABSENCE AVEC INHIBITION GÉOFENCING ACTIVE
# ----------------------------------------------------------

Contexte :  
- override opérateur inactif  
- régime = absence  
- inhibition géofencing active  
- aucun blocage hiérarchique  

| Autorisation simulée | Programme actuel | Décision finale | Justification |
|---------------------|------------------|-----------------|---------------|
| `comfort`           | `reduced`        | `comfort`       | Préservation reprise thermique |
| `comfort`           | `comfort`        | Abstention      | Déjà stabilisé |
| `neutre`            | `comfort`        | `reduced`       | Fin phase confort différé |
| `neutre`            | `reduced`        | Abstention      | Sobriété restaurée |
| `reduced`           | `comfort`        | `reduced`       | Retour sobriété |
| `reduced`           | `reduced`        | Abstention      | Nominal |

Règles :

- confort strictement temporaire,
- retour automatique à `reduced` obligatoire,
- une seule activation par cycle d’absence,
- cette table n’est jamais évaluée lorsque `mode_confort_chauffage` est actif.

---

# ----------------------------------------------------------
# 🔒 8. CAS D’ABSTENTION FORCÉE
# ----------------------------------------------------------

La décision est obligatoirement une abstention lorsque
l’override opérateur est inactif et que l’un des cas suivants
est vérifié :

- programme actuel = `unknown`,
- mode désiré = programme actuel,
- autorisation = `neutre`,
- anti-rebond actif,
- verrou géolocalisation actif.

Ces règles ne s’appliquent jamais lorsque
`mode_confort_chauffage` est actif.

Effet (hors override opérateur) :

- aucune action,
- aucune notification,
- aucun log décisionnel.

Effet (en override opérateur) :

- la décision est évaluée normalement,
- un log explicite est obligatoire,
- la raison `confort_force` est prioritaire.

---

# ----------------------------------------------------------
# 🛑 9. CAS INTERDITS FORMELLEMENT
# ----------------------------------------------------------

Les cas suivants sont STRICTEMENT interdits
en régime automatique, hors override opérateur :

| Cas | Interdiction | Justification |
|-----|--------------|---------------|
| Confort en Vacances | ❌ | Sobriété maximale |
| Confort avec fenêtre ouverte | ❌ | Chauffe absurde |
| Confort pendant aération | ❌ | Violation inertie |
| Confort pendant blocage poêle actif | ❌ | Double source & fenêtre sécurité |
| Confort sans autorisation | ❌ | Violation séparation faits / décision |
| Reprise automatique post-blocage | ❌ | Risque oscillation |
| Maintien confort prolongé en absence | ❌ | Dérive énergétique |
| Confort produit par pré-confort en régime absence | ❌ | Anticipation hors cadre thermique légitime |
| Confort produit par pré-confort pendant Vacances | ❌ | Violation sobriété Vacances |
| Pré-confort cumulée avec inhibition géofencing   | ❌ | Double confort absence interdit |
| Restauration pré-confort après blocage           | ❌ | Reprise automatique interdite |

Note :

Lorsque `mode_confort_chauffage` est actif,
les interdictions ci-dessus sont contournables,
car elles résultent d’un choix opérateur explicite.

Dans ce cas :

- la décision est autorisée,
- elle doit être explicitement tracée,
- la raison `confort_force` est obligatoire,
- les blocages contournés doivent être identifiables.

Toute apparition d’un cas interdit hors override opérateur constitue :

- une erreur critique,
- une rupture de contrat,
- une régression majeure.

---

# ----------------------------------------------------------
# 🔁 10. RÈGLES DE TRANSITION & STABILITÉ
# ----------------------------------------------------------

Règles globales :

- toute transition déclenche un anti-rebond,
- aucune transition silencieuse,
- aucune transition sans raison métier,
- aucune transition en chaîne rapide.

Stabilité :

- priorité à la stabilité sur la réactivité,
- inertie respectée systématiquement,
- cycles courts éliminés.

---

# ----------------------------------------------------------
# 🧱 11. INVARIANTS CANONIQUES
# ----------------------------------------------------------

Invariants absolus :

- une seule règle applicable à un instant donné,
- une seule décision possible,
- aucun cas implicite autorisé,
- aucune ambiguïté tolérée,
- aucune exception non documentée hors table,
- tout override opérateur est explicitement formalisé.

Toute violation constitue :

- une incohérence formelle,
- une perte de déterminisme,
- une erreur d’architecture majeure.

---

# ----------------------------------------------------------
# 🧠 12. DÉPENDANCES CONTRACTUELLES
# ----------------------------------------------------------

Ce contrat est :

- subordonné à :
  - `00_gouvernance_chauffage.md`

- implémenté par :
  - `30_decision_centrale.md`

- complémentaire de :
  - `40_blocages.md`
  - `60_absence_inhibition_geofencing.md`
  - `70_autorisation_thermostat.md`

Il gouverne directement :

- toute transition de programme chauffage,
- toute validation de décision centrale,
- toute évolution future du moteur.

---

# ----------------------------------------------------------
# 📌 13. PORTÉE & STABILITÉ
# ----------------------------------------------------------

Ce contrat est :

- la référence ultime du moteur Chauffage,
- stable long terme,
- intégrant explicitement l’override opérateur comme invariant,
- modifié uniquement lors d’évolutions majeures,
- versionné explicitement,
- opposable à toute implémentation.

Il constitue la **spécification décisionnelle canonique finale  
du Chauffage Arsenal V3 PRO**.

# ==========================================================