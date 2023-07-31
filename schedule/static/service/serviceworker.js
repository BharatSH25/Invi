self.addEventListener('push', function(event) {
    const payload = event.data ? event.data.text() : 'New notification';
  
    event.waitUntil(
      self.registration.showNotification('Notification Title', {
        body: payload,
      })
    );
  });
  
  self.addEventListener('notificationclick', function(event) {
    event.notification.close();
  
    event.waitUntil(
      clients.openWindow('https://www.example.com')
    );
  });
  