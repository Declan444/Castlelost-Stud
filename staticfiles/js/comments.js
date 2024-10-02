/* jshint esversion: 6 */
/* global bootstrap */
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
  //lessonDateInput.addEventListener('change', populateTimeSlots);
  lessonTypeSelect.addEventListener('change', populateTimeSlots);
  instructorSelect.addEventListener('change', populateTimeSlots);

  // Initialize time slots
  populateTimeSlots();
});
const editButtons = document.getElementsByClassName("btn-edit");
const commentText = document.getElementById("id_text");
const commentForm = document.getElementById("commentForm");
const submitButton = document.getElementById("submitButton");
const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("deleteConfirm");


for (let button of editButtons) {
  button.addEventListener("click", (e) => {
    let commentId = e.target.getAttribute("comment_id");
    let commentContent = document.getElementById(`comment${commentId}`).innerText;
    commentText.value = commentContent;
    submitButton.innerText = "Update";
    commentForm.setAttribute("action", `edit_comment/${commentId}`);
    commentText.scrollIntoView({behavior: 'smooth '});
  });
}


for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
      let commentId = e.target.getAttribute("comment_id");
      deleteConfirm.href = `delete_comment/${commentId}`;
      deleteModal.show();
    });
  }