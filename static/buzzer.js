let clicked = false;

let g_user = null;
let g_logout_url = null;
let g_api_click_url = null;
let g_api_reset_url = null;
let g_api_wait_buzz_url = null;
let g_api_wait_reset_url = null;
let g_api_get_users_url = null;
let colors = null;

function setup(user, logout_url, api_click_url, api_reset_url,
               api_wait_buzz_url, api_wait_reset_url, api_get_users_url,
               successColor, failureColor) {
    g_user = user;
    g_logout_url = logout_url;
    g_api_click_url = api_click_url
    g_api_reset_url = api_reset_url;
    g_api_wait_buzz_url = api_wait_buzz_url;
    g_api_wait_reset_url = api_wait_reset_url;
    g_api_get_users_url = api_get_users_url;

    // get the current color of the center div to set as the normal color
    // avoids to define normal color twice in css and javascript
    let center = document.getElementById("centered");
    colors = Object.freeze({
        'NORMAL': center.style.backgroundColor,
        'SUCCESS': successColor, 'FAILURE': failureColor
    });
}

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


function updateUserList() {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', g_api_get_users_url);

    xhr.onreadystatechange = async function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let userList = JSON.parse(xhr.responseText);
            updateUserListText(userList);
            await new Promise(resolve => setTimeout(resolve, 1000));
            updateUserList();
        }
    }
    xhr.send();
}

function updateUserListText(userList) {
    let title = document.getElementById('player-title');
    if (userList.length > 1) title.innerHTML = "Other players:"; else title.innerHTML = "Oh no, you're playing alone!"

    let list = document.getElementById('player-list');
    list.innerHTML = "";
    for (let user of userList) {
        if (user !== g_user) list.innerHTML += `<li>${user}</li>`
    }
}