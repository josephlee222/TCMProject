const PRECACHE = 'precache-v1';
const RUNTIME = '/';

// A list of local resources we always want to be cached.
const PRECACHE_URLS = [
    './static', // Alias for index.html
    'main.js',
];

// The install handler takes care of precaching the resources we always need.
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(PRECACHE)
            .then(cache => cache.addAll(PRECACHE_URLS))
            .then(self.skipWaiting())
    );
});

// The activate handler takes care of cleaning up old caches.
self.addEventListener('activate', event => {
    const currentCaches = [PRECACHE, RUNTIME];
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return cacheNames.filter(cacheName => !currentCaches.includes(cacheName));
        }).then(cachesToDelete => {
            return Promise.all(cachesToDelete.map(cacheToDelete => {
                return caches.delete(cacheToDelete);
            }));
        }).then(() => self.clients.claim())
    );
});

// The fetch handler serves responses for same-origin resources from a cache.
// If no response is found, it populates the runtime cache with the response
// from the network before returning it to the page.
self.addEventListener('fetch', function (event) {
    event.respondWith(
        fetch(event.request).then(function (response) {
            return caches.open(RUNTIME).then(cache => {
                if (event.request.method === "GET") {
                    return cache.put(event.request, response.clone()).then(() => {
                        return response;
                    });
                } else {
                    return response
                }
            })
        }).catch(function () {
            return caches.match(event.request)
        })
    )
})