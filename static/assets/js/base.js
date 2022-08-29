//tick check box
function toggle(source) {
     checkboxes = document.getElementsByName('foo');
     for(let i=0, n=checkboxes.length;i<n;i++) {
        checkboxes[i].checked = source.checked;
     }
    }




