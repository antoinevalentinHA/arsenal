# ==========================================================
# 🧠 ARSENAL — CONTRAT OUTIL EXTERNE
#     Supervision GitHub Actions
# ==========================================================

**Version** : v1.0.0  
**Date** : 24/05/2026  
**Statut** : proposition  
**Chemin** : `homeassistant/00_documentation_arsenal/outils_externes/github_actions_monitoring.md`

---

## 🎯 Objet

Ce contrat définit la supervision des workflows GitHub Actions par Arsenal.

L’objectif est d’exposer dans Home Assistant l’état des tests GitHub Actions associés au dépôt Arsenal, sans donner à GitHub d’accès entrant vers le réseau domestique.

---

## 🧱 Périmètre

Ce contrat couvre :

- la lecture passive de l’état des workflows GitHub Actions ;
- la publication locale des verdicts dans MQTT ;
- l’exposition des états dans Home Assistant ;
- la consommation UI ou diagnostic par Arsenal.

Il ne couvre pas :

- l’exécution des tests ;
- la modification des workflows GitHub Actions ;
- le déclenchement de déploiements ;
- l’écriture directe dans Home Assistant depuis GitHub ;
- toute décision runtime domestique fondée sur un résultat CI.

---

## 🧭 Principe architectural

Architecture retenue :

```text
Arsenal local
  → script local de supervision
  → API GitHub Actions
  → MQTT local
  → capteurs Home Assistant
  → UI / diagnostic Arsenal
```

GitHub Actions ne pousse rien vers Arsenal.

Arsenal lit passivement GitHub.


---

🔒 Invariants

Aucun accès entrant vers Home Assistant n’est ouvert pour GitHub.

Aucun secret Home Assistant n’est stocké dans GitHub.

GitHub Actions ne modifie aucun helper Home Assistant.

GitHub Actions ne publie pas directement sur le broker MQTT local.

Les résultats CI sont de la télémétrie externe.

Les résultats CI ne sont jamais une vérité métier runtime.

Les capteurs Home Assistant exposent un état observé, pas une décision.



---

🔐 Authentification GitHub

La supervision utilise un token GitHub en lecture seule.

Permissions attendues :

Actions: read
Metadata: read
Contents: read

Le token est stocké hors dépôt, dans un fichier local non versionné ou dans une variable d’environnement du service local.

Le token ne doit jamais être présent dans :

un fichier YAML Home Assistant ;

un fichier de documentation ;

un commit Git ;

un log ;

un topic MQTT.



---

📡 Publication MQTT

Topic principal :

arsenal/github/actions/<repo>/<workflow>/state

Exemple :

arsenal/github/actions/homeassistant/contracts_aeration_recommandation/state

Payload JSON attendu :

{
  "repo": "homeassistant",
  "workflow": "contracts_aeration_recommandation",
  "status": "completed",
  "conclusion": "success",
  "branch": "main",
  "commit": "abc1234",
  "run_id": 123456789,
  "run_url": "https://github.com/...",
  "created_at": "2026-05-24T20:00:00Z",
  "updated_at": "2026-05-24T20:01:12Z",
  "published_at": "2026-05-24T20:02:00Z"
}

Le topic est publié avec :

retain = true
qos = 1


---

🧩 États autorisés

status

Valeurs autorisées :

queued
in_progress
completed
unknown
error

conclusion

Valeurs autorisées :

success
failure
cancelled
skipped
timed_out
action_required
neutral
unknown

Si status != completed, conclusion peut valoir unknown.


---

🏠 Exposition Home Assistant

Les capteurs MQTT exposent uniquement l’état publié.

Exemple d’entités cibles :

sensor.github_actions_contracts_aeration_recommandation_status
sensor.github_actions_contracts_aeration_recommandation_conclusion
sensor.github_actions_contracts_aeration_recommandation_age_minutes
binary_sensor.github_actions_contracts_aeration_recommandation_ok
binary_sensor.github_actions_contracts_aeration_recommandation_stale

Rôles :

Entité	Rôle

sensor.*_status	état d’exécution GitHub
sensor.*_conclusion	verdict du dernier run
sensor.*_age_minutes	âge de la dernière publication locale
binary_sensor.*_ok	ON si dernier run terminé avec succès
binary_sensor.*_stale	ON si l’état publié est trop ancien



---

⏱️ Fraîcheur

Un état GitHub Actions est considéré périmé si :

published_at > seuil_stale

Seuil recommandé :

24 h

La fraîcheur mesure la publication locale dans Arsenal, pas uniquement l’exécution GitHub.


---

🧪 Interprétation du verdict

Le verdict nominal est :

status = completed
conclusion = success
stale = false

Cas non nominaux :

Cas	Interprétation

failure	échec de tests
cancelled	run interrompu
timed_out	run expiré
action_required	action humaine requise
unknown	état non interprétable
stale = true	supervision locale non fraîche



---

🚫 Interdictions

Il est interdit :

d’ouvrir un webhook Home Assistant public pour GitHub Actions ;

de stocker un token GitHub dans Home Assistant YAML ;

de déclencher une action domestique à partir d’un échec CI ;

de corriger automatiquement un état Home Assistant sur la base d’un verdict GitHub ;

de considérer un workflow GitHub comme une autorité runtime ;

de publier des secrets ou variables sensibles dans MQTT ;

de mélanger les verdicts GitHub Actions avec les capteurs métier Home Assistant.



---

🖥️ UI Arsenal

La UI peut afficher :

le dernier verdict ;

le workflow concerné ;

la branche ;

le commit court ;

l’âge de publication ;

l’URL du run GitHub.


La UI ne doit pas contenir de logique de décision.

Toute couleur ou synthèse doit être dérivée d’entités Home Assistant dédiées.


---

🔔 Alertes

Une alerte est autorisée uniquement pour :

échec de workflow ;

verdict inconnu ;

état périmé ;

erreur de supervision locale.


Une alerte ne déclenche aucune correction automatique.


---

🛠️ Script local de supervision

Le script local est responsable de :

interroger l’API GitHub ;

sélectionner le dernier run pertinent ;

normaliser le payload ;

publier le JSON MQTT ;

publier une erreur explicite en cas d’échec de lecture.


Le script ne doit pas :

modifier GitHub ;

modifier Home Assistant ;

écrire dans des helpers ;

déclencher de workflow ;

dépendre de Lovelace ou de l’UI.



---

📌 Clause finale

La supervision GitHub Actions est une télémétrie externe de qualité logicielle.

Elle informe Arsenal sur l’état des contrôles automatisés du dépôt.

Elle ne participe à aucune décision domestique, aucun automatisme matériel, aucun état métier runtime.

Toute implémentation contraire à ce contrat est invalide.