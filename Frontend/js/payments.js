document.addEventListener("DOMContentLoaded", loadPayments);

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
    if (status === "pending") return `<span class="badge badge-soft-warning">Pending</span>`;
    if (status === "refunded") return `<span class="badge badge-soft-warning">Refunded</span>`;
    return `<span class="badge badge-soft-danger">Failed</span>`;
}

function openAddModal() {
    const modal = new bootstrap.Modal(document.getElementById("addPaymentModal"));
    modal.show();
}

async function submitAddPayment() {
    const membershipId = document.getElementById("paymentMembershipId").value;
    const amount = document.getElementById("paymentAmount").value;
    const method = document.getElementById("paymentMethod").value;
    const status = document.getElementById("paymentStatus").value;
    const reference = document.getElementById("paymentReference").value.trim();
    const notes = document.getElementById("paymentNotes").value.trim();
    const errorDiv = document.getElementById("form-error");

    if (!membershipId) {
        errorDiv.textContent = "Membership ID is required.";
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
            membership_id: parseInt(membershipId),
            amount: parseFloat(amount),
            payment_method: method,
            status: status,
            reference: reference,
            notes: notes
        });

        bootstrap.Modal.getInstance(document.getElementById("addPaymentModal")).hide();
        showSuccess("Payment registered successfully!");
        loadPayments();
    } catch (error) {
        console.error("Error saving payment:", error);
        errorDiv.textContent = "Could not save payment. Try again.";
        errorDiv.classList.remove("d-none");
    }
}