document.addEventListener("DOMContentLoaded", loadPayments);

const mockPayments = [
  { id: 1, member_id: 1, membership_id: 1, amount: 49.99, date: "2026-05-01", status: "paid", payment_method: "card" },
  { id: 2, member_id: 2, membership_id: 1, amount: 49.99, date: "2026-05-15", status: "pending", payment_method: "transfer" },
  { id: 3, member_id: 3, membership_id: 2, amount: 29.99, date: "2026-05-20", status: "paid", payment_method: "cash" }
];

async function loadPayments() {
  showLoading("payments-table-container");
  try {
    let payments = mockPayments;
    // Cuando el backend esté listo, reemplaza la línea de arriba por:
    // payments = await getData("/payments/");
    renderPaymentsTable(payments);
  } catch (error) {
    showError("payments-table-container", "Could not load payments.");
  }
}

function renderPaymentsTable(payments) {
  const container = document.getElementById("payments-table-container");

  if (!payments || payments.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <h5>No payments found</h5>
        <p>No payment records available yet.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="table-responsive">
      <table class="table align-middle">
        <thead>
          <tr>
            <th>ID</th>
            <th>Member ID</th>
            <th>Membership ID</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Method</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          ${payments.map(p => `
            <tr>
              <td>${p.id}</td>
              <td>${p.member_id}</td>
              <td>${p.membership_id || "-"}</td>
              <td class="fw-semibold">${formatCurrency(p.amount)}</td>
              <td>${formatDate(p.date)}</td>
              <td>${p.payment_method || "-"}</td>
              <td>${renderPaymentBadge(p.status)}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function renderPaymentBadge(status) {
  if (status === "paid") return `<span class="badge badge-soft-success">Paid</span>`;
  if (status === "pending") return `<span class="badge badge-soft-warning">Pending</span>`;
  return `<span class="badge badge-soft-danger">Failed</span>`;
}

function openAddModal() {
  const modal = new bootstrap.Modal(document.getElementById("addPaymentModal"));
  modal.show();
}

async function submitAddPayment() {
  const memberId = document.getElementById("paymentMemberId").value;
  const membershipId = document.getElementById("paymentMembershipId").value;
  const amount = document.getElementById("paymentAmount").value;
  const date = document.getElementById("paymentDate").value;
  const method = document.getElementById("paymentMethod").value;
  const status = document.getElementById("paymentStatus").value;
  const errorDiv = document.getElementById("form-error");

  if (!memberId || !amount || !date) {
    errorDiv.textContent = "Member ID, amount and date are required.";
    errorDiv.classList.remove("d-none");
    return;
  }

  errorDiv.classList.add("d-none");

  const newPayment = {
    member_id: parseInt(memberId),
    membership_id: membershipId ? parseInt(membershipId) : null,
    amount: parseFloat(amount),
    date, status,
    payment_method: method
  };

  try {
    // Cuando el backend esté listo, descomenta esto:
    // await postData("/payments/", newPayment);

    mockPayments.push({ id: mockPayments.length + 1, ...newPayment });

    bootstrap.Modal.getInstance(document.getElementById("addPaymentModal")).hide();
    showSuccess("Payment registered successfully!");
    loadPayments();
  } catch (error) {
    errorDiv.textContent = "Could not save payment. Try again.";
    errorDiv.classList.remove("d-none");
  }
}