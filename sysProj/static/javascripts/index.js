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

