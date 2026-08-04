# Valise — mise en ligne

Deux fichiers, à la racine du dépôt : `index.html` et `sw.js`.

## Déploiement

1. Créer un dépôt public `valise` sur le compte `dy-dev`.
2. Y déposer `index.html` et `sw.js` (glisser-déposer dans l'interface web de GitHub suffit).
3. `Settings` → `Pages` → Source : `Deploy from a branch`, branche `main`, dossier `/ (root)`.
4. Attendre une à deux minutes. L'adresse devient :

```
https://dy-dev.github.io/valise/
```

## Installation sur le téléphone

1. Ouvrir cette adresse dans Chrome sur Android.
2. Menu ⋮ → `Ajouter à l'écran d'accueil` (ou le bouton `Installer l'application` dans les Paramètres de l'app).
3. L'icône apparaît sur l'écran d'accueil et l'application s'ouvre en plein écran, sans barre d'adresse.

À partir de là, plus besoin de réseau : le service worker garde une copie locale.

## Vérification de la persistance

Avant de partir : cocher un objet, fermer complètement l'application (balayer depuis les applications récentes), rouvrir. La coche doit être là.

Si un bandeau rouge apparaît en haut de l'écran, le stockage n'est pas fiable dans ce contexte — ne pas utiliser cette ouverture-là.

## Deux choses indépendantes

- **Tes listes du moment** vivent dans le stockage du navigateur, sur le téléphone. Ajouter un objet ne modifie pas `index.html`, et remplacer `index.html` sur GitHub ne les efface pas.
- **Le contenu d'origine** est le bloc JSON `<script id="seed">` dans `index.html`. Il ne sert qu'une fois : au tout premier lancement, quand le stockage est vide. C'est ce qu'un téléphone neuf recevra.

Mettre à jour le dépôt n'a donc d'intérêt que pour figer tes listes affinées comme nouveau point de départ.

## Remonter les listes du téléphone vers le dépôt

Au retour de voyage, une fois les listes à jour.

**Depuis le téléphone, sans poste :**

1. Paramètres → `Copier le contenu d'origine`.
2. Sur GitHub, ouvrir `index.html`, icône crayon.
3. Sélectionner tout ce qui se trouve entre `/* SEED-START */` et `/* SEED-END */`, coller.
4. Incrémenter `CACHE` dans `sw.js` (`valise-v1` → `valise-v2`), commit.

**Depuis le poste :**

1. Paramètres → `Télécharger seed.json`, récupérer le fichier.
2. ```
   python update_seed.py seed.json
   ```
   Le script repère les balises tout seul, retire les cases cochées et les identifiants, et copie l'ancien fichier en `index.html.bak`.
3. Incrémenter `CACHE` dans `sw.js`, commit.

Le script accepte aussi une sauvegarde complète (`valise-sauvegarde-*.json`) à la place de `seed.json`.

## Mise à jour du code

Même règle : remplacer `index.html`, puis **incrémenter `CACHE` dans `sw.js`**. Sans cela le téléphone continue de servir l'ancienne version depuis son cache. Les données déjà saisies ne sont jamais touchées.

## Sauvegarde

Paramètres → `Copier les données` place l'intégralité des checklists dans le presse-papiers. À coller dans une note ou un e-mail avant un long voyage. `Coller des données` fait le chemin inverse.

`Exporter toutes les données` produit le même contenu sous forme de fichier `.json`.
