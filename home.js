var slider = document.getElementById("slider-outlook");
var expression = document.getElementById("outlook-expression");
expression.innerHTML = "<i id=\"outlook-expression\" class=\"fa fa-meh-o\" aria-hidden=\"true\"></i>";

slider.oninput = function() {
    var sliderValue = this.value;

    if(sliderValue == 1) {
        expression.innerHTML = "<i id=\"outlook-expression\" class=\"fa fa-frown-o\" aria-hidden=\"true\"></i>";
    } else if(sliderValue == 2) {
        expression.innerHTML = "<i id=\"outlook-expression\" class=\"fa fa-meh-o\" aria-hidden=\"true\"></i>";
    } else if(sliderValue == 3) {
        expression.innerHTML = "<i id=\"outlook-expression\" class=\"fa fa-smile-o\" aria-hidden=\"true\"></i>";
    }
}
