"""Replaces the Joker with the Bomb (3 per puzzle, clears all wrong numbers with an explosion)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding="utf-8").read()


def rep(old, new, count=1):
    global t
    n = t.count(old)
    assert n == count, f"expected {count}x, found {n}: {old[:70]!r}"
    t = t.replace(old, new)


# ---------- CSS ----------
start = t.index("/* Joker im Retro-Look")
end = t.index(".tool.joker:disabled")
end = t.index("\n", end) + 1
t = t[:start] + """/* Bombe im Retro-Look der Rekord-Screens: Lila, oranger Versatzschatten, gelber Zähler (in beiden Themes gleich) */
.tool.bomb { position: relative; background: #7b2cbf; border-color: #7b2cbf; color: #fff4dd; box-shadow: 3px 3px 0 #ec6a2a; }
.tool.bomb svg.bomb-ico { width: 34px; height: 34px; margin: -7px 0 -5px; stroke: none; }
.tool.bomb .count {
  position: absolute; top: -7px; right: -6px; min-width: 22px; height: 22px; border-radius: 999px; padding: 4px 5px 0;
  background: #f9d342; color: #7b2cbf; box-shadow: 2px 2px 0 #ec6a2a;
  font: 400 0.95rem/18px "Luckiest Guy", "Arial Black", sans-serif; text-align: center;
}
.tool.bomb:not(:disabled) .fuse-spark { transform-origin: 27px 5px; animation: spark .5s ease-in-out infinite alternate; }
@keyframes spark { to { transform: scale(1.35) rotate(25deg); } }
.tool.bomb:active { transform: translate(2px, 2px); box-shadow: 1px 1px 0 #ec6a2a; }
.tool.bomb:disabled { opacity: .35; cursor: default; box-shadow: none; transform: none; }
.tool.bomb:disabled .count { box-shadow: none; }
/* Explosion über den gesprengten Feldern: weißer Kern, Feuerball aus Wolken, die zu Rauch nachdunkeln, dazu Trümmer und Funken */
.boom { position: absolute; pointer-events: none; z-index: 5; }
.boom > * { position: absolute; left: 50%; top: 50%; border-radius: 50%; }
.boom .core {
  width: 168%; height: 168%; translate: -50% -50%; background: #fffbe8;
  box-shadow: 0 0 14px 6px #f9d342; animation: core .35s ease-out forwards;
}
.boom .puff {
  width: var(--s); height: var(--s); translate: calc(-50% + var(--x)) calc(-50% + var(--y));
  animation: puff 1.15s cubic-bezier(.25, .8, .35, 1) var(--t) both;
}
.boom .deb { width: 3px; height: 3px; border-radius: 2px; background: #2c1a33; animation: deb .8s cubic-bezier(.15, .8, .3, 1) .08s both; }
.boom .em { width: 6px; height: 6px; margin: -3px; background: #f9d342; box-shadow: 0 0 6px #ec6a2a; animation: em .9s cubic-bezier(.2, .7, .3, 1) .1s both; }
@keyframes core { 0% { transform: scale(.1); opacity: 1; } 45% { transform: scale(1); opacity: 1; } 100% { transform: scale(1.15); opacity: 0; } }
@keyframes puff {
  0% { transform: scale(0); background: #fffbe8; box-shadow: 0 0 14px #f9d342; }
  18% { transform: scale(1); background: #fff1a8; box-shadow: 0 0 14px #f9d342; }
  34% { background: #f9d342; box-shadow: 0 0 0 2px #ec6a2a, 0 0 10px #ec6a2a; }
  52% { background: #ec6a2a; box-shadow: 0 0 0 2px #7a2e1a; }
  70% { transform: scale(1.08); background: #4a2d4f; box-shadow: 0 0 0 2px #2c1a33; opacity: 1; }
  100% { transform: scale(1.25) translateY(-18%); background: #3a2a40; box-shadow: 0 0 0 2px #2c1a33; opacity: 0; }
}
@keyframes deb { from { transform: rotate(var(--a)) translateX(0); width: 3px; opacity: 1; } 40% { width: var(--l); } to { transform: rotate(var(--a)) translateX(var(--d)); width: var(--l); opacity: 0; } }
@keyframes em { from { transform: rotate(var(--a)) translateX(0) scale(1); opacity: 1; } to { transform: rotate(var(--a)) translateX(var(--d)) scale(.3); opacity: 0; } }
.board.shake { animation: shake .35s ease-in-out; }
@keyframes shake { 20% { translate: -4px 2px; } 40% { translate: 4px -2px; } 60% { translate: -3px -1px; } 80% { translate: 2px 1px; } }
@media (prefers-reduced-motion: reduce) { .boom { display: none; } .board.shake, .tool.bomb .fuse-spark { animation: none; } }
""" + t[end:]

# ---------- Markup: kleine, süße Bombe mit heller Kontur, Kulleraugen und funkelnder Lunte ----------
rep("""    <button class="tool joker" id="joker" title="Joker: zeigt einen Fehler (J)" data-t-title="jokerTitle">
      <b id="joker-n" aria-hidden="true">3</b><span data-t="joker">Joker</span>
    </button>""", """    <button class="tool bomb" id="bomb" title="Bombe: löscht alle Fehler (B)" data-t-title="bombTitle">
      <svg class="bomb-ico" viewBox="0 0 32 32" aria-hidden="true">
        <path d="M20.5 9.5c1.5-3 4-4.6 6.5-4.5" fill="none" stroke="#fff4dd" stroke-width="1.8" stroke-linecap="round"/>
        <rect x="15.6" y="7.6" width="6.4" height="4.6" rx="1.3" transform="rotate(38 18.8 9.9)" fill="#4a2d6e"/>
        <circle cx="14" cy="19" r="11.3" fill="#fff4dd"/>
        <circle cx="14" cy="19" r="10" fill="#24133a"/>
        <ellipse cx="9.4" cy="13.8" rx="2.6" ry="1.5" transform="rotate(-35 9.4 13.8)" fill="#fff" opacity=".55"/>
        <ellipse cx="10.4" cy="19.6" rx="2.2" ry="2.7" fill="#fff4dd"/><ellipse cx="17.6" cy="19.6" rx="2.2" ry="2.7" fill="#fff4dd"/>
        <circle cx="10.9" cy="20.2" r="1.25" fill="#24133a"/><circle cx="18.1" cy="20.2" r="1.25" fill="#24133a"/>
        <circle cx="11.3" cy="19.6" r=".45" fill="#fff"/><circle cx="18.5" cy="19.6" r=".45" fill="#fff"/>
        <g class="fuse-spark"><path d="M27 1.2l.9 2.6 2.7.1-2.2 1.6.8 2.6-2.2-1.5-2.2 1.5.8-2.6-2.2-1.6 2.7-.1z" fill="#f9d342"/><circle cx="27" cy="5" r="1.1" fill="#ec6a2a"/></g>
      </svg>
      <span data-t="bomb">Bombe</span><b class="count" id="bomb-n" aria-hidden="true">3</b>
    </button>""")

# ---------- Texte ----------
rep("joker: 'Joker', jokerTitle: 'Joker: zeigt einen Fehler (J)', jokerFound: 'Hier stimmt etwas nicht.', jokerNone: 'Bisher alles richtig!', jokerLeft: n => `Joker, noch ${n}`,",
    "bomb: 'Bombe', bombTitle: 'Bombe: löscht alle Fehler (B)', bombHit: n => n === 1 ? 'Ein Fehler weggesprengt!' : `${n} Fehler weggesprengt!`, bombNone: 'Keine Fehler – die Bombe verpufft.', bombLeft: n => `Bombe, noch ${n}`,")
rep("joker: 'Joker', jokerTitle: 'Joker: shows one mistake (J)', jokerFound: 'Something’s wrong here.', jokerNone: 'All correct so far!', jokerLeft: n => `Joker, ${n} left`,",
    "bomb: 'Bomb', bombTitle: 'Bomb: clears all mistakes (B)', bombHit: n => n === 1 ? '1 mistake blown away!' : `${n} mistakes blown away!`, bombNone: 'No mistakes – the bomb fizzles out.', bombLeft: n => `Bomb, ${n} left`,")
rep("joker: 'Jolly', jokerTitle: 'Jolly: mostra un errore (J)', jokerFound: 'Qui c’è qualcosa che non va.', jokerNone: 'Finora tutto giusto!', jokerLeft: n => `Jolly, ne restano ${n}`,",
    "bomb: 'Bomba', bombTitle: 'Bomba: cancella tutti gli errori (B)', bombHit: n => n === 1 ? 'Un errore spazzato via!' : `${n} errori spazzati via!`, bombNone: 'Nessun errore – la bomba fa cilecca.', bombLeft: n => `Bomba, ne restano ${n}`,")
rep("joker: 'ジョーカー', jokerTitle: 'ジョーカー：間違いをひとつ表示 (J)', jokerFound: 'ここが間違っています。', jokerNone: 'ここまで全部正解！', jokerLeft: n => `ジョーカー 残り${n}`,",
    "bomb: 'ボム', bombTitle: 'ボム：まちがいを全部消す (B)', bombHit: n => `まちがいを${n}個ふっとばした！`, bombNone: 'まちがいなし。ボムは不発。', bombLeft: n => `ボム 残り${n}`,")
rep("Entf zum Löschen, J für Joker.", "Entf zum Löschen, B für Bombe.", 2)
rep("Del to erase, J for joker.", "Del to erase, B for bomb.")
rep("Canc per cancellare, J per il jolly.", "Canc per cancellare, B per la bomba.")
rep("Del で消去、J でジョーカー。", "Del で消去、B でボム。")

# ---------- State ----------
rep("  const JOKERS = 3; // Joker pro Rätsel", "  const BOMBS = 3; // Bomben pro Rätsel")
rep("jokers: JOKERS, jokerCell: -1,", "bombs: BOMBS,")
rep("S = saved; if (S.jokers === undefined) { S.jokers = JOKERS; S.jokerCell = -1; } render();",
    "S = saved; if (S.bombs === undefined) S.bombs = BOMBS; delete S.jokers; delete S.jokerCell; render();")

# ---------- Render ----------
rep("\n      if (i === S.jokerCell && v && v !== S.solution[i]) c.classList.add('wrong');", "")
rep("""    $('joker-n').textContent = S.jokers;
    $('joker').disabled = S.solved || S.jokers <= 0;
    $('joker').setAttribute('aria-label', tr().jokerLeft(S.jokers));""",
    """    $('bomb-n').textContent = S.bombs;
    $('bomb').disabled = S.solved || S.bombs <= 0;
    $('bomb').setAttribute('aria-label', tr().bombLeft(S.bombs));""")

# ---------- Logik ----------
start = t.index("  // Joker: zeigt genau eine falsche Zahl")
end = t.index("  function checkWin() {")
t = t[:start] + """  // Bombe: sprengt alle falschen Zahlen (verglichen mit der Lösung) weg, die Felder sind danach leer.
  // Sie ist danach verbraucht, auch wenn es keine Fehler gab.
  const reduceMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  function boomAt(i) {
    const wrap = board.parentElement, w = wrap.getBoundingClientRect(), r = cells[i].getBoundingClientRect();
    const el = document.createElement('div');
    el.className = 'boom';
    el.style.cssText = `left:${r.left - w.left}px;top:${r.top - w.top}px;width:${r.width}px;height:${r.height}px`;
    const cw = r.width * 0.85, rnd = (a, b) => a + Math.random() * (b - a);
    let h = '<i class="core"></i>';
    // Feuerball: 12 Wolken rund um die Mitte, leicht versetzt nacheinander
    for (let k = 0; k < 12; k++) {
      const ang = k / 11 * Math.PI * 2 + rnd(-.3, .3), dist = k === 0 ? 0 : cw * (k < 6 ? rnd(.27, .45) : rnd(.54, .77)); // alles 10 % kleiner als zuerst
      h += `<i class="puff" style="--x:${Math.cos(ang) * dist}px;--y:${Math.sin(ang) * dist}px;--s:${cw * (k < 6 ? rnd(.81, 1.08) : rnd(.54, .81))}px;--t:${k * 15}ms"></i>`;
    }
    for (let k = 0; k < 5; k++) h += `<i class="deb" style="--a:${k * 72 + rnd(-20, 20)}deg;--d:${cw * rnd(.9, 1.35)}px;--l:${cw * rnd(.27, .45)}px"></i>`;
    for (let k = 0; k < 8; k++) h += `<i class="em" style="--a:${k * 45 + rnd(-15, 15)}deg;--d:${cw * rnd(.81, 1.44)}px"></i>`;
    el.innerHTML = h;
    wrap.appendChild(el);
    setTimeout(() => el.remove(), 1400);
  }
  function bomb() {
    if (S.solved || S.bombs <= 0) return;
    S.bombs--;
    const wrong = [...Array(81).keys()].filter(i => S.values[i] && !S.puzzle[i] && S.values[i] !== S.solution[i]);
    if (!wrong.length) { render(); save(); toast(tr().bombNone); return; }
    wrong.forEach(boomAt);
    board.classList.remove('shake'); void board.offsetWidth; board.classList.add('shake');
    // Zahlen verschwinden mitten im Blitz
    setTimeout(() => {
      for (const i of wrong) { S.values[i] = 0; S.notes[i] = 0; }
      S.history = []; // Rückgängig soll die gesprengten Fehler nicht zurückholen
      render(); save(); toast(tr().bombHit(wrong.length));
    }, reduceMotion() ? 0 : 160);
    render(); save();
  }

""" + t[end:]
rep("  $('joker').addEventListener('click', joker);", "  $('bomb').addEventListener('click', bomb);")
rep("    if (k === 'j' || k === 'J') { joker(); return; }", "    if (k === 'b' || k === 'B') { bomb(); return; }")

assert "joker" not in t.lower().replace("jokers; delete s.jokercell", ""), "joker leftovers"
open(dst, "w", encoding="utf-8").write(t)
print("ok")
