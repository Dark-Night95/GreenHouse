const $ = s => document.querySelector(s);
const history = [], maxHistory = 12;
const plantNames = new Map();
const plantRecords = new Map();
const alertRecords = new Map();
const api = { dashboard: "/dashboard/", plants: "/plants/", sensors: "/sensors/", requirements: "/requirements/", alerts: "/alerts/", prediction: "/prediction/latest" };
const get = async (url, options) => {
  let response;
  try { response = await fetch(url, options); }
  catch (error) { throw new Error(`Could not reach ${url}. Open this page through the FastAPI server (usually http://127.0.0.1:8000/).`, { cause: error }); }
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`${url} returned HTTP ${response.status}${detail ? `: ${detail.slice(0, 180)}` : ""}`);
  }
  return response.json();
};
const value = (object, ...keys) => keys.map(key => object[key]).find(item => item !== undefined && item !== null);
const number = item => item === null || item === undefined ? "—" : Number(item).toFixed(1).replace(/\.0$/, "");
const safe = item => { const node = document.createElement("span"); node.textContent = item ?? "—"; return node.innerHTML; };

function notify(text, error = false) { const el = $("#message"); el.textContent = text; el.style.cssText = error ? "color:var(--bad);background:var(--bad-bg);border-left-color:var(--bad)" : ""; setTimeout(() => { if (el.textContent === text) { el.textContent = ""; el.style.cssText = ""; } }, 4500); }
function set(id, item) { $(id).textContent = item ?? "—"; }

function dashboard(data) {
  set("#total-plants", data.total_plants); set("#healthy-plants", data.healthy_plants); set("#warning-plants", data.warning_plants); set("#active-alerts", data.active_alerts);
  [["#temperature",data.temperature],["#humidity",data.humidity],["#light",data.light]].forEach(([id,item]) => set(id, number(item)));
  $("#last-updated").textContent = `Updated ${new Date().toLocaleTimeString([], {hour:"2-digit",minute:"2-digit",second:"2-digit"})}`;
  if (data.temperature !== null && data.humidity !== null) { history.push({ temperature:Number(data.temperature), humidity:Number(data.humidity), label:new Date().toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"}) }); if (history.length > maxHistory) history.shift(); chart(); }
}
function prediction(data, failed = false) {
  const target = $("#prediction-content"), source = $("#prediction-source");
  target.replaceChildren();
  if (failed) { target.innerHTML = '<p class="empty">Prediction is temporarily unavailable.</p>'; source.textContent = "Could not reach the prediction service."; return; }
  const result = value(data, "Prediction and its chances", "prediction", "Prediction", "result");
  if (data?.message && !result) { target.innerHTML = '<p class="empty">No sensor data is available yet. Add a reading to see a water prediction.</p>'; source.textContent = "Prediction uses the latest saved sensor reading."; return; }
  const card = document.createElement("div"); card.className = "prediction-result";
  const caption = document.createElement("p"); caption.className = "prediction-caption"; caption.textContent = "Model prediction"; card.append(caption);
  const main = document.createElement("strong");
  if (result && typeof result === "object") {
    const entries = Array.isArray(result) ? result.map((item, index) => [String(index + 1), item]) : Object.entries(result);
    const decision = value(result, "decision", "label", "prediction");
    main.textContent = decision ?? (entries.length ? String(entries[0][0]) : "No prediction returned");
    card.append(main);
    const confidence = value(result, "confidence", "probability");
    const details = document.createElement("p");
    details.textContent = confidence == null
      ? entries.filter(([key]) => !["decision", "label", "prediction"].includes(key.toLowerCase())).map(([key, item]) => `${key}: ${typeof item === "object" ? JSON.stringify(item) : item}`).join(" · ")
      : `Confidence: ${(Number(confidence) * 100).toFixed(1).replace(/\.0$/, "")}%`;
    if (details.textContent) card.append(details);
  } else { main.textContent = result == null ? "No prediction returned" : String(result); card.append(main); }
  const facts = document.createElement("div"); facts.className = "prediction-facts";
  [["Temperature",data?.temperature,"°C"],["Humidity",data?.humidity,"%"],["Light",data?.light,"lux"]].forEach(([label, item, unit]) => { if (item == null) return; const fact = document.createElement("span"), strong = document.createElement("b"); strong.textContent = `${number(item)} ${unit}`; fact.append(`${label} `, strong); facts.append(fact); });
  target.append(card); if (facts.childElementCount) target.append(facts);
  source.textContent = "Prediction uses the latest saved sensor reading.";
}
function chart() {
  const target = $("#sensor-chart"), empty = $("#chart-empty");
  if (history.length < 2) { target.innerHTML = ""; target.style.setProperty("--points", 1); empty.hidden = false; return; }
  empty.hidden = true; const values = history.flatMap(item => [item.temperature,item.humidity]); const min = Math.min(...values), range = Math.max(...values)-min || 1;
  target.style.setProperty("--points", history.length);
  target.innerHTML = history.map(item => `<div class="chart-column" title="${item.label}: ${number(item.temperature)} °C, ${number(item.humidity)}% humidity"><i class="chart-bar temperature" style="height:${Math.max(4,(item.temperature-min)/range*100)}%"></i><i class="chart-bar humidity" style="height:${Math.max(4,(item.humidity-min)/range*100)}%"></i><span>${item.label}</span></div>`).join("");
  $("#chart-summary").textContent = `Trend chart based on ${history.length} real readings collected in this session.`;
}
function status(name) { name = String(name || "Unknown").toLowerCase(); return name.includes("critical") || name.includes("danger") ? "critical" : name.includes("warn") ? "warning" : "healthy"; }
function plants(items) {
  const target = $("#plant-table");
  const plantSelect = $("#sensor-plant-id");
  plantNames.clear();
  plantRecords.clear();
  items.forEach(item => {
    const id = value(item, "Id", "id");
    const name = value(item, "Name", "name");
    if (id != null) plantRecords.set(String(id), item);
    if (id != null && name) plantNames.set(String(id), name);
  });
  plantSelect.replaceChildren();
  const placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = items.length ? "Select a plant" : "Add a plant first";
  placeholder.disabled = true;
  placeholder.selected = true;
  plantSelect.append(placeholder);
  items.forEach(item => {
    const id = value(item, "Id", "id");
    if (id == null) return;
    const option = document.createElement("option");
    option.value = String(id);
    option.textContent = `#${id} — ${value(item, "Name", "name") || "Unnamed plant"}`;
    plantSelect.append(option);
  });
  plantSelect.disabled = items.length === 0;
  [$("#requirement-plant-id"), $("#alert-plant-id")].forEach(select => {
    if (!select) return;
    select.replaceChildren(new Option(items.length ? "Select a plant" : "Add a plant first", ""));
    items.forEach(item => {
      const id = value(item, "Id", "id");
      if (id == null) return;
      select.append(new Option(`#${id} — ${value(item, "Name", "name") || "Unnamed plant"}`, String(id)));
    });
    select.disabled = items.length === 0;
  });
  if (!items.length) {
    target.innerHTML = '<tr><td colspan="5">No plants have been added yet.</td></tr>';
    return;
  }
  target.innerHTML = items.map(item => {
    const id = value(item,"Id","id");
    const state = value(item,"Status","status") || "Unspecified";
    return `<tr><td><strong>${safe(value(item,"Name","name"))}</strong></td><td>${safe(value(item,"Plant_type","plant_type"))}</td><td>${safe(value(item,"Location","location"))}</td><td><span class="badge ${status(state)}">${safe(state)}</span></td><td><button class="button secondary" type="button" data-edit-plant="${safe(id)}">Edit</button> <button class="button secondary" type="button" data-delete-plant="${safe(id)}">Delete</button></td></tr>`;
  }).join("");
  target.querySelectorAll("[data-edit-plant]").forEach(button => button.addEventListener("click", () => editPlant(plantRecords.get(button.dataset.editPlant))));
  target.querySelectorAll("[data-delete-plant]").forEach(button => button.addEventListener("click", () => deletePlant(button.dataset.deletePlant)));
}
async function loadPlantsForSensor() {
  const select = $("#sensor-plant-id");
  select.disabled = true;
  select.replaceChildren(new Option("Loading plants…", ""));
  try {
    const items = await get(api.plants);
    if (!Array.isArray(items)) throw new Error("The plants endpoint did not return a list.");
    plants(items);
    if (!items.length) notify("Add a plant before saving a sensor reading.", true);
  } catch (error) {
    select.replaceChildren(new Option("Could not load plants — check the server", ""));
    select.disabled = true;
    notify(`Could not load plants: ${error.message}`, true);
  }
}
function alerts(items) {
  const target = $("#alerts-container");
  alertRecords.clear();
  if (!items.length) { target.innerHTML = '<p class="empty">No alert records yet.</p>'; return; }
  items.forEach(item => { if (item.Id != null) alertRecords.set(String(item.Id), item); });
  target.innerHTML = items.slice(0,5).map(item => {
    const id = value(item,"Id","id"), severity = value(item,"Severity","severity") || "INFO";
    const critical = String(severity).toLowerCase().includes("critical");
    const plantId = value(item,"Plant_id","plant_id");
    const plantName = plantNames.get(String(plantId)) || (plantId == null ? "Unknown plant" : `Plant #${plantId}`);
    return `<article class="alert ${critical ? "critical" : ""}"><div class="alert-meta"><strong>${safe(value(item,"Alert_type","alert_type"))}</strong><span>${safe(severity)}</span></div><p><strong>Plant:</strong> ${safe(plantName)}</p><p>${safe(value(item,"Message","message"))}</p><button class="button secondary" type="button" data-edit-alert="${safe(id)}">Edit alert</button></article>`;
  }).join("");
  target.querySelectorAll("[data-edit-alert]").forEach(button => button.addEventListener("click", () => editAlert(alertRecords.get(button.dataset.editAlert))));
}
function editAlert(item) {
  if (!item) return;
  const form = $("#alert-form");
  form.reset();
  form.elements.Id.value = item.Id;
  form.elements.Plant_id.value = item.Plant_id;
  form.elements.Alert_type.value = item.Alert_type || "";
  form.elements.Severity.value = item.Severity || "WARNING";
  form.elements.Message.value = item.Message || "";
  form.elements.Status.value = item.Status || "ACTIVE";
  $("#alert-status-field").hidden = false;
  $("#alert-dialog").querySelector("h2").textContent = "Update alert";
  form.querySelector(".primary").textContent = "Update alert";
  $("#alert-dialog").showModal();
}
function prepareNewAlert() {
  const form = $("#alert-form");
  form.reset();
  $("#alert-status-field").hidden = true;
  $("#alert-dialog").querySelector("h2").textContent = "Add an alert";
  form.querySelector(".primary").textContent = "Save alert";
}
async function load() {
  const refresh = $("#refresh");
  refresh.disabled = true;
  refresh.setAttribute("aria-busy", "true");
  const alertRequest = await Promise.allSettled([get(api.alerts)]);
  const requests = await Promise.allSettled([
    get(api.dashboard), get(api.plants), get(api.prediction)
  ]);
  const errors = [];
  if (requests[0].status === "fulfilled") dashboard(requests[0].value);
  else errors.push(requests[0].reason.message);
  if (requests[1].status === "fulfilled") plants(requests[1].value);
  else errors.push(requests[1].reason.message);
  if (alertRequest[0].status === "fulfilled") alerts(alertRequest[0].value);
  else errors.push(alertRequest[0].reason.message);
  if (requests[2].status === "fulfilled") prediction(requests[2].value);
  else { console.error(requests[2].reason); prediction(null, true); errors.push(requests[2].reason.message); }
  if (errors.length) {
    errors.forEach(error => console.error(error));
    notify(`Some greenhouse data could not load: ${errors.join("; ")}`, true);
  } else {
    notify("");
    document.dispatchEvent(new Event("greenhouse:data-loaded"));
  }
  refresh.disabled = false;
  refresh.removeAttribute("aria-busy");
}
function payload(form) { const result = Object.fromEntries(new FormData(form)); const numeric = ["Id","Plant_id","Temperature","Humidity","Light","Min_temp","Max_temp","Min_humid","Max_humid","Min_light","Max_light"]; numeric.forEach(key => { if (key in result) result[key] = Number(result[key]); }); return result; }
function prepareNewPlant() {
  const form = $("#plant-form");
  form.reset();
  delete form.dataset.plantId;
  $("#plant-dialog").querySelector("h2").textContent = "Add a plant";
  form.querySelector(".primary").textContent = "Save plant";
}
function editPlant(plant) {
  if (!plant) return;
  const form = $("#plant-form");
  form.reset();
  form.dataset.plantId = String(plant.Id);
  ["Name","Plant_type","Location","Date_added","Status"].forEach(name => { form.elements[name].value = plant[name] ?? ""; });
  $("#plant-dialog").querySelector("h2").textContent = "Update plant";
  form.querySelector(".primary").textContent = "Update plant";
  $("#plant-dialog").showModal();
}
async function deletePlant(plantId) {
  const plant = plantRecords.get(String(plantId));
  const name = plant?.Name || `plant #${plantId}`;
  if (!window.confirm(`Delete ${name}?`)) return;
  try {
    await get(`${api.plants}${plantId}`, {method:"DELETE"});
    notify(`${name} deleted.`);
    await load();
  } catch (error) { notify(`Could not delete ${name}: ${error.message}`, true); }
}
$("#plant-form").addEventListener("submit", async event => {
  event.preventDefault();
  const form = event.currentTarget, button = form.querySelector(".primary"), body = payload(form);
  const plantId = form.dataset.plantId, updating = Boolean(plantId);
  button.disabled = true;
  try {
    await get(updating ? `${api.plants}${plantId}` : api.plants, {
      method: updating ? "PUT" : "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(body)
    });
    form.closest("dialog").close();
    notify(updating ? "Plant updated." : "Plant saved.");
    await load();
  } catch (error) { notify(`Could not save plant: ${error.message}`, true); }
  finally { button.disabled = false; }
});
[["#sensor-form",api.sensors,"Sensor reading saved."]].forEach(([selector,url,success]) => $(selector).addEventListener("submit", async event => { event.preventDefault(); const form = event.currentTarget, button = form.querySelector(".primary"); button.disabled = true; try { await get(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload(form))}); form.closest("dialog").close(); form.reset(); notify(success); await load(); } catch (err) { console.error(err); notify(`Could not save this record: ${err.message}`, true); } finally { button.disabled = false; } }));

function prepareRequirementForm() {
  const form = $("#requirement-form");
  form.reset();
  delete form.dataset.requirementId;
  $("#requirement-dialog").querySelector("h2").textContent = "Add plant requirements";
  form.querySelector(".primary").textContent = "Save requirements";
}
async function loadRequirementForPlant() {
  const form = $("#requirement-form"), plantId = $("#requirement-plant-id").value;
  delete form.dataset.requirementId;
  ["Min_temp","Max_temp","Min_humid","Max_humid","Min_light","Max_light"].forEach(name => { form.elements[name].value = ""; });
  if (!plantId) return;
  try {
    const requirement = await get(`${api.requirements}${plantId}`);
    if (!requirement) return;
    ["Min_temp","Max_temp","Min_humid","Max_humid","Min_light","Max_light"].forEach(name => { form.elements[name].value = requirement[name]; });
    form.dataset.requirementId = plantId;
    $("#requirement-dialog").querySelector("h2").textContent = "Update plant requirements";
    form.querySelector(".primary").textContent = "Update requirements";
  } catch (error) { notify(`Could not load requirements: ${error.message}`, true); }
}
$("#requirement-plant-id").addEventListener("change", loadRequirementForPlant);
$("#requirement-form").addEventListener("submit", async event => {
  event.preventDefault();
  const form = event.currentTarget, button = form.querySelector(".primary"), body = payload(form);
  const updating = Boolean(form.dataset.requirementId);
  button.disabled = true;
  try {
    await get(updating ? `${api.requirements}${body.Plant_id}` : api.requirements, {
      method: updating ? "PUT" : "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(body)
    });
    form.closest("dialog").close();
    notify(updating ? "Requirements updated." : "Requirements saved.");
    await load();
  } catch (error) { notify(`Could not save requirements: ${error.message}`, true); }
  finally { button.disabled = false; }
});

$("#alert-form").addEventListener("submit", async event => {
  event.preventDefault();
  const form = event.currentTarget, button = form.querySelector(".primary"), body = payload(form), updating = Boolean(body.Id);
  const alertId = body.Id;
  if (!updating) { delete body.Id; delete body.Status; }
  button.disabled = true;
  try {
    await get(updating ? `${api.alerts}${alertId}` : api.alerts, {
      method: updating ? "PUT" : "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(body)
    });
    form.closest("dialog").close();
    notify(updating ? "Alert updated." : "Alert saved.");
    await load();
  } catch (error) { notify(`Could not save alert: ${error.message}`, true); }
  finally { button.disabled = false; }
});
document.querySelectorAll("[data-open]").forEach(button => button.addEventListener("click", () => {
  const dialog = $("#" + button.dataset.open);
  if (button.dataset.open === "plant-dialog") prepareNewPlant();
  if (button.dataset.open === "requirement-dialog") prepareRequirementForm();
  if (button.dataset.open === "alert-dialog") prepareNewAlert();
  dialog.showModal();
  if (button.dataset.open === "sensor-dialog") loadPlantsForSensor();
}));
document.querySelectorAll(".close").forEach(button => button.addEventListener("click", () => button.closest("dialog").close()));
document.querySelectorAll(".sidebar nav a").forEach(link => link.addEventListener("click", () => { document.querySelectorAll(".sidebar nav a").forEach(item => item.classList.remove("active")); link.classList.add("active"); }));
$("#refresh").addEventListener("click", load); load(); setInterval(load,10000);
