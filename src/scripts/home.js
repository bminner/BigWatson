var slider = document.getElementById("slider-outlook");
var expression = document.getElementById("outlook-expression");
expression.innerHTML = "<i id=\"outlook-expression\" class=\"fa fa-meh-o\" aria-hidden=\"true\"></i>";
changeSearchAction();

slider.oninput = function() {
    var sliderValue = this.value;
    changeSearchAction();

    if(sliderValue == 1) {
        expression.innerHTML = "<i id=\"outlook-expression\" class=\"fa fa-frown-o\" aria-hidden=\"true\"></i>";
    } else if(sliderValue == 2) {
        expression.innerHTML = "<i id=\"outlook-expression\" class=\"fa fa-meh-o\" aria-hidden=\"true\"></i>";
    } else if(sliderValue == 3) {
        expression.innerHTML = "<i id=\"outlook-expression\" class=\"fa fa-smile-o\" aria-hidden=\"true\"></i>";
    }
}

function changeSearchAction() {
    var sliderValue = slider.value;

    if(sliderValue == 1) {
        document["search-form"].action = "./results_negative.html";
    } else if(sliderValue == 2) {
        document["search-form"].action = "./results_neutral.html";
    } else if(sliderValue == 3) {
        document["search-form"].action = "./results_positive.html";
    }
}
