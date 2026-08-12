const weatherForm =
    document.getElementById("weatherForm");

const searchButton =
    document.getElementById("searchButton");

const buttonText =
    document.getElementById("buttonText");

const loader =
    document.getElementById("loader");


if (weatherForm) {

    weatherForm.addEventListener(
        "submit",
        function () {

            searchButton.disabled = true;

            buttonText.textContent =
                "Loading...";

            loader.classList.remove("hidden");

        }
    );

}