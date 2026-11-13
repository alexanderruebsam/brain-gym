"""Notizen-Status (AN/AUS) als kleines Eck-Badge statt als zweite Textzeile, damit alle Werkzeug-Buttons einzeilig bleiben."""
import sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding="utf-8").read()


def rep(old, new):
    global t
    assert t.count(old) == 1, old[:70]
    t = t.replace(old, new)


rep(".tool .badge { font-size: 0.65rem; font-weight: 700; letter-spacing: .06em; }",
    """.tool { position: relative; }
.tool .badge {
  position: absolute; top: -7px; right: -6px; padding: 3px 6px 2px; border-radius: 999px;
  font-size: 0.6rem; font-weight: 700; letter-spacing: .06em; line-height: 1;
  background: var(--paper); color: var(--muted); border: 1px solid var(--line);
}
.tool[aria-pressed="true"] .badge { background: var(--accent); color: var(--paper); border-color: var(--accent); }""")
rep('<span><span data-t="notes">Notizen</span> <span class="badge" id="notes-state">AUS</span></span>',
    '<span data-t="notes">Notizen</span><span class="badge" id="notes-state">AUS</span>')
open(dst, "w", encoding="utf-8").write(t)
print("ok")
