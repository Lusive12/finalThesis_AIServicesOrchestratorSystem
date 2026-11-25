import { api } from "./api.js";

const SERVICES = [
  { id: "ai_photobooth", icon: "✦", title: "AI Photobooth", desc: "Buat potret dengan sentuhan gaya pilihanmu.", detail: "Ambil atau unggah foto, lalu pilih arahan penyempurnaan potret." },
  { id: "virtual_tryon", icon: "◈", title: "Virtual Try-On", desc: "Jelajahi tampilan baru secara virtual.", detail: "Pilih kategori dan gaya pakaian untuk pengalaman coba virtual." },
  { id: "fashion_recommender", icon: "◇", title: "Rekomendasi Gaya", desc: "Temukan inspirasi busana untuk harimu.", detail: "Atur preferensi dan lihat inspirasi outfit yang sesuai." },
  { id: "speech_llm", icon: "◎", title: "AI Conversation", desc: "Tanyakan apa saja kepada asisten AI.", detail: "Mulai percakapan melalui kolom pesan di bawah." }
];
const app = document.querySelector("#app");
const toast = document.querySelector("#toast");
let current = null, stream = null, lastActivity = Date.now(), busy = false, toastTimer, generation = 0;
const session = new Map();
const escapeHTML = value => String(value).replace(/[&<>"']/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[c]));
const showToast = message => { toast.textContent = message; toast.classList.add("show"); clearTimeout(toastTimer); toastTimer = setTimeout(() => toast.classList.remove("show"), 3000); };
const setBusy = value => { busy = value; document.querySelectorAll("button").forEach(button => { if (button.dataset.busyLock === "true") button.disabled = value; }); };

function home() {
  generation++; stopCamera(); current = null; busy = false;
  app.innerHTML = `<section class="home"><div class="hero"><div class="orb"></div><span class="eyebrow">SELAMAT DATANG DI SMART KIOSK</span><h1>Temukan pengalaman<br><em>AI yang baru.</em></h1><p>Satu sentuhan untuk mencoba kreativitas, gaya, dan percakapan yang dirancang untukmu.</p></div><div class="service-grid">${SERVICES.map((s,i)=>`<button class="service-card" data-open="${s.id}"><span class="card-index">EXPERIENCE 0${i+1}</span><span class="card-symbol">${s.icon}</span><h2>${s.title}</h2><p>${s.desc}</p><span class="card-arrow">↗</span></button>`).join("")}</div><div class="availability"><i></i> 4 PENGALAMAN SIAP DIJELAJAHI</div><div class="footnote">Sentuh kartu untuk memulai · Sesi akan berakhir otomatis setelah tidak aktif</div></section>`;
  app.querySelectorAll("[data-open]").forEach(button => button.addEventListener("click", () => enter(button.dataset.open)));
}

async function enter(id) {
  if (busy) return;
  const service = SERVICES.find(item => item.id === id); if (!service) return;
  current = service; busy = true; const viewGeneration = ++generation;
  app.innerHTML = `<section class="service-view"><div class="service-head"><button class="back-button" data-home aria-label="Kembali">‹</button><div><span class="eyebrow">PENGALAMAN AI</span><h1>${service.title}</h1><p>${service.detail}</p></div><span class="status-pill" id="serviceStatus">MENYIAPKAN</span></div><div class="service-body"><div class="work-panel" id="workPanel"><div class="empty"><span class="loading"><i class="spinner"></i> Memeriksa kesiapan layanan…</span></div></div><aside class="side-panel" id="sidePanel"><div class="panel-label">STATUS LAYANAN</div><h2 class="section-title">Menyiapkan pengalaman</h2><p class="helper" id="statusMessage">Orkestrator sedang memastikan layanan siap digunakan. Proses ini dapat memerlukan beberapa saat.</p><div class="notice" id="modeNotice">Respons yang belum terhubung ke layanan AI akan ditandai sebagai simulasi.</div></aside></div></section>`;
  app.querySelector("[data-home]").addEventListener("click", home);
  try {
    let status = await api.status(id);
    if (status.state !== "READY") {
      await api.start(id);
      const deadline = Date.now() + (window.KIOSK_CONFIG?.readyTimeoutMs || 90000);
      do {
        await new Promise(resolve => setTimeout(resolve, 1000));
        status = await api.status(id);
        const msg = document.querySelector("#statusMessage"); if (msg) msg.textContent = `Status layanan: ${status.state}. Menunggu kesiapan layanan…`;
        if (status.state === "ERROR") throw new Error(status.error || "Layanan mengalami kendala saat disiapkan.");
      } while (status.state !== "READY" && Date.now() < deadline);
      if (status.state !== "READY") throw new Error("Layanan belum siap. Silakan coba lagi sebentar.");
    }
    if (!current || current.id !== id) return;
    document.querySelector("#serviceStatus").textContent = "SIAP DIGUNAKAN";
    document.querySelector("#statusMessage").textContent = "Layanan siap. Mulai pengalamanmu di panel sebelah kiri.";
    document.querySelector("#modeNotice").textContent = status.mock_mode ? "MODE SIMULASI · Hasil contoh akan diberi label simulasi." : "Layanan terhubung ke orkestrator.";
    renderService(id);
  } catch (error) {
    if (current?.id !== id) return;
    document.querySelector("#serviceStatus").textContent = "TIDAK TERSEDIA";
    document.querySelector("#statusMessage").textContent = error.message;
    document.querySelector("#workPanel").innerHTML = `<div class="empty"><span class="big-symbol">!</span><strong>Layanan belum tersedia</strong><p class="helper">${escapeHTML(error.message)}</p><button class="secondary" id="retry">Coba lagi</button></div>`;
    document.querySelector("#retry").addEventListener("click", () => enter(id));
  } finally { if (generation === viewGeneration) busy = false; }
}

function renderService(id) {
  const work = document.querySelector("#workPanel"), side = document.querySelector("#sidePanel");
  const data = session.get(id) || {}; session.set(id, data);
  if (id === "speech_llm") { renderChat(work, side, data); return; }
  if (id === "fashion_recommender") { renderFashion(work, side, data); return; }
  const type = id === "ai_photobooth" ? "photo" : "tryon";
  work.innerHTML = `<div class="panel-label">${type === "photo" ? "STUDIO POTRET" : "RUANG COBA VIRTUAL"}</div><div class="preview" id="preview">${data.image ? `<img src="${data.image}" alt="Foto pilihan">` : `<div class="placeholder"><span class="big-symbol">${type === "photo" ? "✦" : "◈"}</span><strong>${type === "photo" ? "Ruang fotomu" : "Mulai dengan fotomu"}</strong><span>Pilih gambar dari perangkat atau gunakan kamera untuk melanjutkan.</span></div>`}</div><div class="control-row"><label class="secondary" style="display:grid;place-items:center;min-width:145px">Unggah foto<input id="imageUpload" type="file" accept="image/*" hidden></label><button class="secondary" id="cameraBtn">Buka kamera</button><button class="secondary" id="captureBtn" hidden>Ambil foto</button></div><div id="workOptions"></div><div class="result-box" id="resultBox"></div>`;
  side.innerHTML = type === "photo" ? `<div class="panel-label">ARAHAN GAYA</div><h2 class="section-title">Potret dengan karaktermu</h2><p class="helper">Pilih arahan untuk disertakan pada permintaan layanan.</p><span class="field-label">Gaya penyempurnaan</span><div class="chip-list">${chips(["Natural", "Editorial", "Warm film", "Studio light"], data.style || "Natural")}</div><span class="field-label">Catatan tambahan</span><input class="chat-compose" id="promptInput" placeholder="Contoh: suasana senja" style="width:100%;height:50px;background:#0a1727;border:1px solid #ffffff15;border-radius:14px;color:white;padding:0 14px"><div class="control-row"><button class="primary" id="submitAction" ${data.image ? "" : "disabled"}>Buat potret</button><button class="secondary" id="resetBtn">Atur ulang</button></div><p class="touch-note">Pemrosesan dilakukan oleh layanan photobooth terpisah.</p>` : `<div class="panel-label">PILIH TAMPILAN</div><h2 class="section-title">Coba gaya yang berbeda</h2><p class="helper">Pilih kategori dan item pakaian untuk dimasukkan ke permintaan virtual try-on.</p><span class="field-label">Kategori pakaian</span><div class="chip-list">${chips(["Atasan", "Outerwear", "Dress"], data.category || "Atasan", "category")}</div><span class="field-label">Pilihan gaya</span><div class="outfit-grid">${[["Jaket modern","Potongan rapi · kasual"],["Gaya minimal","Warna netral · santai"],["Look urban","Layer ringan · aktif"],["Klasik","Siluet timeless"]].map(([a,b],i)=>`<button class="outfit" data-item="${i}"><b>${a}</b><span>${b}</span></button>`).join("")}</div><div class="control-row"><button class="primary" id="submitAction" ${data.image && data.item ? "" : "disabled"}>Buat tampilan</button><button class="secondary" id="resetBtn">Atur ulang</button></div><p class="touch-note">Item adalah placeholder hingga katalog layanan tersedia.</p>`;
  wireImageActions(id, data, type);
  side.querySelectorAll("[data-chip]").forEach(button => button.addEventListener("click", () => { data[button.dataset.group || "style"] = button.dataset.chip; renderService(id); }));
  side.querySelectorAll("[data-item]").forEach(button => button.addEventListener("click", () => { data.item = Number(button.dataset.item); side.querySelectorAll("[data-item]").forEach(item => item.style.borderColor = item === button ? "#e9783599" : ""); side.querySelector("#submitAction").disabled = !data.image; }));
  side.querySelector("#submitAction").addEventListener("click", () => runImageInference(id, data, type));
  side.querySelector("#resetBtn").addEventListener("click", () => { stopCamera(); session.delete(id); renderService(id); });
}

function chips(items, selected, group="style") { return items.map(item => `<button class="chip ${item === selected ? "selected" : ""}" data-chip="${item}" data-group="${group}">${item}</button>`).join(""); }
function wireImageActions(id, data) {
  const upload = document.querySelector("#imageUpload");
  upload.addEventListener("change", () => { const file = upload.files[0]; if (!file) return; if (file.size > 8 * 1024 * 1024) { showToast("Ukuran gambar maksimal 8 MB."); return; } const reader = new FileReader(); reader.onload = () => { data.image = reader.result; renderService(id); }; reader.readAsDataURL(file); });
  document.querySelector("#cameraBtn").addEventListener("click", async event => {
    try { if (stream) { stopCamera(); renderService(id); return; } stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" }, audio: false }); const preview = document.querySelector("#preview"); preview.innerHTML = `<video autoplay playsinline muted id="cameraVideo"></video>`; preview.querySelector("video").srcObject = stream; event.currentTarget.textContent = "Tutup kamera"; document.querySelector("#captureBtn").hidden = false; }
    catch { showToast("Kamera tidak tersedia. Silakan unggah foto."); }
  });
  document.querySelector("#captureBtn").addEventListener("click", () => { const video = document.querySelector("#cameraVideo"); if (!video) return; const canvas = document.createElement("canvas"); canvas.width = video.videoWidth; canvas.height = video.videoHeight; canvas.getContext("2d").drawImage(video,0,0); data.image = canvas.toDataURL("image/jpeg", .88); stopCamera(); renderService(id); });
}
function stopCamera() { if (stream) { stream.getTracks().forEach(track => track.stop()); stream = null; } }

async function runImageInference(id, data, type) {
  const button = document.querySelector("#submitAction"); if (busy || !button) return; busy = true; const viewGeneration = generation; button.disabled = true;
  const box = document.querySelector("#resultBox"); box.classList.add("show"); box.innerHTML = `<span class="loading"><i class="spinner"></i> Mengirim permintaan ke layanan…</span>`;
  const payload = type === "photo" ? { image: data.image, style: data.style, prompt: document.querySelector("#promptInput").value } : { image: data.image, category: data.category, item: data.item };
  try { const result = await api.infer(id, payload); if (generation !== viewGeneration) return; box.innerHTML = `${result.mock ? `<div class="notice">HASIL SIMULASI · Bukan hasil inferensi AI</div>` : ""}<div class="panel-label">FOTO SUMBER</div><img src="${data.image}" alt="Foto sumber">${result.image_url ? `<div class="panel-label" style="margin-top:14px">HASIL LAYANAN</div><img src="${escapeHTML(result.image_url)}" alt="Hasil layanan">` : `<p>${escapeHTML(result.message || result.result || "Permintaan diterima. Hasil visual muncul di sini setelah adapter mengembalikan URL gambar.")}</p>`}<button class="secondary" id="downloadResult">Unduh foto sumber</button>`; document.querySelector("#downloadResult").addEventListener("click", () => download(data.image, "smart-kiosk-photo.jpg")); }
  catch (error) { if (generation !== viewGeneration) return; box.innerHTML = `<p class="helper">Permintaan gagal: ${escapeHTML(error.message)}</p><button class="secondary" id="retryAction">Coba lagi</button>`; document.querySelector("#retryAction").addEventListener("click", () => runImageInference(id, data, type)); }
  finally { if (generation === viewGeneration) { busy = false; if (document.querySelector("#submitAction")) document.querySelector("#submitAction").disabled = !data.image || (type === "tryon" && data.item == null); } }
}
function download(data, name) { const a = document.createElement("a"); a.href = data; a.download = name; a.click(); }

function renderFashion(work, side, data) {
  work.innerHTML = `<div class="panel-label">PAPAN INSPIRASI</div><h2 class="section-title">Outfit pilihan untukmu</h2><p class="helper">Minta rekomendasi untuk melihat inspirasi gaya sesuai preferensimu.</p><div class="outfit-grid" id="outfits">${(data.outfits || []).map(item=>{ const title=Array.isArray(item)?item[0]:item.title, desc=Array.isArray(item)?item[1]:item.description; return `<article class="outfit"><b>${escapeHTML(title || "Rekomendasi")}</b><span>${escapeHTML(desc || "")}</span></article>`; }).join("") || `<div class="empty" style="grid-column:1/-1">Rekomendasi akan muncul di sini.</div>`}</div><div class="control-row"><button class="primary" id="recommend">${data.outfits ? "Perbarui rekomendasi" : "Minta rekomendasi"}</button></div>`;
  side.innerHTML = `<div class="panel-label">PREFERENSIMU</div><h2 class="section-title">Racik gaya yang kamu suka</h2><span class="field-label">Kategori</span><div class="chip-list">${chips(["Kasual", "Formal", "Streetwear"],data.category || "Kasual","category")}</div><span class="field-label">Kesempatan</span><div class="chip-list">${chips(["Sehari-hari", "Kampus", "Acara"],data.occasion || "Sehari-hari","occasion")}</div><span class="field-label">Palet warna</span><div class="chip-list">${chips(["Netral", "Hangat", "Berani"],data.palette || "Netral","palette")}</div><div class="notice">Rekomendasi adalah hasil contoh saat mode simulasi aktif.</div>`;
  side.querySelectorAll("[data-chip]").forEach(button => button.addEventListener("click", () => { data[button.dataset.group] = button.dataset.chip; renderService(current.id); }));
  work.querySelector("#recommend").addEventListener("click", async () => { if (busy) return; busy = true; const viewGeneration = generation, serviceId = current.id, button = work.querySelector("#recommend"); button.disabled = true; button.innerHTML = `<span class="loading"><i class="spinner"></i> Menyiapkan…</span>`; try { const result = await api.infer(serviceId, { category:data.category || "Kasual", occasion:data.occasion || "Sehari-hari", palette:data.palette || "Netral" }); if (generation !== viewGeneration) return; data.outfits = result.outfits || result.recommendations || []; data.mock = !!result.mock; renderService(serviceId); if (result.mock) showToast("Contoh rekomendasi simulasi ditampilkan."); else if (!data.outfits.length) showToast("Layanan belum mengembalikan item rekomendasi."); } catch(error) { if (generation === viewGeneration) { showToast(error.message); button.disabled = false; button.textContent = "Coba lagi"; } } finally { if (generation === viewGeneration) busy = false; } });
}

function renderChat(work, side, data) {
  data.messages ||= [{ role:"ai", text:"Halo! Aku siap membantu menemukan inspirasi. Apa yang ingin kamu tanyakan?" }];
  work.innerHTML = `<div class="panel-label">RUANG PERCAKAPAN</div><div class="chat-layout"><div class="chat-log" id="chatLog">${data.messages.map(message=>`<div class="message ${message.role}">${escapeHTML(message.text)}</div>`).join("")}</div><form class="chat-compose" id="chatForm"><input id="chatInput" autocomplete="off" placeholder="Tulis pesanmu…" aria-label="Pesan"><button class="primary" type="submit">Kirim</button></form></div>`;
  side.innerHTML = `<div class="panel-label">ASISTEN AI</div><h2 class="section-title">Percakapan yang nyaman</h2><p class="helper">Ketik pesan lalu tekan Kirim. Kamu juga dapat menggunakan tombol Enter pada keyboard.</p><div class="notice">${data.mock ? "MODE SIMULASI · Balasan contoh diberi label." : "Balasan diproses oleh layanan percakapan terpisah."}</div><div class="control-row"><button class="secondary" id="clearChat">Hapus percakapan</button></div>`;
  const log = work.querySelector("#chatLog"); log.scrollTop = log.scrollHeight;
  work.querySelector("#chatForm").addEventListener("submit", async event => { event.preventDefault(); const input = work.querySelector("#chatInput"), text = input.value.trim(); if (!text || busy) return; const viewGeneration = generation, serviceId = current.id; data.messages.push({role:"user",text}); input.value = ""; data.messages.push({role:"ai",text:"Menunggu respons layanan…",pending:true}); renderService(serviceId); busy = true; try { const response = await api.infer(serviceId,{message:text,history:data.messages.filter(m=>!m.pending).slice(-12)}); data.mock = !!response.mock; data.messages.pop(); data.messages.push({role:"ai",text:response.message || response.response || "Layanan menerima pesan, tetapi belum mengembalikan teks balasan yang dikenali."}); } catch(error) { data.messages.pop(); data.messages.push({role:"ai",text:`Layanan belum dapat menjawab. ${error.message}`}); } finally { if (generation === viewGeneration) { busy = false; if (current?.id === serviceId) renderService(serviceId); } } });
  side.querySelector("#clearChat").addEventListener("click", () => { data.messages = [{role:"ai",text:"Percakapan dihapus. Ada yang bisa kubantu?"}]; renderService(current.id); });
}

document.querySelector("#brandHome").addEventListener("click", home);
document.addEventListener("pointerdown", () => lastActivity = Date.now(), { passive:true });
document.addEventListener("keydown", () => lastActivity = Date.now());
setInterval(() => { const date = new Date(); document.querySelector("#clock").textContent = date.toLocaleTimeString("id-ID",{hour:"2-digit",minute:"2-digit",timeZone:"Asia/Jakarta"}); },1000);
setInterval(() => { if (current && !busy && Date.now()-lastActivity > (window.KIOSK_CONFIG?.idleTimeoutMs || 180000)) { home(); showToast("Sesi selesai. Selamat datang kembali."); } },5000);
const connection = document.querySelector("#connectionLabel");
api.config().then(config => { window.KIOSK_CONFIG = { ...window.KIOSK_CONFIG, idleTimeoutMs: config.idle_timeout_ms, readyTimeoutMs: config.ready_timeout_ms }; }).catch(() => {});
api.services().then(data => { connection.textContent = data.mock_mode ? "SIMULASI AKTIF" : "ORKESTRATOR ONLINE"; }).catch(() => { connection.textContent = "ORKESTRATOR OFFLINE"; });
home();
