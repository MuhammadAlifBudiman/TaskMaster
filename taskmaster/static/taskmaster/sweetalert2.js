/**
 * Display a basic alert using SweetAlert2.
 * @param {string} info - The message to display in the alert.
 */
function showAlert(info) {
  Swal.fire({
    icon: "success", // The icon to display in the alert (e.g., success, error, warning).
    title: info, // The title or message to display in the alert.
    showConfirmButton: false, // Hides the confirm button.
    timer: 1500, // Automatically closes the alert after 1500 milliseconds.
  });
}

/**
 * Display a toast notification using SweetAlert2.
 * @param {string} title - The title or message to display in the toast.
 * @param {string} icon - The icon to display in the toast (e.g., success, error, warning).
 * @param {number} timer - The duration (in milliseconds) for which the toast is displayed.
 */
function showToast(title, icon, timer) {
  const Toast = Swal.mixin({
    toast: true, // Enables toast-style notifications.
    position: "top-end", // Positions the toast at the top-right corner of the screen.
    showConfirmButton: false, // Hides the confirm button.
    timer: timer, // Sets the duration for the toast.
    timerProgressBar: true, // Displays a progress bar indicating the remaining time.
  });

  Toast.fire({
    icon: icon, // The icon to display in the toast.
    title: title, // The title or message to display in the toast.
  });
}
