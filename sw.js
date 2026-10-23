const CACHE_NAME = 'flavify-v2';
const SHELL_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon-192.svg',
  './icons/icon-512.svg'
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

// AD BLOCKING LISTS
const AD_DOMAINS = [
  'doubleclick.net', 'googlesyndication.com', 'adservice.google.com',
  'pagead2.googlesyndication.com', 'ads.google.com', 'googleadservices.com',
  'adsdrive.com', 'moat.com', 'analytics.google.com', 'googletagmanager.com',
  'facebook.com', 'connect.facebook.net', 'platform.twitter.com',
  'ads.linkedin.com', 'bidder.criteo.com', 'akamaized.net'
];

const YOUTUBE_AD_ENDPOINTS = [
  '/get_ad_break', '/get_ads', '/api/stats/ads', '/api/stats/watchtime',
  '/youtubei', '/get_watch_next', '/ptracking', '/api/stats/',
  '/gen_204', '/pagead/', '/vast', '/adserving'
];

// Check if URL is an ad request
function isAdRequest(url) {
  const urlStr = url.toString();
  const host = url.hostname;

  // Check domains — exact host or a real subdomain, never a name that merely
  // contains the word (searching "adore" must not be treated as an ad).
  if (AD_DOMAINS.some(domain => host === domain || host.endsWith('.' + domain))) return true;

  // Check YouTube ad endpoints (path only, so query text is ignored)
  if (host === 'youtube.com' || host.endsWith('.youtube.com') || host === 'googlevideo.com' || host.endsWith('.googlevideo.com')) {
    const path = url.pathname;
    if (YOUTUBE_AD_ENDPOINTS.some(endpoint => path.startsWith(endpoint))) return true;
  }

  return false;
}

// Fetch — network-first for API calls, cache-first for app shell
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // BLOCK ADS — return empty response for ad requests
  if (isAdRequest(url)) {
    e.respondWith(new Response('', { status: 204 }));
    return;
  }

  // Never cache or intercept search/metadata calls, and skip external hosts
  if (
    url.hostname.includes('youtube.com') ||
    url.hostname.includes('googleapis.com') ||
    url.hostname.includes('googleusercontent.com') ||
    url.hostname.includes('gstatic.com') ||
    url.hostname.includes('googlevideo.com') ||
    url.hostname.includes('ytimg.com') ||
    url.hostname.includes('ggpht.com') ||
    url.pathname.startsWith('/api/') ||
    url.search.includes('filter=videos') ||
    e.request.method !== 'GET'
  ) {
    return;
  }

  // Cache-first for app shell assets
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(response => {
        if (!response || response.status !== 200) return response;
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(e.request, clone));
        return response;
      });
    }).catch(() => {
      if (e.request.mode === 'navigate') {
        return caches.match('./index.html');
      }
    })
  );
});
