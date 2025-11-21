const userId = document.body.getAttribute('data-user-id');

let socket = null;

if (userId !== 'anonymous_id') {
    socket = new WebSocket('ws://' + window.location.host + '/ws/shop/user/' + userId + '/');
}else{
    socket = new WebSocket('ws://' + window.location.host + '/ws/shop/user/anonymous/');
}