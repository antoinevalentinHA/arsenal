# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF D’APPLICATION
#     CHAUFFAGE — STANDBY & HYSTÉRÉSIS D’EXÉCUTION (V3 PRO)
# ==========================================================
#
# 📌 STATUT :
#   CONTRAT NORMATIF D’APPLICATION — STABILISATION MÉCANIQUE
#
# 🔒 AUTORITÉ :
#   Ce document définit le comportement normatif du mécanisme
#   de **standby et d’hystérésis d’exécution** du sous-système Chauffage Arsenal.
#
#   Il formalise :
#     • le rôle du verrou logique `chauffage_standby_force`,
#     • la séparation stricte entre autorisation et application,
#     • les règles de stabilisation mécanique,
#     • les interdictions d’interprétation métier.
#
#   Il est OPPOSABLE à toute implémentation :
#     • automatismes d’application,
#     • scripts de transition,
#     • helpers de verrouillage,
#     • couches matérielles.
#
#   Subordonné à :
#     /homeassistant/00_documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#
#   Utilisé directement par :
#     /homeassistant/00_documentation_arsenal/contrats/chauffage/70_autorisation_thermostat.md
#     /homeassistant/00_documentation_arsenal/contrats/chauffage/30_decision_centrale.md
#
# ==========================================================


# ----------------------------------------------------------
# 🎯 1. OBJET DU CONTRAT
# ----------------------------------------------------------

Ce contrat définit le comportement normatif du mécanisme de  
**standby et d’hystérésis d’exécution** du Chauffage Arsenal.

Il formalise :

- le rôle exact du verrou logique de standby,
- sa fonction de stabilisation mécanique,
- la traduction stricte de l’autorisation thermique,
- l’absence totale de logique métier,
- la prévention des oscillations d’exécution.

Ce mécanisme constitue la **couche d’hystérésis d’application officielle**  
entre décision logique et exécution matérielle.

---

# ----------------------------------------------------------
# 🧠 2. NATURE ARCHITECTURALE DU STANDBY
# ----------------------------------------------------------

Le standby Arsenal n’est PAS :

- un état thermique,
- un régime métier,
- une cause hiérarchique,
- un blocage de sûreté,
- une décision autonome.

Il est exclusivement :

> 🧱 **UN VERROU LOGIQUE D’APPLICATION**

dont le rôle est :

- stabiliser les transitions,
- éviter les oscillations rapides,
- protéger la couche matérielle,
- traduire mécaniquement une intention autorisée.

Principe cardinal :

> ⚠️ Le standby ne décide RIEN.  
> Il applique mécaniquement une intention déjà décidée ailleurs.

---

# ----------------------------------------------------------
# 🧱 3. POSITIONNEMENT DANS LA CHAÎNE D’EXÉCUTION
# ----------------------------------------------------------

Chaîne officielle :

1. Capteurs thermiques → produisent des faits  
2. Autorisation thermique → produit une intention  
3. Décision centrale → choisit un régime  
4. **Standby / Hystérésis** → stabilise l’application  
5. Couche matérielle → exécute physiquement  

Le standby est donc :

- post-décision  
- pré-matériel  
- totalement subordonné  

Il ne connaît :

- ni la hiérarchie,  
- ni les blocages,  
- ni la présence,  
- ni l’absence,  
- ni les seuils,  
- ni le matériel.

---

# ----------------------------------------------------------
# 🌡️ 4. INTERFACE AVEC L’AUTORISATION THERMIQUE
# ----------------------------------------------------------

Le standby est piloté exclusivement par :

- `sensor.chauffage_autorisation_cible`

Correspondance normative :

| Autorisation cible | Effet standby |
|-------------------|---------------|
| `neutre`          | Aucune action |
| `reduced`         | Activation du verrou |
| `comfort`         | Levée du verrou |

---

---

### Autorisations contextuelles & neutralité du standby

Le mécanisme de standby est strictement aveugle
à l’origine de l’autorisation thermique.

Il ne distingue jamais :

- autorisation par présence,
- autorisation par géofencing,
- autorisation forcée utilisateur,
- autorisation contextuelle automatique.

Règles cardinales :

- le standby n’interprète jamais une autorisation,
- le standby n’en mémorise jamais l’origine,
- le standby ne conserve aucune trace d’un contexte automatique,
- le standby ne restaure jamais une autorisation hors décision centrale.

Le pré-confort retour vacances :

- n’est jamais connu du mécanisme de standby,
- n’est jamais mémorisé comme état,
- ne peut jamais être restauré automatiquement après levée de verrou.

---

Règles cardinales :

- `neutre` ne produit AUCUNE écriture,
- `reduced` pose un verrou logique,
- `comfort` lève strictement ce verrou.

Le standby ne connaît PAS :

- les causes de l’autorisation,
- la hiérarchie décisionnelle,
- la stratégie absence,
- les blocages hiérarchiques.

Il applique **sans interprétation**.

---

# ----------------------------------------------------------
# 🔁 5. HYSTÉRÉSIS & STABILISATION MÉCANIQUE
# ----------------------------------------------------------

Le mécanisme de standby constitue :

> 🧠 **LA SEULE HYSTÉRÉSIS D’EXÉCUTION DU SYSTÈME**

Fonctions :

- éviter les bascules rapides comfort / reduced,
- empêcher les cycles courts d’application,
- protéger l’exécution matérielle et la chaudière,
- stabiliser l’état matériel. 

Caractéristiques :

- aucune temporisation métier,
- aucune mémoire thermique,
- aucune logique de seuil,
- aucune anticipation.

Il repose uniquement sur :

- idempotence des écritures,
- verrou logique persistant,
- discipline de la décision centrale.

---

# ----------------------------------------------------------
# 🛑 6. INTERDICTIONS FORMELLES
# ----------------------------------------------------------

Le mécanisme de standby ne doit JAMAIS :

- produire une décision thermique,
- interpréter un état métier,
- déclencher une chauffe,
- modifier une consigne,
- déclencher une transition matérielle directe,
- appeler directement la couche matérielle,
- ignorer une décision centrale.

Il est STRICTEMENT INTERDIT :

- d’y intégrer des seuils,
- d’y intégrer des timers métier,
- d’y intégrer des règles présence / absence,
- d’y intégrer une hiérarchie.

Toute dérive constitue :

- une violation de séparation des responsabilités,
- une régression architecturale majeure,
- un risque direct de pompage thermique.

---

# ----------------------------------------------------------
# 🧩 7. GARANTIES D’APPLICATION
# ----------------------------------------------------------

Garanties cardinales :

- application idempotente uniquement,
- aucune écriture inutile,
- aucune oscillation produite localement,
- aucune initiative autonome,
- comportement strictement déterministe.

---

### Interdiction de restauration automatique d’autorisations

Le mécanisme de standby ne doit JAMAIS :

- restaurer une autorisation précédente après levée de verrou,
- rejouer un état `comfort` mémorisé,
- relancer une transition matérielle sans décision récente valide.

Règles cardinales :

- toute sortie de standby impose une revalidation complète
  par la Décision Centrale,
- aucune autorisation automatique antérieure ne peut être réappliquée,
- toute reprise thermique doit provenir exclusivement
  d’une décision fraîche et explicite.

Le pré-confort retour vacances est intégralement soumis à ces règles.

Toute restauration implicite constitue :

- une violation de souveraineté décisionnelle,
- une reprise automatique illégitime,
- une dérive critique de l’architecture.

---

Le standby garantit :

- stabilité des transitions,
- cohérence exécution / décision,
- robustesse post-reload,
- tolérance aux redémarrages HA.

---

# ----------------------------------------------------------
# 🔒 8. INVARIANTS DE STANDBY
# ----------------------------------------------------------

Invariants absolus :

- le standby n’est jamais une décision,
- le standby n’est jamais une cause métier,
- le standby n’est jamais hiérarchique,
- le standby n’agit que sur un verrou logique,
- le standby ne connaît que trois états d’entrée.

Toute violation constitue :

- une confusion des couches,
- une perte de déterminisme,
- une dette architecturale critique.

---

# ----------------------------------------------------------
# 🧠 9. DÉPENDANCES CONTRACTUELLES
# ----------------------------------------------------------

Ce contrat est :

- subordonné à :
  - `00_gouvernance_chauffage.md`

- utilisé par :
  - `70_autorisation_thermostat.md`
  - `30_decision_centrale.md`

- complémentaire de :
  - `10_souverainete_execution.md`
  - `80_table_decision_canonique.md`

Il gouverne directement :

- `input_boolean.chauffage_standby_force`,
- l’automation `10240000000002`,
- toute couche d’hystérésis d’application.

---

# ----------------------------------------------------------
# 📌 10. PORTÉE & STABILITÉ
# ----------------------------------------------------------

Ce contrat est :

- fondamental pour la stabilité du moteur,
- stable long terme,
- modifié uniquement lors d’évolutions majeures,
- versionné explicitement,
- opposable à toute implémentation.

Il constitue la **couche officielle de stabilisation mécanique  
et d’hystérésis d’exécution du Chauffage Arsenal V3 PRO**.

# ==========================================================