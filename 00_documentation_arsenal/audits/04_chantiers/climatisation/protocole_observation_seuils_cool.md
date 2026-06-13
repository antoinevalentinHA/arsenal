# PROTOCOLE D'OBSERVATION — ABAISSEMENT SEUILS COOL (−0,5 °C)
## Évaluer le confort thermique des chambres en soirée, sans changer l'architecture

> **Statut :** protocole d'observation **expérimental** — observation en cours.
> **Nature :** méthode de mesure et critères de comparaison. **Non normatif** —
> n'est ni un contrat, ni une décision, ni un chantier. **Aucun réglage proposé.**
> **Domaine :** `climatisation`
> **Changement observé :** abaissement runtime des seuils COOL de 0,5 °C (acte
> opérateur déjà réalisé), hystérésis 1 °C conservée. Aucune architecture ni
> logique modifiée.
> **Rattachement :** prolonge l'investigation historique 30 j —
> [`investigation_historique_clim_30j.md`](../../01_rapports/climatisation/investigation_historique_clim_30j.md)
> (référence « avant » du §2). Voir aussi le hub
> [`navigation/domaines/climatisation.md`](../../../navigation/domaines/climatisation.md).

---

> **Changement évalué.** Seuils COOL ON 25,0→**24,5** / OFF 24,0→**23,5** (hystérésis
> 1 °C conservée). Aucune autre modification. Aucun contrat, aucune logique touchés.
>
> **Hypothèse testée.** Un point de départ plus froid au coucher (réserve thermique)
> améliore le confort nocturne portes fermées, **sans** prolonger le fonctionnement
> tardif.
>
> **Caveat de mesure.** Le changement est un **décalage de niveau**, pas de timing.
> Le confort se mesure en **température absolue de la chambre** (°C), jamais en
> écart au seuil (le seuil a bougé). Tout doit être **conditionné à l'extérieur**
> pour neutraliser la météo : la fenêtre de référence couvrait une canicule
> (ext jusqu'à 33,8 °C le soir), une comparaison brute serait fausse.

---

## 1. MÉTRIQUES À SUIVRE (figées avant de regarder les résultats)

### Confort (primaires)
| Métrique | Définition | Fenêtre |
|---|---|---|
| **Temp chambre au coucher** | `temp_max_chambres` moyenne pondérée | proxy coucher (à fixer, ex. 22:00–22:30) |
| **Temp chambre en soirée** | `temp_max_chambres` | 19:00–23:00 |
| **Pic nocturne** | max quotidien de `temp_max_chambres` | 23:00–03:00 |
| **Dispersion inter-pièces** | `temp_max_chambres − temp_min_chambres` | soirée + nuit |

→ Toutes **conditionnées par tranche d'extérieur** (`temperature_jardin`) :
`[15–22[, [22–25[, [25–28[, [28+]` °C.

### Coût (secondaires — à ne pas dégrader au-delà d'un plafond que tu fixes)
| Métrique | Définition |
|---|---|
| **Fonctionnement COOL soirée** | heures `clim_mode_reel='cool'` en 19:00–23:00 |
| **Jours avec COOL en soirée** | nb de jours concernés / total |
| **Fragmentation** | nb de cycles COOL substantiels (≥1 min), médiane de durée |
| **Fonctionnement tardif** | heures COOL en 21:00–23:00 (fenêtre sensible bruit) |

---

## 2. RÉFÉRENCE 30 JOURS (déjà calculée — « avant »)

| Indicateur | Valeur de référence |
|---|---|
| Temp chambre soirée 19–23h (médiane) | **23,5 °C** |
| Temp chambre proxy coucher 22h | **23,5 °C** |
| Temp chambre nuit 23–3h (médiane) | **23,6 °C** |
| Pic nocturne médian/jour | **24,3 °C** |
| **Plafond chambre en soirée chaude (ext ≥22 °C)** | **24,6 °C** *(= ancien seuil −0,4)* |
| COOL total / dont soirée | 51 h / **17 h** |
| Jours avec COOL en soirée | **6 / 31** |

**Confort soirée conditionné ext (référence, °C chambre chaude) :**
`ext 15–22 → 23,2` · `22–25 → 24,6` · `25–28 → 24,6` · `28+ → 24,6`.

> Lecture : dès qu'il fait ≥22 °C dehors le soir, la chambre se cale à **24,6 °C**
> — c'est l'ancien seuil qui borne, pas la météo. **Prédiction testable** : le
> nouveau réglage doit abaisser ce plafond à ~**24,1 °C** dans les mêmes tranches.

---

## 3. DURÉE D'OBSERVATION

Gouvernée par la **couverture météo**, pas par le calendrier. La référence
contenait **11 soirées chaudes** (ext soirée >25 °C). Pour comparer à
conditions semblables :

- **Minimum** : 3 semaines **ET** ≥ 8 soirées avec ext >25 °C.
- **Idéal** : inclure un épisode chaud (ext soir ≥30 °C) comparable à la
  référence, sinon les tranches hautes resteront vides.
- Si l'été reste doux, **ne pas conclure** sur les tranches chaudes : prolonger
  ou marquer « non concluant faute de soirées chaudes ».

---

## 4. MÉTHODE DE COMPARAISON (objective, anti-confondant)

1. Régénérer le CSV sur la période « après » avec **le même outil**
   (`enquete_clim_historique.py`) — le nouveau seuil 24,5 est auto-capturé dans
   `seuil_on_cool_applique`, la donnée s'auto-documente.
2. Comparer **par tranche d'extérieur** (jamais en brut) : pour chaque tranche,
   confronter la temp chambre « avant » vs « après ». Une amélioration réelle se
   voit **à météo égale**.
3. Pondérer par durée (échantillonnage événementiel), comme l'audit.
4. Contrôler la **présence** (la logique diffère présence/absence) : restreindre
   l'analyse confort aux périodes de présence en soirée.

---

## 5. CRITÈRES DE CONCLUSION (pré-enregistrés)

**Le changement AMÉLIORE le confort soirée si, à extérieur égal (présence) :**
- temp chambre au coucher (22h) **abaissée ≥ 0,3 °C** dans les tranches ext ≥22 °C, **ET**
- pic nocturne 23–3h **abaissé ≥ 0,3 °C**, **ET**
- coût maîtrisé : hausse du fonctionnement COOL soirée **sous le plafond que tu fixes**
  (ex. ≤ +50 % d'heures, ou ≤ +X jours/semaine en fenêtre bruit 21–23h), **ET**
- fragmentation non dégradée (cycles substantiels médiane ne chutant pas sous ~20 min).

**Le changement est NEUTRE / À REVOIR si :**
- à ext égal, la temp au coucher **ne baisse pas** → le seuil n'était pas la
  contrainte (le binding réel est la fermeture des portes / le blocage), et un
  décalage de **timing** serait plus pertinent qu'un décalage de niveau.

**Le changement est À ANNULER si :**
- gain de confort < 0,3 °C **mais** coût (fonctionnement tardif, bruit, conso)
  au-dessus de ton plafond → mauvais rapport.

---

## 6. CE QUE CE TEST NE TRANCHERA PAS

- Il ne mesure pas l'effet « portes ouvertes vs fermées » (pas de capteur de
  porte) : le proxy est temporel (soirée/nuit), pas l'état réel des portes.
- Il ne valide pas un **pré-refroidissement ciblé** (boost de consigne avant le
  coucher) : si le test confirme le bénéfice du point de départ plus froid **au
  prix d'un surfonctionnement diffus**, cela *motiverait* d'étudier plus tard un
  pré-refroidissement horaire (changement d'architecture, hors périmètre actuel)
  qui obtiendrait le même gain à moindre coût. À noter, pas à décider ici.

---

*Protocole d'observation only. Aucune modification d'architecture, de contrat ou
de logique. Le runtime reste la référence ; les seuils appliqués sont lus tels
qu'ils sont.*
