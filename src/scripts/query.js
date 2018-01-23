var queryString = decodeURIComponent(window.location.search);
queryString = queryString.substring(1);

var queryTerm = queryString.split("=")[1];

document.title = queryTerm + " - Big Watson"

var showingResults = document.getElementById("showing-results");
showingResults.innerHTML = "Showing results for: <strong>" + queryTerm + "</strong>";