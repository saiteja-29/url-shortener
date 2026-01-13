async function shortenUrl() {
    const url = document.getElementById("urlInput").value;
    const days = document.getElementById("expirySelect").value;
    const error = document.getElementById("error");

    error.innerText = "";

    if (!url) {
        error.innerText = "Please enter a URL";
        return;
    }

    const payload = {
        original_url: url,
        expires_in_days: days ? parseInt(days) : null
    };

    try {
        const response = await fetch("/shorten", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const data = await response.json();
            error.innerText = data.detail || "Error occurred";
            return;
        }

        const data = await response.json();

        const result = document.getElementById("result");
        const shortUrl = document.getElementById("shortUrl");

        shortUrl.href = data.short_url;
        shortUrl.innerText = data.short_url;

        result.classList.remove("hidden");

    } catch (err) {
        error.innerText = "Server error";
    }
}

function copyUrl() {
    const shortUrl = document.getElementById("shortUrl").innerText;
    navigator.clipboard.writeText(shortUrl);
    alert("Copied!");
}
