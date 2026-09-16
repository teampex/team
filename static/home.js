
document.addEventListener("DOMContentLoaded", function () {

    console.log("NexaCart Home JS Loaded");

    // =========================================
    // LOGIN BUTTON
    // =========================================

    const loginButtons = document.querySelectorAll(
        "#loginBtn, #login, .login-btn, .login-button, [data-login]"
    );

    loginButtons.forEach(function (button) {

        // Login button visible rakho
        button.style.display = "inline-flex";
        button.style.visibility = "visible";
        button.style.opacity = "1";
        button.style.pointerEvents = "auto";

        // Login click
        button.addEventListener("click", function (event) {

            event.preventDefault();

            console.log("Login button clicked");

            window.location.href = "/login";

        });

    });


    // =========================================
    // AGAR LOGIN KI ID/CLASS ALAG HAI
    // TEXT SE LOGIN BUTTON FIND KARO
    // =========================================

    document.querySelectorAll("button, a").forEach(function (element) {

        const text = element.textContent.trim().toLowerCase();

        if (text === "login") {

            element.style.display = "inline-flex";
            element.style.visibility = "visible";
            element.style.opacity = "1";
            element.style.pointerEvents = "auto";

            element.addEventListener("click", function (event) {

                event.preventDefault();

                console.log("Login clicked");

                window.location.href = "/login";

            });

        }

    });


    console.log("NexaCart Home JS Ready");

});
