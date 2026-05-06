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

### Ouvertures — état brut agrégé maison
- `binary_sensor.fenetre_ouverte_maison`

### Ouvertures — état qualifié avec temporisation
- `binary_sensor.fenetre_ouverte_maison_avec_delai`

### Tentative en grâce (pré-qualification N0)
- `binary_sensor.tentative_aeration_en_grace`

### Contacts pièce (déclencheurs immédiats hors grâce)
- `binary_sensor.contact_chambre_arnaud`
- `binary_sensor.contact_chambre_matthieu`
- `binary_sensor.contact_entree_fenetre`

### Ouverture qualifiée (frontière aération)
- `binary_sensor.ouverture_qualifiee_maison`

Rôle :

- Signal métier unique de **réouverture bloquante**
- Frontière contractuelle utilisée par :
  - M1 (qualification du fait métier)
  - M3 (garde-fou structurel ΔT)
  - M5 (suspension pendant blocage)

Ce capteur constitue l’interface normative entre le
sous-système *Ouvertures* et le domaine
*Aération → Blocage Chauffage*.

Il ne remplace pas :

- `binary_sensor.fenetre_ouverte_maison`
- `binary_sensor.fenetre_ouverte_maison_avec_delai`

et ne redéfinit aucune logique interne du contrat Ouvertures.

---

## 🛑 INTERDITS

Il est strictement interdit :

- de consommer des entités `capteur_*` dans ce domaine,
- de dupliquer la logique Ouvertures dans le présent domaine,
- de modifier l’interprétation des timers de grâce ici,
- de redéfinir les agrégations ici.

Toute évolution liée aux ouvertures relève exclusivement du contrat Ouvertures.

# ==========================================================