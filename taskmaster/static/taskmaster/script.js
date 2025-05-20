$(document).ready(function () {
  // Retrieve CSRF token from the page for AJAX requests.
  var csrfToken = $('[name="csrfmiddlewaretoken"]').val();

  // Display global message toast if a message is available.
  if (typeof globalMessage !== "undefined") {
    if (typeof success !== "undefined") {
      showToast(globalMessage, success, 3000);
    } else if (typeof error !== "undefined") {
      showToast(globalMessage, error, 3000);
    }
  }

  // Toggle password visibility for password input fields.
  var togglePassword = $(".password-toggle");
  if (togglePassword.length > 0) {
    togglePassword.click(function () {
      var targetId = $(this).data("target");
      var passwordField = $("#" + targetId);
      var passwordFieldType = passwordField.attr("type");
      if (passwordFieldType === "password") {
        passwordField.attr("type", "text");
        $(this).removeClass("uil-eye-slash").addClass("uil-eye");
      } else {
        passwordField.attr("type", "password");
        $(this).removeClass("uil-eye").addClass("uil-eye-slash");
      }
    });
  }

  // Toggle between registration and login forms based on user selection.
  const regLog = $("#reg-log");
  const registerForm = $("#register-form");
  const loginForm = $("#login-form");
  if (regLog.length > 0) {
    toggleForm(regLog, registerForm, loginForm, csrfToken);
    regLog.change(function () {
      toggleForm(regLog, registerForm, loginForm, csrfToken);
    });
  }

  // Event delegation for "See More" and "See Less" buttons in task descriptions.
  $(document).on("click", ".see-more", function (e) {
    e.preventDefault();
    var $taskDesc = $(this).closest(".task-description");
    $taskDesc.find(".truncated-text").hide();
    $taskDesc.find(".full-text").show();
    $taskDesc.find(".see-more").hide();
    $taskDesc.find(".see-less").show();
  });

  $(document).on("click", ".see-less", function (e) {
    e.preventDefault();
    var $taskDesc = $(this).closest(".task-description");
    $taskDesc.find(".truncated-text").show();
    $taskDesc.find(".full-text").hide();
    $taskDesc.find(".see-more").show();
    $taskDesc.find(".see-less").hide();
  });
});

/**
 * Function to toggle between login and register forms.
 *
 * @param {jQuery} regLog - The jQuery object representing the radio button to toggle forms.
 * @param {jQuery} registerForm - The jQuery object representing the register form container.
 * @param {jQuery} loginForm - The jQuery object representing the login form container.
 * @param {string} csrfToken - The CSRF token value.
 */
function toggleForm(regLog, registerForm, loginForm, csrfToken) {
  // Initialize the register and login forms.
  registerFormObject = initializeRegisterForm(registerForm, csrfToken);
  loginFormObject = initializeLoginForm(loginForm);

  // Check the radio button value to determine which form to display.
  if (regLog.is(":checked")) {
    // User wants to register, hide the login form if it exists.
    if (loginFormObject) {
      loginFormObject.remove();
    }
    // Initialize or re-initialize the register form and show it.
    registerFormObject = initializeRegisterForm(registerForm, csrfToken);
    initializeRegisterForm(registerForm, csrfToken);
  } else {
    // User wants to login, hide the register form if it exists.
    if (registerFormObject) {
      registerFormObject.remove();
    }
    // Initialize or re-initialize the login form and show it.
    loginFormObject = initializeLoginForm(loginForm);
    initializeLoginForm(loginForm);
  }
}

/**
 * Initialize the registration form and set up form validation and event handling.
 * @param {object} registerForm - jQuery object representing the registration form.
 * @param {string} csrfToken - Cross-Site Request Forgery token for form submission.
 * @returns {object} An object with a remove() method to clean up event handlers.
 */
function initializeRegisterForm(registerForm, csrfToken) {
  // Initialize form validation rules
  registerForm.validate({
    rules: {
      fullname: {
        required: true,
        lettersOnly: true,
      },
      username: {
        required: true,
        remote: {
          url: "/check_username_availability/",
          type: "post",
          data: {
            csrfmiddlewaretoken: csrfToken,
            username: function () {
              return $("#id_username2").val();
            },
          },
          beforeSend: function () {
            // Display loading message or spinner
            $("#id_username2")
              .siblings(".invalid-feedback")
              .text("Checking availability...");
          },
          dataFilter: function (response) {
            // Parse the JSON response
            var data = JSON.parse(response);
            if (data.is_available) {
              // Return true if username is available
              return "true";
            } else {
              // Return false if username is not available
              return "false";
            }
          },
        },
      },
      password1: {
        required: true,
        minlength: 8,
        uppercase: true,
        lowercase: true,
        digit: true,
        symbol: true,
      },
      password2: {
        required: true,
        equalTo: "#id_password1",
      },
    },
    messages: {
      fullname: {
        required: "Please enter your full name",
        lettersOnly: "Full name should only contain alphabetic characters",
      },
      username: {
        required: "Please enter your username",
        remote: "This username is already taken",
      },
      password1: {
        required: "Please enter your password",
        minlength: "Password must be at least 8 characters long",
      },
      password2: {
        required: "Please confirm your password",
        equalTo: "Passwords do not match",
      },
    },
    errorElement: "div",
    errorPlacement: function (error, element) {
      error.addClass(
        "invalid-feedback position-absolute pe-3 top-0 start-100 text-start"
      );
      error.insertAfter(element);
      error.hide();
      errorMessageShow(element);
    },
    highlight: function (element) {
      $(element).addClass("is-invalid");
      errorMessageShow($(element));
    },
    unhighlight: function (element) {
      $(element).removeClass("is-invalid");
      errorMessageHide($(element));
    },
    submitHandler: function (form) {
      form.submit();
    },
  });

  /**
   * Custom validation methods for password strength.
   */
  $.validator.addMethod(
    "lettersOnly",
    function (value, element) {
      return /^[a-zA-Z\s]+$/.test(value);
    },
    "Please enter only alphabetic characters."
  );

  $.validator.addMethod(
    "uppercase",
    function (value, element) {
      return /^(?=.*[A-Z])/.test(value);
    },
    "Password must contain at least one uppercase letter."
  );

  $.validator.addMethod(
    "lowercase",
    function (value, element) {
      return /^(?=.*[a-z])/.test(value);
    },
    "Password must contain at least one lowercase letter."
  );

  $.validator.addMethod(
    "digit",
    function (value, element) {
      return /^(?=.*\d)/.test(value);
    },
    "Password must contain at least one digit."
  );

  $.validator.addMethod(
    "symbol",
    function (value, element) {
      return /\W/.test(value);
    },
    "Password must contain at least one special character."
  );

  // Re-validate form fields on input
  $("input, textarea").on("input", function () {
    registerForm.validate().element($(this));
  });

  // Handle form submission on Enter key press
  $("input, textarea").on("keydown", function (e) {
    if (e.keyCode === 13) {
      e.preventDefault();
      var currentField = $(this);
      var formFields = $("#register-form .form-style");
      var currentIndex = formFields.index(currentField);
      if (currentIndex === formFields.length - 1) {
        // Submit the form if it's the last field
        if (registerForm.validate().form()) {
          registerForm.submit();
        }
      } else {
        // Move focus to the next field
        if (registerForm.validate().element($(this))) {
          var nextField = formFields.eq(currentIndex + 1);
          nextField.focus();
        }
      }
    }
  });

  return {
    remove: function () {
      // Remove or disable additional functions/methods inside initializeRegisterForm
      $("input, textarea").off("focus input blur keydown");
    },
  };
}

/**
 * Initialize the login form and set up form validation and event handling.
 *
 * @param {jQuery} loginForm - jQuery object representing the login form.
 * @returns {Object} An object with a `remove` method to clean up event handlers.
 */
function initializeLoginForm(loginForm) {
  // Initialize form validation rules
  loginForm.validate({
    rules: {
      username: {
        required: true,
      },
      password: {
        required: true,
      },
    },
    messages: {
      username: {
        required: "Please enter your username",
      },
      password: {
        required: "Please enter your password",
      },
    },
    errorElement: "div",
    errorPlacement: function (error, element) {
      error.addClass(
        "invalid-feedback position-absolute pe-3 top-0 start-100 text-start"
      );
      error.insertAfter(element);
      error.hide();
      errorMessageShow(element);
    },
    highlight: function (element) {
      $(element).addClass("is-invalid");
      errorMessageShow($(element));
    },
    unhighlight: function (element) {
      $(element).removeClass("is-invalid");
      errorMessageHide($(element));
    },
    submitHandler: function (form) {
      form.submit();
    },
  });

  // Re-validate form fields on input
  $("input, textarea").on("input", function () {
    loginForm.validate().element($(this));
  });

  // Handle form submission on Enter key press
  $("input, textarea").on("keydown", function (e) {
    if (e.keyCode === 13) {
      e.preventDefault();
      var currentField = $(this);
      var formFields = $("#login-form .form-style");
      var currentIndex = formFields.index(currentField);
      if (currentIndex === formFields.length - 1) {
        // Submit the form if it's the last field
        if (loginForm.validate().form()) {
          loginForm.submit();
        }
      } else {
        // Move focus to the next field
        if (loginForm.validate().element($(this))) {
          var nextField = formFields.eq(currentIndex + 1);
          nextField.focus();
        }
      }
    }
  });

  return {
    remove: function () {
      // Remove or disable additional functions/methods inside initializeRegisterForm
      $("input, textarea").off("focus input blur keydown");
      loginForm.off("validate");
    },
  };
}

/**
 * Show error message tooltip with smooth animation.
 *
 * @param {jQuery} input - The jQuery object representing the input element to show the error message for.
 */
function errorMessageShow(input) {
  // Add the 'show' class and slide down the error message with smooth animation.
  input.siblings(".invalid-feedback").addClass("show").slideDown(200);
}

/**
 * Hide error message tooltip with smooth animation.
 *
 * @param {jQuery} input - The jQuery object representing the input element to show the error message for.
 */
function errorMessageHide(input) {
  // Remove the 'show' class and slide up the error message with smooth animation.
  input.siblings(".invalid-feedback").removeClass("show").slideUp(200);
}

/**
 * Convert 24-hour time format to 12-hour format with "a.m." or "p.m."
 * @param {string} timeString - The time string in 24-hour format (e.g., "14:30")
 * @returns {string} The time string in 12-hour format with "a.m." or "p.m." (e.g., "2:30 p.m.")
 */
function convertTo12HourFormat(timeString) {
  // Split the time string into hours and minutes
  const time = timeString.split(":");
  let hour = parseInt(time[0]);
  const minute = time[1];

  // Determine the period (a.m. or p.m.) based on the hour
  const period = hour >= 12 ? "p.m." : "a.m.";

  // Convert hour to 12-hour format
  if (hour === 0) {
    hour = 12; // Midnight is 12 a.m.
  } else if (hour > 12) {
    hour -= 12; // Convert afternoon hours to 12-hour format
  }

  // Return the time in 12-hour format with the period
  return `${hour}:${minute} ${period}`;
}

/**
 * Update the task completion badge content dynamically based on the DataTable.
 *
 * @param {DataTable} dataTable - The DataTable instance containing the task list.
 */
function updateBadge(dataTable) {
  // Update the completed_tasks and total_tasks values
  const completedTasks = dataTable.rows(".completed").count();
  const totalTasks = dataTable.rows().count();

  // Update the badge content dynamically
  const badgeContainer = $("#taskCompletionBadge");
  badgeContainer.empty();

  // Check if all tasks are completed
  if (completedTasks === totalTasks && totalTasks !== 0) {
    badgeContainer.append(
      `<span class="badge rounded-pill bg-light complete-all-task">(${completedTasks}/${totalTasks})<i class="uil uil-check-circle check-icon"></i></span>`
    );
  }

  // Check if some tasks are not completed
  else if (completedTasks !== totalTasks && totalTasks !== 0) {
    badgeContainer.append(
      `<span class="badge rounded-pill bg-light not-completed">(${completedTasks}/${totalTasks})<i class="uil uil-times-circle cross-icon"></i></span>`
    );
  }
}

/**
 * Updates the number column in the DataTable to show sequential numbers for the tasks.
 * @param {Object} dataTable - The DataTable instance for the task table.
 */
function updateNumberColumn(dataTable) {
  // Get the current page number and number of rows per page from the DataTable API.
  const currentPage = dataTable.page.info().page + 1;
  const rowsPerPage = dataTable.page.info().length;

  // Calculate the starting number for the tasks on the current page.
  const startNumber = (currentPage - 1) * rowsPerPage + 1;

  // Update the number column for each task row.
  $(".task-num").each(function (index) {
    // Set the sequential number for each task row based on its index and the starting number.
    $(this).text(startNumber + index);
  });
}

/**
 * Reloads the DataTable with the saved page number.
 *
 * @param {object} dataTable - The DataTable object to reload.
 * @param {number} pageNumber - The page number to restore.
 */
function reloadDataTable(dataTable, pageNumber) {
  // Use dataTable.page() method to set the page number (0-based index)
  // We subtract 1 from the pageNumber to convert it to the 0-based index
  // Use dataTable.draw(false) to redraw the DataTable without reloading the data
  dataTable.page(pageNumber - 1).draw(false);
}

/**
 * Function to handle the deletion of a task.
 *
 * @param {DataTable} dataTable - The DataTable instance used to display the tasks.
 */
function deleteTaskHandler(dataTable) {
  // Event listener for the delete task button click
  $(document).on("click", ".delete-task", function () {
    const taskID = $(this).data("task-id");
    const modalID = $(`#deleteTaskModal`);
    const row = $(this).closest("tr");
    const taskTitle = $(`#${taskID} td:eq(1)`).text();
    const deleteConfirm = $(".delete-confirm");
    deleteConfirm.text(`Are you sure you want to delete task ${taskTitle} ?`);
    modalID.modal("show");

    // Store the task ID and row as data attributes on the delete form
    const deleteTaskForm = $("#deleteTaskForm");
    deleteTaskForm.data("task-id", taskID);
    deleteTaskForm.data("task-row", row);
  });

  // Event listener for the delete task form submission
  $(document).on("submit", "#deleteTaskForm", function (e) {
    e.preventDefault();
    const deleteTaskForm = $(this);
    const taskID = deleteTaskForm.data("task-id");
    const taskTitle = $(`#${taskID} td:eq(1)`).text();
    const row = deleteTaskForm.data("task-row");
    // Save the current page number
    pageNumber = dataTable.page.info().page + 1;

    $.ajax({
      type: "DELETE",
      url: `/api/tasks/${taskID}/`,
      data: {},
      contentType: "application/json",
      success: function (data) {
        // Handle success response
        showToast(
          `Task <b>${taskTitle}</b> has been deleted.`,
          "success",
          3000
        );

        // Remove the corresponding row from the DataTable
        dataTable.row(row).remove().draw(false);

        // Update the badge
        updateBadge(dataTable);

        // Reload the DataTable with the saved page number
        reloadDataTable(dataTable, pageNumber);

        // Update the number column
        updateNumberColumn(dataTable);

        // Close the delete task modal
        $(`#deleteTaskModal`).modal("hide");
      },
      error: function (xhr, status, error) {
        // Handle error response
        if (xhr.status == 400) {
          showToast("Something went wrong.", "error", 3000);
        } else if (xhr.status == 401) {
          showToast(
            "You are not authenticated. Please login first.",
            "error",
            3000
          );
        } else if (xhr.status == 403) {
          showToast("You are unauthorized to delete this task.", "error", 3000);
        } else if (xhr.status == 404) {
          showToast("Task is not found.", "error", 3000);
        } else {
          showToast(
            "An error occurred. Please try again later.",
            "error",
            3000
          );
        }
      },
    });
  });
}

/**
 * Function to handle completing a Task via AJAX request.
 * @param {DataTable} dataTable - The DataTable instance used to display tasks.
 */
function completeTaskHandler(dataTable) {
  /**
   * Event handler for clicking the "Complete" button on a task.
   * @param {Event} e - The click event.
   */
  $(document).on("click", ".complete-task", function (e) {
    e.preventDefault();
    const taskId = $(this).data("task-id");
    const completeTaskForm = $("#completeTaskForm");

    // Store the task ID in the form's data attribute for later use during submission.
    completeTaskForm.data("task-id", taskId);

    // Submit the hidden form to trigger the completion process.
    completeTaskForm.submit();
  });

  /**
   * Event handler for submitting the hidden form to complete a task.
   * @param {Event} e - The form submission event.
   */
  $(document).on("submit", "#completeTaskForm", function (e) {
    e.preventDefault();
    const taskId = $(this).data("task-id");

    $.ajax({
      type: "POST",
      url: `/api/tasks/${taskId}/complete/`,
      success: function (data) {
        // Handle success response
        const row = $(`#${taskId}`);
        const completeButton = row.find(".complete-task");
        if (data.completed) {
          showToast(
            `Task <b>${data.title}</b> has been completed.`,
            "success",
            3000
          );
          row.addClass("completed");
          completeButton.addClass("complete-button");
          completeButton.text("uncomplete");
        } else {
          row.removeClass("completed");
          completeButton.removeClass("complete-button");
          completeButton.text("complete");
        }

        // Update the badge showing the number of completed tasks in the DataTable.
        updateBadge(dataTable);
      },
      error: function (xhr, status, error) {
        if (xhr.status == 400) {
          showToast("Something went wrong.", "error", 3000);
        } else if (xhr.status == 401) {
          showToast(
            "You are not authenticated. Please login first.",
            "error",
            3000
          );
        } else if (xhr.status == 403) {
          showToast(
            "You are unauthorized to complete this task.",
            "error",
            3000
          );
        } else if (xhr.status == 404) {
          showToast("Task is not found.", "error", 3000);
        } else {
          showToast(
            "An error occurred. Please try again later.",
            "error",
            3000
          );
        }
      },
    });
  });
}

/**
 * Populates the edit modal with task data.
 *
 * @param {object} task - The task object containing data to populate the edit modal.
 */
function populateEditModal(task) {
  // Get the ID of the edit modal
  const modalID = `#editTaskModal`;

  // Get the editTaskForm within the edit modal
  const form = $(`${modalID} .editTaskForm`);

  // Populate the fields with tasks data and remove any invalid class
  form.find("#id_title_edit").val(task.title).removeClass("is-invalid");
  form
    .find("#id_description_edit")
    .val(task.description)
    .removeClass("is-invalid");
  form
    .find("#id_execution_time_edit")
    .val(task.execution_time)
    .removeClass("is-invalid");
  form
    .find("#id_execution_day_edit")
    .val(task.execution_day)
    .removeClass("is-invalid");
  form
    .find("#id_execution_date_edit")
    .val(task.execution_date)
    .removeClass("is-invalid");

  // Trigger the change event to update the select2 dropdown
  form.find("#id_execution_day_edit").trigger("change");
  form.find("#id_execution_date_edit").trigger("change");

  // Remove the invalid-feedback elements
  form.find(".invalid-feedback").remove();
}

// Function to handle edit task
function editTaskHandler() {
  /**
   * Function to handle the form submission for editing a task.
   */
  $(document).on("submit", "#editTaskForm", function (event) {
    event.preventDefault();
    const taskId = $(this).data("task-id");
    const formData = $(this).serializeArray();
    const newData = {};
    const userID = $(this).data("user-id");

    // Convert the form data into an object
    formData.forEach((field) => {
      newData[field.name] = field.value;
    });

    // Add the user ID to the data
    newData.user = userID;

    $.ajax({
      type: "PUT",
      url: `/api/tasks/${taskId}/`,
      data: JSON.stringify(newData),
      contentType: "application/json",
      success: function (data, status, xhr) {
        // Handle success response
        showToast(
          `Task <b>${data.title}</b> has been edited successfully.`,
          "success",
          3000
        );

        // Update the corresponding row in the DataTable based on the task type
        const row = $(`#${taskId}`);
        if (data.daily) {
          row.find(".task-title").text(data.title);
          row
            .find(".task-execution-time")
            .text(convertTo12HourFormat(data.execution_time));
          row
            .find(".task-description .truncated-text")
            .text(data.description.substring(0, 100));
          row.find(".task-description .full-text").text(data.description);
        } else if (data.weekly) {
          row.find(".task-title").text(data.title);
          row
            .find(".task-description .truncated-text")
            .text(data.description.substring(0, 100));
          row.find(".task-description .full-text").text(data.description);
          row
            .find(".task-execution-time")
            .text(
              `${data.execution_day}, ${convertTo12HourFormat(
                data.execution_time
              )}`
            );
        } else if (data.monthly) {
          row.find(".task-title").text(data.title);
          row
            .find(".task-description .truncated-text")
            .text(data.description.substring(0, 100));
          row.find(".task-description .full-text").text(data.description);
          row
            .find(".task-execution-time")
            .text(
              `Day ${data.execution_date}, ${convertTo12HourFormat(
                data.execution_time
              )}`
            );
        }

        // Create and insert "See More" and "See Less" links if they don't exist
        if (data.description.length > 100) {
          row
            .find(".task-description .truncated-text")
            .text(data.description.substring(0, 100) + "...");
          if (!row.find(".see-more").length) {
            row
              .find(".task-description")
              .append(
                '<a href="#" class="see-more text-decoration-none">See More</a>'
              );
          }
          if (!row.find(".see-less").length) {
            row
              .find(".task-description")
              .append(
                '<a href="#" class="see-less text-decoration-none" style="display: none;">Less</a>'
              );
          }
        }

        // Show/hide "See More" and "See Less" links based on description length
        if (data.description.length > 100) {
          row.find(".see-more").show();
          row.find(".see-less").hide();
        } else {
          row.find(".see-more").hide();
          row.find(".see-less").hide();
        }

        // Close the modal after editing the task
        $(`#editTaskModal`).modal("hide");
      },
      error: function (xhr, status, error) {
        // Handle error responses based on status codes
        if (xhr.status == 400) {
          showToast("Please fill all the field.", "error", 3000);
          const errors = xhr.responseJSON;
          for (const fieldName in errors) {
            const fieldError = errors[fieldName][0];
            const fieldInput = $(`#editTaskForm #id_${fieldName}_edit`);
            let fieldFeedback = fieldInput.siblings(".invalid-feedback");
            if (fieldFeedback.length === 0) {
              // Create the invalid-feedback element if it doesn't exist
              fieldFeedback = $('<div class="invalid-feedback"></div>');
              fieldInput.after(fieldFeedback);
            }
            fieldInput.addClass("is-invalid");
            fieldFeedback.text(fieldError);
          }
        } else if (xhr.status == 401) {
          showToast(
            "You are not authenticated. Please login first.",
            "error",
            3000
          );
        } else if (xhr.status == 403) {
          showToast("You are unauthorized to edit this task.", "error", 3000);
        } else if (xhr.status == 404) {
          showToast("Task is not found.", "error", 3000);
        } else {
          showToast(
            "An error occurred. Please try again later.",
            "error",
            3000
          );
        }
      },
    });
  });

  /**
   * Event listener for the edit task button click.
   * Fetches the task data from the API and populates the edit modal.
   */
  $(document).on("click", ".edit-task", function () {
    const taskID = $(this).closest("tr").data("id");
    const modalID = $(`#editTaskModal`);
    const editTaskForm = $("#editTaskForm");

    editTaskForm.data("task-id", taskID);

    $.ajax({
      type: "GET",
      url: `/api/tasks/${taskID}/`, // Adjust the URL as per your API endpoint
      success: function (data) {
        // Populate the edit modal with the task data
        populateEditModal(data);

        // Show the edit modal
        modalID.modal("show");
      },
      error: function (xhr, status, error) {
        // Handle error response
        // Display an error message or perform other actions
        showToast("An error occurred. Please try again later.", "error", 3000);
      },
    });
  });
}

/**
 * Function to handle adding a new task through AJAX.
 * @param {object} dataTable - The DataTable instance representing the task list table.
 */
function addTaskHandler(dataTable) {
  $("#addTaskForm").on("submit", function (event) {
    event.preventDefault();

    // Serialize form data and convert it to a dictionary
    const formData = $(this).serializeArray();
    const newData = {};
    const userID = $(this).data("user-id");
    const form = $("#addTaskForm");
    const select = $("#addTaskForm .select2");
    formData.forEach((field) => {
      newData[field.name] = field.value;
    });

    // Set the user field to the current user ID
    newData.user = userID;
    $.ajax({
      type: "POST",
      url: `/api/tasks/`,
      data: JSON.stringify(newData),
      contentType: "application/json",
      success: function (data, status, xhr) {
        // Handle success response
        showToast(
          `Task <b>${data.title}</b> has been added successfully.`,
          "success",
          3000
        );

        // Add the new task to the DataTable based on its type (daily, weekly, monthly)
        const taskData = {
          id: data.id,
          title: data.title,
          description: data.description,
          created_at: data.created_at,
          execution_time: data.execution_time,
          completed: false,
        };
        if (data.daily) {
          dataTable.row.add(taskData).draw(false);
        } else if (data.weekly) {
          taskData["execution_day"] = data.execution_day;
          dataTable.row.add(taskData).draw(false);
        } else if (data.monthly) {
          taskData["execution_date"] = data.execution_date;
          dataTable.row.add(taskData).draw(false);
        }

        // Get the last page and reload DataTable
        pageNumber = dataTable.page.info().pages;
        reloadDataTable(dataTable, pageNumber);

        // Update badge for task counts
        updateBadge(dataTable);

        // Close the modal
        $("#addTaskModal").modal("hide");

        // Reset the form and Select2 dropdown
        form[0].reset();
        select.val(null).trigger("change");

        // Remove the invalid-feedback elements and class is-invalid
        form.find(".invalid-feedback").remove();
        form.find(".is-invalid").removeClass("is-invalid");
      },
      error: function (xhr, status, error) {
        // Handle different error responses
        if (xhr.status == 400) {
          showToast("Please fill all the field.", "error", 3000);
          const errors = xhr.responseJSON;
          for (const fieldName in errors) {
            const fieldError = errors[fieldName][0];
            const fieldInput = $(`#addTaskForm #id_${fieldName}`);
            let fieldFeedback = fieldInput.siblings(".invalid-feedback");
            if (fieldFeedback.length === 0) {
              // Create the invalid-feedback element if it doesn't exist
              fieldFeedback = $('<div class="invalid-feedback"></div>');
              fieldInput.after(fieldFeedback);
            }
            fieldInput.addClass("is-invalid");
            fieldFeedback.text(fieldError);
          }
        } else if (xhr.status == 401) {
          showToast(
            "You are not authenticated. Please login first.",
            "error",
            3000
          );
        } else if (xhr.status == 403) {
          showToast("You are unauthorized to edit this task.", "error", 3000);
        } else if (xhr.status == 404) {
          showToast("Task is not found.", "error", 3000);
        } else {
          showToast(
            "An error occurred. Please try again later.",
            "error",
            3000
          );
        }
      },
    });
  });
}

/**
 * Initialize Select2 plugin for a given modal element.
 *
 * @param {string} modalId - The ID of the modal element.
 */
function initializeSelect2(modalId) {
  var select = $("#" + modalId + " .select2");
  if (select.length > 0) {
    select.select2({
      // Initialize Select2 with dropdownParent set to the modal element and initial width as 100%.
      dropdownParent: $("#" + modalId),
      width: "100%",
    });

    // Handle the 'select2:select' event to disable the empty option when a value is selected.
    select.on("select2:select", function (e) {
      var value = e.target.value;
      if (value !== "") {
        $('option[value=""]').prop("disabled", true);
      }
    });

    // Calculate and set the maximum width for the select options
    var maxWidth = 0;
    select.find("option").each(function () {
      var optionWidth = $(this).text().length;
      if (optionWidth > maxWidth) {
        maxWidth = optionWidth;
      }
    });

    // Set the width of the dropdown to the calculated maximum width
    select.select2("destroy"); // Destroy the initial Select2 instance
    select.select2({
      dropdownParent: $("#" + modalId), // Set the dropdownParent to the modal element
      width: maxWidth * 12 + "px", // Set the width based on the maximum width of options
    });

    // Handle the 'select2:select' event again after reinitializing to disable the empty option.
    select.on("select2:select", function (e) {
      var value = e.target.value;
      if (value !== "") {
        $('option[value=""]').prop("disabled", true);
      }
    });
  }
}

/**
 * Function to handle custom day sorting for DataTables.
 *
 * This function adds a custom sorting method for the 'custom-datetime' type in DataTables.
 * The 'custom-datetime' type represents date and time values in a custom format.
 *
 * @param {string[]} customDayOrder - An array containing the custom day order for sorting.
 *                                   It should contain the day names in the desired sorting order.
 *                                   Example: ['Monday', 'Tuesday', ...]
 */
function customDaySorting(customDayOrder) {
  /**
   * Custom sorting method for 'custom-datetime' type.
   *
   * This function is used to convert the 'custom-datetime' value to a sortable numeric value.
   * It separates the date and time parts, then calculates a numeric value based on the custom day order
   * and the time in the 'hh:mm A' format using the moment.js library.
   *
   * @param {string} data - The 'custom-datetime' value to be sorted.
   * @returns {number} A numeric value representing the 'custom-datetime' value for sorting.
   */
  $.fn.dataTable.ext.type.order["custom-datetime-pre"] = function (data) {
    // Custom sorting function for 'custom-datetime' type
    const dayAndTime = data.split(" ");
    const datePart = dayAndTime[0];
    const timePart = dayAndTime[1] + " " + dayAndTime[2];
    const dayIndex = customDayOrder.indexOf(datePart);
    return dayIndex * 1000000 + moment(timePart, "hh:mm A").unix();
  };

  /**
   * Custom sorting methods for 'custom-datetime' type in ascending and descending order.
   *
   * These functions compare two 'custom-datetime' values for sorting in ascending and descending order.
   *
   * @param {string} a - The first 'custom-datetime' value to be compared.
   * @param {string} b - The second 'custom-datetime' value to be compared.
   * @returns {number} -1 if a < b, 1 if a > b, or 0 if a and b are equal.
   */
  $.fn.dataTable.ext.type.order["custom-datetime-asc"] = function (a, b) {
    return a < b ? -1 : a > b ? 1 : 0;
  };
  $.fn.dataTable.ext.type.order["custom-datetime-desc"] = function (a, b) {
    return a < b ? 1 : a > b ? -1 : 0;
  };
}

/**
 * Custom Date Sorting Function
 * Adds custom sorting methods for 'custom-datetime' type in DataTables.
 */
function customDateSorting() {
  /**
   * Pre-sorting function for 'custom-datetime' type.
   * Splits the input data into date and time parts, then converts the time part into Unix timestamp for sorting.
   *
   * @param {string} data - The input data to be sorted.
   * @returns {number} - The sorting value calculated based on date and time for 'custom-datetime' type.
   */
  $.fn.dataTable.ext.type.order["custom-datetime-pre"] = function (data) {
    // Custom sorting function for 'custom-datetime' type
    const dayAndTime = data.split(" ");
    const datePart = dayAndTime[1];
    const timePart = dayAndTime[2] + " " + dayAndTime[3];
    const dayIndex = parseInt(datePart, 10);
    return dayIndex * 1000000 + moment(timePart, "hh:mm A").unix();
  };

  /**
   * Custom sorting methods for 'custom-datetime' type in ascending and descending order.
   *
   * These functions compare two 'custom-datetime' values for sorting in ascending and descending order.
   *
   * @param {string} a - The first 'custom-datetime' value to be compared.
   * @param {string} b - The second 'custom-datetime' value to be compared.
   * @returns {number} -1 if a < b, 1 if a > b, or 0 if a and b are equal.
   */
  $.fn.dataTable.ext.type.order["custom-datetime-asc"] = function (a, b) {
    return a < b ? -1 : a > b ? 1 : 0;
  };
  $.fn.dataTable.ext.type.order["custom-datetime-desc"] = function (a, b) {
    return a < b ? 1 : a > b ? -1 : 0;
  };
}
