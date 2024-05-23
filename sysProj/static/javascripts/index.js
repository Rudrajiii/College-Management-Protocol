console.log('plugged!!');
let timeLine = gsap.timeline();

function time(){
    let initialTime = 0;
    setInterval(()=>{
        initialTime += Math.floor(Math.random()*20);
        if(initialTime < 100){
            document.querySelector('#loader h1').innerHTML = initialTime + '%';
        }else{
            initialTime = 100;
            document.querySelector('#loader h1').innerHTML = initialTime + '%';
        }
    },150);
}
timeLine.to('#loader .head',{
    y:-50,
    repeat:-1,
    delay:.5,
    duration:.5,
    yoyo:true
})
timeLine.to("#loader h1",{
    delay:0.5,
    duration:1,
    // onStart:time()
})
timeLine.to("#loader",{
    top:"-100vh",
    delay:0.5,
    duration:1.5
})

function checkWindowSize() {
    const firstCard = document.getElementById('firstCard');
    const lastCard = document.getElementById('lastCard');
    const secondCard = document.getElementById('secondCard');
    const thirdCard = document.getElementById('thirdCard');
    const cpy_div = document.getElementById('cpy-div');
    const for_mobile_device = document.getElementById('for-mobile-device');
    const god_div = document.getElementById('god-div');
    const apply = document.querySelector('.apply');
    const login = document.querySelector('.login');
    const dropdown = document.getElementById('dropdown');
    const dropdown2 = document.getElementById('dropdown2');
    const dropdown_menu = document.querySelector('.dropdown-menu');
    const add = document.getElementById('add');
    const jkj = document.getElementById('jkj');
    const dropdown_menu2 = document.getElementById('dropdown-menu2');
    const blankSpace_forMovile_devices = document.querySelector('.blankSpace-forMovile-devices');
    
    if (window.innerWidth <= 1320) {
        if(cpy_div){
            cpy_div.style.display = 'flex';
        }
        if(for_mobile_device){
            for_mobile_device.style.display = 'none';
        }
        if (firstCard) {
            firstCard.style.display = 'none';
        }
        if (lastCard) {
            lastCard.style.display = 'none';
        }
        if (secondCard) {
            secondCard.style.display = 'none';
        }
        if (thirdCard) {
            thirdCard.style.display = 'none';
        }
    } else {
        if (firstCard) {
            firstCard.style.display = 'grid';
        }
        if (lastCard) {
            lastCard.style.display = 'grid';
        }
        if(for_mobile_device){
            for_mobile_device.style.display = 'none';
        }
        if(cpy_div){
            cpy_div.style.display = 'none';
        }
        if(for_mobile_device){
            for_mobile_device.style.display = 'none';
        }
    }
    if(window.innerWidth < 1263){
        if(dropdown){
            dropdown.style.display = 'grid';
        }
        if(apply){
            apply.style.display = 'none';
        }
        if(login){
            login.style.display = 'none';
        }
    }else{
        if(dropdown){
            dropdown.style.display = 'none';
            
        }
        if(apply){
            apply.style.display = 'grid';
        }
        if(login){
            login.style.display = 'grid';
        }
    }
    if(window.innerWidth > 895){
        if(dropdown2){
            dropdown2.style.display = 'none';
        }
        if(add){
            add.style.display = 'flex';
            add.style.alignItems = 'center';
            add.style.justifyContent = 'center';
        }
        if(jkj){
            jkj.style.display = 'flex';
        }
    }else{
        if(dropdown2){
            dropdown2.style.display = 'grid';
            
        }
        
        if(dropdown_menu2){
            dropdown_menu2.style.display = 'flex';
            dropdown_menu2.style.flexDirection = 'column';
            dropdown_menu2.style.padding = '0 0';
            
            
        }
        if(add){
            add.style.display = 'none';
        }
        if(jkj){
            jkj.style.display = 'none';
        }
    }
    if(window.innerWidth < 838){
        if(cpy_div){
            cpy_div.style.display = 'none';
        }
        if(for_mobile_device){
            for_mobile_device.style.display = 'grid';
        }
        if(god_div){
            god_div.style.display = 'none';
        }
    }
    if(window.innerWidth >= 837){
        if(blankSpace_forMovile_devices){
            blankSpace_forMovile_devices.style.display = 'none';
        }else{
            if(blankSpace_forMovile_devices){
                blankSpace_forMovile_devices.style.display = 'flex';
            }
            // if(lastCard){
            //     lastCard.style.display = 'none !important';
            // }
        }
    }
    if(window.innerWidth < 413){
        if(blankSpace_forMovile_devices){
            blankSpace_forMovile_devices.style.hight = '90vh';
        }else{
            if(blankSpace_forMovile_devices){
                blankSpace_forMovile_devices.style.hight = '110vh'
            }
        }
    }
}

window.addEventListener('resize', checkWindowSize);
window.addEventListener('load', checkWindowSize);

const btn = document.querySelector('.btn');
const dropdown2 = document.getElementById('dropdown2');
dropdown2.addEventListener('click',()=>{
    const dropdown_menu2 = document.getElementById('dropdown-menu2');
    dropdown_menu2.style.display = 'grid';
    // dropdown_menu2.style.flexDirection = 'column';
});
