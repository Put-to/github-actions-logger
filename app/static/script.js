function fetchEvents() {
    $.get('/webhook/latest_events', function(events) {
        let eventDisplay = '';
        events.forEach(function(event) {
            eventDisplay += `<p class="event">${event}</p>`;
        });
        $('#events').html(eventDisplay);
    });
}
setInterval(fetchEvents, 15000);
window.onload = fetchEvents;
