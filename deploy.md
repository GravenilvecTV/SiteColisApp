# Mise en place

1. Accèder au vps
Rendez vous sur le HPanel https://hpanel.hostinger.com/

2. Connectez-vous en SSH
Sur Windows : 
- Installer un client comme https://putty.org/index.html
- Renseigner root@IP_DE_VOTRE_VPS
- PORT 22
Sur Linux/Mac : 
- Ouvrir un terminal
- Tapez ssh root@IP_DE_VOTRE_VPS

Ou depuis le HPanel avec le bouton "Terminal" en haut à droite (aucune installation requise)

3. Enregistrement du domaine (recommandé)

- Your domain : Renseignez votre omaine (ex: graventutos.tech)
- Please verify it is correct (tapez y)
- Do you wish to issue a Let's encrypt certificate for this domain? (tapez y)
- Please enter your E-mail: renseigner un email pour le certificat (ex: monemail@gmail.com)
- Please verify it is correct (tapez y)

Attention ! Le domaine doit bien pointer vers votre vps
Votre certificat sera enregistré en deux fichiers

Certificate is saved at: /etc/letsencrypt/live/VOTRE_DOMAINE/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/VOTRE_DOMAINE/privkey.pem

- Do you wish to force HTTPS rewrite rule for this domain? (si vous voulez forcer le https) (tapez y)
- Do you wish to update the system now? This will update the web server as well. (tapez y)


4. Clonage du projet

- Créer un dossier 'sitecolis'   
mkdir -p /var/www/sitecolis

- Aller dans le dossier
cd /var/www/sitecolis

- Cloner le projet avec git
git clone https://github.com/GravenilvecTV/SiteColisApp app

- Aller dans le dossier ap
cd app

5. Créer l'environnement virtuel

- Installer python3 pour les environnements virtuels
apt install python3.12-venv

- Créer l'environnement
python3 -m venv venv

- Activer l'environnement
source ./venv/bin/activate

6. Dependances

- Installons les dependances du fichier requirements.txt
pip install -r requirements.txt

- Lançons la migration pour regenerer la db sqlite
python manage.py migrate

- Générer une secrete key de production 
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
Copier la clé-prod

7. Fichier environnement

- Créer un fichier .env
touch .env

- Ouvrir avec un editeur (nano, vi, ...)
nano .env

- Et coller le contenu de votre .env
SECRET_KEY=la-clé-prod
DEBUG=False

Pour sortir CTRL+X , Y pour sauvegarder, puis entrer

8. Modifier le settings.py
nano colisproject/settings.py

Aller à la fin pour activer

CSRF_TRUSTED_ORIGINS = ['http://IP_DU_SERVEUR', 'https://ton-domaine.com']
SESSION_COOKIE_SECURE = False   # True si HTTPS activé
CSRF_COOKIE_SECURE = False      # True si HTTPS activé
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

Pour sortir CTRL+X , Y pour sauvegarder, puis entrer

9. Fichier statique

- python manage.py collectstatic

# Mise en place Gunicorn (Reverse Proxy)

- Installer gunicorn
pip install gunicorn

- Lancer gunicorn avec l'application
gunicorn colisproject.wsgi:application --bind 127.0.0.1:8000

Pour sortir CTRL+C (ou redelancer le terminal si bloquer)

- Stopper le port en cas de besoin
sudo lsof -i :8000

- Créer le fichier gunicorn-sitecolis.service (qui va se lancer au demarrage)
nano /etc/systemd/system/gunicorn-sitecolis.service

- Completer la config suivante
[Unit]
Description=Gunicorn daemon for sitecolis Django project
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/sitecolis
Environment="PATH=/var/www/sitecolis/app/venv/bin"
ExecStart=/var/www/sitecolis/app/venv/bin/gunicorn colisproject.wsgi:application --bind 127.0.0.1:8000 --workers 3 --timeout 120 --access-logfile - --error-logfile -

Restart=always
RestartSec=5
KillSignal=SIGQUIT
Type=simple

[Install]
WantedBy=multi-user.target

- Relancement de gunicorn

systemctl daemon-reload
systemctl enable --now gunicorn-sitecolis
systemctl status gunicorn-sitecolis --no-pager

# OpenLiteSpeed


# Activation de OpenLiteSpeed

1. Mise en place

- Démarrage de l'outil 
/usr/local/lsws/bin/lswsctrl start

- Autorisation du port 7080 sur le parafeu (ufw)
ufw allow 7080/tcp

- Récuperer le mot de passe admin
cat /home/ubuntu/.litespeed_password
admin_pass=VOTRE_MOT_DE_PASSE_GENERER 
(ex : hBmw78wc0dslgeze)

- Tester en allant sur http://votresite.fr:7080 ou http://votreip:7080
Connexion non sécurisé c'est normal, poursuivez tout de meme

nom d'utilisateur : admin
mot de passe : celui que vous avez copié

#  Nouveau VirtualHost 'sitecolis'

Aller dans Virtual Hosts -> Cliquez sur le +
- Virtual Host Name : sitecolis
- Virtual Host Root : /var/www/sitecolis/app/
- Config file : /usr/local/lsws/conf/vhosts/graventutos.tech/vhconf.conf
- Note : Django Colis App
- Enable Scripts/ExtApps: Yes
- Restrained: No

--> Enregistrer
Erreur sur le config file : il demande Click to create
Faites le puis enregistrer

# Configuration du 'sitecolis'
Ouvrir le vhost avec la loupe 'View'

Onglet General (indispensable souvent oublié)
- Document Root : /var/www/sitecolis/app/public/
- Domain Name : votedomaine.tech
Sauvegarder

Onglet ExternalApp 
- Type 'Web Server', suivant (avec la fleche à droite)
- Name : gunicorn_sitecolis
- Address : 127.0.0.1:8000
- Max Connections : 2000
- Initial Request Timeout (secs) : 60
- Retry Timeout (secs): 5
Sauvegarder

Onglet Rewrite
- Enable Rewrite : Yes
Sauvegarder

Onglet SSL
- Private key file : /etc/letsencrypt/live/VOTRE_DOMAINE/privkey.pem
- Certificate File : /etc/letsencrypt/live/VOTR_DOMAINE/fullchain.pem
- Chained Certificate : Yes
Sauvegarder

Onglet Context
- Nouveau de type 'Proxy'
- URI: /
- Location: Choisir gunicorn_sitecolis
- Application Type : WSGI
Sauvegarder

Onglet Context
- Nouveau de type 'Static'
- URI: /python/static/
- Location : /var/www/sitecolis/app/public/static
- Accessible : Yes
Sauvegarder

Relancer le serveur 'Grateful restart'

# Listeners

- Aller dans l'onglet Listeners
- Ouvrir 'Default' et changer le VirtualHost 'Example' par 'sitecolis'
- Ouvrir 'DefaultSSL' et changer le VirtualHost 'Example' par 'sitecolis'
Restez sur DefaultSSL, et aller dans le TAB SSL


Onglet SSL
- Private key file : /etc/letsencrypt/live/VOTRE_DOMAINE/privkey.pem
- Certificate File : /etc/letsencrypt/live/VOTR_DOMAINE/fullchain.pem
- Chained Certificate : Yes

Relancer le serveur 'Grateful restart'