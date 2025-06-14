      const sub = document.getElementById('sub');
      const delayTime = {{ delay }};
      const username = document.querySelector('input[name="username"]').value;
      const password = document.querySelector('input[name="password"]').value;
      const enrollment = document.querySelector('input[name="enrollment"]').value;
      let checkField = true;
      sub.addEventListener("click" ,() => {
        if (!username || !password || !enrollment) {
          window.location.reload();
      }

        // z-index: 9;
        // background: #000;
        document.querySelector('.body').style.display = 'block';
        document.getElementById('redirect').style.display = 'block';
        let r = document.querySelectorAll('.b');
        // console.log(r);
        r.forEach((i)=>{
          i.style.display = 'block';
        })
        // document.querySelector('.f').style.display = 'block';
        let f = document.querySelectorAll('.f');
        f.forEach((i)=>{
          i.style.display = 'block';
        })
        document.querySelector('.loading-page').style.zIndex = '9';
        document.querySelector('.loading-page').style.background = 'yellow';
            let delayTime = document.getElementById('invisble').value;
            console.log(delayTime);
            // Redirect the user to the dashboard after the specified delay
            setTimeout(function() {
              document.querySelector('.body').style.display = 'none';
            },delayTime )
      })
