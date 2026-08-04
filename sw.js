/* Service worker de l'application Valise.
   Rôle unique : garder l'application accessible sans réseau.
   Changer CACHE à chaque mise à jour de index.html pour forcer le rafraîchissement. */

const CACHE = "valise-v1";
const FILES = ["./", "./index.html", "./sw.js"];

// Mise en cache initiale, puis activation immédiate.
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(FILES))
      .then(() => self.skipWaiting())
  );
});

// Suppression des anciennes versions du cache.
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Réseau d'abord pour récupérer une version à jour, cache en secours hors ligne.
self.addEventListener("fetch", event => {
  if(event.request.method !== "GET") return;
  event.respondWith(
    fetch(event.request)
      .then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(event.request, copy));
        return res;
      })
      .catch(() => caches.match(event.request).then(r => r || caches.match("./index.html")))
  );
});
