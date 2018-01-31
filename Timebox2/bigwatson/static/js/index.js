window.onload = function () {
    var slider = document.getElementById("effect-slider");
    var expression = document.getElementById("effect-expression");

    slider.oninput = function() {
        var sliderValue = this.value;
    
        if (sliderValue == 1) {
            expression.innerHTML = "<i class=\"fa fa-frown-o\" aria-hidden=\"true\"></i>";
        } else if (sliderValue == 2) {
            expression.innerHTML = "<i class=\"fa fa-meh-o\" aria-hidden=\"true\"></i>";
        } else if (sliderValue == 3) {
            expression.innerHTML = "<i class=\"fa fa-smile-o\" aria-hidden=\"true\"></i>";
        }
    }
}