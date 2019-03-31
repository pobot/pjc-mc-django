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