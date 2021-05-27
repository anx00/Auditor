/** CHART **/
let chart
//Initial and End dates of scan
date_created = $('#date_created').text()
date_finished = $('#date_finished').text()

/** Intentos de conseguir valores únicos del array **/

/*function onlyUnique(value, index, self) {
  return self.indexOf(value) === index;
}

var unique = label_deauth.filter(onlyUnique);
console.log(unique)

var unique2 = [...new Set(label_deauth)]*/

function get_occurences(arr) {
    var a = [],
        b = [],
        prev;

    arr.sort();
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] !== prev) {
            a.push(arr[i]);
            b.push(1);
        } else {
            b[b.length - 1]++;
        }
        prev = arr[i];
    }

    return [a, b];
}

$(document).ready(function () {
    /** Deauth frames chart **/
    label_deauth = []
    $('.deauth_frames_time').each(function () {
        if (($(this).text() > date_created) && $(this).text() < date_finished) {
            label_deauth.push($(this).text())
        }

    })
    var deauth_data = get_occurences(label_deauth);

    deauth_data[0].unshift(date_created)
    deauth_data[0].push(date_finished)
    const labels_deauth = deauth_data[0]


    deauth_data[1].unshift(0)
    deauth_data[1].push(0)
    const data_label_deauth = deauth_data[1]

    var deauth_chart = new Chart(
        document.getElementById('deauth_chart').getContext('2d'),
        config = {
            type: 'line',
            data: {
                labels: labels_deauth,
                datasets: [{
                    backgroundColor: 'rgb(2, 133, 191)',
                    borderColor: 'rgb(2, 133, 191)',
                    data: data_label_deauth,
                },
                ]
            },
            options: {
                plugins: {
                    legend: {
                        display: false,
                    }
                },
                scales: {
                    x: {
                        display: true
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Frames',
                        },
                    }
                },
            }
        }
    );

    /** Auth frames chart **/
    label_auth = []
    $('.auth_frames_time').each(function () {
        if (($(this).text() > date_created) && $(this).text() < date_finished) {
            label_auth.push($(this).text())
        }
    })
    var auth_data = get_occurences(label_auth);

    auth_data[0].unshift(date_created)
    auth_data[0].push(date_finished)
    const labels_auth = auth_data[0]


    auth_data[1].unshift(0)
    auth_data[1].push(0)
    const data_label_auth = auth_data[1]

    var auth_chart = new Chart(
        document.getElementById('auth_chart').getContext('2d'),
        config = {
            type: 'line',
            data: {
                labels: labels_auth,
                datasets: [{
                    backgroundColor: 'rgb(2, 133, 191)',
                    borderColor: 'rgb(2, 133, 191)',
                    data: data_label_auth,
                },
                ]
            },
            options: {
                plugins: {
                    legend: {
                        display: false,
                    }
                },
                scales: {
                    x: {
                        display: true
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Frames',
                        },
                    }
                },
            }
        }
    );

    /** Disas frames chart **/
    label_disas = []
    $('.disas_frames_time').each(function () {
        if (($(this).text() > date_created) && $(this).text() < date_finished) {
            label_disas.push($(this).text())
        }
    })
    var disas_data = get_occurences(label_disas);

    disas_data[0].unshift(date_created)
    disas_data[0].push(date_finished)
    const labels_disas = disas_data[0]


    disas_data[1].unshift(0)
    disas_data[1].push(0)
    const data_label_disas = disas_data[1]


    var disas_chart = new Chart(
        document.getElementById('disas_chart').getContext('2d'),
        config = {
            type: 'line',
            data: {
                labels: labels_disas,
                datasets: [{
                    backgroundColor: 'rgb(2, 133, 191)',
                    borderColor: 'rgb(2, 133, 191)',
                    data: data_label_disas,
                },
                ]
            },
            options: {
                plugins: {
                    legend: {
                        display: false,
                    }
                },
                scales: {
                    x: {
                        display: true
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Frames',
                        },
                    }
                },
            }
        }
    );

    /** AssosReq frames chart **/
    label_assosreq = []
    $('.assosreq_frames_time').each(function () {
        if (($(this).text() > date_created) && $(this).text() < date_finished) {
            label_assosreq.push($(this).text())
        }
    })
    var assosreq_data = get_occurences(label_assosreq);

    assosreq_data[0].unshift(date_created)
    assosreq_data[0].push(date_finished)
    const labels_assosreq = assosreq_data[0]


    assosreq_data[1].unshift(0)
    assosreq_data[1].push(0)
    const data_label_assosreq = assosreq_data[1]


    var assosreq_chart = new Chart(
        document.getElementById('assosreq_chart'),
        config = {
            type: 'line',
            data: {
                labels: labels_assosreq,
                datasets: [{
                    backgroundColor: 'rgb(2, 133, 191)',
                    borderColor: 'rgb(2, 133, 191)',
                    data: data_label_assosreq,
                },
                ]
            },
            options: {
                plugins: {
                    legend: {
                        display: false,
                    }
                },
                scales: {
                    x: {
                        display: true,
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Frames',
                        },
                    }
                },
            }
        }
    );

    /** AssosResp frames chart **/
    label_assosresp = []
    $('.assosresp_frames_time').each(function () {
        if (($(this).text() > date_created) && $(this).text() < date_finished) {
            label_assosresp.push($(this).text())
        }
    })
    var assosresp_data = get_occurences(label_assosresp);
    console.log('[' + assosresp_data[0] + ']', '[' + assosresp_data[1] + ']')

    assosresp_data[0].unshift(date_created)
    assosresp_data[0].push(date_finished)
    const labels_assosresp = assosresp_data[0]


    assosresp_data[1].unshift(0)
    assosresp_data[1].push(0)
    const data_label_assosresp = assosresp_data[1]


    var assosresp_chart = new Chart(
        document.getElementById('assosresp_chart').getContext('2d'),
        config = {
            type: 'line',
            data: {
                labels: labels_assosresp,
                datasets: [{
                    backgroundColor: 'rgb(2, 133, 191)',
                    borderColor: 'rgb(2, 133, 191)',
                    data: data_label_assosresp,
                },
                ]
            },
            options: {
                plugins: {
                    legend: {
                        display: false,
                    }
                },
                scales: {
                    x: {
                        display: true
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Frames',
                        },
                    }
                },
            }
        }
    );
});