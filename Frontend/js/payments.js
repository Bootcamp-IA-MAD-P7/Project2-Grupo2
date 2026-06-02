document.addEventListener("DOMContentLoaded", loadPayments);

async function loadPayments() {
    showLoading("payments-table-container");
    try {
        const payments = await getData("/payments/");
        renderPaymentsTable(payments);
    } catch (error) {
        showError("Failed to fetch payment records.");
    }
}

function renderPaymentsTable(payments) {
    const container = document.getElementById("payments-table-container");
    container.innerHTML = `
        <table class="table">
            <thead>
                <tr>
                    <th>Member ID</th>
                    <th>Amount</th>
                    <th>Date</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                ${payments.map(p => `
                    <tr>
                        <td>${p.member_id}</td>
                        <td>${formatCurrency(p.amount)}</td>
                        <td>${formatDate(p.payment_date)}</td>
                        <td>${p.status}</td>
                    </tr>`).join("")}
            </tbody>
        </table>`;
}