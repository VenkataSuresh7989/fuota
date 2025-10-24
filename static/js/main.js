// ----------------------------
// Get Details
// ----------------------------
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

// ----------------------------
// Split Data
// ----------------------------
function splitData() {
  const input = document.getElementById("splitInput").value.trim().replace(/\s+/g, '');
  const outputDiv = document.getElementById("splitOutput");

  if (!input) {
    outputDiv.innerHTML = `<p style="color:red;">Please enter data to split.</p>`;
    return;
  }

  const parts = input.match(/.{1,2}/g) || [];
  outputDiv.innerHTML = parts.map((val, idx) => `
    <div class="split-box">
      <span class="index">#${idx}</span>
      <span class="value">${val}</span>
    </div>
  `).join("");
}

// ----------------------------
// Reset Functions
// ----------------------------
function resetDetails() {
  document.getElementById("rxInput").value = "";
  document.getElementById("output").innerHTML = `<p><em>Result will appear here...</em></p>`;
}

function resetSplit() {
  document.getElementById("splitInput").value = "";
  document.getElementById("splitOutput").innerHTML = `<p><em>Split results will appear here...</em></p>`;
}

// ----------------------------
// Load Status Options
// ----------------------------
async function loadMappings() {
  try {
    const res = await fetch("/status_options");
    const data = await res.json();

    document.getElementById("xprOptions").innerHTML = Object.entries(data["XPR Progress"])
      .map(([k,v]) => `<tr><td><strong>${k}</strong></td> <td>${v}</td></tr>`).join("");

    document.getElementById("hexOptions").innerHTML = Object.entries(data["Hex Binary"])
      .map(([k,v]) => `<tr><td><strong>${k}</strong></td> <td>${v}</td></tr>`).join("");
  } catch(err) {
    console.error("Failed to load status mappings:", err);
  }
}

loadMappings();


function validateInteger(input) {
  input.value = input.value.replace(/[^0-9]/g, ''); // allow only integers
}

function calculateLoopback() {
  const deviceCount = parseInt(document.getElementById("deviceCount").value) || 0;
  const count = parseInt(document.getElementById("count").value) || 0;
  const times = parseInt(document.getElementById("times").value) || 0;

  const output = document.getElementById("loopbackResult");

  if (deviceCount === 0 || count === 0 || times === 0) {
    output.innerHTML = `<p class="split-error">Please enter all values (only integers allowed).</p>`;
    return;
  }

  // Formula: (DeviceCount * 2 * Times) + ((DeviceCount * Count) * Times)
  const finalCount = (deviceCount * 2 * times) + ((deviceCount * count) * times);

  output.innerHTML = `
    <div class="result-box">
      <p><strong>Device Count:</strong> ${deviceCount}</p>
      <p><strong>Count:</strong> ${count}</p>
      <p><strong>No. of Times:</strong> ${times}</p>
      <h4>🔢 Final Result: <span class="final-count">${finalCount}</span></h4>
    </div>
  `;
}

function resetLoopback() {
  document.getElementById("deviceCount").value = "";
  document.getElementById("count").value = "";
  document.getElementById("times").value = "";
  document.getElementById("loopbackResult").innerHTML = `<p><em>Result will appear here...</em></p>`;
}

