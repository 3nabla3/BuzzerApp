// Code to synchronise the buzzer with the server

// when a buzzer has been clicked, used to avoid buzzing before reset
let clicked = false;

// executes when someone else presses the buzzer before you
function failure(user) {
    // disable your buzzer until someone resets
    clicked = true;
    console.log("failure: " + user);
    setBuzzerAppearance("Too late! " + user + " already pressed the button", colors.FAILURE);
}

// executes if you were the first to press the buzzer
function success() {
    console.log("success");
    setBuzzerAppearance("You pressed the button!", colors.SUCCESS);
}

// sets the color of big center box (changes when a buzzer is pressed)
function setBuzzerAppearance(text, color) {
    let center = document.getElementById("centered");
    let buzzer = document.getElementById("buzzer");
    center.style.backgroundColor = color;
    buzzer.innerHTML = text;
}

// resets your buzzer to allow more buzzes
function resetBuzzer() {
    console.log("reset buzzer");
    setBuzzerAppearance(g_user, colors.NORMAL);
    clicked = false;
}

// when you want to change your username
function logout() {
    let center = document.getElementById("centered");
    center.style.animation = "0.2s ease-in-out 1 zoomOut";
    console.log('logging out!');

    let xhr = new XMLHttpRequest();
    xhr.open('POST', g_logout_url)
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // window.location.reload();
            console.log(xhr.responseText);
        }
    }
    xhr.send();
}

// when you click the buzzer
function buzzerClick() {
    if (clicked) return;
    console.log('buzzer clicked!');
    clicked = true;

    let xhr = new XMLHttpRequest();
    xhr.open('POST', g_api_click_url);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let resp = xhr.responseText;
            console.log("resp: " + resp);
            if (resp === "pressed") success();
        }
    }
    xhr.send();
}

// when you click the reset buzzer button
// tells the server to reset all buzzers
function sendResetBuzzerSig() {
    // if no one pressed the buzzer yet, ignore
    if (!clicked) return;

    console.log('button reset!');
    let xhr = new XMLHttpRequest();
    xhr.open('POST', g_api_reset_url);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
            if (xhr.responseText === "reset") resetBuzzer();
        }
    }
    xhr.send();
}

// Sends a request to the server that only gets answered when someone buzzes
function waitForClick() {
    console.log("wait for click");

    let xhr = new XMLHttpRequest();
    xhr.open('POST', g_api_wait_buzz_url);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log("Someone buzzed!!");
            let resp = xhr.responseText;
            if (resp !== g_user && resp !== "") failure(resp);
            // Now wait for someone (possibly you) to reset the buzzers
            waitForReset();
        }
    }
    xhr.send();
}

// Sends a request to the server that only gets answered when someone resets
function waitForReset() {
    console.log("wait for reset");

    let xhr = new XMLHttpRequest();
    xhr.open('POST', g_api_wait_reset_url);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            resetBuzzer();
            // Now wait for someone (possibly you) to press their buzzer
            waitForClick();
        }
    }
    xhr.send();
}