var cursor;

/** TABLES SORTING VER_APS **/
function sortTable(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("maintable");
    switching = true;
    //Set the sorting direction to ascending:
    dir = "asc";
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
        //start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /*Loop through all table rows (except the
        first, which contains table headers):*/
        for (i = 1; i < (rows.length - 1); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            /*Get the two elements you want to compare,
            one from current row and one from the next:*/
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            /*check if the two rows should switch place,
            based on the direction, asc or desc:*/
            if (n === 0 || n === 3 || n === 4) {

                if (n === 3) {
                    if (dir === "desc") {
                        if (Number(x.innerHTML) > Number(y.innerHTML)) {
                            shouldSwitch = true;
                            break;
                        }
                    } else if (dir === "asc") {
                        if (Number(x.innerHTML) < Number(y.innerHTML)) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                } else {
                    if (dir === "asc") {
                        if (Number(x.innerHTML) > Number(y.innerHTML)) {
                            shouldSwitch = true;
                            break;
                        }
                    } else if (dir === "desc") {
                        if (Number(x.innerHTML) < Number(y.innerHTML)) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                }
            } else {
                if (dir === "asc") {
                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                } else if (dir === "desc") {
                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                }
            }
        }
        if (shouldSwitch) {
            /*If a switch has been marked, make the switch
            and mark that a switch has been done:*/
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            //Each time a switch is done, increase this count by 1:
            switchcount++;
        } else {
            /*If no switching has been done AND the direction is "asc",
            set the direction to "desc" and run the while loop again.*/
            if (switchcount === 0 && dir === "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}


/** TABLES SORTING VER_DISPOSITIVOS **/

function sortDevices(n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("maintable2");
    switching = true;
    //Set the sorting direction to ascending:
    dir = "asc";
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
        //start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /*Loop through all table rows (except the
        first, which contains table headers):*/
        for (i = 1; i < (rows.length - 1); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            /*Get the two elements you want to compare,
            one from current row and one from the next:*/
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            /*check if the two rows should switch place,
            based on the direction, asc or desc:*/
            if (n === 0) {
                if (dir === "asc") {
                    if (Number(x.innerHTML) > Number(y.innerHTML)) {
                        shouldSwitch = true;
                        break;
                    }
                } else if (dir === "desc") {
                    if (Number(x.innerHTML) < Number(y.innerHTML)) {
                        shouldSwitch = true;
                        break;
                    }
                }
            } else if (n === 1) {
                if (dir === "asc") {
                    if (Number(x.innerHTML.split('.')[3]) > Number(y.innerHTML.split('.')[3])) {
                        shouldSwitch = true;
                        break;
                    }
                } else if (dir === "desc") {
                    if (Number(x.innerHTML.split('.')[3]) < Number(y.innerHTML.split('.')[3])) {
                        shouldSwitch = true;
                        break;
                    }
                }
            } else {
                if (dir === "asc") {
                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                } else if (dir === "desc") {
                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                        // If so, mark as a switch and break the loop:
                        shouldSwitch = true;
                        break;
                    }
                }
            }
        }
        if (shouldSwitch) {
            /*If a switch has been marked, make the switch
            and mark that a switch has been done:*/
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            //Each time a switch is done, increase this count by 1:
            switchcount++;
        } else {
            /*If no switching has been done AND the direction is "asc",
            set the direction to "desc" and run the while loop again.*/
            if (switchcount === 0 && dir === "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}


/* submit data */
$('#boton-start').click(function () {
    $('#formulario').submit()
});

/** COLLAPSIBLE BOTON DEAUTH **/

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
}


/** FUNCIONALIDAD MONITOR CON CAMBIO DE BOTON START-STOP*/
function updateAPS() {
    $("#table-container").load(window.location.href + " #table-container");
    $("#tabla_eventos").load(window.location.href + " #table_body");
    $("#mynetwork").load(window.location.href + " #mynetwork");
}

$('#boton-start').click(function () {
    document.getElementById("loader").style.display = "block"
    document.getElementById("boton-start").style.display = "none"
    document.getElementById("boton-stop").style.display = "block"
    refresh = setInterval(function () {
        updateAPS()
    }, 50);
    /*hacer un hide y mostrar el stop cuando sea tal */
});

function update() {
    document.getElementById("loader").style.display = "block"
    document.getElementById("boton-start").style.display = "none"
    document.getElementById("boton-stop").style.display = "block"
    setInterval(function () {
        updateAPS()
    }, 10);
}

$('#boton-stop').click(function () {
    //clearInterval(refresh);
    document.getElementById("boton-stop").style.display = "none"
    document.getElementById("boton-start").style.display = "block"
    document.getElementById("loader").style.display = "none"
});

/**SCAN PERSONAL AP **/
$('#upvote').click(function () {
    var scan_time = $('#time').find(":selected").val();
    $.ajax({
        url: window.location.href,
        type: 'POST',
        data: {"scan_time": scan_time},
    });
    alert("Scanning another network will stop this scan from working.")
    location.reload()
});

function collapse(element) {
    element.classList.toggle("active");
    var content = element.nextElementSibling;
    if (content.style.display === "block") {
        content.style.display = "none";
    } else {
        content.style.display = "block";
    }
}

/** RSSI COLOR **/

rssi_color = document.getElementsByClassName('rssi')
for (var i = 0; i < rssi_color.length; i++) {
    console.log(rssi_color[i].innerHTML)
    if (rssi_color[i].innerHTML <= -80) {
        rssi_color[i].style.color = "red"
    }
    else if (rssi_color[i].innerHTML <= -70) {
        rssi_color[i].style.color = "orange"
    }
    else if (rssi_color[i].innerHTML <= -50) {
        rssi_color[i].style.color = "limegreen"
    }
    else {
        rssi_color[i].style.color = "green"
    }
}
