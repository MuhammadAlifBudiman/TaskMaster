// Display a basic alert
function showAlert(info) {
  Swal.fire({
  icon: 'success',
  title: info,
  showConfirmButton: false,
  timer: 1500
})
}

// Display a toast notification
function showToast(title, icon) {
  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true
  });

  Toast.fire({
    icon: icon,
    title: title
  });
}