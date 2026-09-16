/* Trial Recall service worker - build 4181f15fc7
   Cache-first so the deck opens instantly and works with no connection, with a
   background refresh so a sync reaches you on the next launch. */
var CACHE = "trial-recall-4181f15fc7";
var SHELL = ["./", "index.html", "trials.json", "manifest.webmanifest",
             "icon-180.png", "icon-192.png", "icon-512.png"];

self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) {
    return c.addAll(SHELL);
  }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.map(function (k) {
      if (k !== CACHE) return caches.delete(k);
    }));
  }).then(function () { return self.clients.claim(); }));
});

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;
  e.respondWith(caches.match(req).then(function (hit) {
    var net = fetch(req).then(function (res) {
      if (res && res.status === 200 && (res.type === "basic" || res.type === "cors")) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
      }
      return res;
    }).catch(function () { return hit; });
    return hit || net;          /* cached wins for speed; network refills behind it */
  }));
});
