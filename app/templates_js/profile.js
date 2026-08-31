(function () {

    var hamburger = document.getElementById("hamburgerBtn");
    var sidebar = document.getElementById("sidebar");
    var overlay = document.getElementById("sidebarOverlay");

    function openSidebar() {
        sidebar.classList.add("open");
        overlay.classList.add("open");
        hamburger.classList.add("open");
        hamburger.setAttribute("aria-expanded", "true");
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
    overlay.addEventListener("click", closeSidebar);

    var model = document.getElementById("itemModel");
    if (!model) return;

    var currentRow = null;
    var yesBtn = document.getElementById("itemModelYes");

    var toast = document.getElementById("cancelToast");
    var toastTimer = null;

    function showCancelToast(text) {
        document.getElementById("cancelToastText").textContent =
            text || "Buyment is accsesful cancel";
        toast.classList.remove("hidden", "hide"); 
        clearTimeout(toastTimer);
        toastTimer = setTimeout(function () {
            toast.classList.add("hide");
            setTimeout(function () { toast.classList.add("hidden"); }, 300);
        }, 3500);
    }

    function openItemModel(data) {
        document.getElementById("itemModelTitle").textContent = "Product";
        document.getElementById("itemTitle").textContent = data.title || "-";
        document.getElementById("itemDate").textContent = data.date || "-";
        document.getElementById("itemQty").textContent = data.qty || "-";
        document.getElementById("itemTotal").textContent =
            data.total ? data.total + " €" : "-";
        document.getElementById("itemStatus").textContent = data.status || "-";
        model.classList.remove("hidden");
    }

    function closeItemModel() {
        model.classList.add("hidden");
    }

    document.querySelectorAll(".row-x").forEach(function (btn) {
        btn.addEventListener("click", function () {
            currentRow = btn.closest("tr");
            openItemModel(btn.dataset);
        });
    });

    document.getElementById("itemModelClose").addEventListener("click", closeItemModel);
    document.getElementById("itemModelNo").addEventListener("click", closeItemModel);

    yesBtn.addEventListener("click", function () {
        var purchaseId = currentRow
            ? currentRow.querySelector(".row-x").dataset.id
            : null;
        if (!purchaseId) {
            closeItemModel();
            return;
        }

        yesBtn.disabled = true;
        fetch("/profile/purchases/" + purchaseId, { method: "DELETE" })
            .then(function (response) {
if (!response.ok) throw new Error("HTTP " + response.status);
if (currentRow) currentRow.remove();
closeItemModel();
showCancelToast();
            })
            .catch(function () {
alert("No managed close bayment. Please repeat again.")
            })
            .finally(function () {
yesBtn.disabled = false;
            });
    });

    model.addEventListener("click", function (e) {
        if (e.target === model) closeItemModel();
    });
})();