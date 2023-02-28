var passcode = document.forms["register"]["password"];
var rep_passcode = document.forms["register"]["rep_password"];
var b = document.getElementById('b');

rep_passcode.addEventListener("keyup", (event) => {
    if (rep_passcode.value === passcode.value) {
        b.classList.remove('red');
        b.classList.add('green');
    } else {
        b.classList.add('red');
        b.classList.remove('green');
    }
});

var containerClasses = document.getElementsByClassName('container')[0].classList;
document.getElementById('toggle').addEventListener('click', function () {
    containerClasses.add('active');
});

document.getElementById('close').addEventListener('click', function () {
    containerClasses.remove('active');
});
