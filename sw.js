const CACHE_NAME = 'flavify-v1';
const SHELL_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png'
];

// Install — cache app shell
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(SHELL_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activate — clean old caches
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// AD BLOCKING — common ad domains to block
const AD_DOMAINS = [
  'doubleclick.net',
  'googlesyndication.com',
  'adservice.google.com',
  'pagead2.googlesyndication.com',
  'ads.google.com',
  'googleadservices.com',
  'adsdrive.com',
  'moat.com',
  'adsensecustomsearchads.com',
  'pagead46.googlesyndication.com',
  'pagead-googlehosted.l.google.com',
  'analytics.google.com',
  'googletagmanager.com',
  'facebook.com/tr',
  'connect.facebook.net',
  'platform.twitter.com',
  'ads.linkedin.com',
  'bidder.criteo.com',
  'ib.adnxs.com',
  'akamaized.net',
  'pubads.g.doubleclick.net',
  'securepubads.g.doubleclick.net',
  'tpc.googlesyndication.com',
  'www-googletagmanager.l.google.com',
  'google-analytics.com',
  'stats.g.doubleclick.net'
];

// Fetch — network-first for API calls, cache-first for app shell
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // BLOCK ADS — return empty response for ad domains
  if (AD_DOMAINS.some(domain => url.hostname.includes(domain))) {
    e.respondWith(new Response('', { status: 204 }));
    return;
  }

  // Skip YouTube API, iframe, and external requests — always go to network
  if (
    url.hostname.includes('youtube.com') ||
    url.hostname.includes('googleapis.com') ||
    url.hostname.includes('googleusercontent.com') ||
    url.hostname.includes('google.com') ||
    url.hostname.includes('gstatic.com') ||
    e.request.method !== 'GET'
  ) {
    return;
  }

  // Cache-first for app shell assets
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(response => {
        // Don't cache non-ok or opaque responses
        if (!response || response.status !== 200) return response;
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
        return response;
      });
    }).catch(() => {
      // Fallback for navigation requests
      if (e.request.mode === 'navigate') {
        return caches.match('./index.html');
      }
    })
  );
});
