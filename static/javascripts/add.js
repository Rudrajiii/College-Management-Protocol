console.log('plugged');
const hook = document.querySelector('.hook');
console.log(hook);
const popUp = document.getElementById('popUp');
console.log(popUp);
const cross = document.getElementById('cross');
console.log(cross);
hook.addEventListener('click', (e) => {
    e.preventDefault();
    if (popUp.style.display === 'block') {
        popUp.style.display = 'none';
    } else {
        popUp.style.display = 'none';
        setTimeout(() => {
            popUp.style.display = 'block';
            popUp.style.transition = 'all 1.5s ease-in-out';
        }, 300);
    }
});

cross.addEventListener('click', (e) =>{
    popUp.style.display = 'none';
});
