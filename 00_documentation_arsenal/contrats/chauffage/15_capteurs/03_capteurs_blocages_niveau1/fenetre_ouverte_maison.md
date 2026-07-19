# 🔍 binary_sensor.fenetre_ouverte_maison

- Domaine : Ouvertures / Aération / Sécurité thermique bâtiment
- Autorité : **CAPTEUR STRUCTURANT INDIRECT**

---

🎯 Rôle :
Fournir le **signal brut global d'ouverture de fenêtres de la maison**,
indiquant qu'au moins un ouvrant est physiquement ouvert,
sans temporisation ni qualification métier.

Ce capteur constitue la **mesure physique instantanée** de l'état de l'enveloppe thermique.
Il n'est pas une autorité de blocage directe.
Il alimente des **conditions de garde** dans les pipelines aération
qui vérifient la fermeture physique réelle du bâtiment.

La **frontière NIVEAU 1 finale** de qualification thermique est assurée par :
`binary_sensor.fenetre_ouverte_maison_avec_delai`

---

🧭 Périmètre d'influence autorisé :
- Condition de garde dans les pipelines aération (vérification fermeture physique réelle)
- Affichage UI diagnostics ouvertures
- **Ne constitue jamais une autorité de blocage directe**
- **Ne conditionne jamais la décision centrale chauffage**

---

⛔ Interdictions absolues :
- Ne déclenche jamais directement un blocage thermique
- Ne conditionne jamais une décision de mode confort / réduit
- Ne modifie jamais une consigne
- Ne modifie jamais un offset
- Ne conditionne jamais une autorisation thermostat
- Ne pilote jamais directement la chaudière
- Ne produit jamais de diagnostic calibrant
- Ne sert jamais de seuil thermique
- Ne déclenche jamais un auto-ajustement
- Ne participe jamais à la table de décision

---

🔒 Garanties exigées :
- Agrégation **exhaustive de tous les ouvrants thermiquement pertinents**
- Valeur binaire pure : au moins une ouverture / toutes fermées
- Aucune temporisation interne (brut, sans délai de grâce)
- Aucune logique thermique
- Aucune qualification métier
- Détection instantanée d'ouverture réelle
- Reload-safe / runtime-safe
- Stabilité stricte intra-état
- Absence totale d'effet matériel direct

---

🔗 Dépendances :

Sources physiques d'ouverture :
- `binary_sensor.capteur_chambre_enfants`
- `binary_sensor.capteur_chambre_matthieu`
- `binary_sensor.capteur_chambre_parents_droite`
- `binary_sensor.capteur_chambre_parents_gauche`
- `binary_sensor.capteur_chambre_parents_milieu`
- `binary_sensor.capteur_fenetre_entree`
- `binary_sensor.capteur_fenetre_sejour_1`
- `binary_sensor.capteur_fenetre_sejour_2`
- `binary_sensor.capteur_fenetre_sejour_3`
- `binary_sensor.capteur_fenetre_sejour_4`

Consommateurs contractuels :
- `m0_remediation_incoherence.yaml` — condition de garde (vérification fermeture physique)
- `guard.yaml` (blocage_chauffage) — trigger de réévaluation + condition de garde
- `securite_blocage.yaml` — condition de garde
- Lovelace / dashboards diagnostics ouvertures — affichage UI uniquement

---

⚠️ Risques :
- Blocage critique si un capteur reste figé ouvert (impact indirect via pipelines aération)
- Sous-protection si un ouvrant thermique est oublié dans l'agrégation
- Dérive dangereuse s'il est utilisé directement comme condition de blocage N1
- Rupture de souveraineté si court-circuité dans les automations hors consommateurs listés

---

❗ Statut particulier :
**CAPTEUR STRUCTURANT INDIRECT**
Signal brut de détection physique d'ouverture.
Alimente les conditions de garde des pipelines aération.
N'est jamais consommé directement par la décision centrale chauffage.
La frontière N1 finale est `binary_sensor.fenetre_ouverte_maison_avec_delai`.

---

⚠️ Classification :
INCLUS DANS [`index.md`](../index.md)
Section : Blocages / Aération physique
Classe : Capteur STRUCTURANT INDIRECT
