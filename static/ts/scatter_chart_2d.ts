import Chart = require("chart.js");

export class ScatterChart2D {
    TYPE = "scatter";
    DEFAULT_OPTIONS = {
        animation: {
            duration: 0, // general animation time
        },
        hover: {
            animationDuration: 0, // duration of animations when hovering an item
        },
        responsiveAnimationDuration: 0, // animation duration after a resize
        elements: {
            line: {
                tension: 0, // disables bezier curves
            }
        },
        responsive: false,
        scales: {
            xAxes: [{
                type: 'time'
            }]
        },
    };

    _chart: Chart;

    constructor(element_id: string) {
        this._chart = new Chart(<HTMLCanvasElement>document.getElementById(element_id),
            {
                type: this.TYPE
                , data: {datasets: []}
                , options: this.DEFAULT_OPTIONS
            }
        );
    }

    dataset_exists(dataset_label: string) {
        let dataset_id = this._chart.data.datasets.findIndex(
            (dataset) => {
                return dataset.label === dataset_label
            }
        );
        return -1 === dataset_id;
    }

    add_dataset(label: string) {
        this._chart.data.datasets.push(
            {
                data: [],
                showLine: true,
                label: label,
                fill: false
            }
        )
    }

    add_point_dataset_id(x_val, y_val, dataset_id: number) {
        this._chart.data.datasets[dataset_id].data.push({x: x_val, y: y_val});
    }

    add_point_dataset_label(x_val, y_val, dataset_label: string) {
        let dataset_id = this._chart.data.datasets.findIndex(
            (dataset) => {
                return dataset.label === dataset_label
            }
        );
        this.add_point_dataset_id(x_val, y_val, dataset_id);
    }

    update() {
        this._chart.update()
    }
}