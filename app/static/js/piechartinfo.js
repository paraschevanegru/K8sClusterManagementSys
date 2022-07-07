Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Preluam elmentul pentru pie chart din HTMl dupa id-ul corespunzator 
var ctworkload = document.getElementById("WorkloadPieChart");
var ctconfiguration = document.getElementById("ConfigurationPieChart");
var ctnetwork = document.getElementById("NetworkPieChart");
var ctstorage = document.getElementById("StoragePieChart");

// Preluam obiectele pe care vrem sa le vizualizam in pie chart din HTMl dupa id-ul corespunzator 
var pods = document.getElementById("pods").innerHTML;
var deployments = document.getElementById("deployments").innerHTML;
var daemonsets = document.getElementById("daemonsets").innerHTML;
var statefulsets = document.getElementById("statefulsets").innerHTML;
var replicasets = document.getElementById("replicasets").innerHTML;
var jobs = document.getElementById("jobs").innerHTML;
var cronjobs = document.getElementById("cronjobs").innerHTML;
var configmaps = document.getElementById("configmaps").innerHTML;
var secrets = document.getElementById("secrets").innerHTML;
var services = document.getElementById("services").innerHTML;
var endpoints = document.getElementById("endpoints").innerHTML;
var ingresses = document.getElementById("ingresses").innerHTML;
var volumeclaims = document.getElementById("volumeclaims").innerHTML;
var volumes = document.getElementById("volumes").innerHTML;
var storageclasses = document.getElementById("storageclasses").innerHTML;

// Pie chart pentru obiectele din Workload
var WorkloadPieChart = new Chart(ctworkload, {
    type: 'doughnut',
    data: {
        labels: ["Pods", "Deployments", "DaemonSets", "StatefulSets", "Replica Sets", "Jobs", "CronJobs"],
        datasets: [{
            data: [this.pods, this.deployments, this.daemonsets, this.statefulsets, this.replicasets, this.jobs, this.cronjobs],
            backgroundColor: ['#1cc88a', '#4e73df', '#36b9cc', '#7d1cc8', '#174980', '#3da63f', '#d19649'],
            hoverBackgroundColor: ['#17a673', '#2e59d9', '#2c9faf', '#521780', '#0f2d4d', '#216122', '#634721'],
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    },
    options: {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
        },
        legend: {
            display: false
        },
        cutoutPercentage: 80,
    },
});

// Pie chart pentru obiectele din Configuration
var ConfigurationPieChart = new Chart(ctconfiguration, {
    type: 'doughnut',
    data: {
        labels: ["Config Maps", "Secrets"],
        datasets: [{
            data: [this.configmaps, this.secrets],
            backgroundColor: ['#db6232', '#c9cf21'],
            hoverBackgroundColor: ['#943915', '#8d9110'],
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    },
    options: {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
        },
        legend: {
            display: false
        },
        cutoutPercentage: 80,
    },
});

// Pie chart pentru obiectele din Network
var NetworkPieChart = new Chart(ctnetwork, {
    type: 'doughnut',
    data: {
        labels: ["Services", "Endpoints", "Ingresses"],
        datasets: [{
            data: [this.services, this.endpoints, this.ingresses],
            backgroundColor: ['#f0a911', '#0be353', '#b01ce6'],
            hoverBackgroundColor: ['#825b08', '#08782e', '#4b0963'],
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    },
    options: {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
        },
        legend: {
            display: false
        },
        cutoutPercentage: 80,
    },
});


// Pie chart pentru obiectele din Storage
var StoragePieChart = new Chart(ctstorage, {
    type: 'doughnut',
    data: {
        labels: ["Persistent Volume Claim", "Persistent Volumes", "Storage Classes"],
        datasets: [{
            data: [this.volumeclaims, this.volumes, this.storageclasses],
            backgroundColor: ['#d069f5', '#e86490', '#f25138'],
            hoverBackgroundColor: ['#643575', '#78374d', '#6e291f'],
            hoverBorderColor: "rgba(234, 236, 244, 1)",
        }],
    },
    options: {
        maintainAspectRatio: false,
        tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 15,
            yPadding: 15,
            displayColors: false,
            caretPadding: 10,
        },
        legend: {
            display: false
        },
        cutoutPercentage: 80,
    },
});