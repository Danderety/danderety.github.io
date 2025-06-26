self.addEventListener('install', function(event) {
  console.log('✅ Service Worker установлен');
  self.skipWaiting();
});

self.addEventListener('activate', function(event) {
  console.log('✅ Service Worker активирован');
});

self.addEventListener('fetch', function(event) {
  // Пока просто пропускаем запросы
});