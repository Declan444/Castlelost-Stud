document.addEventListener('DOMContentLoaded', () => {
    const timeSlotSelect = document.getElementById('timeSlot');
    const lessonDateInput = document.getElementById('lessonDate');
    const lessonTypeSelect = document.getElementById('lessonType');
    const instructorSelect = document.getElementById('instructor');

    // Function to populate time slots
    function populateTimeSlots() {
        const selectedDate = lessonDateInput.value;
        const lessonTypeId = lessonTypeSelect.value;
        const instructorId = instructorSelect.value;

        if (selectedDate && lessonTypeId && instructorId) {
            fetch(`/api/get_available_times/?date=${selectedDate}&lesson_type=${lessonTypeId}&instructor=${instructorId}`)
                .then(response => response.json())
                .then(data => {
                    timeSlotSelect.innerHTML = '';
                    data.time_slots.forEach(slot => {
                        const option = document.createElement('option');
                        option.value = slot.id;
                        option.textContent = `${slot.start_time} - ${slot.end_time}`;
                        timeSlotSelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Error fetching time slots:', error));
        }
    }

    // Event listeners
    lessonDateInput.addEventListener('change', populateTimeSlots);
    lessonTypeSelect.addEventListener('change', populateTimeSlots);
    instructorSelect.addEventListener('change', populateTimeSlots);

    // Initialize time slots
    populateTimeSlots();
});