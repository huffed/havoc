$(document).ready(function () {
  var error = $("#error-message");
  var submit = $(".submit-button");

  if (error.text() != "") {
    submit.css("margin-top", "0");
  } else {
    submit.css("margin-top", "40px");
  }

  var timeout;

  function validateinput() {
    var input = $(".register input[name='username']");
    var username = input.val();
    var error = $("#error-message");
    var submit = $(".submit-button");

    if (error.text() == "Username or password incorrect.") {
      clearError(error, submit);
    }

    if (username != null) {
      if (username.length === 0) {
        clearError(error, submit);
      } else if (username.length <= 2) {
        clearTimeout(timeout);
        timeout = setTimeout(function () {
          clearError(error, submit);
          error.text("Username must be at least 3 characters long");
          submit.css("margin-top", "0");
        }, 300);
      } else {
        clearError(error, submit);

        clearTimeout(timeout);
        timeout = setTimeout(function () {
          checkUsernameAvailability(username, error);
        }, 500);
      }
    }
  }

  function checkUsernameAvailability(username, error) {
    $.ajax({
      type: "GET",
      url: "/check_availability",
      data: { username: username },
      success: function (data) {
        var response = JSON.parse(data);

        if (response.available == true) {
          error.css("color", "green");
        } else {
          error.css("color", "red");
        }
        error.text(response.message);
      },
    });
  }

  function clearError(error, other) {
    error.text("");
    error.css("color", "red");
    other.css("margin-top", "40px");
  }

  ["input", "blur"].forEach(function (event) {
    window.addEventListener(event, validateinput);
  });
});
