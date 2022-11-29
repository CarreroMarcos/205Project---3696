
  document.querySelectorAll('input[name="degreeType"]').forEach((elem) => {
    elem.addEventListener("change", function(event) {
      let degree = event.value;
      document.getElementById("tempNum").innerText = this.id;
    });
  });
