(function () {
    var hamburger = document.getElementById("hamburgerBtn");
    var sidebar = document.getElementById("sidebar");
    var overlay = document.getElementById("sidebarOverlay");

    function openSidebar() {
        sidebar.classList.add("open");
        overlay.classList.add("open");
        hamburger.classList.add("aria-expanded", "true");
    }
    function closeSidebar() {
        sidebar.classList.remove("open");
        overlay.classList.remove("open");
        hamburger.classList.remove("open");
        hamburger.setAttribute("aria-expanded", "false");
    }

    hamburger.addEventListener("click", function() {
        sidebar.classList.contains("open") ? closeSidebar() : openSidebar();
    });
})();

const FALLBACK_SHOPS = [
    { id: 1,  name: "Санлайт",      address: "ТЦ «Атриум», Земляной Вал, д. 33, Москва",hours: "10:00–22:00", phone: "+7 495 000-11-01", quantity_1g: 3,  quantity_5g: 5,  quantity_10g: 1  },
    { id: 2,  name: "Адамас",       address: "ТЦ «Европейский», пл. Киевского Вокзала, д. 2, Москва",    hours: "10:00–22:00", phone: "+7 495 000-11-02", quantity_1g: 2,  quantity_5g: 6,  quantity_10g: 3  },
    { id: 3,  name: "SOKOLOV",      address: "ГУМ, Красная площадь, д. 3, Москва",       hours: "10:00–22:00", phone: "+7 495 000-11-03", quantity_1g: 7,  quantity_5g: 6,  quantity_10g: 1  },
    { id: 4,  name: "585 Золотой",  address: "ТЦ «Охотный Ряд», Манежная площадь, д. 1, Москва",         hours: "10:00–22:00", phone: "+7 495 000-11-04", quantity_1g: 11, quantity_5g: 12, quantity_10g: 56 },
    { id: 5,  name: "Pandora",      address: "ТЦ «Цветной», Цветной бульвар, д. 15, Москва",             hours: "10:00–22:00", phone: "+7 495 000-11-05", quantity_1g: 6,  quantity_5g: 34, quantity_10g: 5  },
];

const WEIGHTS = {
    "1g":  { key: "quantity_1g",  label: "1g"  },
    "5g":  { key: "quantity_5g",  label: "5g"  },
    "10g": { key: "quantity_10g", label: "10g" },
};

let shops = [];
let currentWeight = "1g";
let currentShop = null;

const grid = document.getElementById("grid");
const countEl = document.getElementById("count");
const sourceEl = document.getElementById("source");

function parseWeightFromUrl() {
    const w = new URLSearchParams(window.location.search).get("weight");
    return (w === "1g" || w === "5g" || w === "10g") ? w : null;
}

function activateTab(weight) {
    currentWeight = weight;
    document.querySelectorAll(".tab").forEach(t => {
        const active = t.dataset.weight === weight;
        t.classList.toggle("active", active);
        t.setAttribute("aria-selected", active);
    });
}

async function loadShops() {
    try {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), 4000);
        const res = await fetch("/api/shops", { signal: controller.signal });
        clearTimeout(timer);
        if (!res.ok) throw new Error("HTTP" + res.status);
        const data = await res.json();
        shops = Array.isArray(data.shops) ? data.shops : [];
        if (!shops.length) throw new Error("empty");
        sourceEl.textContent = "Source data: server /api/shops";
    } catch (err) {
        shops = FALLBACK_SHOPS;
        sourceEl.textContent = "Source data: demo-data (server no found)";
    }
    render();
}
function render() {
    const w = WEIGHTS[currentWeight];
    const available = shops.filter(s => Number(s[w.key]) > 0);
    const total = shops.length;

    countEl.textContent = available.length;
    grid.innerHTML = "";

    if (!available.length) {
        const empty = document.createElement("article");
        empty.className = "card none";
        empty.innerHTML = "<h3>Not stores</h3><p>Neither one point gold " + currentWeight + " in stock.</p>";
        grid.appendChild(empty);
        return;
    }

    available.sort((a, b) => Number(b[w.key]) - Number(a[w.key]));

    available.forEach((s, i) => {
        const qty = Number(s[w.key]);
        const card = document.createElement("article");
        card.className = "card";
        card.style.animationDelay = (i * 40) + "ms";
        card.innerHTML = `
            <div class="stock-badge ${qty <= 0 ? "zero" : ""}">${w.label}: ${qty} thing.</div>
            <h3>${escapeHtml(s.name || "-")}</h3>
            <p>📍 ${escapeHtml(s.address || "-")}</p>
            <p>🕐 ${escapeHtml(s.hours || "-")}</p>
            <p>📞 ${escapeHtml(s.phone || "-")}</p>
            <button class="btn-buy" type="button" data-shop-id="${s.id}">Buy</button>
        `;
        grid.appendChild(card);
    });

    const note = document.createElement("p");
    note.className = "note";
    note.textContent = "Shown " + available.length + " from " + total + " stores (reverse " + currentWeight + " > 0).";
    grid.appendChild(note);
}

function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, c => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    }[c]));
}

document.getElementById("tabs").addEventListener("click", (e) => {
    const btn = e.target.closest(".tab");
    if (!btn) return;
    currentWeight = btn.dataset.weight;
    document.querySelectorAll(".tab").forEach(t => {
        const active = t === btn;
        t.classList.toggle("active", active);
        t.setAttribute("aria-selected", active);
    });
    render();
});

const weightFromUrl = parseWeightFromUrl();
if (weightFromUrl) activateTab(weightFromUrl);

loadShops();

const buyModel = document.getElementById("buyModel")
const buyToast = document.getElementById("buyToast")

let toastTimer = null;
function showBuyToast(text) {
    document.getElementById("buyToastText").textContent =
        text || "Your are successful bayment";
    buyToast.classList.remove("hidden", "hide");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
        buyToast.classList.add("hide");
        setTimeout(() => buyToast.classList.add("hidden"), 300);
    }, 3500);
}

function openBuyModel() {
    buyModel.classList.remove("hidden");
}
function closeBuyModel() {
    buyModel.classList.add("hidden");
}

grid.addEventListener("click", (e) => {
    const btn = e.target.closest(".btn-buy");
    if (!btn) return;
    e.preventDefault();
    const card = btn.closest(".card");
    const shopName = card ? card.querySelector("h3").textContent : "";
    currentShop = shops.find(s => s.id === Number(btn.dataset.shopId)) || null;
    document.getElementById("buyModelText").textContent =
        "Store «" + shopName + "», weight " + currentWeight + ". Accept buyment.";
    openBuyModel();
});

async function confirmPurchase() {
    if (!currentShop) return;
    const btn = document.getElementById("buyModelYes");
    btn.disabled = true;
    const prevText = btn.textContent;
    btn.textContent = "...";
    try {
        const res = await fetch("/api/shops/" + currentShop.id + "/buy", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ weight: currentWeight }),
        });
        const data = await res.json();
        if (!res.ok) {
            alert("Error: " + (data.message || res.status));
            return;
        }
        const shop = shops.find(s => s.id === currentShop.id);
        if (shop) {
            shop.quantity_1g = data.quantities.quantity_1g;
            shop.quantity_5g = data.quantities.quantity_5g;
            shop.quantity_10g = data.quantities.quantity_10g;
        }
        render();
        closeBuyModel();
        currentShop = null;
        const paid = data.purchase ? Number(data.purchase.total_price) : null;
        showBuyToast(
            "Successful bayment. Purchase added to your profile" +
            (paid != null && !isNaN(paid) ? " (" + paid.toFixed(2) + " €)" : "") + "."
        );
    } catch (err) {
        alert("Buyment failed: " + err);
    } finally {
        btn.disabled = false;
        btn.textContent = prevText;
    }
}

document.getElementById("butModelClose").addEventListener("click", closeBuyModel);
document.getElementById("buyModelNo").addEventListener("click", closeBuyModel);
document.getElementById("buyModelYes").addEventListener("click", confirmPurchase);
buyModel.addEventListener("click", (e) => {
    if (e.target === buyModel) closeBuyModel();
});