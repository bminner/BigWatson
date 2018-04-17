/**
 * @author Kurtis
 */
window.onload = function () {
    var tryitSlider = document.getElementById("tryit-slider");
    var tryitExpression = document.getElementById("effect-text");

    tryitSlider.oninput = function() {
        var sliderValue = this.value;
    
        if (sliderValue == 1) {
            tryitExpression.innerHTML = "negative";
        } else if (sliderValue == 2) {
            tryitExpression.innerHTML = "neutral";
        } else if (sliderValue == 3) {
            tryitExpression.innerHTML = "positive";
        }
    }
}