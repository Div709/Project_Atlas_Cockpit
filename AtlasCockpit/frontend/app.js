async function updateTelemetry() {

    const response = await fetch("http://127.0.0.1:8000/telemetry");

    const data = await response.json();

    document.getElementById("rpm").textContent =
        data.rpm;

    const throttlePercent =
        Math.round((data.pot / 1023) * 100);

    document.getElementById("throttle-value").textContent =
        throttlePercent + "%";

    document.getElementById("throttle-bar").style.width =
        throttlePercent + "%";

    document.getElementById("status").textContent =
        data.state;
}

updateTelemetry();

setInterval(updateTelemetry, 50);
