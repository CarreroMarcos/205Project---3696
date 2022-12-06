
document.querySelectorAll('input[name="degreeType"]').forEach((elem) => {
    elem.addEventListener("change", function(event) {
        var ele = document.getElementsByName('degreeType');
        var b;
        for(i = 0; i < ele.length; i++) {
            if(ele[i].checked){
                b = ele[i].value;
            }
        }
        var temps = document.getElementsByClassName("tempNumber");
        if(b=="c"){
            for (var i = 0; i < temps.length; i++) {
                var f = temps[i].innerHTML;
                f = f.replace('°F','');
                f = (f - 32)/1.8;
                f = Math.round(f)
                temps[i].innerHTML = f + '°C';
            }
        }
        else{
            for (var i = 0; i < temps.length; i++) {
                var f = temps[i].innerHTML;
                f = f.replace('°C','');
                f = (f * 1.8) + 32;
                f = Math.round(f)
                temps[i].innerHTML =  f + '°F';
            }
        }
    });
  });

  function forecastType(){
    var v = document.getElementById("fType").value;
    var temps = document.getElementsByClassName("forecastBox");

    var t = document.getElementById("titleForecast");

    var info = document.getElementsByClassName("forecastWeather");
    if(v==14){
        for (var i = 0; i < info.length; i++) {
            info[i].style.display="none";
            info[i].style.visibility="hidden";
        }
        t.innerHTML="14-Day Forecast";
    }
    else{
        for (var i = 0; i < info.length; i++) {
            info[i].style.display="block";
            info[i].style.visibility="visible";
        }
        t.innerHTML="7-Day Forecast";
    }
    for (var i = 0; i < temps.length; i++) {
        if(i>=v){
            temps[i].style.display="none";
            temps[i].style.visibility="hidden";
        }
        else{
            temps[i].style.display="block";
            temps[i].style.visibility="visible";
        }
    }
  }