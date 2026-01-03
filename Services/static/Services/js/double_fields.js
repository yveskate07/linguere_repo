const slug = document.body.dataset.slug;

const ids = {'broderie-numerique':[['support-type', 'other-support']], 
            'impression-sur-objets-personnalises':[['object-type', 'other-object'], ['design-file', 'other-file']], 
            'impression-sur-papier-et-supports-rigides':[['format','other-format'],['paper-type', 'other-paper'], ['design-file', 'other-file']], 
            'impression-sur-textiles-et-vetements':[['textile-type', 'other-textile'], ['design-file', 'other-file']]}



if(Object.keys(ids).includes(slug)){
    ids[slug].forEach(([mainId, otherId]) => {
        if(document.getElementById(mainId)){
            document.getElementById(mainId).addEventListener('change', function() {
                if (this.value === 'Autre (Préciser)') {
                    document.getElementById(otherId).style.display = 'block';
                }else{
                    document.getElementById(otherId).style.display = 'none';
                }
            })
        }
    });
}