/* jshint esversion: 6 */
document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('messageModal')) {
        let myModal = new bootstrap.Modal(document.getElementById('messageModal'), {
            keyboard: false
        });
        myModal.show();
    }
});


document.addEventListener('DOMContentLoaded', function () {
    let contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent default form submission

            let form = this;
            let formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
                },
            }).then(response => response.json())
              .then(data => {
                  if (data.success) {
                      // Show the success modal
                      var successModal = new bootstrap.Modal(document.getElementById('successModal'));
                      successModal.show();
                      form.reset(); // Reset the form
                  } else {
                      // Handle errors
                      console.error('Form submission failed.');
                  }
              })
              .catch(error => {
                  console.error('Error:', error);
              });
        });
    }
});
