document.addEventListener('DOMContentLoaded', function () {
    if(parseInt('{{errors}}',10)===1){
        let modal = new bootstrap.Modal(document.getElementById('errorModal'));
        modal.show();
    }else if(parseInt('{{success}}')===1){
        let modal = new bootstrap.Modal(document.getElementById('successModal'));
        modal.show();
    }
});