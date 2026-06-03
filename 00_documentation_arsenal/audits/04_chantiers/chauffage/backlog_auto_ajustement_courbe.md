# 📋 ARSENAL — BACKLOG
## Chauffage — Auto-ajustement de la courbe de chauffe

| Champ | Valeur |
|---|---|
| **Type** | Backlog |
| **Domaine** | Chauffage / Auto-ajustement courbe |
| **Statut** | Vivant |
| **Origine** | Audit `01_rapports/chauffage/audit_auto_ajustement_courbe.md` (clôturé 2026-06-03) |
| **Objet** | Tracer les sujets différés, les sujets rejetés et les errata documentaires |

> Ce backlog capitalise autant les **décisions de ne pas faire** que les sujets différés. Un sujet rejeté ici ne doit pas être rouvert sans élément nouveau.

---

## 1. Sujets différés

### D-1 — Possession des protections empruntées (fenêtre / aération / poêle actif)

- **Résumé.** Aujourd'hui, l'auto-ajustement est protégé contre l'apprentissage en fenêtre ouverte, aération ou blocage poêle actif **uniquement par effet de bord** : ces contextes font passer la décision centrale en mode réduit, la consigne appliquée quitte le confort, et les capteurs d'écart cessent d'échantillonner. La protection fonctionne, mais le domaine ne la **possède** pas : elle est révocable par une évolution distante (décision centrale ou garde d'écart) **sans aucun signal**.
- **Décision.** **Différé** (« oui mais plus tard »). Classé Important mais non urgent.
- **Justification.** Aucune défaillance actuelle ; il s'agit d'une fragilité latente de robustesse future, pas d'un défaut de comportement. À traiter après le chantier d'observabilité, qui rendra d'ailleurs cette dépendance visible et donc surveillable.

---

## 2. Sujets rejetés

### R-1 — Brancher `pourcentage_consigne_eco_24h` tel quel

- **Résumé.** Câbler le proxy de représentativité existant (part du temps en mode Eco sur 24 h) comme verrou d'apprentissage.
- **Décision.** **Rejeté.**
- **Justification.** Le proxy mesure un rapport cyclique de la **demande de confort**, pas le **travail de la chaudière sous charge propre**. Il est redondant avec la garde confort et la bande morte là où il fonctionne, **aveugle** là où le biais résiduel subsiste (journées douces/ensoleillées/inertielles en confort), et **destructeur de données rares et précieuses** (faux négatifs sur les soirées froides après absence diurne). Le brancher constituerait un filtre médiocre, susceptible d'introduire autant de problèmes qu'il en résout. Le besoin physique de représentativité reste réel mais appellerait un **signal fondé sur le travail/charge réels**, non traité ici.

### R-2 — Imposer une suspension totale de la calibration liée au poêle

- **Résumé.** Aligner le runtime sur les contrats en suspendant **toute** calibration (hausse comme baisse) dès qu'une influence poêle est présente ou récente.
- **Décision.** **Rejeté.**
- **Justification.** Métier-faux. Le poêle peut créer une **fausse surchauffe** : il doit interdire surtout la **baisse** de courbe. Une **sous-chauffe malgré poêle récent** reste significative (chaudière réellement insuffisante) et la **hausse** doit rester permise. L'asymétrie actuelle du runtime (baisse bloquée, hausse permise) est correcte ; la suspension totale serait une **régression**.

### R-3 — Élargir artificiellement l'apprentissage de la pente

- **Résumé.** Étendre la fenêtre d'apprentissage de la pente (p. ex. relâcher la garde froid `t_ext ≤ 5 °C`) pour augmenter le nombre d'occasions.
- **Décision.** **Rejeté.**
- **Justification.** Contre-productif en climat doux (type bordelais). La rareté des occasions de pente est une **protection**, pas un défaut : peu d'occasions = peu de risque et peu de bénéfice. La prudence de la pente est cohérente avec sa nature (correction structurelle de régime froid).

---

## 3. Errata documentaires

> Corrections **opportunistes** : à effectuer au fil de l'eau, jamais comme chantier dédié (faible rentabilité établie). Le runtime fait autorité sur le comportement ; ces écarts créent un risque de **confusion future du mainteneur**, pas un risque de comportement.

### E-1 — Capteur d'immunité poêle : divergence 75 ↔ 06

- **Résumé.** `75_auto_ajustement_courbe.md` désigne `binary_sensor.signature_thermique_poele` comme verrou d'immunité ; `06_capteurs_auto_ajustement_calibration.md` désigne `binary_sensor.poele_en_fonction_stable` comme « frontière d'immunité officielle ». Le runtime suit le second.
- **Décision.** Errata — aligner les deux contrats sur le capteur réellement utilisé.
- **Justification.** Deux contrats nomment deux capteurs différents pour la même fonction ; ambiguïté d'autorité.

### E-2 — « Suspension totale » poêle : formulation métier-fausse dans les contrats

- **Résumé.** `75` (§9) et `06` exigent de « suspendre / interdire toute calibration » sous influence poêle.
- **Décision.** Errata — reformuler pour décrire l'**asymétrie correcte** (baisse interdite, hausse permise) implémentée par le runtime.
- **Justification.** Les contrats sont métier-faux sur ce point ; le runtime est plus juste (cf. R-2). Tant que l'erratum n'est pas fait, ces énoncés ne doivent pas être pris comme autorité.

### E-3 — Renvoi pendant `85_` vs fichier `75_`

- **Résumé.** `06_capteurs_auto_ajustement_calibration.md` référence un consommateur `85_auto_ajustement_courbe.md` ; le fichier réel est `75_auto_ajustement_courbe.md`. Aucun `85_` n'existe.
- **Décision.** Errata — corriger le renvoi.
- **Justification.** Référence morte.

### E-4 — Source de calibration de la pente : divergence 75 ↔ runtime/06

- **Résumé.** `75` (§5.2) indique la pente fondée sur `ecart_consigne_moyenne_froid` / `ecart_consigne_instantane_froid` ; le runtime (et `06`) consomment `ecart_consigne_stats_froid`.
- **Décision.** Errata — aligner `75` sur la source réellement consommée.
- **Justification.** `06` et le runtime concordent ; seul `75` diverge. Confusion potentielle sur la grandeur de référence.

---
*Backlog issu de l'audit clôturé du 2026-06-03. Sujets rejetés à ne pas rouvrir sans élément nouveau.*
