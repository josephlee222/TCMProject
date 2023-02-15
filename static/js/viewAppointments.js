function showDeleteModal(name, link) {
    document.getElementById("delete-treatment-text").innerHTML = "Delete appointment '" + decodeURIComponent(name) + "'?"
    document.getElementById("delete-treatment-link").href = link
    var deleteModel = new bootstrap.Modal(document.getElementById("deleteModal"), {});

    deleteModel.show()
}

document.addEventListener('DOMContentLoaded', function () {
    console.log(appointments)
    var appointmentCalendar = document.getElementById('calendar')
    var events = []
    function makeEvents(item, index) {
        events.push({
            title: item.name,
            description: item.notes,
            start: item.startTime,
            end: item.endTime,
            url: "/admin/appointments/details/" + item.id
        })
    }

    appointments.forEach(makeEvents)
    console.log(events)
    var calendar = new FullCalendar.Calendar(appointmentCalendar, {
        initialView: 'listWeek',
        nowIndicator: true,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
        },
        events: events
    });
    calendar.render()
})