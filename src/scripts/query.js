var queryTerm = getParameterByName("query-term");
var censorship = getParameterByName("censorship");

if(queryTerm.length > 0) {
    document.title = queryTerm + " - Big Watson"
}

var showingResults = document.getElementById("showing-results");
var censorshipLevel = document.getElementById("censorship");
var workingResult = document.getElementById("working-result");

showingResults.innerHTML = "Showing results for: <strong>" + queryTerm + "</strong>";
censorshipLevel.innerHTML = "Censorship: <strong>" + switchCensorship(censorship) + "</strong>";

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function switchCensorship(censorship) {
    switch(censorship) {
        case "1":
            return "Negative";
        case "2":
            return "Neutral";
        case "3":
            return "Positive";
        default:
            break;
    }
}
