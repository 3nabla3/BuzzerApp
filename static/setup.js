let g_user = null;
let g_api_get_users_url = null;
let g_logout_url = null;
let g_api_click_url = null;
let g_api_reset_url = null;
let g_api_wait_buzz_url = null;
let g_api_wait_reset_url = null;
let colors = null;

function setup(user, get_users_url, logout_url, api_click_url, api_reset_url,
                     api_wait_buzz_url, api_wait_reset_url,
                     successColor, failureColor) {

    g_user = user;
    g_api_get_users_url = get_users_url;
    g_logout_url = logout_url;
    g_api_click_url = api_click_url
    g_api_reset_url = api_reset_url;
    g_api_wait_buzz_url = api_wait_buzz_url;
    g_api_wait_reset_url = api_wait_reset_url;

    // get the current color of the center div to set as the normal color
    // avoids to define normal color twice in css and javascript
    let center = document.getElementById("centered");
    colors = Object.freeze({
        'NORMAL': center.style.backgroundColor,
        'SUCCESS': successColor, 'FAILURE': failureColor
    });
}