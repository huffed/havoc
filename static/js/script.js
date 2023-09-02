$(document).ready(function () {
  function ready() {
    var error = $("#error-message");
    var submit = $(".submit-button");

    if (error.text() != null) {
      submit.css("margin-top", "0");
    } else {
      submit.css("margin-top", "40px");
    }
  }
  var timeout;

  function validateinput() {
    var input = $(".register-container input[name='username']");
    var username = input.val();
    var error = $("#error-message");
    var submit = $(".submit-button");

    if (error.text() == "Username or password incorrect.") {
      error.text("");
      submit.css("margin-top", "40px");
    }

    if (username != null) {
      if (username.length === 0) {
        error.text("");
        submit.css("margin-top", "40px");
        input.removeClass("input-error");
      } else if (username.length <= 2) {
        clearTimeout(timeout);
        timeout = setTimeout(function () {
          error.text("Username must be at least 3 characters long");
          submit.css("margin-top", "0");
          input.addClass("input-error");
        }, 300);
      } else {
        error.text("");
        input.removeClass("input-error");

        clearTimeout(timeout);
        timeout = setTimeout(function () {
          checkUsernameAvailability(username);
        }, 500);
      }
    }
  }

  function checkUsernameAvailability(username) {
    $.ajax({
      type: "GET",
      url: "/check_availability",
      data: { username: username },
      success: function (response) {
        // Handle the response if needed
      },
    });
  }

  ["input", "blur"].forEach(function (event) {
    window.addEventListener(event, validateinput);
  });

  window.addEventListener("load", ready);
});
