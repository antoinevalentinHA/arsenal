# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF DE DOMAINE
#     CHAUFFAGE — AUTO-AJUSTEMENT DE LA COURBE DE CHAUFFE (V3 PRO)
# ==========================================================
#
# 📌 STATUT :
#   CONTRAT NORMATIF DE DOMAINE — CALIBRATION THERMIQUE SUPERVISÉE
#
# 🔒 AUTORITÉ :
#   Ce document définit le comportement normatif du mécanisme
#   d’**auto-ajustement de la courbe de chauffe** du sous-système Chauffage Arsenal.
#
#   Il formalise la gouvernance officielle de la calibration thermique :
#     • pente de courbe,
#     • parallèle de courbe,
#     • conditions d’apprentissage,
#     • frontières décision / exécution / diagnostic.
#
#   Il est OPPOSABLE à toute implémentation :
#     • capteurs de suggestion,
#     • automations décisionnelles,
#     • scripts d’application,
#     • UI de réglage,
#     • mécanismes d’apprentissage.
#
#   Subordonné à :
#     /documentation_arsenal/contrats/chauffage/00_gouvernance_chauffage.md
#
#   Utilisé directement par :
#     /documentation_arsenal/contrats/chauffage/30_decision_centrale.md
#
# ==========================================================


# ----------------------------------------------------------
# 🎯 1. OBJET DU CONTRAT
# ----------------------------------------------------------

Ce contrat définit le comportement normatif du mécanisme
d’**auto-ajustement de la courbe de chauffe**.

Il formalise :

- la finalité réelle de la calibration thermique,
- les conditions légitimes d’apprentissage,
- la séparation stricte proposition / décision / exécution,
- les garde-fous d’immunité thermique,
- les interdictions absolues.

Ce mécanisme constitue une **calibration supervisée lente**,  
et non un pilotage adaptatif autonome.

---

# ----------------------------------------------------------
# 🧠 2. FINALITÉ RÉELLE DE L’AUTO-AJUSTEMENT
# ----------------------------------------------------------

L’auto-ajustement ne vise PAS :

- une régulation adaptative en boucle fermée,
- une optimisation temps réel,
- une compensation automatique d’erreur instantanée,
- une décision thermique autonome,
- un pilotage direct de la chaudière.

Il vise exclusivement :

- corriger lentement la loi de chauffe globale,
- stabiliser la qualité de confort long terme,
- réduire les dérives structurelles de réglage,
- assister le réglage utilisateur de manière objective.

Objectif fondamental :

> 🧠 **Améliorer durablement la loi de chauffe  
> sans jamais créer de boucle thermique autonome.**

---

# ----------------------------------------------------------
# 🧱 3. POSITIONNEMENT ARCHITECTURAL
# ----------------------------------------------------------

L’auto-ajustement :

- est hors décision centrale,
- ne modifie jamais un mode thermique,
- ne produit jamais une autorisation,
- ne pilote jamais directement un service.

Il agit exclusivement sur :

- `input_number.chauffage_pente_consigne`
- `input_number.chauffage_parallele_consigne`

via une chaîne stricte :

1. **Diagnostics structurants**
2. **Capteurs de suggestion**
3. **Décision supervisée**
4. **Scripts d’application blindés**

Il est :

- post-décisionnel  
- non critique temps réel  
- strictement supervisé  

---

# ----------------------------------------------------------
# 🧠 4. GRANDEURS CANONIQUES UTILISÉES
# ----------------------------------------------------------

Grandeurs de base autorisées :

- écart consigne instantané (régime doux / froid)
- moyenne glissante 24 h de l’écart
- moyennes spécialisées doux / froid
- température extérieure locale
- température intérieure minimale gouvernée

Grandeurs interdites :

- présence
- géolocalisation
- puissance chaudière
- durée de marche
- états cloud instables
- capteurs non gouvernés

Principe :

> ⚠️ Toute calibration doit être fondée exclusivement  
> sur des écarts thermiques mesurés gouvernés.

---

# ----------------------------------------------------------
# 🧠 5. SÉMANTIQUE DES PARAMÈTRES DE COURBE
# ----------------------------------------------------------

## 5.1 Parallèle de courbe (offset)

Rôle :

- corriger un biais thermique global
- agir principalement en régime doux
- déplacer verticalement la loi de chauffe

Grandeur de référence :

- `sensor.ecart_consigne_moyenne_24h`
- `sensor.ecart_consigne_moyenne_doux`

Effet autorisé :

- translation lente de la courbe
- correction fine de confort stationnaire

---

## 5.2 Pente de courbe

Rôle :

- corriger la réponse thermique en régime froid
- ajuster la sensibilité extérieure / intérieure
- stabiliser le comportement hivernal

Grandeur de référence :

- `sensor.ecart_consigne_moyenne_froid`
- `sensor.ecart_consigne_instantane_froid`

Effet autorisé :

- modification lente de la loi de chauffe globale
- correction structurelle en conditions sévères

---

# ----------------------------------------------------------
# 🧠 6. CHAÎNE NORMATIVE D’AUTO-AJUSTEMENT
# ----------------------------------------------------------

Chaîne obligatoire :

1. **Capteurs diagnostiques gouvernés**
2. **Capteurs de proposition (`*_suggeree`)**
3. **Automation décisionnelle supervisée**
4. **Écriture helpers consigne**
5. **Scripts d’application ViCare**
6. **Journalisation événementielle**

Interdictions absolues :

- aucun capteur n’écrit directement un paramètre
- aucune automation ne calcule une suggestion
- aucun script ne décide une valeur
- aucune boucle fermée n’est autorisée

Principe cardinal :

> 🔒 **La décision est unique, centralisée et supervisée.**

---

# ----------------------------------------------------------
# 🛑 7. CONDITIONS D’AUTORISATION LÉGITIMES
# ----------------------------------------------------------

L’auto-ajustement est autorisé uniquement si :

- auto-ajustement activé explicitement
- API ViCare disponible
- régime maison = Normal
- aucune influence poêle active ou récente
- grandeurs diagnostiques valides et stables
- au moins une suggestion différente de la consigne courante

Interdictions :

- jamais en Vacances
- jamais en absence
- jamais en reprise
- jamais en post-aération
- jamais en présence d’apports externes

---

# ----------------------------------------------------------
# 🔒 8. IMMUNITÉ THERMIQUE & PROTECTIONS
# ----------------------------------------------------------

Frontière d’immunité thermique :

- binary_sensor.signature_thermique_poele
- mémoire thermique récente (24 h)

Principe :

Toute signature thermique compatible avec un apport poêle
rend la période thermique impropre à l’apprentissage.

La présence d’une signature thermique active ou récente
suspend toute calibration de la courbe de chauffe.

---

# ----------------------------------------------------------
# 🔁 9. TEMPORALITÉ & RYTHME
# ----------------------------------------------------------

Règles temporelles :

- exécution planifiée lente (quotidienne typiquement)
- une décision maximum par cycle
- pas de rafale
- pas de recalcul rapide
- pas de dépendance événementielle temps réel

Objectifs :

- éviter oscillations lentes
- garantir stabilité longue
- préserver lisibilité utilisateur

---

# ----------------------------------------------------------
# 🧩 10. TRAÇABILITÉ OBLIGATOIRE
# ----------------------------------------------------------

Toute décision d’auto-ajustement doit produire :

- un événement `chauffage_adjustment`
- un logbook explicite
- une ligne mémoire lisible
- distinction simulation / réel

Champs normatifs minimaux :

- mode (simulation / real)
- pente_before / pente_after
- para_before / para_after
- timestamp

Principe :

> 🧠 **Toute calibration doit être auditée humainement.**

---

# ----------------------------------------------------------
# 🔒 11. INTERDICTIONS FORMELLES
# ----------------------------------------------------------

Il est strictement interdit :

- toute écriture automatique sans supervision
- toute boucle fermée thermique
- toute calibration temps réel
- toute dépendance cloud instable
- toute décision hors automation dédiée
- toute modification hors helpers consigne
- toute application directe depuis un capteur
- toute réécriture non tracée

Toute violation constitue :

- une rupture de gouvernance thermique,
- un risque d’instabilité systémique,
- une régression architecturale majeure.

---

# ----------------------------------------------------------
# 🧱 12. INVARIANTS DU MÉCANISME
# ----------------------------------------------------------

Invariants absolus :

- séparation stricte calcul / décision / application
- aucune boucle fermée
- supervision humaine implicite
- immunité aux apports externes
- traçabilité complète
- stabilité longue privilégiée
- aucune urgence thermique

---

# ----------------------------------------------------------
# 🧠 13. DÉPENDANCES CONTRACTUELLES
# ----------------------------------------------------------

Subordonné à :

- `00_gouvernance_chauffage.md`

Complémentaire de :

- `15_capteurs_thermiques.md`
- `70_autorisation_thermostat.md`
- `80_table_decision_canonique.md`
- `90_semantique_thermique.md`

Gouverne directement :

- toutes suggestions de pente / parallèle
- toutes décisions de calibration
- toutes écritures de courbe
- tous mécanismes d’apprentissage thermique

---

# ----------------------------------------------------------
# 📌 14. PORTÉE & STABILITÉ
# ----------------------------------------------------------

Ce contrat est :

- stratégique dans l’architecture Chauffage,
- frontière critique d’optimisation thermique,
- stable long terme,
- modifié uniquement lors d’évolutions majeures,
- versionné explicitement,
- opposable à toute implémentation.

Il constitue la **stratégie officielle de calibration thermique  
supervisée du Chauffage Arsenal V3 PRO**.

# ==========================================================
