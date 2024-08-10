document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('messageModal')) {
        var myModal = new bootstrap.Modal(document.getElementById('messageModal'), {
            keyboard: false
        });
        myModal.show();
    }
});

