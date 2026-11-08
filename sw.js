const C = 'kioku-v1';
const CORE = ['./', 'index.html', 'wanakana.min.js', 'manifest.webmanifest', 'icon-192.png', 'apple-touch-icon.png'];
self.addEventListener('install', e => { self.skipWaiting(); e.waitUntil(caches.open(C).then(c => c.addAll(CORE))); });
self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
self.addEventListener('fetch', e => {
  const req = e.request; if (req.method !== 'GET') return;
  const local = new URL(req.url).origin === location.origin;
  if (local) {
    // mạng trước (lấy bản mới nhất), mất mạng thì dùng bản đã lưu
    e.respondWith(fetch(req).then(r => { const cp = r.clone(); caches.open(C).then(c => c.put(req, cp)); return r; })
      .catch(() => caches.match(req).then(r => r || caches.match('index.html'))));
  } else if (/fonts\.(googleapis|gstatic)\.com/.test(req.url)) {
    e.respondWith(caches.match(req).then(r => r || fetch(req).then(res => { const cp = res.clone(); caches.open(C).then(c => c.put(req, cp)); return res; })));
  }
});
