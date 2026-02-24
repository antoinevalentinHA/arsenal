# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (SOCLE TRANSVERSAL)
#     ÉTATS CANONS & INVARIANTS STRUCTURELS
# ==========================================================

## 🎯 OBJET

Définir les états canons autorisés du domaine
Aération → Blocage Chauffage.

Un état canon :

- est cohérent
- est stable
- respecte tous les invariants
- ne nécessite aucune remédiation

Tout état non conforme est considéré incohérent.

---

# 🧱 1️⃣ ÉTAT CANON — REPOS TOTAL

Condition :

- aeration_episode_en_cours = off
- chauffage_blocage_aeration = off
- aeration_pipeline_arme = off
- timer.aeration_blocage = idle
- timer.aeration_analyse_delta_t = idle
- chauffage_fin_blocage_aeration neutralisé
- analyse_deltat_disponible neutralisé

Signification :

- aucun épisode actif
- aucun blocage
- aucune échéance programmée
- système propre

---

# 🧱 2️⃣ ÉTAT CANON — ÉPISODE ACTIF (M1)

Condition :

- aeration_episode_en_cours = on
- aeration_pipeline_arme = on
- chauffage_blocage_aeration = off
- timers = idle
- aeration_debut valide

Signification :

- épisode en cours
- pas encore clôturé
- pas de blocage actif

Interdiction :

- aucun timer ne doit être actif
- aucun blocage ne doit être ON

---

# 🧱 3️⃣ ÉTAT CANON — BLOCAGE ACTIF (POST M2)

Condition :

- aeration_episode_en_cours = off
- aeration_pipeline_arme = on
- chauffage_blocage_aeration = on
- timer.aeration_blocage = active
- chauffage_fin_blocage_aeration valide
- timer.aeration_analyse_delta_t = active OU idle (selon timing)

Signification :

- épisode clôturé
- blocage en cours
- sortie exclusivement temporelle (M4)

Invariant :

- au moins un mécanisme temporel doit exister
  (timer actif ou datetime valide)

---

# 🧱 4️⃣ ÉTAT CANON — APRÈS PROLONGATION (M3 FORT)

Condition :

- chauffage_blocage_aeration = on
- aeration_pipeline_arme = on
- timer.aeration_blocage = active
- chauffage_fin_blocage_aeration valide
- nouvelle échéance ≥ ancienne

Signification :

- blocage étendu
- monotonicité respectée

Interdiction :

- réduction d’échéance
- redémarrage chauffage

---

# 🧱 5️⃣ ÉTAT CANON — MAINTIEN (M3 FAIBLE)

Condition :

- chauffage_blocage_aeration = on
- analyse_deltat_disponible neutralisé
- timer.aeration_blocage inchangé

Signification :

- analyse consommée
- aucun changement d’échéance

---

# 🧱 6️⃣ ÉTAT CANON — FIN TOTALE (POST M4)

Condition :

- chauffage_blocage_aeration = off
- aeration_pipeline_arme = off
- timers annulés
- chauffage_fin_blocage_aeration neutralisé
- analyse_deltat_disponible neutralisé

Signification :

- cycle totalement terminé
- aucun résidu temporel

---

# 🧱 7️⃣ ÉTAT CANON — INVALIDATION TENTATIVE

Condition :

- aeration_episode_en_cours = off
- chauffage_blocage_aeration = off
- aeration_pipeline_arme = off
- aucun timer actif

Signification :

- tentative annulée avant confirmation
- aucun effet métier

---

# 🚫 8️⃣ ÉTATS IMPOSSIBLES (INCOHÉRENTS)

Les combinaisons suivantes sont interdites :

1) Blocage ON + pipeline OFF  
2) Blocage ON + datetime neutralisé  
3) Pipeline ON + épisode OFF + blocage OFF + aucune ouverture  
4) Timer actif + blocage OFF  
5) Analyse disponible valide + blocage OFF  
6) Blocage OFF + timer blocage actif  

Ces états doivent être captés par :

- détecteur cohérence KO
- mini-guard
- sécurité démarrage
- M0 recover

---

# 🛑 INVARIANTS ABSOLUS

- Levée du blocage uniquement en M4.
- Monotonicité stricte des échéances.
- Aucun redémarrage thermique direct.
- Aucune dépendance circulaire avec la décision centrale.
- Aucune persistance d’état résiduel après M4.

---

# 🔒 CONSÉQUENCE CONTRACTUELLE

Tout ajout futur :

- doit préserver ces états canons,
- ne peut introduire un nouvel état implicite,
- ne peut contourner M4 pour lever un blocage.

# ==========================================================