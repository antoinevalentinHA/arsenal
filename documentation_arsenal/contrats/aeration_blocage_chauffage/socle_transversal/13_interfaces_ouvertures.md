# ==========================================================
# 🧠 ARSENAL — CONTRAT NORMATIF (SOCLE TRANSVERSAL)
#     INTERFACES EXTERNES — CONTRAT OUVERTURES (RÉFÉRENCE)
# ==========================================================

## 🎯 OBJET

Déclarer les dépendances externes du domaine :

- Aération → Blocage Chauffage

vers le domaine :

- Ouvertures (portes / fenêtres)

Ce document ne redéfinit aucun mécanisme d’ouverture.
Il référence un contrat externe clos et figé.

---

## 🔗 CONTRAT EXTERNE DE RÉFÉRENCE

Domaine :
- Ouvertures (portes / fenêtres)

Statut :
- Contrat NORMATIF — clos et figé

Portée :
- détection, agrégation, temporisation, qualification, UI, helpers associés

Ce domaine est hors périmètre du présent contrat Aération/Blocage Chauffage.

---

## 🧩 INTERFACES CONSOMMÉES (LISTE FERMÉE)

Le domaine Aération/Blocage Chauffage consomme uniquement les entités suivantes,
telles que définies par le contrat Ouvertures :

### Ouvertures — état brut maison
- `binary_sensor.fenetre_ouverte_maison`

### Ouvertures — état qualifié avec temporisation
- `binary_sensor.fenetre_ouverte_maison_avec_delai`

### Tentative en grâce (pré-qualification)
- `binary_sensor.tentative_aeration_en_grace`

### Capteurs bruts (déclencheurs M1 immédiats)
- `binary_sensor.capteur_fenetre_entree`
- `binary_sensor.capteur_chambre_arnaud`
- `binary_sensor.capteur_chambre_matthieu`

---

## 🛑 INTERDITS

Il est strictement interdit :

- de dupliquer la logique Ouvertures dans le présent domaine,
- de modifier l’interprétation des timers de grâce ici,
- de redéfinir les agrégations ici.

Toute évolution liée aux ouvertures relève exclusivement du contrat Ouvertures.

# ==========================================================