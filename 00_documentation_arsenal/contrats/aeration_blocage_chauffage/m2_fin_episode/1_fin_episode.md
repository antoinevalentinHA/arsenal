# 🧠 ARSENAL — CONTRAT NORMATIF (M2) · FIN D'ÉPISODE — CADRE GÉNÉRAL

## 🎯 OBJET

Définir le comportement normatif de l’étape M2 :

- clôture de l’épisode d’aération,
- activation du blocage chauffage,
- calcul des échéances M3 (analyse ΔT) et M4 (fin blocage),
- programmation monotone des timers,
- journalisation.

M2 ne prend aucune décision métier.
Il ne déclenche aucun redémarrage thermique.

---

## 🚦 CONDITIONS STRUCTURELLES

M2 ne peut être exécuté que si :

- `aeration_episode_en_cours = on`
- `chauffage_blocage_aeration = off`
- `aeration_pipeline_arme = on`
- `binary_sensor.fenetres_maison_fermees_stable = on`
- `systeme_stable = on`
- `aeration_debut` valide

Toute exécution hors de ce cadre constitue
une violation contractuelle.

### 🔁 RÉCONCILIATION SUR ÉTAT (anti front consommé)

La clôture ne dépend plus d’un front unique. Le pipeline maître
ré-évalue la porte M2 sur plusieurs triggers, dont le nominal :

- nominal : `trigger.id == 'fermeture_stable'` (littéral conservé) ;
- réconciliation : `reconciliation_feature_active`,
  `reconciliation_systeme_stable`, `reconciliation_pipeline_arme`,
  `reconciliation_fermees_stable_unknown`,
  `reconciliation_fermees_stable_unavailable`.

Chaque trigger de réconciliation correspond à une garde
transitoirement fausse au moment du front nominal
(interrupteur maître, système instable, pipeline non armé,
capteur template en `unknown`/`unavailable` post-boot) qui
redevient compatible.

**Le trigger n’est jamais une preuve de fermeture.** La preuve
fonctionnelle vient exclusivement de l’état courant
`binary_sensor.fenetres_maison_fermees_stable == 'on'`
(garde de branche + assertion interne du script M2).

---

## 🧩 AUTORITÉ

- Script exécuté : `script.aeration_m2_fin_episode`
- Appelé exclusivement par le pipeline maître.
- M2 n’est jamais appelé directement par M0, M3, M4, M5 ou M6.

---

## 🔁 SÉQUENCE STRUCTURELLE (ORDRE STRICT)

1. `aeration_episode_en_cours` → OFF  
2. `chauffage_blocage_aeration` → ON  
3. Calcul des échéances cibles (monotone)  
4. Mise à jour des `input_datetime` de diagnostic  
5. Démarrage / extension monotone des timers  
6. `aeration_confirmee` → OFF  
7. Journalisation éventuelle 

---

## 🔒 PORTÉE

M2 est le seul point légitime :

- d’activation initiale du blocage chauffage,
- de programmation initiale des échéances M3 et M4.

M5 peut geler ces échéances.
M6 peut les relancer.
M4 est le seul point autorisé de levée du blocage.

---

## 🛑 INTERDITS

M2 ne doit jamais :

- lever le blocage,
- appeler M3 ou M4 directement,
- déclencher une action thermique,
- raccourcir une échéance existante,
- modifier les snapshots T_REF,
- réactiver un blocage déjà actif.

# ==========================================================