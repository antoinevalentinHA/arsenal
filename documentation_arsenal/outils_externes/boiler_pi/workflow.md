# Workflow Git — boiler-bridge
## PC → GitHub → Pi

> **Objectif** : zéro bricolage, zéro surprise, rollback trivial.  
> **Principe** : toute modification naît sur le PC, transite par GitHub, est déployée sur le Pi. Jamais l'inverse.

---

## 0. Structure cible

```
boiler-bridge/
├── boiler_mqtt.py
├── README.md
├── systemd/
│   └── boiler_bridge.service
└── .gitignore
```

---

## 1. PC — Initialisation

### 1.0 Dossier de travail PC (obligatoire)

Toutes les opérations sont réalisées dans le dossier dédié :

```bash
cd C:/boiler
```

> Ce dossier est la racine unique des dépôts liés au boiler bridge. Structure locale : `C:/boiler/boiler-bridge/`.

### 1.1 Créer le dépôt local

```bash
mkdir boiler-bridge
cd boiler-bridge
git init
```

### 1.2 Capturer l'état initial depuis le Pi

```bash
scp pi@192.168.1.119:/home/pi/boiler-bridge/boiler_mqtt.py .
ls -l boiler_mqtt.py
```

> Cette copie constitue la capture de l'état de production initial du boiler bridge.  
> Nécessite OpenSSH (installé par défaut sur Windows 10/11).

### 1.3 `.gitignore` (obligatoire)

```
__pycache__/
*.pyc
.env
.env.*
*.log
venv/
```

### 1.4 Commit initial

```bash
git add .
git commit -m "init: boiler bridge"
```

---

## 2. GitHub — Dépôt privé

Créer un dépôt privé nommé **`boiler-bridge`**, puis :

```bash
git remote add origin git@github.com:antoinevalentinHA/boiler-bridge.git
git branch -M main
git push -u origin main
```

> **Prérequis :** clé SSH configurée (voir section 9).

---

## 3. Pi — Installation initiale

Connexion SSH classique.

### 3.1 Cloner le dépôt (SSH obligatoire)

```bash
cd /home/pi
git clone git@github.com:antoinevalentinHA/boiler-bridge.git
cd boiler-bridge
```

### 3.2 Déployer le service

```bash
sudo cp /home/pi/boiler-bridge/systemd/boiler_bridge.service /etc/systemd/system/boiler_bridge.service
```

### 3.3 Activer et démarrer

```bash
sudo systemctl daemon-reload
sudo systemctl enable boiler_bridge.service
sudo systemctl restart boiler_bridge.service
```

### 3.4 Vérifier

```bash
sudo systemctl status boiler_bridge.service
```

---

## 4. Workflow quotidien

### Sur le PC — modifier et publier

```bash
python -m py_compile boiler_mqtt.py   # Windows : python ; Pi : python3
git add .
git commit -m "fix: gestion ACK timeout"
git push
```

### Sur le Pi — déployer

```bash
cd /home/pi/boiler-bridge
git fetch origin
git reset --hard origin/main
python3 -m py_compile boiler_mqtt.py
sudo systemctl restart boiler_bridge.service
sudo systemctl status boiler_bridge.service
sudo journalctl -u boiler_bridge.service -n 50 --no-pager
```

> `fetch` + `reset --hard origin/main` est déterministe : le Pi reflète exactement `origin/main`, sans merge implicite, sans surprise si un fichier a été modifié localement par erreur.  
> `py_compile` avant le restart est un garde-fou obligatoire : un script syntaxiquement cassé ne doit jamais atteindre systemd.

---

## 5. Rollback

```bash
cd /home/pi/boiler-bridge
git log --oneline
git reset --hard <commit_id>
python3 -m py_compile boiler_mqtt.py
sudo systemctl restart boiler_bridge.service
sudo systemctl status boiler_bridge.service
```

Pour revenir ensuite sur la dernière version de `main` :

```bash
git fetch origin
git reset --hard origin/main
python3 -m py_compile boiler_mqtt.py
sudo systemctl restart boiler_bridge.service
```

> `reset --hard` est plus net que `checkout` pour une machine d'exécution : pas de *detached HEAD*, état du dépôt sans ambiguïté.

---

## 6. Discipline — règles non négociables

| Règle | Détail |
|-------|--------|
| **Jamais modifier sur le Pi** | Le Pi est un environnement d'exécution, pas de développement. Toute modification directe casse le modèle. |
| **Toujours committer avant de déployer** | Le Pi n'exécute que du code versionné. |
| **Un commit = une intention claire** | Pas de commits "test", "wip" ou "misc". |

Configuration git recommandée sur le Pi (à faire une fois) :

```bash
git config --global pull.ff only
git config --global advice.detachedHead false
```

---

## 7. Secrets — ne jamais versionner

Ne jamais mettre dans git :

- identifiant MQTT
- mot de passe MQTT
- tokens / clés API

**Emplacement obligatoire :**

```
/home/pi/boiler_bridge.env
```

Créer le fichier :

```ini
MQTT_USER=monuser
MQTT_PASSWORD=monpassword
```

Verrouiller les droits (obligatoire) :

```bash
chmod 600 /home/pi/boiler_bridge.env
chown pi:pi /home/pi/boiler_bridge.env
```

Référencer dans le service :

```ini
EnvironmentFile=/home/pi/boiler_bridge.env
```

> Le fichier `/home/pi/boiler_bridge.env` est hors du dépôt git et hors de `/home/pi/boiler-bridge/`. Il n'est jamais versionné.

---

## 8. README minimal (à inclure dans le repo)

```markdown
# Boiler Bridge

Bridge Optolink/MQTT pour Arsenal — architecture locale, zéro cloud.

## Déploiement

    git fetch origin
    git reset --hard origin/main
    python3 -m py_compile boiler_mqtt.py
    sudo systemctl restart boiler_bridge.service

## Logs

    sudo journalctl -u boiler_bridge.service -f
```

---

## 9. Authentification SSH vers GitHub (obligatoire)

```bash
ssh-keygen -t ed25519 -C "arsenal-boiler-bridge"
cat ~/.ssh/id_ed25519.pub   # coller dans GitHub → Settings → SSH keys
```

Vérifier que le remote utilise SSH :

```bash
git remote set-url origin git@github.com:antoinevalentinHA/boiler-bridge.git
```

---

## 10. Script de déploiement en une commande

Créer `/home/pi/boiler-bridge/deploy.sh` :

```bash
#!/bin/bash
set -e

cd /home/pi/boiler-bridge

# Garde-fou : aucune modification locale tolérée
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "ERREUR : modifications locales détectées — abandon"
  exit 1
fi

git fetch origin
git reset --hard origin/main

python3 -m py_compile boiler_mqtt.py

sudo systemctl restart boiler_bridge.service
sudo systemctl status boiler_bridge.service
sudo journalctl -u boiler_bridge.service -n 50 --no-pager
```

```bash
chmod +x deploy.sh
```

Déploiement en une commande depuis le Pi :

```bash
./deploy.sh
```

---

## 11. Backup (obligatoire)

Script local :

```
/home/pi/backup_boiler_bridge.sh
```

Contenu du script :

```bash
#!/bin/bash
set -e

if ! mountpoint -q /mnt/backups_boiler_pi; then
  echo "ERREUR : NAS non monté — backup annulé"
  exit 1
fi

DEST="/mnt/backups_boiler_pi/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$DEST"

cp -a /home/pi/boiler-bridge/ "$DEST/"
cp /etc/systemd/system/boiler_bridge.service "$DEST/"
cp /home/pi/boiler_bridge.env "$DEST/"

# Rotation : conserver les 7 dernières sauvegardes
ls -dt /mnt/backups_boiler_pi/*/ | tail -n +8 | xargs -r rm -rf

echo "Backup OK : $DEST"
```

```bash
chmod +x /home/pi/backup_boiler_bridge.sh
```

Contenu sauvegardé :

```
/home/pi/boiler-bridge/
/etc/systemd/system/boiler_bridge.service
/home/pi/boiler_bridge.env
```

Destination :

```
/mnt/backups_boiler_pi/
```

Politique : conservation des 7 dernières sauvegardes, rotation automatique.

> ⚠️ **Invariant** : si le NAS n'est pas monté, le script échoue immédiatement. Aucun backup silencieux en local.

---

## Résumé

| Élément | Choix |
|---------|-------|
| Versioning | Git (local + GitHub privé) |
| Déploiement | `git fetch` + `reset --hard origin/main` + restart |
| Rollback | `git reset --hard <commit_id>` + restart |
| Secrets | `/home/pi/boiler_bridge.env`, hors git |
| Remote GitHub | SSH obligatoire |

**Invariants de production :**

```
service actif  = boiler_bridge.service
script exécuté = /home/pi/boiler-bridge/boiler_mqtt.py
config         = /home/pi/boiler_bridge.env
```
