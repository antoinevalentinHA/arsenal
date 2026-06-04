# 🧠 ARSENAL — CONTRAT NORMATIF (SOCLE TRANSVERSAL) · ÉTATS CANONS & INVARIANTS STRUCTURELS

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
- timer.aeration_analyse_delta_t =
  active si délai analyse non encore consommé
  idle si analyse déjà exécutée (M3 faible ou fort)

Signification :

- épisode clôturé
- blocage en cours
- sortie exclusivement temporelle (M4)

Invariant :

- au moins un mécanisme temporel doit exister :
  - timer actif
  OU
  - échéance datetime valide future

---

# 🧱 4️⃣ ÉTAT CANON — SUSPENSION PENDANT BLOCAGE (M5)

Condition :

- chauffage_blocage_aeration = on
- aeration_pipeline_arme = on
- binary_sensor.contact_fenetres_maison = on
- input_boolean.aeration_suspension_active = on
- input_datetime.aeration_reouverture_last valide
- timer.aeration_blocage = active OU idle (selon suspension)
- timer.aeration_analyse_delta_t = active OU idle (selon suspension)

Signification :

- blocage actif
- réouverture qualifiée détectée
- exécution temporelle suspendue ou réarmable
- aucune levée possible

Invariants :

- blocage reste ON
- pipeline reste ON
- enveloppe ouverte ⇒ suspension_active = on
- aucune levée autorisée
- aucune réduction d’échéance
- aucune analyse ΔT autorisée tant que l’enveloppe est ouverte

---

# 🧱 5️⃣ ÉTAT CANON — APRÈS PROLONGATION (M3 FORT)

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

# 🧱 6️⃣ ÉTAT CANON — MAINTIEN (M3 FAIBLE)

Condition :

- chauffage_blocage_aeration = on
- analyse_deltat_disponible neutralisé
- timer.aeration_blocage inchangé

Signification :

- analyse consommée
- aucun changement d’échéance

---

# 🧱 7️⃣ ÉTAT CANON — FIN TOTALE (POST M4)

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

# 🧱 8️⃣ ÉTAT CANON — INVALIDATION TENTATIVE

Condition :

- aeration_episode_en_cours = off
- chauffage_blocage_aeration = off
- aeration_pipeline_arme = off
- aucun timer actif

Signification :

- tentative annulée avant confirmation
- aucun effet métier

---

# 🚫 9️⃣ ÉTATS IMPOSSIBLES (INCOHÉRENTS)

Les combinaisons suivantes sont interdites :

1) Blocage ON + pipeline OFF  
2) Blocage ON + datetime neutralisé  
3) Pipeline ON + épisode OFF + blocage OFF
   ET aucune transition M2/M4 en cours
   ET aucune ouverture active
4) Timer actif + blocage OFF  
5) Analyse disponible valide + blocage OFF  
6) Blocage OFF + timer blocage actif  
7) Blocage ON + enveloppe ON + suspension_active OFF

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