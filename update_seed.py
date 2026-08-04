"""
update_seed.py — remplace le contenu d'origine de index.html.

Usage :
    python -m pip  (rien à installer : bibliothèque standard uniquement)

    python update_seed.py seed.json
    python update_seed.py valise-sauvegarde-2026-08-04.json
    python update_seed.py seed.json --html chemin\\vers\\index.html

Accepte deux formes de fichier d'entrée :
  - seed.json           tel que produit par « Télécharger seed.json »
  - sauvegarde complète telle que produite par « Exporter toutes les données »

L'ancien index.html est copié en index.html.bak avant écriture (copie, jamais
déplacement : la source reste en place).
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

START = "/* SEED-START */"
END = "/* SEED-END */"


def load_seed(path: Path):
    """Retourne la liste de checklists au format contenu d'origine."""
    data = json.loads(path.read_text(encoding="utf-8"))

    # Forme 1 : seed.json, tableau de checklists.
    if isinstance(data, list):
        checklists = data
    # Forme 2 : sauvegarde complète.
    elif isinstance(data, dict) and isinstance(data.get("checklists"), list):
        checklists = data["checklists"]
    else:
        sys.exit("Format non reconnu : ni seed.json, ni sauvegarde complete.")

    return [normalise(c) for c in checklists]


def normalise(checklist: dict) -> dict:
    """Retire identifiants, cases cochees et etats de pli."""
    return {
        "name": checklist.get("name", "Sans nom"),
        "emoji": checklist.get("emoji", "\U0001F9F3"),
        "sections": [
            {
                "name": section.get("name", "Sans nom"),
                "items": [normalise_item(i) for i in section.get("items", [])],
            }
            for section in checklist.get("sections", [])
        ],
    }


def normalise_item(item):
    """Un objet devient une chaine, ou un couple nom/quantite si une quantite existe."""
    if isinstance(item, str):
        return item
    qty = item.get("qty")
    if qty:
        return {"name": item.get("name", ""), "qty": qty}
    return item.get("name", "")


def render(checklists) -> str:
    """Mise en forme fixe : une ligne par objet, diff git lisible."""
    q = lambda v: json.dumps(v, ensure_ascii=False)
    lines = ["["]
    for ci, c in enumerate(checklists):
        lines.append('  {')
        lines.append('    "name": %s, "emoji": %s,' % (q(c["name"]), q(c["emoji"])))
        lines.append('    "sections": [')
        for si, s in enumerate(c["sections"]):
            lines.append('      { "name": %s, "items": [' % q(s["name"]))
            for ii, it in enumerate(s["items"]):
                comma = "," if ii < len(s["items"]) - 1 else ""
                lines.append("        %s%s" % (q(it), comma))
            lines.append("      ] }" + ("," if si < len(c["sections"]) - 1 else ""))
        lines.append("    ]")
        lines.append("  }" + ("," if ci < len(checklists) - 1 else ""))
    lines.append("]")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Met a jour le contenu d'origine de index.html")
    parser.add_argument("source", help="seed.json ou sauvegarde complete")
    parser.add_argument("--html", default="index.html", help="chemin de index.html")
    args = parser.parse_args()

    source = Path(args.source)
    html_path = Path(args.html)

    if not source.is_file():
        sys.exit("Introuvable : %s" % source)
    if not html_path.is_file():
        sys.exit("Introuvable : %s" % html_path)

    checklists = load_seed(source)
    html = html_path.read_text(encoding="utf-8")

    if START not in html or END not in html:
        sys.exit("Reperes SEED absents de %s : fichier incompatible." % html_path)

    head, rest = html.split(START, 1)
    _, tail = rest.split(END, 1)

    # Sauvegarde de l'ancien fichier avant ecriture.
    backup = html_path.with_suffix(html_path.suffix + ".bak")
    shutil.copy2(html_path, backup)

    new_html = head + START + "\n" + render(checklists) + "\n" + END + tail
    html_path.write_text(new_html, encoding="utf-8")

    total = sum(len(s["items"]) for c in checklists for s in c["sections"])
    print("%s mis a jour : %d checklists, %d objets." % (html_path, len(checklists), total))
    print("Ancienne version conservee : %s" % backup)
    print("Pensez a incrementer CACHE dans sw.js avant de commiter.")


if __name__ == "__main__":
    main()
