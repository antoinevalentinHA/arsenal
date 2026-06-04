# 🔒 binary_sensor.fenetres_maison_fermees_stable

- Domaine : Ouvertures / Enveloppe / Clôture stable
- Autorité : **CANON OUVERTURES — Signal canonique de clôture stable consommé par la couche blocages chauffage**

---

🎯 Rôle :
Fournir le **signal canonique stable de clôture de l'enveloppe**,
garantissant que toutes les fenêtres sont fermées sans oscillation ni faux OFF furtifs.

Ce capteur est un **canon de stabilisation** au sens du contrat Ouvertures :
il stabilise localement le signal N2 (`contact_fenetres_maison`) avec un délai minimal
pour supprimer les transitions parasites avant consommation par l'orchestration.

Il constitue le **signal canonique de clôture stable** utilisé pour :

- déclencher la fin d'épisode aération (M2)
- déclencher les invalidations / reprises sûres du chauffage
- signaler la clôture stable de l'enveloppe thermique

---

🧭 Périmètre d'influence autorisé :
- Déclenchement de clôture du pipeline aération (M2)
- Déclenchement des reprises / recalculs sûrs chauffage
- Protection contre les états transitoires (anti-faux "tout fermé")

---

⛔ Interdictions absolues :
- Ne qualifie jamais une aération
- Ne produit jamais de blocage direct
- Ne remplace jamais `binary_sensor.fenetre_ouverte_maison` (observation brute)
- Ne remplace jamais `binary_sensor.fenetre_ouverte_maison_avec_delai` (qualification temporelle)
- Ne participe à aucune décision de mode thermique
- Ne sert jamais de preuve d'ouverture — rôle exclusivement de clôture

---

🔒 Garanties exigées :
- Signal stable, déterministe, restart-safe
- Signal canonique de clôture stable utilisé par M2
- Dépendance exclusive à `binary_sensor.contact_fenetres_maison` (N2 Ouvertures)
- Aucune dépendance directe aux capteurs physiques N0 (`capteur_*`) ou N1 (`contact_*` individuels)
- Délai localisé (`delay_on`) porté par ce capteur — aucune stabilisation dispersée dans les pipelines
- Absence d'effet de bord

---

🔗 Dépendances :

Source unique :
- `binary_sensor.contact_fenetres_maison` (N2 Ouvertures — agrégat OR de tous les contacts fenêtres)

Paramètre de stabilisation :
- `delay_on: 00:00:02` — suppression des OFF furtifs uniquement

Consommateurs contractuels :
- Pipelines aération normatifs (M2 — clôture d'épisode)
- Triggers décisionnels chauffage (clôture globale / reprise sûre)

---

⚠️ Risques :
- Faux positifs de "fermé" si `contact_fenetres_maison` a un périmètre incomplet
- Blocage de clôture si un contact physique reste figé ouvert
- Confusion de rôle si utilisé comme signal d'ouverture (interdit)

---

❗ Statut particulier :
**CANON OUVERTURES — stabilisation de clôture**
Signal stable de fermeture globale de l'enveloppe.
Consommé par la couche blocages chauffage et les pipelines aération.
Ne produit aucun blocage direct — déclenche uniquement des transitions de sortie de contexte.

---

⚠️ Classification :
Section : Canons Ouvertures / Clôture stable
Classe : **CANON — stabilisation N2 → signal de clôture orchestration**
