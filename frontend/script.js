const $ = s => document.querySelector(s);
const history = [], maxHistory = 12;
const api = { dashboard: "/dashboard/", plants: "/plants/", sensors: "/sensors/", requirements: "/requirements/", alerts: "/alerts/" };
const get = async (url, options) => { const response = await fetch(url, options); if (!response.ok) throw new Error(response.status); return response.json(); };
const value = (object, ...keys) => keys.map(key => object[key]).find(item => item !== undefined && item !== null);
const number = item => item === null || item === undefined ? "—" : Number(item).toFixed(1).replace(/\.0$/, "");
const safe = item => { const node = document.createElement("span"); node.textContent = item ?? "—"; return node.innerHTML; };

function notify(text, error = false) { const el = $("#message"); el.textContent = text; el.style.cssText = error ? "color:var(--bad);background:var(--bad-bg);border-left-color:var(--bad)" : ""; setTimeout(() => { if (el.textContent === text) { el.textContent = ""; el.style.cssText = ""; } }, 4500); }
function set(id, item) { $(id).textContent = item ?? "—"; }

function dashboard(data) {
  set("#total-plants", data.total_plants); set("#healthy-plants", data.healthy_plants); set("#warning-plants", data.warning_plants); set("#active-alerts", data.active_alerts);
  [["#temperature",data.temperature],["#humidity",data.humidity],["#soil-moisture",data.soil_moisture],["#light",data.light]].forEach(([id,item]) => set(id, number(item)));
  $("#last-updated").textContent = `Updated ${new Date().toLocaleTimeString([], {hour:"2-digit",minute:"2-digit",second:"2-digit"})}`;
  if (data.temperature !== null && data.humidity !== null) { history.push({ temperature:Number(data.temperature), humidity:Number(data.humidity), label:new Date().toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"}) }); if (history.length > maxHistory) history.shift(); chart(); }
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
function plants(items) { const target = $("#plant-table"); if (!items.length) { target.innerHTML = '<tr><td colspan="4">No plants have been added yet.</td></tr>'; return; } target.innerHTML = items.map(item => { const state = value(item,"Status","status") || "Unspecified"; return `<tr><td><strong>${safe(value(item,"Name","name"))}</strong></td><td>${safe(value(item,"Plant_type","plant_type"))}</td><td>${safe(value(item,"Location","location"))}</td><td><span class="badge ${status(state)}">${safe(state)}</span></td></tr>`; }).join(""); }
function alerts(items) { const target = $("#alerts-container"); if (!items.length) { target.innerHTML = '<p class="empty">No alert records yet.</p>'; return; } target.innerHTML = items.slice(0,6).map(item => { const severity = value(item,"Severity","severity") || "INFO", critical = String(severity).toLowerCase().includes("critical"); return `<article class="alert ${critical ? "critical" : ""}"><div class="alert-meta"><strong>${safe(value(item,"Alert_type","alert_type"))}</strong><span>${safe(severity)}</span></div><p>${safe(value(item,"Message","message"))}</p></article>`; }).join(""); }
async function load() { const refresh = $("#refresh"); refresh.disabled = true; refresh.setAttribute("aria-busy", "true"); try { const [summary,plantData,alertData] = await Promise.all([get(api.dashboard),get(api.plants),get(api.alerts)]); dashboard(summary); plants(plantData); alerts(alertData); document.dispatchEvent(new Event("greenhouse:data-loaded")); } catch (err) { console.error(err); notify("Unable to load greenhouse data. Check that FastAPI and MySQL are running.", true); } finally { refresh.disabled = false; refresh.removeAttribute("aria-busy"); } }
function payload(form) { const result = Object.fromEntries(new FormData(form)); const numeric = ["Plant_id","Temperature","Humidity","Soil_moisture","Light","Min_temp","Max_temp","Min_humid","Max_humid","Min_light","Max_light"]; numeric.forEach(key => { if (key in result) result[key] = Number(result[key]); }); return result; }
[["#plant-form",api.plants,"Plant saved."],["#sensor-form",api.sensors,"Sensor reading saved."],["#requirement-form",api.requirements,"Requirements saved."],["#alert-form",api.alerts,"Alert saved."]].forEach(([selector,url,success]) => $(selector).addEventListener("submit", async event => { event.preventDefault(); const form = event.currentTarget, button = form.querySelector(".primary"); button.disabled = true; try { await get(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload(form))}); form.closest("dialog").close(); form.reset(); notify(success); await load(); } catch (err) { console.error(err); notify("Could not save this record. Check the form values and referenced plant ID.", true); } finally { button.disabled = false; } }));
document.querySelectorAll("[data-open]").forEach(button => button.addEventListener("click", () => $("#" + button.dataset.open).showModal()));
document.querySelectorAll(".close").forEach(button => button.addEventListener("click", () => button.closest("dialog").close()));
document.querySelectorAll(".sidebar nav a").forEach(link => link.addEventListener("click", () => { document.querySelectorAll(".sidebar nav a").forEach(item => item.classList.remove("active")); link.classList.add("active"); }));
$("#refresh").addEventListener("click", load); load(); setInterval(load,10000);
