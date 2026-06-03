document.addEventListener("DOMContentLoaded", loadPayments);

// Precios fijos por plan_id
const PLAN_PRICES = { 1: 30, 2: 150, 3: 270 };
const PLAN_NAMES  = { 1: "Mensual", 2: "Semestral", 3: "Anual" };

async function loadPayments() {
    showLoading("payments-table-container");
    try {
        const payments = await getData("/payments/");
        renderPaymentsTable(payments);
    } catch (error) {
        console.error("Error loading payments:", error);
        showError("payments-table-container", "Failed to fetch payment records.");
    }
}

function renderPaymentsTable(payments) {
    const container = document.getElementById("payments-table-container");

    if (!payments || payments.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h5>No payments found</h5>
                <p>No payment records available yet.</p>
            </div>`;
        return;
    }

    container.innerHTML = `
        <div class="table-responsive">
            <table class="table align-middle">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Membership ID</th>
                        <th>Amount</th>
                        <th>Date</th>
                        <th>Method</th>
                        <th>Reference</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${payments.map(p => `
                        <tr>
                            <td>${p.id}</td>
                            <td>${p.membership_id}</td>
                            <td class="fw-semibold">${formatCurrency(p.amount)}</td>
                            <td>${formatDate(p.payment_date)}</td>
                            <td class="text-capitalize">${p.payment_method || "-"}</td>
                            <td>${p.reference || "-"}</td>
                            <td>${renderPaymentBadge(p.status)}</td>
                        </tr>`).join("")}
                </tbody>
            </table>
        </div>`;
}

function renderPaymentBadge(status) {
    if (status === "completed") return `<span class="badge badge-soft-success">Completed</span>`;
    if (status === "pending")   return `<span class="badge badge-soft-warning">Pending</span>`;
    if (status === "refunded")  return `<span class="badge badge-soft-warning">Refunded</span>`;
    return `<span class="badge badge-soft-danger">Failed</span>`;
}

// ── ADD ───────────────────────────────────────────────────────────────────
async function openAddModal() {
    document.getElementById("form-error").classList.add("d-none");
    document.getElementById("paymentAmount").value = "";

    const membershipSelect = document.getElementById("paymentMembershipId");
    membershipSelect.innerHTML = `<option value="">Loading memberships...</option>`;

    try {
        const memberships = await getData("/memberships/");
        const active = (memberships || []).filter(m => ["active", "pending"].includes(m.status));

        if (!active.length) {
            membershipSelect.innerHTML = `<option value="">No active memberships found</option>`;
        } else {
            membershipSelect.innerHTML = `<option value="">Select a membership...</option>` +
                active.map(m => {
                    const planName = PLAN_NAMES[m.plan_id] || `Plan ${m.plan_id}`;
                    const price    = PLAN_PRICES[m.plan_id] ? `€${PLAN_PRICES[m.plan_id]}` : "";
                    return `<option value="${m.id}"
                        data-plan-id="${m.plan_id}"
                        data-price="${PLAN_PRICES[m.plan_id] || ""}">
                        ${m.id} — Member ${m.member_id} · ${planName} ${price}
                    </option>`;
                }).join("");
        }
    } catch {
        membershipSelect.innerHTML = `<option value="">Could not load memberships</option>`;
    }

    const modal = new bootstrap.Modal(document.getElementById("addPaymentModal"));
    modal.show();
}

// Al seleccionar membresía, rellena el importe automáticamente
function onMembershipSelected() {
    const select         = document.getElementById("paymentMembershipId");
    const selectedOption = select.options[select.selectedIndex];
    const price          = selectedOption.getAttribute("data-price");
    const amountField    = document.getElementById("paymentAmount");

    if (price && select.value !== "") {
        amountField.value    = parseFloat(price).toFixed(2);
        amountField.readOnly = true;
        amountField.classList.add("bg-light");
    } else {
        amountField.value    = "";
        amountField.readOnly = false;
        amountField.classList.remove("bg-light");
    }
}

async function submitAddPayment() {
    const membershipId = document.getElementById("paymentMembershipId").value;
    const amount       = document.getElementById("paymentAmount").value;
    const method       = document.getElementById("paymentMethod").value;
    const status       = document.getElementById("paymentStatus").value;
    const reference    = document.getElementById("paymentReference").value.trim();
    const notes        = document.getElementById("paymentNotes").value.trim();
    const errorDiv     = document.getElementById("form-error");

    if (!membershipId) {
        errorDiv.textContent = "Please select a membership.";
        errorDiv.classList.remove("d-none");
        return;
    }
    if (!amount || parseFloat(amount) <= 0) {
        errorDiv.textContent = "Amount must be greater than 0.";
        errorDiv.classList.remove("d-none");
        return;
    }

    errorDiv.classList.add("d-none");

    try {
        await postData("/payments/", {
            membership_id:  parseInt(membershipId),
            amount:         parseFloat(amount),
            payment_method: method,
            status:         status,
            reference:      reference,
            notes:          notes
        });

        bootstrap.Modal.getInstance(document.getElementById("addPaymentModal")).hide();
        // Reset amount field
        document.getElementById("paymentAmount").readOnly = false;
        document.getElementById("paymentAmount").classList.remove("bg-light");
        showSuccess("Payment registered successfully!");
        loadPayments();
    } catch (error) {
        console.error("Error saving payment:", error);
        errorDiv.textContent = "Could not save payment. Try again.";
        errorDiv.classList.remove("d-none");
    }
}