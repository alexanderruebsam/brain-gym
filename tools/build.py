"""Baut index.html (installierbare Web-App) aus src/sudoku.html.
Aufruf: python3 tools/build.py [quelle] [ziel]   (Standard: src/sudoku.html -> index.html)"""
import sys, os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, "src", "sudoku.html")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(root, "index.html")

page = open(src, encoding="utf-8").read()
pre, rest = page.split("<style>", 1)
style, body = rest.split("</style>", 1)
pre = pre.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")

head_extra = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Sudoku: drei Rätsel am Tag, vier Schwierigkeitsstufen, Notizen und Bestzeiten.">
<meta name="theme-color" content="#eef1f4" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#11161d" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Brain Gym">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
"""

reset = """/* Basis, die vorher das Artifact-Gerüst lieferte */
:root { color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
body { margin: 0; font-size: 14px; -webkit-tap-highlight-color: transparent; }
img { max-width: 100%; }
[hidden] { display: none !important; }

"""

sw = """
<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
}
</script>
"""

html = ('<!doctype html>\n<html lang="de">\n<head>\n' + head_extra + pre + "<style>\n" + reset
        + style.lstrip("\n") + "</style>\n</head>\n<body>\n" + body.lstrip("\n").rstrip("\n") + "\n" + sw + "</body>\n</html>\n")
open(out, "w", encoding="utf-8").write(html)
print("built", out)
