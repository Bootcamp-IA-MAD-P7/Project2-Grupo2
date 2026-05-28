import streamlit as st
import requests
from datetime import date, datetime

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="GymAPI Manager",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background-color: #0f0f0f;
        color: #f0f0f0;
    }

    section[data-testid="stSidebar"] {
        background-color: #1a1a1a;
        border-right: 1px solid #2a2a2a;
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: #f0f0f0 !important;
    }

    h1, h2, h3 {
        font-family: 'Space Mono', monospace;
        color: #e8ff47;
        letter-spacing: -0.5px;
    }

    .metric-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 20px;
        margin: 8px 0;
    }

    .tag {
        display: inline-block;
        background: #e8ff47;
        color: #0f0f0f;
        font-family: 'Space Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 4px;
        margin: 2px;
    }

    .tag-red { background: #ff4747; color: white; }
    .tag-green { background: #47ff8a; color: #0f0f0f; }
    .tag-blue { background: #47b4ff; color: #0f0f0f; }
    .tag-grey { background: #444; color: #f0f0f0; }

    .stButton > button {
        background: #e8ff47;
        color: #0f0f0f;
        font-family: 'Space Mono', monospace;
        font-weight: 700;
        border: none;
        border-radius: 6px;
        padding: 8px 20px;
        cursor: pointer;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        background: #ffffff;
        transform: translateY(-1px);
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > div > input {
        background: #1a1a1a !important;
        color: #f0f0f0 !important;
        border: 1px solid #333 !important;
        border-radius: 6px !important;
    }

    .stSuccess { background: #1a2e1a !important; }
    .stError { background: #2e1a1a !important; }

    hr { border-color: #2a2a2a; }

    .row-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 8px;
        padding: 16px;
        margin: 6px 0;
    }
</style>
""", unsafe_allow_html=True)


def api_get(endpoint, params=None):
    try:
        r = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to API. Is the server running?"
    except requests.exceptions.HTTPError as e:
        return None, f"Error {e.response.status_code}: {e.response.json().get('detail', str(e))}"
    except Exception as e:
        return None, str(e)


def api_post(endpoint, data):
    try:
        r = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to API. Is the server running?"
    except requests.exceptions.HTTPError as e:
        return None, f"Error {e.response.status_code}: {e.response.json().get('detail', str(e))}"
    except Exception as e:
        return None, str(e)


def api_patch(endpoint, data=None):
    try:
        r = requests.patch(f"{BASE_URL}{endpoint}", json=data, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to API. Is the server running?"
    except requests.exceptions.HTTPError as e:
        return None, f"Error {e.response.status_code}: {e.response.json().get('detail', str(e))}"
    except Exception as e:
        return None, str(e)


def api_delete(endpoint):
    try:
        r = requests.delete(f"{BASE_URL}{endpoint}", timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to API. Is the server running?"
    except requests.exceptions.HTTPError as e:
        return None, f"Error {e.response.status_code}: {e.response.json().get('detail', str(e))}"
    except Exception as e:
        return None, str(e)


def status_tag(status):
    colors = {
        "confirmed": "tag-green",
        "cancelled": "tag-red",
        "no_show": "tag-grey",
        "active": "tag-green",
        "inactive": "tag-grey",
        "suspended": "tag-red",
        "pending": "tag-blue",
        "paid": "tag-green",
        "overdue": "tag-red",
    }
    css = colors.get(status, "tag")
    return f'<span class="tag {css}">{status.upper()}</span>'


# ── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏋️ GymAPI")
    st.markdown("---")
    module = st.radio(
        "Module",
        ["Shifts", "Reservations", "Members", "Memberships", "Plans", "Payments", "Attendance"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown(f"<small style='color:#555'>API: {BASE_URL}</small>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# SHIFTS
# ══════════════════════════════════════════════════════════════════════════
if module == "Shifts":
    st.markdown("# Shifts")

    tab1, tab2, tab3 = st.tabs(["📋 List", "➕ Create", "📊 Availability"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            day_filter = st.selectbox("Filter by day", ["All", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])
        with col2:
            name_filter = st.text_input("Filter by name")

        params = {}
        if day_filter != "All":
            params["day_of_week"] = day_filter
        if name_filter:
            params["name"] = name_filter

        data, err = api_get("/shifts/", params=params)
        if err:
            st.error(err)
        elif data:
            for shift in data:
                with st.container():
                    st.markdown(f"""
                    <div class="row-card">
                        <strong style="font-family:'Space Mono',monospace;color:#e8ff47">{shift.get('class_name','')}</strong>
                        &nbsp;&nbsp;<span class="tag">{shift.get('day_of_week','').upper()}</span>
                        &nbsp;<span class="tag tag-blue">{shift.get('start_time','')} – {shift.get('end_time','')}</span>
                        &nbsp;<span class="tag tag-grey">👤 {shift.get('instructor','')}</span>
                        &nbsp;<span class="tag">Max {shift.get('max_capacity','')} spots</span>
                        <span style="float:right;color:#555;font-size:12px">ID: {shift.get('id','')}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    col_u, col_d = st.columns([1, 1])
                    with col_u:
                        with st.expander("Edit"):
                            new_instructor = st.text_input("Instructor", value=shift.get("instructor", ""), key=f"inst_{shift['id']}")
                            new_capacity = st.number_input("Max capacity", value=shift.get("max_capacity", 1), min_value=1, key=f"cap_{shift['id']}")
                            if st.button("Save", key=f"save_{shift['id']}"):
                                result, err = api_patch(f"/shifts/{shift['id']}", {"instructor": new_instructor, "max_capacity": new_capacity})
                                if err:
                                    st.error(err)
                                else:
                                    st.success("Updated")
                                    st.rerun()
                    with col_d:
                        if st.button("🗑 Delete", key=f"del_{shift['id']}"):
                            result, err = api_delete(f"/shifts/{shift['id']}")
                            if err:
                                st.error(err)
                            else:
                                st.success("Deleted")
                                st.rerun()
        else:
            st.info("No shifts found.")

    with tab2:
        st.markdown("### Create new shift")
        col1, col2 = st.columns(2)
        with col1:
            class_name = st.text_input("Class name")
            instructor = st.text_input("Instructor")
            day_of_week = st.selectbox("Day of week", ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])
        with col2:
            start_time = st.time_input("Start time")
            end_time = st.time_input("End time")
            max_capacity = st.number_input("Max capacity", min_value=1, value=10)
            active_slot = st.checkbox("Active", value=True)

        if st.button("Create Shift"):
            if not class_name or not instructor:
                st.error("Class name and instructor are required.")
            else:
                payload = {
                    "class_name": class_name,
                    "instructor": instructor,
                    "day_of_week": day_of_week,
                    "start_time": str(start_time),
                    "end_time": str(end_time),
                    "max_capacity": max_capacity,
                    "active_slot": active_slot
                }
                result, err = api_post("/shifts/", payload)
                if err:
                    st.error(err)
                else:
                    st.success(f"Shift created with ID {result['id']}")

    with tab3:
        st.markdown("### Check availability")
        shifts_data, _ = api_get("/shifts/")
        if shifts_data:
            shift_options = {f"{s['class_name']} ({s['day_of_week']}) — ID {s['id']}": s['id'] for s in shifts_data}
            selected = st.selectbox("Select shift", list(shift_options.keys()))
            check_date = st.date_input("Date", value=date.today())

            if st.button("Check"):
                shift_id = shift_options[selected]
                avail, err = api_get(f"/shifts/{shift_id}/availability", params={"date": str(check_date)})
                if err:
                    st.error(err)
                else:
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Max Capacity", avail["max_capacity"])
                    col2.metric("Active Bookings", avail["active_bookings"])
                    col3.metric("Available Spots", avail["available_spots"])
                    if avail["is_available"]:
                        st.success("✅ Class has available spots")
                    else:
                        st.error("❌ Class is full")


# ══════════════════════════════════════════════════════════════════════════
# RESERVATIONS
# ══════════════════════════════════════════════════════════════════════════
elif module == "Reservations":
    st.markdown("# Reservations")

    tab1, tab2 = st.tabs(["📋 List", "➕ Create"])

    with tab1:
        member_id_filter = st.number_input("Filter by Member ID", min_value=0, value=0, step=1)

        if member_id_filter > 0:
            data, err = api_get(f"/reservations/member/{int(member_id_filter)}")
        else:
            data, err = None, "Enter a member ID to search"

        if err and member_id_filter > 0:
            st.error(err)
        elif data:
            for r in data:
                st.markdown(f"""
                <div class="row-card">
                    <strong style="font-family:'Space Mono',monospace">Reservation #{r.get('id')}</strong>
                    &nbsp;&nbsp;{status_tag(r.get('status',''))}
                    <br><small style="color:#888">Shift ID: {r.get('shift_id')} &nbsp;|&nbsp; Date: {r.get('date')} &nbsp;|&nbsp; Member: {r.get('member_id')}</small>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    if r.get("status") == "confirmed":
                        if st.button("Cancel", key=f"cancel_{r['id']}"):
                            result, err = api_patch(f"/reservations/{r['id']}/cancel")
                            if err:
                                st.error(err)
                            else:
                                st.success("Cancelled")
                                st.rerun()
                with col2:
                    if r.get("status") == "confirmed":
                        if st.button("No Show", key=f"noshow_{r['id']}"):
                            result, err = api_patch(f"/reservations/{r['id']}/no-show")
                            if err:
                                st.error(err)
                            else:
                                st.success("Marked as no-show")
                                st.rerun()
        elif member_id_filter == 0:
            st.info("Enter a member ID above to see their reservations.")

    with tab2:
        st.markdown("### Create new reservation")
        shifts_data, _ = api_get("/shifts/")
        if shifts_data:
            shift_options = {f"{s['class_name']} ({s['day_of_week']}) — ID {s['id']}": s['id'] for s in shifts_data}
            selected_shift = st.selectbox("Select shift", list(shift_options.keys()))
            reservation_date = st.date_input("Date", value=date.today())

            if st.button("Create Reservation"):
                payload = {
                    "shift_id": shift_options[selected_shift],
                    "date": str(reservation_date)
                }
                result, err = api_post("/reservations/", payload)
                if err:
                    st.error(err)
                else:
                    st.success(f"Reservation created — ID {result['id']} | Status: {result['status']}")
        else:
            st.warning("No shifts available. Create a shift first.")


# ══════════════════════════════════════════════════════════════════════════
# MEMBERS
# ══════════════════════════════════════════════════════════════════════════
elif module == "Members":
    st.markdown("# Members")

    tab1, tab2 = st.tabs(["📋 List", "➕ Create"])

    with tab1:
        data, err = api_get("/members/")
        if err:
            st.error(err)
        elif data:
            for m in data:
                st.markdown(f"""
                <div class="row-card">
                    <strong style="font-family:'Space Mono',monospace;color:#e8ff47">{m.get('first_name','')} {m.get('last_name','')}</strong>
                    &nbsp;&nbsp;{status_tag(m.get('is_active') and 'active' or 'inactive')}
                    <br><small style="color:#888">📧 {m.get('email','')} &nbsp;|&nbsp; 📞 {m.get('phone','')} &nbsp;|&nbsp; ID: {m.get('id')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No members found.")

    with tab2:
        st.markdown("### Register new member")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First name")
            last_name = st.text_input("Last name")
            email = st.text_input("Email")
        with col2:
            phone = st.text_input("Phone")
            birth_date = st.date_input("Birth date", value=None)

        if st.button("Register Member"):
            if not first_name or not last_name or not email:
                st.error("First name, last name and email are required.")
            else:
                payload = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone": phone,
                }
                if birth_date:
                    payload["birth_date"] = str(birth_date)
                result, err = api_post("/members/", payload)
                if err:
                    st.error(err)
                else:
                    st.success(f"Member registered — ID {result['id']}")


# ══════════════════════════════════════════════════════════════════════════
# MEMBERSHIPS
# ══════════════════════════════════════════════════════════════════════════
elif module == "Memberships":
    st.markdown("# Memberships")

    tab1, tab2 = st.tabs(["📋 List", "➕ Create"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox("Filter by status", ["All", "active", "inactive", "expired"])
        with col2:
            member_filter = st.number_input("Filter by Member ID", min_value=0, value=0, step=1)

        params = {}
        if status_filter != "All":
            params["status"] = status_filter
        if member_filter > 0:
            params["member_id"] = int(member_filter)

        data, err = api_get("/memberships/", params=params)
        if err:
            st.error(err)
        elif data:
            for m in data:
                st.markdown(f"""
                <div class="row-card">
                    <strong style="font-family:'Space Mono',monospace">Membership #{m.get('id')}</strong>
                    &nbsp;&nbsp;{status_tag(m.get('status',''))}
                    <br><small style="color:#888">Member ID: {m.get('member_id')} &nbsp;|&nbsp; Plan ID: {m.get('plan_id')} &nbsp;|&nbsp; {m.get('start_date','')} → {m.get('end_date','')}</small>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Renew", key=f"renew_{m['id']}"):
                        result, err = api_post(f"/memberships/{m['id']}/renew", {})
                        if err:
                            st.error(err)
                        else:
                            st.success("Renewed")
                            st.rerun()
        else:
            st.info("No memberships found.")

        st.markdown("---")
        st.markdown("### ⚠️ Expiring soon")
        days = st.slider("Days ahead", 1, 60, 7)
        expiring, err2 = api_get("/memberships/expiring-soon", params={"days": days})
        if err2:
            st.error(err2)
        elif expiring:
            for m in expiring:
                st.markdown(f"""
                <div class="row-card">
                    <strong>Membership #{m.get('id')}</strong> — Member {m.get('member_id')} — expires {m.get('end_date')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success(f"No memberships expiring in the next {days} days.")

    with tab2:
        st.markdown("### Create membership")
        plans_data, _ = api_get("/plans/")
        if plans_data:
            plan_options = {f"{p.get('name','Plan')} — ID {p['id']}": p['id'] for p in plans_data}
            selected_plan = st.selectbox("Select plan", list(plan_options.keys()))
        else:
            selected_plan = None
            st.warning("No plans available.")

        member_id = st.number_input("Member ID", min_value=1, step=1)
        start_date = st.date_input("Start date", value=date.today())

        if st.button("Create Membership"):
            if not plans_data:
                st.error("No plans available.")
            else:
                payload = {
                    "member_id": int(member_id),
                    "plan_id": plan_options[selected_plan],
                    "start_date": str(start_date)
                }
                result, err = api_post("/memberships/", payload)
                if err:
                    st.error(err)
                else:
                    st.success(f"Membership created — ID {result['id']}")


# ══════════════════════════════════════════════════════════════════════════
# PLANS
# ══════════════════════════════════════════════════════════════════════════
elif module == "Plans":
    st.markdown("# Plans")

    tab1, tab2 = st.tabs(["📋 List", "➕ Create"])

    with tab1:
        data, err = api_get("/plans/")
        if err:
            st.error(err)
        elif data:
            for p in data:
                st.markdown(f"""
                <div class="row-card">
                    <strong style="font-family:'Space Mono',monospace;color:#e8ff47">{p.get('name','')}</strong>
                    &nbsp;&nbsp;<span class="tag">€{p.get('price','')}</span>
                    &nbsp;<span class="tag tag-blue">{p.get('duration_days','')} days</span>
                    <span style="float:right;color:#555;font-size:12px">ID: {p.get('id')}</span>
                    <br><small style="color:#888">{p.get('description','')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No plans found.")

    with tab2:
        st.markdown("### Create new plan")
        plan_name = st.text_input("Plan name")
        plan_price = st.number_input("Price (€)", min_value=0.0, step=0.01)
        plan_duration = st.number_input("Duration (days)", min_value=1, value=30)
        plan_description = st.text_area("Description")

        if st.button("Create Plan"):
            if not plan_name:
                st.error("Plan name is required.")
            else:
                payload = {
                    "name": plan_name,
                    "price": plan_price,
                    "duration_days": plan_duration,
                    "description": plan_description
                }
                result, err = api_post("/plans/", payload)
                if err:
                    st.error(err)
                else:
                    st.success(f"Plan created — ID {result['id']}")


# ══════════════════════════════════════════════════════════════════════════
# PAYMENTS
# ══════════════════════════════════════════════════════════════════════════
elif module == "Payments":
    st.markdown("# Payments")

    tab1, tab2 = st.tabs(["📋 List", "➕ Register"])

    with tab1:
        data, err = api_get("/payments/")
        if err:
            st.error(err)
        elif data:
            for p in data:
                st.markdown(f"""
                <div class="row-card">
                    <strong style="font-family:'Space Mono',monospace">Payment #{p.get('id')}</strong>
                    &nbsp;&nbsp;{status_tag(p.get('status',''))}
                    &nbsp;<span class="tag">€{p.get('amount','')}</span>
                    &nbsp;<span class="tag tag-grey">{p.get('payment_method','')}</span>
                    <br><small style="color:#888">Membership ID: {p.get('membership_id')} &nbsp;|&nbsp; Date: {p.get('payment_date','')}</small>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("📥 Export CSV"):
            csv_data, err = api_get("/payments/export-csv")
            if err:
                st.error(err)
            else:
                st.download_button("Download CSV", data=str(csv_data), file_name="payments.csv", mime="text/csv")

    with tab2:
        st.markdown("### Register payment")
        membership_id = st.number_input("Membership ID", min_value=1, step=1)
        amount = st.number_input("Amount (€)", min_value=0.0, step=0.01)
        method = st.selectbox("Payment method", ["cash", "card", "transfer"])
        reference = st.text_input("Reference (optional)")

        if st.button("Register Payment"):
            payload = {
                "membership_id": int(membership_id),
                "amount": amount,
                "payment_method": method,
            }
            if reference:
                payload["reference"] = reference
            result, err = api_post("/payments/", payload)
            if err:
                st.error(err)
            else:
                st.success(f"Payment registered — ID {result['id']}")


# ══════════════════════════════════════════════════════════════════════════
# ATTENDANCE
# ══════════════════════════════════════════════════════════════════════════
elif module == "Attendance":
    st.markdown("# Attendance")

    tab1, tab2 = st.tabs(["📋 List", "➕ Register"])

    with tab1:
        data, err = api_get("/attendances/")
        if err:
            st.error(err)
        elif data:
            for a in data:
                st.markdown(f"""
                <div class="row-card">
                    <strong style="font-family:'Space Mono',monospace">Attendance #{a.get('id')}</strong>
                    <br><small style="color:#888">Reservation ID: {a.get('reservation_id')} &nbsp;|&nbsp; Check-in: {a.get('check_in','')} &nbsp;|&nbsp; Check-out: {a.get('check_out','—')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No attendance records found.")

    with tab2:
        st.markdown("### Register attendance")
        reservation_id = st.number_input("Reservation ID", min_value=1, step=1)
        notes = st.text_input("Notes (optional)")

        if st.button("Register Attendance"):
            payload = {"reservation_id": int(reservation_id)}
            if notes:
                payload["notes"] = notes
            result, err = api_post("/attendances/", payload)
            if err:
                st.error(err)
            else:
                st.success(f"Attendance registered — ID {result['id']}")
