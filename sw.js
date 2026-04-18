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
  
  // Check domains
  if (AD_DOMAINS.some(domain => url.hostname.includes(domain))) return true;
  
  // Check YouTube ad endpoints
  if (url.hostname.includes('youtube.com') || url.hostname.includes('googlevideo.com')) {
    if (YOUTUBE_AD_ENDPOINTS.some(endpoint => urlStr.includes(endpoint))) return true;
  }
  
  // Check for pattern-based ad URLs
  if (/(ad|tracking|stats)/.test(urlStr) && 
      (urlStr.includes('google') || urlStr.includes('doubleclick') || urlStr.includes('youtube'))) {
    return true;
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

  // Skip external requests — always go to network
  if (
    url.hostname.includes('youtube.com') ||
    url.hostname.includes('googleapis.com') ||
    url.hostname.includes('googleusercontent.com') ||
    url.hostname.includes('gstatic.com') ||
    url.hostname.includes('googlevideo.com') ||
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
