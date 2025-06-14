console.log("hello")
document.querySelectorAll("#receipt-viewer").forEach(btn => {
    btn.addEventListener("click",function(){
        let semester = this.getAttribute("data-sem"); 
        console.log(semester);
        fetch(`/make-receipt-url?semester=${encodeURIComponent(semester)}`,{
            method: "GET",
            headers:{
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if(data.error){
                // console.log("MSG => " + data.error)
                alert("You Have not paid yet for this semester...");
            }else{
                window.location.href = data.url;
            }
        })
        .catch(error => console.error(error));
    })
});

