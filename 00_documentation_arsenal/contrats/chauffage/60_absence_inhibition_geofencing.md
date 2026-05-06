# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF DE DOMAINE
#     CHAUFFAGE — ABSENCE & INHIBITION GÉOFENCING (V3 PRO)
# ==========================================================
#
# 📌 STATUT :
#   CONTRAT NORMATIF DE DOMAINE — STRATÉGIE THERMIQUE D’ABSENCE
#
# 🔒 AUTORITÉ :
#   Ce document définit le comportement normatif du mécanisme
#   d’**inhibition du géofencing** du sous-système Chauffage Arsenal.
#
#   Il formalise la stratégie officielle de confort différé en absence,
#   destinée à préserver la qualité de la reprise thermique tout en
#   maintenant un haut niveau de sobriété énergétique.
#
#   Il est OPPOSABLE à toute implémentation :
#     • helpers,
#     • capteurs seuils,
#     • scripts de contrôle,
#     • lectures par la Décision Centrale.
#
#   Subordonné à :
#     /00_documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#
#   Utilisé directement par :
#     /00_documentation_arsenal/contrats/chauffage/30_decision_centrale.md
#
# ==========================================================


# ----------------------------------------------------------
# 🎯 1. OBJET DU CONTRAT
# ----------------------------------------------------------

Ce contrat définit le comportement normatif du mécanisme
d’**inhibition du géofencing en régime d’absence**.

Il formalise :

- l’objectif thermique réel de ce mécanisme,
- les conditions d’activation légitimes,
- les règles d’autorisation en absence,
- les garde-fous de sobriété,
- les limites strictes de ce dispositif.

Ce mécanisme constitue une **stratégie de confort différé**,
et non un mécanisme de sûreté bâtiment.

---

# ----------------------------------------------------------
# 🧠 2. FINALITÉ RÉELLE DU MÉCANISME
# ----------------------------------------------------------

L’inhibition du géofencing ne vise PAS :

- la protection du bâti,
- la prévention du gel,
- la sécurité matérielle,
- la continuité de confort en absence.

Elle vise exclusivement :

- empêcher qu’une zone froide ne descende trop bas,
- préserver une inertie thermique exploitable,
- garantir une reprise en confort **douce et suffisamment rapide**,
- limiter les appels de puissance violents,
- éviter le pompage thermique au retour en présence.

Objectif fondamental :

> 🧠 **Optimiser la dynamique de reprise thermique**,  
> tout en maximisant la sobriété pendant l’absence.

---

# ----------------------------------------------------------
# 🧱 3. POSITIONNEMENT ARCHITECTURAL
# ----------------------------------------------------------

Ce mécanisme :

- s’applique uniquement en régime **absence**,
- ne modifie PAS le régime de référence,
- ne modifie PAS la hiérarchie métier,
- ne court-circuite PAS la Décision Centrale,
- ne pilote JAMAIS directement le matériel.

Il agit exclusivement sur :

> 🧠 **L’autorisation simulée de confort en absence**

via la couche définie dans :

- `70_autorisation_thermostat.md`

---

### Séparation avec les mécanismes d’anticipation

L’inhibition du géofencing est STRICTEMENT distincte :

- des mécanismes d’anticipation de retour,
- du pré-confort retour vacances,
- de toute stratégie temporelle prédictive.

Règles cardinales :

- l’inhibition du géofencing ne connaît JAMAIS les dates de retour,
- elle ne déclenche JAMAIS une anticipation,
- elle ne prépare JAMAIS un retour utilisateur,
- elle ne s’active QUE par risque thermique immédiat.

Le pré-confort retour vacances :

- n’appartient PAS à la stratégie d’absence,
- n’interagit PAS avec l’inhibition du géofencing,
- ne peut jamais activer ni prolonger une inhibition.

Ces deux mécanismes sont ARCHITECTURALEMENT ORTHOGONAUX
et ne doivent produire aucun effet combiné.

---

# ----------------------------------------------------------
# 🌡️ 4. PRINCIPE DE FONCTIONNEMENT
# ----------------------------------------------------------

En régime absence :

- le régime thermique reste `absence`,
- la décision de référence reste `reduced`,
- aucune recherche permanente de confort n’est autorisée.

Lorsque certaines conditions thermiques sont réunies :

- une **autorisation simulée de présence** est produite,
- l’autorisation cible devient temporairement `comfort`,
- la Décision Centrale peut décider un passage contrôlé en confort.

Ce mécanisme permet :

- une chauffe minimale préventive,
- strictement limitée dans le temps,
- strictement limitée en amplitude.

---

# ----------------------------------------------------------
# 🧠 5. CONDITIONS D’ACTIVATION
# ----------------------------------------------------------

L’inhibition du géofencing peut être autorisée uniquement si :

- le régime courant est **absence**,
- aucune interdiction hiérarchique n’est active,
- aucune aération n’est en cours ou bloquée,
- aucune fenêtre n’est ouverte,
- aucun poêle n’est actif,
- le mode maison n’est PAS `Vacances`.

Et surtout :

- la température de la **zone la plus froide** est inférieure
  à un seuil de confort différé configuré.

Règle cardinale :

> ⚠️ L’inhibition est déclenchée uniquement par un RISQUE  
> de dégradation de la dynamique de reprise, jamais par confort.

---

# ----------------------------------------------------------
# 🔁 6. EFFETS NORMATIFS
# ----------------------------------------------------------

Lorsque l’inhibition est active :

- l’autorisation thermique simulée devient `comfort`,
- la Décision Centrale peut décider un passage en confort,
- le régime reste officiellement **absence**,
- toute hiérarchie supérieure continue de s’appliquer.

Effets interdits :

- aucune continuité de confort prolongée,
- aucune élévation durable de consigne,
- aucune annulation du régime d’absence.

---

# ----------------------------------------------------------
# 🛑 7. GARDE-FOUS DE SOBRIÉTÉ
# ----------------------------------------------------------

Garde-fous absolus :

- durée strictement bornée,
- hystérésis thermique obligatoire,
- anti-rebond obligatoire,
- impossibilité de cycles rapprochés.

Règles :

- une seule activation par cycle d’absence,
- aucune oscillation autorisée,
- retour automatique à `reduced` après stabilisation,
- interdiction de maintien prolongé en confort.

Objectifs :

- préserver l’inertie,
- éviter les cycles courts,
- maximiser la sobriété réelle.

---

### Interdiction de cumul avec les mécanismes d’anticipation

Lorsqu’une inhibition du géofencing est active ou vient de se terminer :

- aucun mécanisme d’anticipation ne peut être activé,
- aucun pré-confort ne peut être déclenché,
- aucune autorisation automatique ne peut être cumulée.

Règles cardinales :

- une inhibition termine toujours par un retour strict à `reduced`,
- aucun pré-confort ne peut être restauré après une inhibition,
- toute anticipation ultérieure doit repasser
  par une fenêtre temporelle légitime indépendante.

Le pré-confort retour vacances ne peut :

- ni prolonger une inhibition,
- ni la renforcer,
- ni être déclenché par sa sortie.

Toute interaction constitue :

- une rupture de sobriété,
- un risque de confort implicite,
- une dérive critique de stratégie thermique.

---

# ----------------------------------------------------------
# 🧩 8. INDÉPENDANCE & NEUTRALITÉ
# ----------------------------------------------------------

Ce mécanisme :

- ne connaît PAS la présence réelle,
- ne déclenche PAS de retour de présence,
- ne modifie PAS les états de géolocalisation,
- ne produit AUCUNE décision autonome.

Il agit uniquement comme :

> 🧠 **UN CORRECTEUR DE DYNAMIQUE THERMIQUE EN ABSENCE**

---

# ----------------------------------------------------------
# 🔒 9. INTERDICTIONS FORMELLES
# ----------------------------------------------------------

L’inhibition du géofencing ne doit JAMAIS :

- forcer un régime présence,
- maintenir un confort permanent en absence,
- court-circuiter un blocage hiérarchique,
- ignorer une interdiction système,
- déclencher une décision directe,
- écrire une consigne,
- appeler directement la couche matérielle.

Toute dérive constitue :

- une rupture de sobriété,
- un risque de pompage,
- une régression architecturale majeure.

---

# ----------------------------------------------------------
# 🧱 10. INVARIANTS DU MÉCANISME
# ----------------------------------------------------------

Invariants absolus :

- mécanisme actif uniquement en absence,
- activation uniquement par seuil thermique froid,
- durée bornée impérativement,
- amplitude thermique limitée,
- aucun impact sur la hiérarchie,
- aucune mémoire inter-cycle.

Toute violation constitue :

- une perte de maîtrise thermique,
- une dérive de confort implicite,
- une rupture de gouvernance.

---

# ----------------------------------------------------------
# 🧠 11. DÉPENDANCES CONTRACTUELLES
# ----------------------------------------------------------

Ce contrat est :

- subordonné à :
  - `00_gouvernance_chauffage.md`

- utilisé par :
  - `30_decision_centrale.md`

- complémentaire de :
  - `70_autorisation_thermostat.md`
  - `80_table_decision_canonique.md`

Il gouverne directement :

- `input_boolean.chauffage_inhibition_geofencing`,
- les capteurs seuils de zone froide,
- toute logique de confort différé en absence.

---

# ----------------------------------------------------------
# 📌 12. PORTÉE & STABILITÉ
# ----------------------------------------------------------

Ce contrat est :

- stratégique dans l’architecture Chauffage,
- stable long terme,
- modifié uniquement lors d’évolutions majeures,
- versionné explicitement,
- opposable à toute implémentation.

Il constitue la **stratégie officielle anti-pompage et confort différé  
du Chauffage Arsenal V3 PRO**.

# ==========================================================