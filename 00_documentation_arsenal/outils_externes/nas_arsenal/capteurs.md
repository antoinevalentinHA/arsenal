# Contrat — Template Binary Sensors UPS

Domaine : Infrastructure
Version : v1.0
Statut : Actif
Dernière révision : 2026-04-24

---

1. Objet

Définir les quatre template binary sensors qui exposent, sous forme de booléens
normalisés, les critères décisionnels du contrat UPS / Arrêt NAS (v1.1).

Ces sensors représentent des états observables à l'instant "t".
Ils ne portent aucune logique temporelle — la discipline de durée
(coupure durable ≥ 60 s) appartient à l'automation via "for:".

---

2. Sources d'entrée

Entité| Rôle
"sensor.ups_code_d_etat"| Flags NUT — détection mode batterie
"sensor.ups_autonomie_de_la_batterie"| Autonomie résiduelle en secondes
"sensor.ups_autonomie_de_la_batterie_faible"| Seuil d'alerte bas natif UPS en secondes

---

3. Templates définis

3.1 "binary_sensor.critere_ups_sur_batterie"

Sémantique : L'UPS est actuellement en mode batterie.

Condition :

'OB' in sensor.ups_code_d_etat

États :

Valeur| Signification
"on"| "OB" présent dans le code d'état
"off"| "OB" absent — secteur présent ou état indéterminé

Remarque : Conforme à l'invariant I-1 du contrat UPS / Arrêt NAS —
implication stricte, sans symétrie.

---

3.2 "binary_sensor.critere_ups_autonomie_nas_critique"

Sémantique : L'autonomie résiduelle est insuffisante pour garantir
un arrêt NAS ordonné.

Condition :

sensor.ups_autonomie_de_la_batterie < 1800

États :

Valeur| Signification
"on"| Autonomie < 1 800 s (< 30 min) — seuil critique atteint
"off"| Autonomie ≥ 1 800 s — marge suffisante

Remarque : Ce sensor est "off" lorsque "sensor.ups_autonomie_de_la_batterie"
est indisponible ("unavailable" / "unknown"). L'implémentation doit traiter
explicitement ces états pour éviter un déclenchement par défaut.

---

3.3 "binary_sensor.critere_ups_batterie_faible"

Sémantique : L'UPS a atteint son seuil d'alerte interne de batterie faible.

Condition :

sensor.ups_autonomie_de_la_batterie <= sensor.ups_autonomie_de_la_batterie_faible

États :

Valeur| Signification
"on"| Autonomie résiduelle ≤ seuil natif UPS
"off"| Autonomie résiduelle > seuil natif UPS

Remarque : SBF est prioritaire sur ANC dans la règle de décision :
sa vérification déclenche "ups_arret_nas_recommande" indépendamment du seuil ANC.
Ce sensor doit être "off" si l'un ou l'autre des deux capteurs source est
indisponible.

---

3.4 "binary_sensor.ups_arret_nas_recommande"

Sémantique : Synthèse décisionnelle — les critères d'autonomie justifient
un arrêt NAS, sous réserve que la coupure soit durable (évalué par l'automation).

Condition :

critere_ups_autonomie_nas_critique OR critere_ups_batterie_faible

États :

Valeur| Signification
"on"| Au moins un critère d'autonomie est atteint
"off"| Aucun critère d'autonomie atteint

Remarque :
Ce sensor recommande l'arrêt NAS uniquement au regard des critères d'autonomie.
Il ne suffit jamais à déclencher l'action sans validation du critère CD par l'automation.

La règle complète du contrat UPS / Arrêt NAS est :

ARRÊT NAS ← CD  AND  ups_arret_nas_recommande

CD est exclusivement évalué par l'automation via "for:".

---

4. Invariants d'implémentation

#| Invariant
T-1| Tout état "unavailable" ou "unknown" sur une source doit produire "off" sur le sensor dépendant — jamais "on" par défaut
T-2| Aucun de ces sensors ne porte de logique temporelle ("for:", délai, debounce)
T-3| "ups_arret_nas_recommande" ne référence que les deux sensors 3.2 et 3.3 — jamais directement les capteurs UPS bruts
T-4| Ces sensors sont en lecture seule — aucune automation ne les modifie directement

---

5. Exclusions

Ces templates n'encodent pas :

- le critère CD (coupure durable ≥ 60 s) — appartient à l'automation,
- la décision finale d'arrêt NAS — appartient à l'automation,
- l'invariant I-5 (anti double déclenchement) — appartient à l'automation.

---

6. Références

Document| Lien
Contrat UPS / Arrêt NAS| "contrat_ups_arret_nas_v1.1.md"