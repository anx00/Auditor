/** VIS.JS AND MAPPING MODULE **/

async function getData() {
    var response = await fetch('/api/devices');
    return await response.json()
}

// api url
const api_url1 =
    '/api/aps';
const api_url2 =
    '/api/clients';
const api_url3 =
    '/api/devices';


// Defining async function
async function getapi(url1, url2) {

    // Storing response
    const response = await fetch(url1);
    const response2 = await fetch(url2);

    // Storing data in form of JSON
    var data = await response.json();
    var data2 = await response2.json();

    show(data, data2)
}

// Calling that async function
getapi(api_url1, api_url2, api_url3);

function show(data1, data2) {
    var DIR = "../img/";
    var nodes = [];
    var edges = [];
    var container = document.getElementById("mynetwork");
    /*container.style.background = "url('https://image.freepik.com/free-vector/abstract-connections-banner-design_1048-10068.jpg')"*/
    nodes.push({
            id: 0,
            image: home,
            shape: "image"
        },
    )
    for (let device of data1) {
        var style
        if (`${device.deauth_frames}` > 0) {
            style = "red"
        } else {
            style = "black"
        }
        nodes.push({
                id: `${device.id}`,
                ssid: `${device.essid}`,
                bssid: `${device.bssid}`,
                encriptacion: `${device.encriptacion}`,
                canal: `${device.canal}`,
                fspl: `${device.fspl}`,
                deauth: `${device.deauth_frames}`,
                label: `${device.essid}`,
                font: {
                    color: style,
                },
                manufacturer: `${device.manufacturer}`,
                type: "ap",
                image: ap,
                shape: "image"
            },
        )
        edges.push({
            from: 0,
            length: `${device.fspl}` * 2,
            to: `${device.id}`,
            /*label: `~${device.fspl}m`,*/
            color: {
                opacity: 0
            },
        });
        for (let client of data2) {
            if (`${client.connected_to}` === `${device.bssid}`) {
                nodes.push({
                        id: `${device.id}` + "-" + `${client.id}`,
                        mac: `${client.mac_device}`,
                        vendor: `${client.manufacturer}`,
                        label: `${client.mac_device}`,
                        type: "device",
                        image: dispositivo,
                        shape: "image",
                    },
                )
                edges.push({
                    from: `${device.id}` + "-" + `${client.id}`,
                    length: 10,
                    to: `${device.id}`,
                    color: {
                        color: '#5B707C',
                        highlight: '#A22'
                    },
                })
            }
        }

    }
    //var nodes = new vis.DataSet(datos)

    var data = {
        nodes: nodes,
        edges: edges
    };

    var options = {
        nodes: {font: {strokeWidth: 0}},
        edges: {font: {strokeWidth: 0}},
        physics: {
            enabled: true,
        },
        interaction: {
            hover: true
        },
        layout: {
            improvedLayout: true,
        }
    }

    var network = new vis.Network(container, data, options);

    function getNode(option) {
        for (var i = 0; i < nodes.length; i++) {
            if (option === nodes[i].id) {
                return nodes[i];
            }
        }
    }

    network.on("stabilizationIterationsDone", function () {
        //network.setOptions({physics: false});
    });

    network.on('blurNode', function () {
        $('#mynetwork').css('cursor', 'default');
    });

    network.on('hoverNode', function (properties) {
        $('#mynetwork').css('cursor', 'pointer');
    });

    network.on('zoom', function () {
        $("#menuOperation").hide();
        $("#menuOperation").empty();//Empty the div after removal
    });

    network.on('dragStart', function (properties) {
        var clickNodeList = getNode(properties.nodes[0]);
        if (typeof (clickNodeList) != "undefined") {
            network.setOptions({physics: true})
        }
    })

    network.on('dragEnd', function (properties) {
        var clickNodeList = getNode(properties.nodes[0]);
        if (typeof (clickNodeList) != "undefined") {
            network.setOptions({physics: false})
        }
    });

    network.on('hold', function (properties) {
        network.setOptions({physics: true})
    })

    network.on('click', function (properties) {
        $("#menuOperation").hide();
        $("#menuOperation").empty();//Empty the div after removal
        var clickNodeList = getNode(properties.nodes[0]);
        if (typeof (clickNodeList) == "undefined") {
            network.setOptions({physics: true})
        }
        var $ul
        if (typeof (clickNodeList) == "undefined") {
            $('#menuOperation').hide();
        } else {
            if (clickNodeList.type === "ap") {
                if (clickNodeList.font.color === "black") {
                    var test = $('<button/>',
                        {
                            text: 'VER',
                            click: function () {
                                window.open(clickNodeList.id + '/informacion');
                            }
                        });
                    $ul = "<ul>"
                        + "<li><span style='color: darkgrey'>ID：</span>" + clickNodeList.id + "</li>"
                        + "<li><span style='color: darkgrey'>SSID：</span>" + clickNodeList.ssid + "</li>"
                        + "<li><span style='color: darkgrey'>BSSID：</span>" + clickNodeList.bssid + "</li>"
                        + "<li><span style='color: darkgrey'>SECURITY：</span>" + clickNodeList.encriptacion + "</li>"
                        + "<li><span style='color: darkgrey'>CHANNEL：</span>" + clickNodeList.canal + "</li>"
                        + "<li><span style='color: darkgrey'>DISTANCE：~</span>" + clickNodeList.fspl + "m" + "</li>"
                        + "<li><span style='color: darkgrey'>VENDOR：</span>" + clickNodeList.manufacturer + "</li>"
                        + "</ul>"
                } else {
                    var test = $('<button/>',
                        {
                            text: 'VER',
                            click: function () {
                                window.open(clickNodeList.id + '/informacion');
                            }
                        });
                    $ul = "<ul>"
                        + "<li><span style='color: darkgrey'>ID：</span>" + clickNodeList.id + "</li>"
                        + "<li><span style='color: darkgrey'>SSID：</span>" + clickNodeList.ssid + "</li>"
                        + "<li><span style='color: darkgrey'>BSSID：</span>" + clickNodeList.bssid + "</li>"
                        + "<li><span style='color: darkgrey'>SECURITY：</span>" + clickNodeList.encriptacion + "</li>"
                        + "<li><span style='color: darkgrey'>CHANNEL：</span>" + clickNodeList.canal + "</li>"
                        + "<li><span style='color: darkgrey'>DISTANCE：~</span>" + clickNodeList.fspl + "m" + "</li>"
                        + "<li><span style='color: darkgrey'>VENDOR：</span>" + clickNodeList.manufacturer + "</li>"
                        + "<li style='color: red'>DEAUTH FRAMES DETECTED：" + clickNodeList.deauth + "</li>"
                        + "</ul>"
                }


            } else if (clickNodeList.type === "device") {
                $ul = "<ul>"
                    + "<li><span style='color: darkgrey'>ID：</span>" + clickNodeList.id + "</li>"
                    + "<li><span style='color: darkgrey'>MAC：</span>" + clickNodeList.mac + "</li>"
                    + "<li><span style='color: darkgrey'>VENDOR：</span>" + clickNodeList.vendor + "</li>"
                    + "</ul>";
            }
            $("#menuOperation").append($ul);
            $("#menuOperation").append(test);
            $('#menuOperation').css({
                'display': 'block',
                'left': properties.event.center.x + 15,
                'top': properties.event.center.y + 15
            });
            $("#divHoverNode").hide();
        }
    });
    network.on("stabilizationProgress", function (params) {
        $('#mynetwork').css('cursor', 'wait'); //
    })
    network.once("stabilizationIterationsDone", function () {
        $('#mynetwork').css('cursor', 'default'); //
    })
}