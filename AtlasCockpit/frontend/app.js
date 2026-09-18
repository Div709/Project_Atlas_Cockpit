async function updateTelemetry()
{
    try
    {
        const response =
            await fetch(
                "http://127.0.0.1:8000/telemetry"
            );

        const data =
            await response.json();

        // RPM

        document.getElementById("rpm").textContent =
            data.RPM ?? "0";

        // Engine Status

        const status =
            document.getElementById("status");

        status.textContent =
            data.STATE ?? "OFF";

        if (data.STATE === "RUNNING")
        {
            status.style.background =
                "#166534";
        }
        else if (data.STATE === "STARTING")
        {
            status.style.background =
                "#a16207";
        }
        else if (data.STATE === "SHUTTING OFF")
        {
            status.style.background =
                "#dc2626";
        }
        else
        {
            status.style.background =
                "#475569";
        }

        // Throttle

        const pot =
            Number(data.POT ?? 0);

        const throttlePercent =
            Math.round(
                (pot / 4095) * 100
            );

        document.getElementById("throttle-value").textContent =
            throttlePercent + "%";

        document.getElementById("throttle-bar").style.width =
            throttlePercent + "%";

        // Pitch & Roll

        const pitch =
            Number(data.PITCH ?? 0);

        const roll =
            Number(data.ROLL ?? 0);

        document.getElementById("pitch").textContent =
            pitch.toFixed(1) + "°";

        document.getElementById("roll").textContent =
            roll.toFixed(1) + "°";

        // Artificial Horizon

        const horizon =
            document.getElementById("horizon");

        horizon.style.transform =
            `translateY(${-pitch * 0.8}px) rotate(${-roll}deg)`;
    }
    catch(error)
    {
        console.log(error);
    }
}

updateTelemetry();

setInterval(
    updateTelemetry,
    50
);