const userId = document.body.getAttribute('data-user-id');

let socket = null;

if (userId !== 'anonymous_id') {
    socket = new WebSocket('ws://' + window.location.host + '/ws/products/user/' + userId + '/');
    //console.log('Utilisateur connecté avec ID:', userId);
}else{
    socket = new WebSocket('ws://' + window.location.host + '/ws/products/user/anonymous/');
    //console.log('Utilisateur anonyme connecté !')
}