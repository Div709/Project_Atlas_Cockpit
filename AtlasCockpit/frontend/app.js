async function updateTelemetry() {

    const response =
        await fetch("http://127.0.0.1:8000/telemetry");

    const data =
        await response.json();

    document.getElementById("rpm").textContent =
        data.rpm;

    document.getElementById("throttle-value").textContent =
        data.pot + "%";

    document.getElementById("throttle-bar").style.width =
        data.pot + "%";

    document.getElementById("status").textContent =
        data.state;
}

setInterval(updateTelemetry, 500);

updateTelemetry();