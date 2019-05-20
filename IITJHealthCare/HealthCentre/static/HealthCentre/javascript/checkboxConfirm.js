function checkConfirm() {
    if (document.getElementById("confirmCheck").checked === true)
    {
       return true;
    }
    else
    {
       alert('Please tick confirm.');
       return false;
    }
}
