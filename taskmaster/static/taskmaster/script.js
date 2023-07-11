$(document).ready(function() {
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

  var formStyleInputs = $('.form-style');
  if (formStyleInputs.length > 0) {
    formStyleInputs.focus(function() {
      $(this).siblings('.invalid-feedback').hide();
      if ($(this).attr('name') === 'password1') {
        $('[name="password2"]').siblings('.invalid-feedback').hide();
      }
    });

    formStyleInputs.blur(function() {
      if ($(this).attr('name') === 'password2' && $(this).hasClass('is-invalid') && $('[name="password1"]').val() === '') {
        $(this).siblings('.invalid-feedback').show();
      }
      else if ($(this).attr('name') === 'password1' && $(this).hasClass('is-invalid') && $(this).val() === '') {
        $('[name="password2"]').siblings('.invalid-feedback').show();
      }
      else if ($(this).hasClass('is-invalid') && $(this).val() === '' && $(this).attr('name') !== 'password2') {
        $(this).siblings('.invalid-feedback').show();
      }
    });

    // formStyleInputs.keydown(function(e) {
    //   if (e.keyCode === 13) {  // 13 represents the Enter key
    //     e.preventDefault();
    //     var currentField = $(this);
    //     var formFields = $('.form-style');
    //     var currentIndex = formFields.index(currentField);

    //     if (currentIndex === formFields.length - 1) {
    //       // Submit the form if it's the last field
    //       currentField.closest('form').submit();
    //     } else {
    //       // Move focus to the next field
    //       var nextField = formFields.eq(currentIndex + 1);
    //       nextField.focus();
    //     }
    //   }
    // });
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

  var selectDay = $('.select-day')
  if (selectDay.length > 0){
    selectDay.on('change', function (e){
      var value = e.target.value;
      if (value !== '') {
        $('option[value=""]').prop('disabled', true);
      }
    });
  }
});
