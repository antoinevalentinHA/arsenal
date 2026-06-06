# 🔒 binary_sensor.fenetre_ouverte_maison_avec_delai

- Domaine : Aération / Qualification / Blocages thermiques
- Autorité : **FRONTIÈRE NIVEAU 1 FINALE**

---

🎯 Rôle :
Fournir le **signal canonique qualifié d'ouverture thermique de la maison**,
distinguant les ouvertures brèves tolérables (en grâce)
des épisodes d'aération effectifs.

Ce capteur constitue la **frontière temporelle qualifiée NIVEAU 1 finale** entre :

- enveloppe thermique fermée ou en grâce transitoire,
- et aération thermique réelle qualifiée.

Il fournit la **source normative du signal de blocage consommé par la décision centrale chauffage et ses triggers**.

---

🧭 Périmètre d'influence autorisé :
- Blocage chauffage NIVEAU 1 par ouverture qualifiée (décision centrale)
- Trigger décisionnel chauffage (off→on / on→off)
- Condition de garde dans les pipelines aération
- Armement / progression du pipeline aération (M1 / M5)
- Qualification "aération effective" pour diagnostics et UI
- Support UI aération (tentative vs qualifiée)

---

⛔ Interdictions absolues :
- Ne décide jamais d'un mode confort / réduit de manière autonome
- Ne modifie jamais une consigne
- Ne modifie jamais un offset
- Ne conditionne jamais une autorisation thermostat
- Ne pilote jamais directement la chaudière
- Ne produit jamais de diagnostic calibrant
- Ne sert jamais de seuil thermique
- Ne déclenche jamais un auto-ajustement
- Ne remplace jamais `binary_sensor.fenetre_ouverte_maison` comme signal brut physique
- Ne sert jamais de preuve de fermeture physique réelle du bâtiment — ce rôle appartient exclusivement au capteur brut

---

🔒 Garanties exigées :
- Agrégation **hiérarchisée de sous-capteurs qualifiés**
- Distinction stricte immédiat / temporisé selon zones
- Valeur binaire pure : aération qualifiée présente / absente
- Monotonie intra-épisode : absence d'oscillation tant que la fermeture physique réelle n'est pas confirmée durablement
- Aucune temporisation interne propre — toute temporisation est portée par les sous-capteurs
- Aucune logique thermique
- Dépendance exclusive à des capteurs déjà temporisés ou physiques immédiats
- Immunité aux micro-ouvertures
- Reload-safe / runtime-safe
- Stabilité stricte intra-état
- Absence totale d'effet matériel direct

---

🔗 Dépendances :

Ouvertures immédiates :
- `binary_sensor.contact_entree_fenetre`

Sous-systèmes temporisés :
- `binary_sensor.fenetre_sejour_ouverte_avec_delai`
- `binary_sensor.fenetre_ouverte_etage_avec_delai`

Consommateurs contractuels :
- `decision_centrale.yaml` — blocage `desired_mode = reduced` + raison [`fenetre_ouverte_maison.md`](fenetre_ouverte_maison.md)
- `decision_centrale_trigger.yaml` — trigger NIVEAU 1 (off→on / on→off)
- `m0_remediation_incoherence.yaml` — condition de garde (double vérification avec brut)
- `12_template_sensors/chauffage/diagnostic/raison.yaml` — diagnostic de raison chauffage
- `12_template_sensors/aeration/coherence.yaml` — capteur de cohérence aération
- [`07_coherence_ko_detecteur.md`](../../../aeration_blocage_chauffage/socle_transversal/07_coherence_ko_detecteur.md) — conditions de détection d'incohérence pipeline aération
- [`13_interfaces_ouvertures.md`](../../../aeration_blocage_chauffage/socle_transversal/13_interfaces_ouvertures.md) — interface transversale aération / blocage chauffage
- [`07_capteurs_diagnostics_structurants.md`](../07_capteurs_diagnostics_structurants.md) — référencé comme blocage structurant
- [`40_blocages.md`](../../40_blocages.md) — via [`30_decision_centrale.md`](../../30_decision_centrale.md) (section 4.1 blocage fenêtres)
- UI diagnostics ouvertures / aération (tentative / qualifiée)

---

⚠️ Risques :
- Faux négatifs si délais de grâce trop longs
- Blocage tardif si ouverture réellement prolongée
- Pollution thermique si sous-capteurs mal calibrés
- Dérive dangereuse si utilisé comme signal brut d'ouverture
  (rôle réservé à `binary_sensor.fenetre_ouverte_maison`)
- Rupture de souveraineté si court-circuité dans les automations

---

❗ Statut particulier :
**FRONTIÈRE NIVEAU 1 FINALE — BLOCAGE THERMIQUE PAR OUVERTURE QUALIFIÉE**
Autorité directe sur la décision centrale chauffage.
Seule frontière temporelle officielle entre ouverture brute et aération thermique réelle.
Pilier du pipeline aération et des blocages post-aération Arsenal.

---

⚠️ Classification :
INCLUS DANS [`index.md`](../index.md)
Section : Blocages / Aération qualifiée
Classe : **FRONTIÈRE NIVEAU 1 FINALE**
