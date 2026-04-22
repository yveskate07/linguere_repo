document.addEventListener('DOMContentLoaded', function () {
    const main_cat_field = document.querySelector('#id_main_category');
    const cat_field = document.querySelector('#id_category');

    function toggleIban() {
        const main_cat_field_value = main_cat_field.value;
        const cat_field_value = cat_field.value;
        
        if (main_cat_field_value !== 'Kits Arduino et IOT') {
            cat_field.value = '';
            cat_field.setAttribute('disabled', 'disabled');
            /*if(cat_field_value === 'Kits Arduino' || cat_field_value === 'Composants IoT' || cat_field_value === 'Robotique' || cat_field_value === 'Capteurs') {
                
            }*/
        } else {
            ibanField.setAttribute('disabled', 'disabled');
            cat_field.removeAttribute('disabled');
        }
    }

    // Initial check (important en édition)
    toggleIban();

    // Écoute des changements
    main_cat_field.addEventListener('input', toggleIban);
});