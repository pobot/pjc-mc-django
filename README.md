# POBOT Junior Cup - Gestion de la compétition

Version Django

## Présentation

Ce projet est la nouvelle version du système de gestion 
de notre compétition POBOT Junior Cup. Le projet de départ est disponible
dans le repository **pobot/POBOT_Junior_Cup** (https://github.com/pobot/POBOT_Junior_Cup)

## Avertissement

Comme pour le projet précédent, il ne s'agit nullement d'un système prêt à l'emploi
pour d'autres contextes d'utilisation, mais uniquement d'un exemple de vraie application
développée en Django qui peut être exploré pour découvrir ce fabuleux framwork
ou en explorer une partie de ses fonctionnalités.

Sa vocation est donc essentiellement pédagogique, notamment à l'attention de mes 
camarades de l'association POBOT qui se sont lancés dans l'aventure Python.

Il n'a enfin nullement la prétention d'être un exemple parfait de la manière d'utiliser
Django. Disons que j'ai essayé de faire le plus proprement possible. 
 
## Evolutions

### Techniques

Cette version est une réécriture totale en **Python 3.4** et basée sur **Django** (https://www.djangoproject.com/).

Pourquoi Django pour gérer un si faible volume de données ? C'est simple :
* pour ce pas réinventer la roue et utiliser les fonctionnalités d'un framework écrit par
des gens bien meilleurs que moi, afin de se concentrer sur la définition du
modèle de données et les fonctions métier et non pas sur la mécanique de base de la
persistence des données, du serveur Web, de la gestion des utilisateurs,...
* pour bénéficier d'un back-office d'administration out-of-the-box dont le développement
équivalent représenterait des mois de travail
* pour le fun

### Fonctionnelles

Des évolutions fonctionnelles majeures ont de plus été ajoutées :
* la saisie en temps réel des résultats de match **directement par les arbitres** depuis 
leurs smartphones (voir la page _Screenshots_ du Wiki projet)
* la gestion de plusieurs catégories de classement, maintenant que les robots à base
d'Arduino peuvent concourir aux côtés des ceux en Mindstorms.

Ce sont d'ailleurs les réflexions relatives à l'implémentation de ces gros changements
qui ont poussé vers la réécriture avec Django, afin de limiter le volume de code global
à développer.

La nouvelle application est maintenant à des années lumière fonctionnellement et 
technniquement de sa version précédente.

## Utilisation du projet

Comme pour tout projet Python, il est plus que fortement conseillé de travail dans
un _virtualenv_. Si vous ne savez pas encore ce que c'est, faites un tour pour commencer
sur le site de sa documentation de référence (https://virtualenv.pypa.io/en/stable/).

Clonez ensuite le projet, et installez les dépendances via : 

`pip install -r requirements-dev.txt`

Cette commande installera les packages utilisés pour le développement en plus des paquets
du runtime.

Fabric n'est plus utilisé dans les dernières versions et a été remplacé par un Makefile,
compte tenu de la simplicité des tâches à gérer. Ca fait toujours une dépendance en moins ;)

## Remarques techniques

**gunicorn** (http://gunicorn.org/) est utilisé comme serveur de production et son fichier 
de configuration est également fourni à la racine du projet. Je n'ai pas jugé utile de
lui ajouter un nginx en frontal, compte tenu qu'il n'y a au bout du compte que 6 clients :
les 3 arbitres, les deux RPi connectées aux écrans TVHD pour la diffusion des informations 
de déroulement et l'admin du back-office. 

**whitenoise** (http://whitenoise.evans.io/en/stable/)
fait du très bon boulot pour servir les ressources statiques de manière optimisée derrière
gunicorn sans devoir jouer avec `manage.py collectstatic` et un serveur HTTP en frontal pour servir 
ces ressources.

## Evolutions 2020

Ayant eu quelques inquiétudes lors de l'édition 2019 avec des messages zarbis relatifs 
à la base de données SQLite, on est passé à un vrai serveur car j'ai fini par avoir des doutes
en cas de requêtes attaquant simultanément la database.

Comme il n'est pas question cependant de devoir installer un SGBD sur les machines de dev
et de prod, la solution magique est Docker. L'ensemble de l'application a donc été migrée
vers un stack Docker-compose, composé de 2 containers:
- l'application Django
- un serveur PostgreSQL

### Préparation du déploiement

Créer un répertoire pour les fichiers du stack:

    $ makdir pjcmc
    $ cd pjcmc

Créer le network externe au stack pour pouvoir accéder
à l'appli depuis le host:

    $ docker network create pjc_mc
    
Créer le volume persistent pour les données de PostgreSQL:
 
    $ docker volume create pjcmc_db_data
    
Créer le répertoire partagé pour échanger des fichiers avec l'appli Django 
(ex: les PDF produits par la *management command* `make_docs`) :

    $ mkdir shared
    
Transférer les fichiers suivant dans le répertoire du stack:
- `docker-compose.yaml`
- `.env`

### Transfert de l'image Docker de l'appli

Sur la machine de développement, sauvegarder l'image:

    $ docker save local/pjc_mc:latest --output pjc_mc-latest.tar
    
La transférer sur la machine de prod:

    $ scp pjc_mc-latest.tar <hostname>:/relpath/to/pjcmc/
    
Sur la machine de prod, charger l'image dans le repo local:
    
    $ docker load -i pjc_mc-latest.tar
    
### Premier lancement

Ce lancement ne conduira pas à un stack opérationnel, car la database n'existe pas encore
et que l'appli Django doit être initialisée. Il permettra cependant d'effectuer ces opérations.

Note: dans les exemples suivants, on suppose que l'alias `dc` a été créé au préalable 
pour la commande `docker-compose`.

Lancer le stack en mode *detached* et vérifier que les deux containers tournent:

    $ dc up -d
    Creating db ... done
    Creating django-app ... done
    $ docker ps
    CONTAINER ID    IMAGE               COMMAND     ....    NAMES
    ...             local/pjc_mc:latest ...         ....    django-app
    ...             postgres            ...         ....    db

Créer la database de l'appli dans le serveur PostgreSQL:

    $ dc exec db psql -U postgres
    psql (11.1...)
    Type "help" for help.
    
    postgres=# create database pjc_mc;
    
Relancer le container django-app dont le log doit contenir une erreur liée au fait
que la base n'existait pas lors du premier lancement:

    $ dc restart django-app
    
Si on examine le log, on doit cette fois-ci voir les messages de la migration initiale
qui crée l'ensemble des tables de l'appli.

Il faut maintenant initialiser le superuser Django:

    $ dc exec django-app ./manage.py createsuperuser
    
Il ne reste plus qu'à initialiser le pool des fidèles arbitres:

    $ dc exec django-app ./manage.py create_referees
    
Et voilà, c'est prêt :) 

On peut maintenant aller sur l'admin en local à l'URL
`http://localhost:8000/admin`. Il doit afficher le formulaire de login, et si on
y entre les credentials du superuser créé précédemment, on doit obtenir la page d'accueil
de l'admin. 

En profiter pour vérifier que les users des arbitres ont bien été créés.

### Sauvegarde des données

Le plus simple est de faire un dump PostgreSQL, l'autre option étant d'utiliser les 
management commands de Django.

    $ dc exec db pg_dump -U postgres pjc_mc | gzip > pjc_mc-dump.gz
    
Au moins on est certain de tout avoir, y compris les tables internes de Django 
(migrations et autres).

### Génération des documents

Plusieurs documents sont produits au format PDF à partir des données gérées par 
l'application, à l'aide de la *management command* `make_docs`:
- certificats de participation des équipes
- diplômes à remplir
- listes des équipes
- feuilles de match nomminatives
- fiches nomminatives d'évaluation des exposés, des posters
- étiquettes nominatives des stands
- signalétique
- ...


    $ dc exec django-app ./manage.py make_docs

Utiliser l'option `--help` pour obtenir la liste des options disponibles, dont:

- `-g` pour définir quels documents produire
- `-o` pour définir le répertoire dans lequel les documents sont produits

Concernant le répertoire de sortie, se souvenir que le répertoire host `pjcmc/shared` 
est monté dans le container sous `/var/lib/shared`, avec un uid/gid `1000/1000` afin
que les fichiers soient accessibles en R/W sous le host. 