const $ = s => document.querySelector(s);
const history = [], maxHistory = 12;
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
    main.textContent = entries.length ? String(entries[0][1]) : "No prediction returned";
    card.append(main);
    if (entries.length > 1) { const details = document.createElement("p"); details.textContent = entries.slice(1).map(([key, item]) => `${key}: ${typeof item === "object" ? JSON.stringify(item) : item}`).join(" · "); card.append(details); }
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
  if (!items.length) {
    target.innerHTML = '<tr><td colspan="4">No plants have been added yet.</td></tr>';
    set("#healthy-plants", 0);
    set("#warning-plants", 0);
    return;
  }
  let healthy = 0, warning = 0;
  target.innerHTML = items.map(item => {
    const state = value(item,"Status","status") || "Unspecified";
    const normalized = String(state).toLowerCase();
    if (normalized.includes("healthy")) healthy++;
    else if (normalized.includes("warn") || normalized.includes("critical") || normalized.includes("danger")) warning++;
    return `<tr><td><strong>${safe(value(item,"Name","name"))}</strong></td><td>${safe(value(item,"Plant_type","plant_type"))}</td><td>${safe(value(item,"Location","location"))}</td><td><span class="badge ${status(state)}">${safe(state)}</span></td></tr>`;
  }).join("");
  set("#healthy-plants", healthy);
  set("#warning-plants", warning);
}
function alerts(items) { const target = $("#alerts-container"); if (!items.length) { target.innerHTML = '<p class="empty">No alert records yet.</p>'; return; } target.innerHTML = items.slice(0,6).map(item => { const severity = value(item,"Severity","severity") || "INFO", critical = String(severity).toLowerCase().includes("critical"); return `<article class="alert ${critical ? "critical" : ""}"><div class="alert-meta"><strong>${safe(value(item,"Alert_type","alert_type"))}</strong><span>${safe(severity)}</span></div><p>${safe(value(item,"Message","message"))}</p></article>`; }).join(""); }
async function load() {
  const refresh = $("#refresh");
  refresh.disabled = true;
  refresh.setAttribute("aria-busy", "true");
  const requests = await Promise.allSettled([
    get(api.dashboard), get(api.plants), get(api.alerts), get(api.prediction)
  ]);
  const errors = [];
  if (requests[0].status === "fulfilled") dashboard(requests[0].value);
  else errors.push(requests[0].reason.message);
  if (requests[1].status === "fulfilled") plants(requests[1].value);
  else errors.push(requests[1].reason.message);
  if (requests[2].status === "fulfilled") alerts(requests[2].value);
  else errors.push(requests[2].reason.message);
  if (requests[3].status === "fulfilled") prediction(requests[3].value);
  else { console.error(requests[3].reason); prediction(null, true); errors.push(requests[3].reason.message); }
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
function payload(form) { const result = Object.fromEntries(new FormData(form)); const numeric = ["Plant_id","Temperature","Humidity","Light","Min_temp","Max_temp","Min_humid","Max_humid","Min_light","Max_light"]; numeric.forEach(key => { if (key in result) result[key] = Number(result[key]); }); return result; }
[["#plant-form",api.plants,"Plant saved."],["#sensor-form",api.sensors,"Sensor reading saved."],["#requirement-form",api.requirements,"Requirements saved."],["#alert-form",api.alerts,"Alert saved."]].forEach(([selector,url,success]) => $(selector).addEventListener("submit", async event => { event.preventDefault(); const form = event.currentTarget, button = form.querySelector(".primary"); button.disabled = true; try { await get(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload(form))}); form.closest("dialog").close(); form.reset(); notify(success); await load(); } catch (err) { console.error(err); notify("Could not save this record. Check the form values and referenced plant ID.", true); } finally { button.disabled = false; } }));
document.querySelectorAll("[data-open]").forEach(button => button.addEventListener("click", () => $("#" + button.dataset.open).showModal()));
document.querySelectorAll(".close").forEach(button => button.addEventListener("click", () => button.closest("dialog").close()));
document.querySelectorAll(".sidebar nav a").forEach(link => link.addEventListener("click", () => { document.querySelectorAll(".sidebar nav a").forEach(item => item.classList.remove("active")); link.classList.add("active"); }));
$("#refresh").addEventListener("click", load); load(); setInterval(load,10000);
