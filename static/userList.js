
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
    // remove own name from list
    let otherUsers = userList.filter(function(e) { return e !== g_user})
    if (otherUsers.length === 0)
        title.innerHTML = "Oh no, you're playing alone!"
    else
        title.innerHTML = "Other players (" + otherUsers.length + "):";

    let list = document.getElementById('player-list');
    list.innerHTML = "";
    for (let user of otherUsers) {
        list.innerHTML += `<div>${user}</div>`
    }
}