const userId = document.body.getAttribute('data-user-id');

const protocol = window.location.protocol === "https:" ? "wss" : "ws";


let socket = null;

if (userId !== 'anonymous_id') {
    socket = new WebSocket(protocol+'://' + window.location.host + '/ws/shop/user/' + userId + '/');
}else{
    socket = new WebSocket(protocol+'://' + window.location.host + '/ws/shop/user/anonymous/');
}