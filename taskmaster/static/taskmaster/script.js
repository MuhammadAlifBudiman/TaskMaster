$(document).ready(function() {
  if (typeof globalMessage !== 'undefined'){
    if(typeof success !== 'undefined'){
      showToast(globalMessage, success, 3000);
    }else if(typeof error !== 'undefined'){
      showToast(globalMessage, error, 3000);
    }    
  }

  var csrfToken = $('[name="csrfmiddlewaretoken"]').val();
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

  var completeButton = $('.complete-button')
  if (completeButton.length > 0){
    completeButton.text('uncomplete')
  }

  var moreButton = $('.see-more')
  if (moreButton.length > 0){
    moreButton.on('click', function(e){
      e.preventDefault();
      var $taskDesc = $(this).closest('.task-description');
      $taskDesc.find('.truncated-text').hide();
      $taskDesc.find('.full-text').show();
      $taskDesc.find('.see-more').hide();
      $taskDesc.find('.see-less').show();
    });
  }

  var lessButton = $('.see-less')
  if (lessButton.length > 0){
    lessButton.on('click', function(e) {
      var $taskDesc = $(this).closest('.task-description');
      $taskDesc.find('.truncated-text').show();
      $taskDesc.find('.full-text').hide();
      $taskDesc.find('.see-more').show();
      $taskDesc.find('.see-less').hide();
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



});
