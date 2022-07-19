let clicked = false;

function failure(user) {
    console.log("failure: " + user);
    let buzzer = document.getElementById("buzzer");
    buzzer.innerHTML = "Too late! " + user + " already pressed the button";
    setCenterColor(colors.FAILURE);
    clicked = true;
}

function success() {
    console.log("success");
    let buzzer = document.getElementById("buzzer");
    buzzer.innerHTML = "You pressed the button!";
    setCenterColor(colors.SUCCESS)
}

function setCenterColor(color) {
    let buzzer = document.getElementById("centered");
    buzzer.style.backgroundColor = color;
}

function resetBuzzerAppearance() {
    let buzzer = document.getElementById("buzzer");
    console.log("reset buzzer text");
    buzzer.innerHTML = g_user;
    setCenterColor(colors.NORMAL);
    clicked = false;
}

function logout() {
    let center = document.getElementById("centered");
    center.style.animation = "0.2s ease-in-out 1 zoomOut";

    console.log('logging out!');

    let xhr = new XMLHttpRequest();
    xhr.open('POST', g_logout_url)

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            window.location.reload();
            console.log(xhr.responseText);
        }
    }

    xhr.send();
}

function buzzerClick() {
    if (clicked) return;
    clicked = true;

    console.log('buzzer clicked!');
    // record the time that the buzzer was clicked
    let ts = Date.now() / 1000;

    let xhr = new XMLHttpRequest();
    xhr.open('POST', g_api_click_url);

    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let resp = xhr.responseText;
            console.log("resp: " + resp);
            if (resp === "pressed") success(); else failure(resp);
        }
    }
    xhr.send("ts=" + ts);
}

function sendResetBuzzerSig() {
    if (!clicked) return;
    clicked = false;

    console.log('button reset!');
    let xhr = new XMLHttpRequest();
    xhr.open('POST', g_api_reset_url);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
            if (xhr.responseText === "reset") resetBuzzerAppearance();
        }
    }
    xhr.send();
}

function waitForClick() {
    console.log("wait for click");

    let xhr = new XMLHttpRequest();
    xhr.open('POST', g_api_wait_buzz_url);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log("Someone buzzed!!");
            let resp = xhr.responseText;
            if (resp !== g_user && resp !== "") failure(resp);
            waitForReset();
        }
    }

    xhr.send();
}

function waitForReset() {
    console.log("wait for reset");

    let xhr = new XMLHttpRequest();
    xhr.open('POST', g_api_wait_reset_url);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            if (xhr.responseText === "reset") resetBuzzerAppearance();
            waitForClick();
        }
    }
    xhr.send();
}