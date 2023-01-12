function showDeleteModal(name, link) {
    document.getElementById("delete-treatment-text").innerHTML = "Delete appointment '" + name + "'?"
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
            start: item.datetime,
            url: "/admin/appointments/details/" + item.id
        })
    }

    appointments.forEach(makeEvents)
    console.log(events)
    var calendar = new FullCalendar.Calendar(appointmentCalendar, {
        initialView: 'listWeek',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
        },
        events: events
    });
    calendar.render()
})