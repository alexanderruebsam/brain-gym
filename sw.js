// Offline-Unterstützung für Brain Gym. Bei jeder Änderung an der App VERSION erhöhen.
const VERSION = 'v13';
const CACHE = `brain-gym-${VERSION}`;
const FILES = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icons/apple-touch-icon.png',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable-512.png',
  './icons/favicon-32.png',
];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k.startsWith('brain-gym-') && k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const isFont = url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com';
  if (url.origin !== location.origin && !isFont) return;

  // Seite: erst Netz (damit Updates ankommen), sonst Cache
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req)
        .then(res => { caches.open(CACHE).then(c => c.put('./index.html', res.clone())); return res; })
        .catch(() => caches.match('./index.html'))
    );
    return;
  }

  // Alles andere (Symbole, Schriften): Cache zuerst, im Hintergrund auffrischen
  event.respondWith(
    caches.match(req).then(hit => {
      const net = fetch(req).then(res => {
        if (res.ok || res.type === 'opaque') caches.open(CACHE).then(c => c.put(req, res.clone()));
        return res;
      }).catch(() => hit);
      return hit || net;
    })
  );
});
