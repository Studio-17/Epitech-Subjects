## AutoDoc

Ce projet à pour but d'automatiser la création de README au norme de **Studio-17**

- [AutoDoc](#autodoc)
- [Requirements:](#requirements)
- [Execution](#execution)
- [Help du projet:](#help-du-projet)
- [Types de Readme](#types-de-readme)
- [Structure des sujets:](#structure-des-sujets)
- [Creation automatique:](#creation-automatique)

## Requirements:

- Tkinter
- Selenium
- Pyperclip

*cf requirements.txt* 

## Execution

Executer `main.py` avec les paramètres voulus

Lors de l'ouverture de la page web, ne rien faire

## Help du projet:


```
Usage:
    ./main.py -b e -url https://my.epitech.eu/index.html#d/2023/B-CPE-110/organized/5979804 -cp

Arguments:
    -b      => choix du Browser entre Edge (e) par défault, Chrome (c) et Firefox (f)
    -url    => url d'une mouli du projet / Module
    -p      => nombre de personnes sur le projet
    -t      => temps en semaines pour le projet
    -cp     => écriture du readme dans le clipboard
    --type  => Type de Readme si l'automatique ne plait pas ("g" => global, "s" => semestre, "m" => module, "p" => projet)

Permet de créer un Readme qui suis les normes établies
```

## Types de Readme

Par défault les choix du type de readme est automatique mais peut être forcé avec le flag [`--type`](#help-du-projet)

**Attention:** Forcer le type de README peut entraîner des erreurs

**Les types de README sont:**
- **Project**:
  - Le temps de travail
  - La taille du groupe
  - Les tests de MRVN
- **Module**:
  - Les détails du module de l'intra
  - Les détails de chaque projet (temps et nom)
- **Semestre**:
  - La liste des Modules du semestre et leurs crédits
  - La liste de projet dans chaque module
- **Global**:
  - La liste des Semestre
  - La liste des modules de chaque Semestre et leurs crédits

## Structure des sujets:

- Le Repo est composé de plusieurs semestres avec chacun un README.md

- Chaque semestre contient un ou plusieurs modules qui ont tous un README.md

- Chaque module contient plusieurs dossiers qui sont des projet et qui ont un README.md

- Chaque projet peut contenir n'importe quoi, si il y a un Bootstrap, il doit être dans un dossier dans le projet

Exemple d'un module dans un Semestre:

📂---Semestre-1

ㅤㅤ|\_\_\_Module-1

ㅤㅤㅤㅤ|\_\_\_Projet-1

ㅤㅤㅤㅤㅤ  |\_\_\_Bootstrap

ㅤㅤㅤㅤㅤㅤㅤㅤ|\_\_\_Fichier_Example.pdf

ㅤㅤㅤㅤㅤ  |\_\_\_Projet

ㅤㅤㅤㅤㅤㅤㅤㅤ|\_\_\_Fichier_Example.pdf

ㅤㅤㅤㅤㅤ  |\_\_\_**README.md** (Readme du projet avec les units tests)

ㅤㅤㅤㅤ|\_\_\_Projet-2

ㅤㅤㅤㅤㅤ  |\_\_\_Fichier_Example.pdf

ㅤㅤㅤㅤㅤ  |\_\_\_**README.md** (Readme du projet avec les units tests)

ㅤㅤㅤㅤ|\_\_\_**README.md** (Readme du Module avec la liste des projets, leurs durée et les détail de l'intra)

ㅤㅤ|\_\_\_**README.md** (Readme du Semestre avec la liste des Module et de chacun de leurs projets)

|\_\_\_**README.md** (Readme du Repo avec tout les Semestre et tous les modules)

---

## Creation automatique:

Un script `create_default_readme.py` existe et à pour objectif de créer des Readme par défaut pour tous les dossiers sans

Les PR et les issues sont les bienvenues en cas de problème ou de suggestion
