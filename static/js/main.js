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






//====================================================
// Arrays
//====================================================

let devEuiArr = [];
let fixedMsgPayload = {
    "7011 msg" : "000070110a0000040515000000010000020000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000",
    "Package Ver": "00",
    "Device F/W, H/W Ver": "01",
    "Reboot": "0200000000",
    "Reboot wait time(60 sec)": "033C0000",
    "Get img version/status": "04",
    "Delete upgraded img": "0500000000"
};
let msgPayload = {...fixedMsgPayload};
let fportArr = [1,2,10,11,12,203];

//====================================================
// Add DevEUI
//====================================================
refreshArrays();
function addDevEUI() {

    const value = document.getElementById("txtDevEUI").value.trim();

    if (value === "") {
        alert("Please enter DevEUI.");
        document.getElementById("txtDevEUI").focus();
        return;
    }

    if (devEuiArr.includes(value)) {
        alert("DevEUI already exists.");
        return;
    }

    devEuiArr.push(value);

    document.getElementById("txtDevEUI").value = "";

    refreshArrays();

}

//====================================================
// Add Payload
//====================================================

function addPayload() {

    const name = document.getElementById("txtPayloadName").value.trim();
    const value = document.getElementById("txtPayloadValue").value.trim();

    if (name === "") {
        alert("Please enter Payload Name.");
        document.getElementById("txtPayloadName").focus();
        return;
    }

    if (value === "") {
        alert("Please enter Payload Value.");
        document.getElementById("txtPayloadValue").focus();
        return;
    }

    if (msgPayload[name]) {
        alert("Payload Name already exists.");
        return;
    }

    msgPayload[name] = value;

    document.getElementById("txtPayloadName").value = "";
    document.getElementById("txtPayloadValue").value = "";

    refreshArrays();
}


//====================================================
// Add FPort
//====================================================

function addFport() {

    const value = document.getElementById("txtFport").value.trim();

    if (value === "") {
        alert("Please enter FPort.");
        document.getElementById("txtFport").focus();
        return;
    }

    if (isNaN(value)) {
        alert("FPort must be numeric.");
        return;
    }

    if (fportArr.includes(value)) {
        alert("FPort already exists.");
        return;
    }

    fportArr.push(value);

    document.getElementById("txtFport").value = "";

    refreshArrays();

}

//====================================================
// Refresh Dropdowns
//====================================================

function refreshArrays() {
    fillSelect("devEuiSelect", devEuiArr);
    fillPayloadSelect();
    fillSelect("fportSelect", fportArr);
    refreshPayloadTable();
}

//====================================================
// Fill Payload Dropdown
//====================================================

function fillPayloadSelect() {

    const select = document.getElementById("payloadSelect");

    select.innerHTML = "";

    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.text = "-- Select Payload --";
    select.appendChild(defaultOption);

    Object.keys(msgPayload).forEach(name => {

        const option = document.createElement("option");

        option.value = msgPayload[name];   // Actual payload
        option.text = name;                // Display name

        select.appendChild(option);

    });

}

//====================================================
// Fill Dropdown
//====================================================

function fillSelect(id, array) {

    const select = document.getElementById(id);

    select.innerHTML = "";

    // Default Option
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.text = "-- Select --";
    select.appendChild(defaultOption);

    array.forEach(item => {

        const option = document.createElement("option");

        option.value = item;
        option.text = item;

        select.appendChild(option);

    });

}

//====================================================
// Validate Form
//====================================================

function validateEnqueue() {

    const baseURL = document.getElementById("serverIP").value.trim();
    const BEARER_TOKEN  = document.getElementById("loginToken").value.trim();
    const dev_eui = document.getElementById("devEuiSelect").value;
    const payload = document.getElementById("payloadSelect").value;
    const fport = document.getElementById("fportSelect").value;

    if (baseURL === "") {
        alert("Server IP cannot be empty.");
        document.getElementById("serverIP").focus();
        return false;
    }

    if (BEARER_TOKEN === "") {
        alert("Token cannot be empty.");
        document.getElementById("loginToken").focus();
        return false;
    }

    if (devEuiArr.length === 0) {
        alert("Please add at least one DevEUI.");
        return false;
    }

    if (Object.keys(msgPayload).length === 0) {
        alert("Please add at least one Payload.");
        return false;
    }

    if (fportArr.length === 0) {
        alert("Please add at least one FPort.");
        return false;
    }

    if (dev_eui === "") {
        alert("Please select DevEUI.");
        document.getElementById("devEuiSelect").focus();
        return false;
    }

    if (payload === "") {
        alert("Please select Payload.");
        document.getElementById("payloadSelect").focus();
        return false;
    }

    if (fport === "") {
        alert("Please select FPort.");
        document.getElementById("fportSelect").focus();
        return false;
    }

    return true;

}

//====================================================
// Submit
//====================================================

function submitEnqueue() {

    if (!validateEnqueue()) {
        return;
    }

    const baseURL = document.getElementById("serverIP").value.trim();
    const BEARER_TOKEN  = document.getElementById("loginToken").value.trim();
    const dev_eui = document.getElementById("devEuiSelect").value;
    const PAYLOAD = document.getElementById("payloadSelect").value;
    const FPORT = document.getElementById("fportSelect").value;

    const url =
        `http://${baseURL}/enqueue?dev_eui=${encodeURIComponent(dev_eui)}&data=${encodeURIComponent(PAYLOAD)}&fport=${encodeURIComponent(FPORT)}`;

    console.log(url);

    alert("Generated URL:\n\n" + url);
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${BEARER_TOKEN}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        alert("Enqueue Successful");
    })
    .catch(error => {
        console.error(error);
        alert("Request Failed\n" + error.message);
    });

}

//====================================================
// Refresh Payload Table
//====================================================

function refreshPayloadTable() {

    const tbody = document.querySelector("#payloadTable tbody");

    tbody.innerHTML = "";

    for (const [name, value] of Object.entries(fixedMsgPayload)) {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${name}</td>
            <td>${value}</td>
        `;

        tbody.appendChild(row);
    }

}