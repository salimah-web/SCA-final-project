var dropdown = document.querySelector("nav .fa-bars");

var cancel = document.querySelector("nav .fa-times");

var button = document.querySelector("nav .dropdown");

function menu(){
    if(dropdown.style.display === "grid"){
        dropdown.style.display = "none";
        cancel.style.visibility = "hidden";

    }else{
        dropdown.style.display = "grid";
        cancel.style.visibility = "visible";
        dropdown.style.visibility = "hidden";
    }
    addEventListener("resize", function(){
        if(window.innerWidth > 700){
            dropdown.style.display = "none";
        cancel.style.visibility = "hidden";

        }
    })
}




