async function getDetails() {
  const deviceType = document.getElementById("deviceType").value;
  const rx = document.getElementById("rxInput").value.trim();

  if (!rx) {
    document.getElementById("output").innerHTML = `<p style="color:red;">Please enter RX input.</p>`;
    return;
  }

  document.getElementById("output").innerHTML = `<p>Processing...</p>`;

  try {
    const res = await fetch("/get_details", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ device_type: deviceType, rx })
    });

    const data = await res.json();

    document.getElementById("output").innerHTML = `
      <p><strong>Status:</strong> ${data.Status}</p>
      <p><strong>Device Status:</strong> ${data["Device Status"]}</p>
      <p><strong>Device Status Message:</strong> ${data["Device Status Message"]}</p>
      <p><strong>Device Percentage:</strong> ${data["Device Percentage"]}</p>
      <p><strong>Firmware Version:</strong> ${data["Firmware Version"]}</p>
    `;
  } catch (err) {
    document.getElementById("output").innerHTML = `<p style="color:red;">Server not responding. Try again later.</p>`;
  }
}

function splitData() {
  const input = document.getElementById("splitInput").value.trim().replace(/\s+/g, '');
  const outputDiv = document.getElementById("splitOutput");

  if (!input) {
    outputDiv.innerHTML = `<p style="color:red;">Please enter data to split.</p>`;
    return;
  }

  const parts = input.match(/.{1,2}/g) || [];

  let html = "";
  parts.forEach((val, idx) => {
    html += `
      <div class="split-box">
        <span class="index">#${idx}</span>
        <span class="value">${val}</span>
      </div>
    `;
  });

  outputDiv.innerHTML = html || "<p>No data found.</p>";
}

/* 🔹 Reset Functions */
function resetDetails() {
  document.getElementById("rxInput").value = "";
  document.getElementById("output").innerHTML = `<p><em>Result will appear here...</em></p>`;
}

function resetSplit() {
  document.getElementById("splitInput").value = "";
  document.getElementById("splitOutput").innerHTML = `<p><em>Split results will appear here...</em></p>`;
}
