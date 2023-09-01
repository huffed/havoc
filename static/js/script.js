$(document).ready(function() {
    var timeout;

  function validateinput() {
    var input = $(".register-container input[name='username']");
    var username = input.val();
    var error = $("#error-message");

    error.hide();

    if (username != null) {
      if (username.length === 0) {
        error.hide();
        input.removeClass("input-error");
      } else if (username.length <= 2) {
        clearTimeout(timeout);
        timeout = setTimeout(function () {
          error.text("Username must be at least 3 characters long");
          error.show();
          input.addClass("input-error");
        }, 300);
      } else {
        error.hide();
        input.removeClass("input-error");

            clearTimeout(timeout);
            timeout = setTimeout(function() {
                checkUsernameAvailability(username);
            }, 500);
        }
    }

    function checkUsernameAvailability(username) {
        $.ajax({
            type: "GET",
            url: "/check_availability",
            data: { username: username },
            success: function(response) {
                // Handle the response if needed
            }
        });
    }

    ['input', 'blur'].forEach(function(event){
        window.addEventListener(event,validateinput);
    });
});
