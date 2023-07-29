$(document).ready(function() {
  var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
  if (typeof globalMessage !== 'undefined'){
    if(typeof success !== 'undefined'){
      showToast(globalMessage, success, 3000);
    }else if(typeof error !== 'undefined'){
      showToast(globalMessage, error, 3000);
    }    
  }

  var togglePassword = $('.password-toggle')
  if (togglePassword.length > 0){
    togglePassword.click(function() {
      var targetId = $(this).data('target');
      var passwordField = $('#' + targetId);
      var passwordFieldType = passwordField.attr('type');
      if (passwordFieldType === 'password') {
        passwordField.attr('type', 'text');
        $(this).removeClass('uil-eye-slash').addClass('uil-eye');
      } else {
        passwordField.attr('type', 'password');
        $(this).removeClass('uil-eye').addClass('uil-eye-slash');
      }
    });
  }

  const regLog = $('#reg-log')
  const registerForm = $('#register-form')
  const loginForm = $('#login-form')
  if (regLog.length > 0){
    toggleForm();
    regLog.change(function() {
      toggleForm();
    });

    function toggleForm(){
      registerFormObject = initializeRegisterForm();
      loginFormObject = initializeLoginForm();
      if (regLog.is(":checked")) {
        if (loginFormObject) {
          loginFormObject.remove();
        }
        registerFormObject = initializeRegisterForm();
        initializeRegisterForm();
      } else {
        if (registerFormObject) {
          registerFormObject.remove();
        }
        loginFormObject = initializeLoginForm();
        initializeLoginForm();
      }
    }

    function initializeRegisterForm(){
      // Initialize form validation rules
      registerForm.validate({
        rules: {
          fullname: {
            required: true,
            lettersOnly: true
          },
          username: {
            required: true,
            remote: {
            url: '/check_username_availability/',
            type: 'post',
            data: {
              csrfmiddlewaretoken: csrfToken,
              username: function() {
                return $('#id_username2').val();
                }
              },
            beforeSend: function() {
              // Display loading message or spinner
              $('#id_username2').siblings('.invalid-feedback').text('Checking availability...');
            },
            dataFilter: function(response) {
              // Parse the JSON response
              var data = JSON.parse(response);
              if (data.is_available) {
                // Return true if username is available
                return 'true';
              } else {
                // Return false if username is not available
                return 'false';
                }
              }
            }
          },
          password1: {
            required: true,
            minlength: 8,
            uppercase: true,
            lowercase: true,
            digit: true,
            symbol: true
          },
          password2: {
            required: true,
            equalTo: '#id_password1'
          }
        },
        messages: {
          fullname: {
            required: 'Please enter your full name',
            lettersOnly: 'Full name should only contain alphabetic characters'
          },
          username: {
            required: 'Please enter your username',
            remote: 'This username is already taken'
          },
          password1: {
            required: 'Please enter your password',
            minlength: 'Password must be at least 8 characters long'
          },
          password2: {
            required: 'Please confirm your password',
            equalTo: 'Passwords do not match'
          }
        },
        errorElement: 'div',
        errorPlacement: function(error, element) {
          error.addClass('invalid-feedback position-absolute pe-3 top-0 start-100 text-start');
          error.insertAfter(element);
          error.hide();
          errorMessageShow(element);
        },
        highlight: function(element) {
          $(element).addClass('is-invalid');
          errorMessageShow($(element));
        },
        unhighlight: function(element) {
          $(element).removeClass('is-invalid');
          errorMessageHide($(element));
        },
        submitHandler: function(form) {
          form.submit();      
        }
      });

      $.validator.addMethod('lettersOnly', function(value, element) {
        return /^[a-zA-Z\s]+$/.test(value);
      }, 'Please enter only alphabetic characters.');

      $.validator.addMethod('uppercase', function(value, element) {
        return /^(?=.*[A-Z])/.test(value);
      }, 'Password must contain at least one uppercase letter.');

      $.validator.addMethod('lowercase', function(value, element) {
        return /^(?=.*[a-z])/.test(value);
      }, 'Password must contain at least one lowercase letter.');

      $.validator.addMethod('digit', function(value, element) {
        return /^(?=.*\d)/.test(value);
      }, 'Password must contain at least one digit.');

      $.validator.addMethod('symbol', function(value, element) {
        return /\W/.test(value);
      }, 'Password must contain at least one special character.');

      $('input, textarea').on('input', function() {
        registerForm.validate().element($(this));
      });

      $('input, textarea').on('keydown', function(e) {
        if (e.keyCode === 13) {
          e.preventDefault();
          var currentField = $(this);
          var formFields = $('#register-form .form-style');
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
        remove: function() {
          // Remove or disable additional functions/methods inside initializeRegisterForm
          $('input, textarea').off('focus input blur keydown');
        }
      };
    }

    function initializeLoginForm(){
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
            required: 'Please enter your username',
          },
          password: {
            required: 'Please enter your password',
          },
        },
        errorElement: 'div',
        errorPlacement: function(error, element) {
          error.addClass('invalid-feedback position-absolute pe-3 top-0 start-100 text-start');
          error.insertAfter(element);
          error.hide();
          errorMessageShow(element);
        },
        highlight: function(element) {
          $(element).addClass('is-invalid');
          errorMessageShow($(element));
        },
        unhighlight: function(element) {
          $(element).removeClass('is-invalid');
          errorMessageHide($(element));
        },
        submitHandler: function(form) {
          form.submit();      
        }
      });

      $('input, textarea').on('input', function() {
        loginForm.validate().element($(this));
      });

      $('input, textarea').on('keydown', function(e) {
        if (e.keyCode === 13) {
          e.preventDefault();
          var currentField = $(this);
          var formFields = $('#login-form .form-style');
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
        remove: function() {
          // Remove or disable additional functions/methods inside initializeRegisterForm
          $('input, textarea').off('focus input blur keydown');
          loginForm.off('validate')
        }
      };
    }

    function errorMessageShow(input){
      input.siblings('.invalid-feedback').addClass('show').slideDown(200);
    }

    function errorMessageHide(input){
      input.siblings('.invalid-feedback').removeClass('show').slideUp(200);
    }

  }

  // Use event delegation for "See More" and "See Less" buttons
  $(document).on('click', '.see-more', function(e) {
    e.preventDefault();
    var $taskDesc = $(this).closest('.task-description');
    $taskDesc.find('.truncated-text').hide();
    $taskDesc.find('.full-text').show();
    $taskDesc.find('.see-more').hide();
    $taskDesc.find('.see-less').show();
  });

  $(document).on('click', '.see-less', function(e) {
    e.preventDefault();
    var $taskDesc = $(this).closest('.task-description');
    $taskDesc.find('.truncated-text').show();
    $taskDesc.find('.full-text').hide();
    $taskDesc.find('.see-more').show();
    $taskDesc.find('.see-less').hide();
  });







});
// Function to convert 24-hour time format to 12-hour format with "a.m." or "p.m."
function convertTo12HourFormat(timeString) {
  const time = timeString.split(":");
  let hour = parseInt(time[0]);
  const minute = time[1];
  const period = hour >= 12 ? "p.m." : "a.m.";

  if (hour === 0) {
    hour = 12;
  } else if (hour > 12) {
    hour -= 12;
  }

  return `${hour}:${minute} ${period}`;
}

function updateBadge(dataTable){
  // Update the completed_tasks and total_tasks values
  const completedTasks = dataTable.rows('.completed').count();
  const totalTasks = dataTable.rows().count();


  // Update the badge content dynamically
  const badgeContainer = $('#taskCompletionBadge');
  badgeContainer.empty();
  if (completedTasks === totalTasks && totalTasks !== 0) {
    badgeContainer.append(
      `<span class="badge rounded-pill bg-light complete-all-task">(${completedTasks}/${totalTasks})<i class="uil uil-check-circle check-icon"></i></span>`
    );
  } else if (completedTasks !== totalTasks && totalTasks !== 0) {
    badgeContainer.append(
      `<span class="badge rounded-pill bg-light not-completed">(${completedTasks}/${totalTasks})<i class="uil uil-times-circle cross-icon"></i></span>`
    );
  }
}

// Function to update the number column
function updateNumberColumn(dataTable) {
  const currentPage = dataTable.page.info().page + 1;
  const rowsPerPage = dataTable.page.info().length;
  const startNumber = (currentPage - 1) * rowsPerPage + 1;
  $('.task-num').each(function(index) {
    $(this).text(startNumber + index);
  });
}

// Function to reload the DataTable with the saved page number
function reloadDataTable(dataTable, pageNumber) {
  dataTable.page(pageNumber - 1).draw(false); // Use draw(false) to prevent reloading the table
}

// Function to handle delete Task
function deleteTaskHandler(dataTable){
  // Event listener for the delete task button click
  $(document).on('click', '.delete-task', function () {
    const taskID = $(this).data('task-id');
    const modalID = $(`#deleteTaskModal`);
    const row = $(this).closest('tr');
    const taskTitle = $(`#${taskID} td:eq(1)`).text();
    const deleteConfirm = $('.delete-confirm');
    deleteConfirm.text(`Are you sure you want to delete task ${taskTitle} ?`);
    modalID.modal('show');

    // Store the task ID and row as data attributes on the delete form
    const deleteTaskForm = $('#deleteTaskForm');
    deleteTaskForm.data('task-id', taskID);
    deleteTaskForm.data('task-row', row);
  });

  // Event listener for the delete task form submission
  $(document).on('submit', '#deleteTaskForm', function (e) {
    e.preventDefault();
    const deleteTaskForm = $(this);
    const taskID = deleteTaskForm.data('task-id');
    const taskTitle = $(`#${taskID} td:eq(1)`).text();
    const row = deleteTaskForm.data('task-row');
    // Save the current page number
    pageNumber = dataTable.page.info().page + 1;


    $.ajax({
      type: "DELETE",
      url: `/api/tasks/${taskID}/`,
      data: {},
      contentType: "application/json",
      success: function (data) {
        // Handle success response
        showToast(`Task <b>${taskTitle}</b> has been deleted.`, "success", 3000);

        // Remove the corresponding row from the DataTable
        dataTable.row(row).remove().draw(false);


        // Update the badge
        updateBadge(dataTable);

        // Reload the DataTable with the saved page number
        reloadDataTable(dataTable, pageNumber);

        // Update the number column
        updateNumberColumn(dataTable);

        // Close the add task modal
        $(`#deleteTaskModal`).modal('hide');
      },
      error: function (xhr, status, error) {
        // Handle error response
        if (xhr.status == 400) {
          showToast('Something went wrong.', "error", 3000);
        } else if (xhr.status == 401) {
          showToast('You are not authenticated. Please login first.', "error", 3000);
        } else if (xhr.status == 403) {
          showToast('You are unauthorized to delete this task.', "error", 3000);
        } else if (xhr.status == 404) {
          showToast('Task is not found.', "error", 3000);
        } else {
          showToast('An error occurred. Please try again later.', "error", 3000);
        }
      },
    });
  });
}

// Function to handle complete Task
function completeTaskHandler(dataTable){
  $(document).on('click', '.complete-task', function(e) {
    e.preventDefault();
    const taskId = $(this).data('task-id');
    const completeTaskForm = $('#completeTaskForm');

    completeTaskForm.data('task-id', taskId);

    completeTaskForm.submit();
  });

  $(document).on('submit', '#completeTaskForm', function(e){
    e.preventDefault();
    const taskId = $(this).data("task-id");
    $.ajax({
      type: "POST",
      url: `/api/tasks/${taskId}/complete/`,
      success: function (data) {
        // Handle success response
        const row = $(`#${taskId}`);
        const completeButton = row.find('.complete-task');
        if(data.completed){
          showToast(`Task <b>${data.title}</b> has been completed.`, "success", 3000);
          row.addClass('completed');
          completeButton.addClass('complete-button');
          completeButton.text('uncomplete')
        }
        else{
          // location.reload();
          row.removeClass('completed');
          completeButton.removeClass('complete-button');
          completeButton.text('complete')
        }
        updateBadge(dataTable);
      },
      error: function (xhr, status, error) {
        if(xhr.status == 400){
          showToast('Something went wrong.', "error", 3000);
        }
        else if(xhr.status == 401){
          showToast('You are not authenticated. Please login first.', "error", 3000);
        }
        else if(xhr.status == 403){
          showToast('You are unauthorized to complete this task.', "error", 3000);
        }
        else if(xhr.status == 404){
          showToast('Task is not found.', "error", 3000);
        }
        else{
          showToast('An error occurred. Please try again later.', "error", 3000);
        }
      },
    });
  });
}

// Function to populate the edit modal with task data
function populateEditModal(task) {
  const modalID = `#editTaskModal`;
  const form = $(`${modalID} .editTaskForm`);
  form.find('#id_title_edit').val(task.title).removeClass('is-invalid');
  form.find('#id_description_edit').val(task.description).removeClass('is-invalid');
  form.find('#id_execution_time_edit').val(task.execution_time).removeClass('is-invalid');
  form.find('#id_execution_day_edit').val(task.execution_day).removeClass('is-invalid');
  form.find('#id_execution_date_edit').val(task.execution_date).removeClass('is-invalid');

  // Trigger the change event to update the select2 dropdown
  form.find('#id_execution_day_edit').trigger('change');
  form.find('#id_execution_date_edit').trigger('change');

  // Remove the invalid-feedback elements
  form.find('.invalid-feedback').remove();
}

// Function to handle edit task
function editTaskHandler(){
  // Event listener for edit task submit
  $(document).on('submit', '#editTaskForm', function(event) {
    event.preventDefault();
    const taskId = $(this).data("task-id");
    const formData = $(this).serializeArray();
    const newData = {};
    const userID = $(this).data('user-id')
    formData.forEach((field) => {
      newData[field.name] = field.value;
    });

    newData.user = userID;
    $.ajax({
      type: "PUT",
      url: `/api/tasks/${taskId}/`,
      data: JSON.stringify(newData),
      contentType: "application/json",
      success: function (data, status, xhr) {
        // Handle success response
        showToast(`Task <b>${data.title}</b> has been edited successfully.`, "success", 3000);

        // Update the corresponding row in the DataTable
        const row = $(`#${taskId}`);
        if (data.daily){
          row.find('.task-title').text(data.title);
          row.find('.task-execution-time').text(convertTo12HourFormat(data.execution_time));
          row.find('.task-description .truncated-text').text(data.description.substring(0,100));
          row.find('.task-description .full-text').text(data.description);
        }
        else if (data.weekly){
          row.find('.task-title').text(data.title);
          row.find('.task-description .truncated-text').text(data.description.substring(0,100));
          row.find('.task-description .full-text').text(data.description);
          row.find('.task-execution-time').text(`${data.execution_day}, ${convertTo12HourFormat(data.execution_time)}`);
        }
        else if (data.monthly){
          row.find('.task-title').text(data.title);
          row.find('.task-description .truncated-text').text(data.description.substring(0,100));
          row.find('.task-description .full-text').text(data.description);
          row.find('.task-execution-time').text(`Day ${data.execution_date}, ${convertTo12HourFormat(data.execution_time)}`);
        }


        // Create and insert "See More" and "See Less" links if they don't exist
        if (data.description.length > 100) {
          row.find('.task-description .truncated-text').text(data.description.substring(0,100)+'...');
          if (!row.find('.see-more').length) {
            row.find('.task-description').append('<a href="#" class="see-more text-decoration-none">See More</a>');
          }
          if (!row.find('.see-less').length) {
            row.find('.task-description').append('<a href="#" class="see-less text-decoration-none" style="display: none;">Less</a>');
          }
        }

        // Show/hide "See More" and "See Less" links based on description length
        if (data.description.length > 100) {
          row.find('.see-more').show();
          row.find('.see-less').hide();
        } else {
          row.find('.see-more').hide();
          row.find('.see-less').hide();
        }

        // Close the modal after editing the task
        $(`#editTaskModal`).modal('hide');
      },
      error: function (xhr, status, error) {
        if(xhr.status == 400){
          showToast('Please fill all the field.', "error", 3000);
          const errors = xhr.responseJSON;
          for (const fieldName in errors) {
            const fieldError = errors[fieldName][0];
            const fieldInput = $(`#editTaskForm #id_${fieldName}_edit`);
            let fieldFeedback = fieldInput.siblings('.invalid-feedback');
            if (fieldFeedback.length === 0) {
              // Create the invalid-feedback element if it doesn't exist
              fieldFeedback = $('<div class="invalid-feedback"></div>');
              fieldInput.after(fieldFeedback);
            }
            fieldInput.addClass('is-invalid');
            fieldFeedback.text(fieldError);
          }
        }
        else if(xhr.status == 401){
          showToast('You are not authenticated. Please login first.', "error", 3000);
        }
        else if(xhr.status == 403){
          showToast('You are unauthorized to edit this task.', "error", 3000);
        }
        else if(xhr.status == 404){
          showToast('Task is not found.', "error", 3000);
        }
        else{
          showToast('An error occurred. Please try again later.', "error", 3000);
        }
      },
    });
  });

  // Event listener for the edit task button click
  $(document).on('click', '.edit-task', function () {
    const taskID = $(this).closest('tr').data('id');
    const modalID = $(`#editTaskModal`);
    const editTaskForm = $('#editTaskForm');

    editTaskForm.data('task-id', taskID);

    $.ajax({
      type: "GET",
      url: `/api/tasks/${taskID}/`, // Adjust the URL as per your API endpoint
      success: function (data) {
        populateEditModal(data);
        modalID.modal('show');
      },
      error: function (xhr, status, error) {
        // Handle error response
        // Display an error message or perform other actions
        showToast('An error occurred. Please try again later.', "error", 3000);
      },
    });
  });
}

// Function to handle add task
function addTaskHandler(dataTable){
  $('#addTaskForm').on('submit', function(event) {
    event.preventDefault();
    const formData = $(this).serializeArray();
    const newData = {};
    const userID = $(this).data('user-id')
    const form = $('#addTaskForm')
    const select = $('#addTaskForm .select2');
    formData.forEach((field) => {
      newData[field.name] = field.value;
    });

    newData.user = userID;
    $.ajax({
      type: "POST",
      url: `/api/tasks/`,
      data: JSON.stringify(newData),
      contentType: "application/json",
      success: function (data, status, xhr) {
        // Handle success response
        showToast(`Task <b>${data.title}</b> has been added successfully.`, "success", 3000);

        // Add the new task to the DataTable
        if (data.daily){
          dataTable.row.add({
            "id": data.id,
            "title": data.title,
            "description": data.description,
            "created_at": data.created_at,
            "execution_time": data.execution_time,
            "completed": false,
          }).draw(false);
        }
        else if (data.weekly){
          dataTable.row.add({
            "id": data.id,
            "title": data.title,
            "description": data.description,
            "created_at": data.created_at,
            "execution_time": data.execution_time,
            "execution_day": data.execution_day,
            "completed": false,
          }).draw(false);
        }
        else if (data.monthly){
          dataTable.row.add({
            "id": data.id,
            "title": data.title,
            "description": data.description,
            "created_at": data.created_at,
            "execution_time": data.execution_time,
            "execution_date": data.execution_date,
            "completed": false,
          }).draw(false);
        }

        // Get last page
        pageNumber = dataTable.page.info().pages;

        reloadDataTable(dataTable, pageNumber);

        updateBadge(dataTable);

        // Close the modal
        $('#addTaskModal').modal('hide');

        // Reset the form
        form[0].reset();
        // Reset the Select2 dropdown to its initial state
        select.val(null).trigger('change');

        // Remove the invalid-feedback elements
        form.find('.invalid-feedback').remove();

        // Remove class is-invalid
        form.find('.is-invalid').removeClass('is-invalid');
      },
      error: function (xhr, status, error) {
        if(xhr.status == 400){
          showToast('Please fill all the field.', "error", 3000);
          const errors = xhr.responseJSON;
          for (const fieldName in errors) {
            const fieldError = errors[fieldName][0];
            const fieldInput = $(`#addTaskForm #id_${fieldName}`);
            let fieldFeedback = fieldInput.siblings('.invalid-feedback');
            if (fieldFeedback.length === 0) {
              // Create the invalid-feedback element if it doesn't exist
              fieldFeedback = $('<div class="invalid-feedback"></div>');
              fieldInput.after(fieldFeedback);
            }
            fieldInput.addClass('is-invalid');
            fieldFeedback.text(fieldError);
          }
        }
        else if(xhr.status == 401){
          showToast('You are not authenticated. Please login first.', "error", 3000);
        }
        else if(xhr.status == 403){
          showToast('You are unauthorized to edit this task.', "error", 3000);
        }
        else if(xhr.status == 404){
          showToast('Task is not found.', "error", 3000);
        }
        else{
          showToast('An error occurred. Please try again later.', "error", 3000);
        }
      },
    });
  });
}

// Function to initialize select2
function initializeSelect2(modalId) {
  var select = $('#' + modalId + ' .select2');
  if (select.length > 0) {
    select.select2({
      dropdownParent: $('#' + modalId), // Set the dropdownParent to the modal element
      width: '100%' // Set the initial width to 100%
    });

    select.on('select2:select', function (e) {
      var value = e.target.value;
      if (value !== '') {
        $('option[value=""]').prop('disabled', true);
      }
    });

    // Calculate and set the maximum width for the select options
    var maxWidth = 0;
    select.find('option').each(function () {
      var optionWidth = $(this).text().length;
      if (optionWidth > maxWidth) {
        maxWidth = optionWidth;
      }
    });

    // Set the width of the dropdown to the calculated maximum width
    select.select2('destroy'); // Destroy the initial Select2 instance
    select.select2({
      dropdownParent: $('#' + modalId), // Set the dropdownParent to the modal element
      width: (maxWidth * 12) + 'px' // Set the width based on the maximum width of options
    });

    select.on('select2:select', function (e) {
      var value = e.target.value;
      if (value !== '') {
        $('option[value=""]').prop('disabled', true);
      }
    });
  }
}

// Function to handle custom day sorting
function customDaySorting(customDayOrder){
  // Add a custom sorting method for 'custom-datetime'
  $.fn.dataTable.ext.type.order['custom-datetime-pre'] = function(data) {
    // Custom sorting function for 'custom-datetime' type
    const dayAndTime = data.split(' ');
    const datePart = dayAndTime[0];
    const timePart = dayAndTime[1] + ' ' + dayAndTime[2];
    const dayIndex = customDayOrder.indexOf(datePart);
    return dayIndex * 1000000 + moment(timePart, 'hh:mm A').unix();
  };

  // Set the default sorting method for 'custom-datetime' type
  $.fn.dataTable.ext.type.order['custom-datetime-asc'] = function(a, b) {
    return a < b ? -1 : a > b ? 1 : 0;
  };
  $.fn.dataTable.ext.type.order['custom-datetime-desc'] = function(a, b) {
    return a < b ? 1 : a > b ? -1 : 0;
  };
}

// Function to handle custome date sorting
function customDateSorting(){
  // Add a custom sorting method for 'custom-datetime'
  $.fn.dataTable.ext.type.order['custom-datetime-pre'] = function(data) {
    // Custom sorting function for 'custom-datetime' type
    const dayAndTime = data.split(' ');
    const datePart = dayAndTime[1];
    const timePart = dayAndTime[2] + ' ' + dayAndTime[3];
    const dayIndex = parseInt(datePart, 10);
    return dayIndex * 1000000 + moment(timePart, 'hh:mm A').unix();
  };

  // Set the default sorting method for 'custom-datetime' type
  $.fn.dataTable.ext.type.order['custom-datetime-asc'] = function(a, b) {
    return a < b ? -1 : a > b ? 1 : 0;
  };
  $.fn.dataTable.ext.type.order['custom-datetime-desc'] = function(a, b) {
    return a < b ? 1 : a > b ? -1 : 0;
  };
}