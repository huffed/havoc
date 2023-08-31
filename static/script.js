$(document).ready(function() {
    var usernameInput = $("input[name='u']");
    var errorMessage = $("#error-message");

    usernameInput.on("input", function() {
        var username = usernameInput.val();

        if (username.length <= 2) {
            errorMessage.text("Username must be at least 3 characters long");
            errorMessage.show();
            usernameInput.css("border-color", "red")
        } else {
            errorMessage.hide();
            usernameInput.css("border-color", "")
        }
    });

    usernameInput.on("blur", function() {
        if (usernameInput.val().length === 0) {
            errorMessage.hide();
            usernameInput.css("border-color", "");
        }
    });
});
