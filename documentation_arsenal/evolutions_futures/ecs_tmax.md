==========================================================
🧠 ARSENAL — NOTE D’ÉVOLUTION ARCHITECTURALE
ECS — Redéfinition du pic thermique et inertie post-cycle
----------------------------------------------------------

Chemin : homeassistant/documentation_arsenal/evolutions_futures/ecs_tmax.md
Statut : ÉVOLUTION FUTURE — TRACE CONCEPTUELLE
Domaine : Eau Chaude Sanitaire / Observabilité thermique
Priorité : STRUCTURANTE (non urgente)
==========================================================

🎯 OBJET

Cette note formalise une prise de conscience architecturale concernant la notion actuelle de pic thermique ECS (Tmax) dans ARSENAL.

Elle documente :

la définition actuelle du pic ECS,
ses limites physiques intrinsèques,
la divergence de modèle avec la thermique maison,
et ouvre une piste d’évolution future vers une observabilité inertielle ECS étendue.

Aucune implémentation n’est décidée à ce stade. Cette note constitue une trace conceptuelle fondatrice.

---

🧭 CONTEXTE

Le sous-système ECS d’ARSENAL dispose aujourd’hui :

d’une source thermique primaire sécurisée (sensor.ecs_temperature_ballon_securisee),
d’un capteur de maximum de cycle (sensor.ecs_temperature_max_cycle),
d’un mécanisme de capture du timestamp de Tmax (input_datetime.ecs_tmax_timestamp),
d’une consolidation documentaire figée en fin de cycle.

Le pic thermique ECS est actuellement utilisé pour :

le diagnostic post-cycle,
le calcul de la durée réelle de chauffe,
l’auto-ajustement des offsets ECS.

---

🔍 DÉFINITION ACTUELLE DU PIC ECS

Fenêtre d’observation

Dans l’architecture actuelle :

la température maximale ECS est observée uniquement tant que :
input_boolean.ecs_cycle_en_cours == on

dès que :
ecs_cycle_en_cours passe à off

alors :

le capteur sensor.ecs_temperature_max_cycle est gelé définitivement,
aucune élévation thermique ultérieure n’est plus prise en compte,
la consolidation documentaire est déclenchée,
le pic est figé.

Objet réellement mesuré

Le « pic ECS » actuel correspond donc strictement à :
> Tmax atteint par le ballon ECS pendant la phase de chauffe pilotée, bornée par le verrou logique de cycle.

Ce pic est :

un pic de phase métier,
un indicateur de performance de commande,
non un pic thermique physique complet.

---

⚠️ LIMITATION PHYSIQUE IDENTIFIÉE

Des observations réelles montrent que :

après l’arrêt de chauffe ECS,
pendant la phase inertielle post-arrêt,
la température réelle du ballon continue à augmenter,
et atteint un maximum physique supérieur au pic figé.

Exemple observé :

pic ECS figé : 45.7 °C
pic physique réel : 46.5 °C
écart inertiel : +0.8 °C

Ce phénomène est dû à :

inertie thermique interne,
stratification du ballon,
homogénéisation post-arrêt,
latence échangeur / sonde.

Cette phase est aujourd’hui volontairement hors périmètre ECS.

---

🧠 COMPARAISON AVEC LE MODÈLE THERMIQUE MAISON

Modèle maison (thermique inertiel étendu)

Dans le sous-système chauffage :

l’arrêt de commande produit un ancrage canonique B0,
l’inertie post-arrêt est observée explicitement,
le pic thermique intéressant est post-commande,

la grandeur mesurée est :

> ΔT_inertie = T_max_post_arrêt − T_arrêt

Ce ΔT constitue :

un invariant système,
un marqueur de dynamique physique,
une base de calibration thermique.

Modèle ECS actuel (thermique tronqué métier)

Dans le sous-système ECS :

aucun ancrage B0 n’existe,
l’arrêt de commande est assimilé à la fin du phénomène,
l’inertie est ignorée,
le pic est recherché avant arrêt,

la grandeur mesurée est :

> T_max_pendant_commande

Ce n’est pas un invariant inertiel, mais :

un indicateur de régulation,
dépendant de la consigne,
dépendant du régime,
dépendant de la température initiale.

---

🧩 CONSÉQUENCE ARCHITECTURALE

Il existe aujourd’hui dans ARSENAL deux modèles thermiques distincts :

Domaine	Modèle	Pic mesuré

Maison	Inertiel étendu	Pic post-arrêt + overshoot
ECS	Métier piloté	Pic pendant commande

Le pic ECS actuel :

est cohérent,
est stable,
est déterministe,

mais ne représente pas le phénomène thermique complet du ballon.

Il est donc parfaitement valide pour :

diagnostiquer la commande,
évaluer la régulation,
piloter un offset de consigne.

Mais il est incomplet pour :

caractériser l’inertie réelle du ballon,
mesurer un invariant thermique stable,
aligner le modèle ECS avec le modèle maison.

---

🛣️ PISTE D’ÉVOLUTION FUTURE (NON DÉCIDÉE)

Sans décision d’implémentation à ce stade, une convergence conceptuelle avec le modèle maison impliquerait potentiellement :

introduction d’un B0 ECS :
température exacte au moment de l’arrêt chauffe ECS

observation d’une phase inertielle post-cycle ECS

définition d’un nouvel invariant possible :

> ΔT_inertie_ECS = T_max_post_cycle − T_arrêt_cycle

dissociation entre :

pic de commande ECS
pic physique inertiel ECS

Cette évolution permettrait :

une calibration plus physique des offsets,
une meilleure caractérisation du ballon,
une unification conceptuelle maison / ECS.

---

🔒 STATUT ET GOUVERNANCE

Cette note est :

une trace conceptuelle
non normative
sans impact opérationnel immédiat
sans chantier ouvert

Toute évolution future devra :

respecter le contrat ECS fondateur,
préserver la stabilité actuelle,
être introduite comme nouvelle couche d’observabilité, jamais comme modification destructive.

---

📌 CONCLUSION

Le système ECS actuel d’ARSENAL est :

sain,
robuste,
cohérent,
parfaitement déterministe.

Il mesure aujourd’hui :
> la performance thermique de la phase de chauffe pilotée.

Il ne mesure pas encore :
> la dynamique inertielle complète du ballon ECS.

Cette différence n’est ni une erreur ni un bug, mais :
> une limite volontaire de modèle, désormais identifiée.

Cette note constitue la référence fondatrice pour toute réflexion future sur l’extension inertielle de l’observabilité ECS.