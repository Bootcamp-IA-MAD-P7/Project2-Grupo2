import streamlit as st
import requests
from datetime import date, datetime

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="GymAPI Manager",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    .stApp {
        background-color: #f3f0fa;
        color: #3b2f5e;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #e8e0f8 0%, #ddd5f5 100%);
        border-right: 1px solid #cdc0ef;
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: #4a3880 !important;
        font-weight: 600;
    }

    h1, h2, h3 {
        font-family: 'Nunito', sans-serif;
        color: #6b4fbb;
        font-weight: 800;
        letter-spacing: -0.3px;
    }

    h1::before { content: "✦ "; }

    .tag {
        display: inline-block;
        background: #e8e0f8;
        color: #6b4fbb;
        font-family: 'Nunito', sans-serif;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 999px;
        margin: 2px;
        border: 1px solid #cdc0ef;
    }

    .tag-red { background: #fde8f0; color: #c0436a; border-color: #f5b8cf; }
    .tag-green { background: #e6f8f0; color: #2d8f66; border-color: #a8e8cc; }
    .tag-blue { background: #e8f0fd; color: #3a5fc0; border-color: #b8caee; }
    .tag-grey { background: #eeebf8; color: #7a6ea0; border-color: #cdc0ef; }

    .stButton > button {
        background: linear-gradient(135deg, #9b7fe8, #b89af0);
        color: white;
        font-family: 'Nunito', sans-serif;
        font-weight: 700;
        border: none;
        border-radius: 999px;
        padding: 8px 22px;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: 0 2px 8px rgba(155,127,232,0.3);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #8b6fd8, #a88ae0);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(155,127,232,0.4);
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > div > input {
        background: #ffffff !important;
        color: #3b2f5e !important;
        border: 1.5px solid #cdc0ef !important;
        border-radius: 12px !important;
    }

    .stSuccess { background: #e6f8f0 !important; border-radius: 12px; }
    .stError { background: #fde8f0 !important; border-radius: 12px; }
    .stInfo { background: #eee8fc !important; border-radius: 12px; }
    .stWarning { background: #fdf5e8 !important; border-radius: 12px; }

    hr { border-color: #cdc0ef; }

    .row-card {
        background: #ffffff;
        border: 1.5px solid #e0d8f5;
        border-radius: 18px;
        padding: 16px 20px;
        margin: 8px 0;
        box-shadow: 0 2px 12px rgba(107,79,187,0.07);
        transition: box-shadow 0.2s;
    }

    .row-card:hover {
        box-shadow: 0 4px 20px rgba(107,79,187,0.13);
    }

    /* Slider purple */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #9b7fe8, #b89af0) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #ece6f9;
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-family: 'Nunito', sans-serif;
        font-weight: 700;
        color: #7a6ea0;
    }

    .stTabs [aria-selected="true"] {
        background: #9b7fe8 !important;
        color: white !important;
    }

    /* Metrics */
    [data-testid="metric-container"] {
        background: #ffffff;
        border: 1.5px solid #e0d8f5;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(107,79,187,0.07);
    }

    [data-testid="metric-container"] label {
        color: #9b7fe8 !important;
        font-weight: 700;
    }

    /* Sidebar logo area */
    .sidebar-logo {
        text-align: center;
        padding: 10px 0 5px 0;
        font-size: 32px;
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
    st.markdown('<div class="sidebar-logo">🌸</div>', unsafe_allow_html=True)
    st.markdown("## GymAPI")
    st.markdown("---")
    module = st.radio(
        "Module",
        ["Shifts", "Reservations", "Members", "Memberships", "Plans", "Payments", "Attendance"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown(f"<small style='color:#a090c8'>API: {BASE_URL}</small>", unsafe_allow_html=True)

module_icons = {
    "Shifts": "🗓️",
    "Reservations": "📌",
    "Members": "👤",
    "Memberships": "💜",
    "Plans": "📋",
    "Payments": "💳",
    "Attendance": "✅",
}


# ══════════════════════════════════════════════════════════════════════════
# SHIFTS
# ══════════════════════════════════════════════════════════════════════════
if module == "Shifts":
    st.markdown(f"# {module_icons['Shifts']} Shifts")

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
                        <strong style="font-family:'Nunito',sans-serif;color:#6b4fbb;font-size:16px">✦ {shift.get('class_name','')}</strong>
                        &nbsp;&nbsp;<span class="tag">{shift.get('day_of_week','').upper()}</span>
                        &nbsp;<span class="tag tag-blue">🕐 {shift.get('start_time','')} – {shift.get('end_time','')}</span>
                        &nbsp;<span class="tag tag-grey">👤 {shift.get('instructor','')}</span>
                        &nbsp;<span class="tag">🏃 Max {shift.get('max_capacity','')} spots</span>
                        <span style="float:right;color:#b0a0d8;font-size:12px">ID: {shift.get('id','')}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    col_u, col_d = st.columns([1, 1])
                    with col_u:
                        with st.expander("✏️ Edit"):
                            new_instructor = st.text_input("Instructor", value=shift.get("instructor", ""), key=f"inst_{shift['id']}")
                            new_capacity = st.number_input("Max capacity", value=shift.get("max_capacity", 1), min_value=1, key=f"cap_{shift['id']}")
                            if st.button("Save changes", key=f"save_{shift['id']}"):
                                result, err = api_patch(f"/shifts/{shift['id']}", {"instructor": new_instructor, "max_capacity": new_capacity})
                                if err:
                                    st.error(err)
                                else:
                                    st.success("✨ Updated!")
                                    st.rerun()
                    with col_d:
                        if st.button("🗑️ Delete", key=f"del_{shift['id']}"):
                            result, err = api_delete(f"/shifts/{shift['id']}")
                            if err:
                                st.error(err)
                            else:
                                st.success("Deleted")
                                st.rerun()
        else:
            st.info("💜 No shifts found.")

    with tab2:
        st.markdown("### ✨ Create new shift")
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

        if st.button("🌸 Create Shift"):
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
                    st.success(f"✨ Shift created with ID {result['id']}")

    with tab3:
        st.markdown("### 🔍 Check availability")
        shifts_data, _ = api_get("/shifts/")
        if shifts_data:
            shift_options = {f"{s['class_name']} ({s['day_of_week']}) — ID {s['id']}": s['id'] for s in shifts_data}
            selected = st.selectbox("Select shift", list(shift_options.keys()))
            check_date = st.date_input("Date", value=date.today())

            if st.button("✦ Check availability"):
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
                        st.success("✅ Class has available spots!")
                    else:
                        st.error("❌ Class is full")


# ══════════════════════════════════════════════════════════════════════════
# RESERVATIONS
# ══════════════════════════════════════════════════════════════════════════
elif module == "Reservations":
    st.markdown(f"# {module_icons['Reservations']} Reservations")

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
                    <strong style="font-family:'Nunito',sans-serif;color:#6b4fbb">✦ Reservation #{r.get('id')}</strong>
                    &nbsp;&nbsp;{status_tag(r.get('status',''))}
                    <br><small style="color:#9b8ec4">Shift ID: {r.get('shift_id')} &nbsp;|&nbsp; 📅 {r.get('date')} &nbsp;|&nbsp; 👤 Member {r.get('member_id')}</small>
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
            st.info("💜 Enter a member ID above to see their reservations.")

    with tab2:
        st.markdown("### ✨ Create new reservation")
        shifts_data, _ = api_get("/shifts/")
        if shifts_data:
            shift_options = {f"{s['class_name']} ({s['day_of_week']}) — ID {s['id']}": s['id'] for s in shifts_data}
            selected_shift = st.selectbox("Select shift", list(shift_options.keys()))
            reservation_date = st.date_input("Date", value=date.today())

            if st.button("🌸 Create Reservation"):
                payload = {
                    "shift_id": shift_options[selected_shift],
                    "date": str(reservation_date)
                }
                result, err = api_post("/reservations/", payload)
                if err:
                    st.error(err)
                else:
                    st.success(f"✨ Reservation created — ID {result['id']} | Status: {result['status']}")
        else:
            st.warning("No shifts available. Create a shift first.")


# ══════════════════════════════════════════════════════════════════════════
# MEMBERS
# ══════════════════════════════════════════════════════════════════════════
elif module == "Members":
    st.markdown(f"# {module_icons['Members']} Members")

    tab1, tab2 = st.tabs(["📋 List", "➕ Create"])

    with tab1:
        data, err = api_get("/members/")
        if err:
            st.error(err)
        elif data:
            for m in data:
                st.markdown(f"""
                <div class="row-card">
                    <strong style="font-family:'Nunito',sans-serif;color:#6b4fbb;font-size:16px">✦ {m.get('first_name','')} {m.get('last_name','')}</strong>
                    &nbsp;&nbsp;{status_tag(m.get('is_active') and 'active' or 'inactive')}
                    <br><small style="color:#9b8ec4">📧 {m.get('email','')} &nbsp;|&nbsp; 📞 {m.get('phone','')} &nbsp;|&nbsp; ID: {m.get('id')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("💜 No members found.")

    with tab2:
        st.markdown("### ✨ Register new member")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First name")
            last_name = st.text_input("Last name")
            email = st.text_input("Email")
        with col2:
            phone = st.text_input("Phone")
            birth_date = st.date_input("Birth date", value=None)

        if st.button("🌸 Register Member"):
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
                    st.success(f"✨ Member registered — ID {result['id']}")


# ══════════════════════════════════════════════════════════════════════════
# MEMBERSHIPS
# ══════════════════════════════════════════════════════════════════════════
elif module == "Memberships":
    st.markdown(f"# {module_icons['Memberships']} Memberships")

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
                    <strong style="font-family:'Nunito',sans-serif;color:#6b4fbb">✦ Membership #{m.get('id')}</strong>
                    &nbsp;&nbsp;{status_tag(m.get('status',''))}
                    <br><small style="color:#9b8ec4">👤 Member {m.get('member_id')} &nbsp;|&nbsp; 📋 Plan {m.get('plan_id')} &nbsp;|&nbsp; 📅 {m.get('start_date','')} → {m.get('end_date','')}</small>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Renew", key=f"renew_{m['id']}"):
                        result, err = api_post(f"/memberships/{m['id']}/renew", {})
                        if err:
                            st.error(err)
                        else:
                            st.success("✨ Renewed!")
                            st.rerun()
        else:
            st.info("💜 No memberships found.")

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
                    <strong style="color:#c0436a">⚠️ Membership #{m.get('id')}</strong> — Member {m.get('member_id')} — expires {m.get('end_date')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success(f"✨ No memberships expiring in the next {days} days.")

    with tab2:
        st.markdown("### ✨ Create membership")
        plans_data,