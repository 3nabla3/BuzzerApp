
function updateUserList() {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', g_api_get_users_url);

    xhr.onreadystatechange = async function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(g_api_get_users_url);
            console.log(xhr.responseText);
            let userList = JSON.parse(xhr.responseText);
            updateUserListText(userList);
            await new Promise(resolve => setTimeout(resolve, 1000));
            updateUserList();
        }
    }
    xhr.send();
}

function updateUserListText(userList) {
    let title = document.getElementById('player-list-title');
    if (userList.length === 0 ||
        userList.length === 1 && userList[0] === g_user)
        title.innerHTML = "Oh no, you're playing alone!"
    else
        title.innerHTML = "Other players:";

    let list = document.getElementById('player-list');
    list.innerHTML = "";
    for (let user of userList) {
        if (user !== g_user) list.innerHTML += `<li>${user}</li>`
    }
}