import {ScatterChart2D} from "./scatter_chart_2d"
import * as io from 'socket.io-client'
import * as $ from "jquery"
import * as moment from "moment";

let DEFAULT_CHART = "<canvas id=\"chart-name\" width=\"800\" height=\"450\"></canvas>";

let charts = {};

let socket_io = io('http://' + document.domain + ':' + location.port);
socket_io.on('connect', function () {
    socket_io.on("initial_values", get_initial_values);
    socket_io.emit('request_initial_values');
});

function handle_update(data) {
    let name = data[0];
    let x_y = data[1];
    if (!(name in charts)) {
        create_new_chart(name, [x_y])
    } else {
        charts[name].add_point_dataset_label(moment.unix(x_y[0]), x_y[1], name);
        charts[name].update();
    }
}

function get_initial_values(initial_data: { string: any }) {
    socket_io.removeListener("initial_values", get_initial_values);

    for (let name in initial_data) {
        let data = initial_data[name];
        create_new_chart(name, data)
    }

    socket_io.on("data_update", handle_update)
}

function create_new_chart(label: string, values) {
    let chart_name = "chart-" + label;
    $("#graphs").append(DEFAULT_CHART.replace("chart-name", chart_name));
    let chart = new ScatterChart2D(chart_name);
    chart.add_dataset(label);
    for (let x_y of values) {
        chart.add_point_dataset_label(moment.unix(x_y[0]), x_y[1], label);
    }
    chart.update();
    charts[label] = chart;
}