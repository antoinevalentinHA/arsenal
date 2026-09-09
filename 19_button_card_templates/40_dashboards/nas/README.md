# `40_dashboards/nas/` — Architecture UI

## Nature du dossier

`nas/` est un **dashboard de supervision locale d'infrastructure domestique**, centré sur l'état du NAS et de son environnement immédiat.

Ce n'est pas une UI transactionnelle comme `boiler/`, ni un cockpit transverse comme `arsenal/`. C'est une **UI de supervision diagnostique légère**, orientée lisibilité et détection d'anomalies.

Le domaine expose des informations système simples, des états textuels interprétés, des états binaires de sécurité et des températures techniques.

---

## Structure implicite identifiée

Le dossier est organisé en **4 familles UI distinctes** :

### A. Informations système simples

Exemple : `carte_info_systeme`

- Uptime, timestamp, dernier démarrage — sans qualification sémantique ni seuil
- **Type UI : info** (lecture informative pure)

---

### B. Diagnostics textuels interprétés

Exemples : `carte_nas_drive_etat`, `carte_nas_smart_etat`, `carte_capteur_etat_textuel`

- Détection de mots-clés dans un état textuel libre
- Production d'une sémantique couleur avec hiérarchie d'anomalie
- **Type UI : diagnostic** (interprétation textuelle, qualification d'état)

> `carte_capteur_etat_textuel` est la carte générique canonique de cette famille. `carte_nas_drive_etat` et `carte_nas_smart_etat` sont des spécialisations DSM historiques en coexistence transitoire — leur rationalisation vers la carte générique est la cible.

---

### C. Diagnostics binaires de sécurité

Exemple : `carte_etat_securite`

- Mapping direct : `off = OK`, `on = alerte`
- **Type UI : pure** (convention binaire constitutive)

> La sémantique `off = OK` est constitutive du template. Ne pas réutiliser sur un binaire où `on` est un état souhaitable ou neutre.

---

### D. Diagnostics thermiques techniques

Exemple : `carte_nas_temperature_disque`

- Température disque qualifiée par seuils : nominal / élevé / critique
- **Type UI : diagnostic** (qualification par seuils, lecture de santé matérielle)

---

### E. Action de commandabilité NAS (C51 Lot 7)

Exemple : `carte_action_nas_admission_demander`

- Déclenche, après confirmation, l'un des scripts backend du socle
  transactionnel `contrats/nas_transactionnel.md` (`AUDIT` ou
  `RELEASE_DIFF`) — chantier `audits/04_chantiers/transverses/c51_commandabilite_nas.md`
- Ne publie jamais de message MQTT elle-même : appelle uniquement
  `script.turn_on` sur le script backend désigné par l'instance
- **Type UI : action** — première introduction de ce type dans ce
  domaine (les couches A à D ci-dessus étaient jusqu'ici toutes
  diagnostiques)

---

### F. Diagnostic transactionnel NAS Admission (C51 Lot 7)

Exemple : `carte_nas_admission_etat_transaction`

- Affiche le dernier verdict **transactionnel** (admission/terminaison
  NAS) d'une opération du socle `nas_transactionnel.md` — jamais un
  résultat métier
- Satellite générique commun à `AUDIT` et `RELEASE_DIFF` (deux
  instances du même template) ; le résultat métier correspondant
  (`arsenal_self`/`arsenal_nas`) reste affiché par une carte séparée,
  hors de ce domaine (`40_dashboards/system/20_supervision/`) —
  séparation stricte transaction/résultat métier opposable par
  `nas_transactionnel.md` §12
- **Type UI : diagnostic**, sur un plan distinct des diagnostics
  matériels A à D : ce n'est pas une lecture de santé NAS, mais l'état
  d'une commande envoyée au NAS

---

## Taxonomie des types UI

| Type UI        | Signification                                                                                    | Exemples                                                                  |
|----------------|--------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| info           | lecture informative pure, sans qualification                                                    | `carte_info_systeme`                                                      |
| diagnostic     | qualifie un état ou une mesure par rapport à une référence ou des seuils                        | `carte_nas_drive_etat`, `carte_nas_smart_etat`, `carte_capteur_etat_textuel`, `carte_nas_temperature_disque`, `carte_nas_admission_etat_transaction` |
| pure           | aucune transformation, convention binaire constitutive                                          | `carte_etat_securite`                                                     |
| interprétative | transformation locale tolérée *(non utilisé dans ce domaine)*                                   | —                                                                         |
| action         | proxy UI d'une commande backend                                                                  | `carte_action_nas_admission_demander` *(C51 Lot 7)*                       |

---

## Architecture en couches (lecture système)

```
Niveau 1 — Information               → 10_info/
Niveau 2 — Statut binaire            → 20_statut_binaire/
Niveau 3 — Diagnostic textuel        → 30_diagnostic_textuel/
Niveau 4 — Diagnostic thermique      → 40_diagnostic_thermique/
```

> Cette architecture en couches est normative. Toute carte doit appartenir à une seule couche. Aucune carte hybride n'est autorisée.
>
> Les templates C51 Lot 7 (`carte_action_nas_admission_demander`,
> `carte_nas_admission_etat_transaction`) vivent dans des couches
> propres à part (`10_action/`, `20_diagnostic_transaction/`), non
> numérotées dans la séquence 10→40 ci-dessus : elles ne qualifient
> pas le NAS lui-même (matériel), mais une commande envoyée au NAS —
> un axe orthogonal aux quatre niveaux d'origine, volontairement non
> intercalé pour ne pas renuméroter l'existant.

---

## Structure cible recommandée

```
40_dashboards/nas/

  10_info/
    carte_info_systeme.yaml

  20_statut_binaire/
    carte_etat_securite.yaml

  30_diagnostic_textuel/
    carte_nas_drive_etat.yaml        ← spécialisation DSM historique
    carte_nas_smart_etat.yaml        ← spécialisation DSM historique
    carte_capteur_etat_textuel.yaml  ← cible canonique

  40_diagnostic_thermique/
    carte_nas_temperature_disque.yaml

  10_action/                                    ← C51 Lot 7
    carte_action_nas_admission_demander.yaml

  20_diagnostic_transaction/                    ← C51 Lot 7
    carte_nas_admission_etat_transaction.yaml
```

---

## Question d'architecture ouverte

`carte_capteur_etat_textuel` change la lecture du dossier : le domaine `nas/` ne vise plus une spécialisation DSM figée, mais une **grammaire de supervision générique** applicable au NAS.

La question à trancher explicitement : **officialiser `carte_capteur_etat_textuel` comme remplaçant canonique** de `carte_nas_drive_etat` et `carte_nas_smart_etat`, et planifier leur dépréciation.

Deux options, mutuellement exclusives :

**Option A — Coexistence assumée**
Les spécialisations DSM restent pour des raisons de nommage ou de compatibilité existante. Dette documentée, non bloquante.

**Option B — Rationalisation vers le générique**
`carte_capteur_etat_textuel` devient la seule carte de diagnostic textuel. Les deux spécialisations sont dépréciées et supprimées à terme.

> Ne pas laisser cette question ouverte indéfiniment : choisir une option et la documenter dans les entêtes des cartes concernées.

---

## Points de fragilité documentés

### 1. Détection textuelle par inclusion

Les cartes de diagnostic textuel dépendent du contenu exact des libellés (variantes fr/en, chaînes DSM). Robuste en pratique, mais jamais garanti face aux mises à jour upstream.

### 2. Spécialisations DSM potentiellement redondantes

`carte_nas_drive_etat` et `carte_nas_smart_etat` semblent absorbables par `carte_capteur_etat_textuel`. Dette de rationalisation clairement identifiée — voir question d'architecture ouverte.

### 3. Seuils thermiques fixes

Les seuils 45/55 °C sont pertinents pour HDD, moins universels pour SSD/NVMe. À relativiser selon le matériel en place.

### 4. `carte_etat_securite` — convention `off = OK`

Convention constitutive. Ne pas réutiliser sur un binaire où `on` est souhaitable.

---

## Plan d'action

**Étape 1 — Déplacer les fichiers** (sans toucher au code)
Créer les dossiers, déplacer les fichiers selon la structure cible.

**Étape 2 — Mettre à jour les entêtes**
Ajouter le champ `TYPE UI` normalisé :

```yaml
# 🧱 TYPE UI : diagnostic
```

**Étape 3 — Trancher sur la rationalisation textuelle**
Choisir Option A ou Option B et documenter la décision dans les entêtes des trois cartes concernées.

**Étape 4 — Documenter les fragilités**
Ajouter dans les entêtes : convention `off = OK` (`carte_etat_securite`), seuils thermiques relatifs au matériel (`carte_nas_temperature_disque`).
