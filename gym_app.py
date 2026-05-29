import streamlit as st
import requests
from datetime import date

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="GymAPI Admin",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }
.stApp { background: #f3f0fa; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg,#e8e0f8,#ddd5f5); border-right:1px solid #cdc0ef; }
section[data-testid="stSidebar"] * { color:#4a3880 !important; }
h1,h2,h3 { font-family:'Nunito',sans-serif !important; color:#6b4fbb !important; font-weight:800 !important; }
.stButton>button { background:linear-gradient(135deg,#9b7fe8,#b89af0) !important; color:white !important; font-family:'Nunito',sans-serif !important; font-weight:700 !important; border:none !important; border-radius:999px !important; padding:8px 22px !important; box-shadow:0 2px 8px rgba(155,127,232,0.3) !important; }
.stButton>button:hover { background:linear-gradient(135deg,#8b6fd8,#a88ae0) !important; transform:translateY(-1px) !important; }
.stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea { background:#fff !important; color:#3b2f5e !important; border:1.5px solid #cdc0ef !important; border-radius:12px !important; }
.stSelectbox>div>div { background:#fff !important; border:1.5px solid #cdc0ef !important; border-radius:12px !important; }
.stDateInput>div>div>input { background:#fff !important; border:1.5px solid #cdc0ef !important; border-radius:12px !important; }
.stTabs [data-baseweb="tab-list"] { background:#ece6f9; border-radius:12px; padding:4px; gap:4px; }
.stTabs [data-baseweb="tab"] { border-radius:8px !important; font-family:'Nunito',sans-serif !important; font-weight:700 !important; color:#7a6ea0 !important; }
.stTabs [aria-selected="true"] { background:#9b7fe8 !important; color:white !important; }
[data-testid="metric-container"] { background:#fff; border:1.5px solid #e0d8f5; border-radius:16px; padding:16px; box-shadow:0 2px 8px rgba(107,79,187,0.07); }
[data-testid="metric-container"] label { color:#9b7fe8 !important; font-weight:700 !important; }
.card { background:#fff; border:1.5px solid #e0d8f5; border-radius:18px; padding:18px 22px; margin:8px 0; box-shadow:0 2px 12px rgba(107,79,187,0.07); transition:box-shadow 0.2s; }
.card:hover { box-shadow:0 4px 20px rgba(107,79,187,0.13); }
.pill { display:inline-block; font-size:11px; font-weight:700; padding:3px 10px; border-radius:999px; margin:2px; border:1px solid; }
.pill-default { background:#e8e0f8; color:#6b4fbb; border-color:#cdc0ef; }
.pill-green { background:#e6f8f0; color:#2d8f66; border-color:#a8e8cc; }
.pill-red { background:#fde8f0; color:#c0436a; border-color:#f5b8cf; }
.pill-blue { background:#e8f0fd; color:#3a5fc0; border-color:#b8caee; }
.pill-amber { background:#fdf5e8; color:#b07d1e; border-color:#f0d8a0; }
.pill-grey { background:#eeebf8; color:#7a6ea0; border-color:#cdc0ef; }
.form-section { background:#fff; border:1.5px solid #e0d8f5; border-radius:18px; padding:24px; margin-top:8px; }
.section-label { font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.08em; color:#b0a0d8; margin-bottom:4px; }
</style>
""", unsafe_allow_html=True)


def api_get(endpoint, params=None):
    try:
        r = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to API. Is the server running on localhost:8000?"
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = e.response.text or str(e)
        return None, f"Error {e.response.status_code}: {detail}"
    except Exception as e:
        return None, str(e)


def api_post(endpoint, data):
    try:
        r = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to API."
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = e.response.text or str(e)
        return None, f"Error {e.response.status_code}: {detail}"
    except Exception as e:
        return None, str(e)


def api_patch(endpoint, data=None):
    try:
        r = requests.patch(f"{BASE_URL}{endpoint}", json=data, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to API."
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = e.response.text or str(e)
        return None, f"Error {e.response.status_code}: {detail}"
    except Exception as e:
        return None, str(e)


def api_delete(endpoint):
    try:
        r = requests.delete(f"{BASE_URL}{endpoint}", timeout=5)
        r.raise_for_status()
        try:
            return r.json(), None
        except Exception:
            return {}, None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to API."
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = e.response.text or str(e)
        return None, f"Error {e.response.status_code}: {detail}"
    except Exception as e:
        return None, str(e)


def pill(label, kind="default"):
    return f'<span class="pill pill-{kind}">{label}</span>'


def status_pill(status):
    mapping = {
        "confirmed": ("confirmed", "green"),
        "cancelled": ("cancelled", "red"),
        "no_show": ("no show", "grey"),
        "active": ("active", "green"),
        "inactive": ("inactive", "grey"),
        "suspended": ("suspended", "red"),
        "pending": ("pending", "amber"),
        "paid": ("paid", "green"),
        "completed": ("completed", "green"),
        "failed": ("failed", "red"),
        "refunded": ("refunded", "blue"),
        "overdue": ("overdue", "red"),
        "expired": ("expired", "red"),
    }
    label, kind = mapping.get(status, (status, "default"))
    return pill(label, kind)


with st.sidebar:
    st.markdown("## 🏋️ GymAPI Admin")
    st.markdown("<small>Superuser panel</small>", unsafe_allow_html=True)
    st.markdown("---")
    module = st.radio(
        "nav",
        ["📅 Shifts", "📌 Reservations", "👤 Members", "💜 Memberships", "📋 Plans", "💳 Payments", "✅ Attendance"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown(f"<small style='color:#a090c8'>API · {BASE_URL}</small>", unsafe_allow_html=True)

module = module.split(" ", 1)[1]


if module == "Shifts":
    st.markdown("# 📅 Shifts")
    tab_list, tab_create, tab_avail = st.tabs(["All shifts", "Create shift", "Check availability"])

    with tab_list:
        c1, c2 = st.columns(2)
        with c1:
            day_filter = st.selectbox("Day", ["All", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])
        with c2:
            name_filter = st.text_input("Search class name", placeholder="Yoga, Spinning...")

        params = {}
        if day_filter != "All":
            params["day_of_week"] = day_filter
        if name_filter:
            params["name"] = name_filter

        data, err = api_get("/shifts/", params=params)
        if err:
            st.error(err)
        elif not data:
            st.info("No shifts found.")
        else:
            st.markdown(f"**{len(data)} shift(s) found**")
            for s in data:
                st.markdown(f"""
                <div class="card">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start">
                    <div>
                      <strong style="font-size:16px;color:#6b4fbb">{s.get('class_name','')}</strong>
                      <span style="font-size:11px;color:#b0a0d8;margin-left:10px">ID {s.get('id')}</span><br>
                      {pill(s.get('day_of_week','').capitalize(),'blue')}
                      {pill(f"{s.get('start_time','')} – {s.get('end_time','')}","default")}
                      {pill(f"👤 {s.get('instructor','')}","grey")}
                      {pill(f"Max {s.get('max_capacity','')}","default")}
                      {pill("Active","green") if s.get('active_slot') else pill("Inactive","grey")}
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander(f"Edit / Delete — {s.get('class_name','')}"):
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        new_instructor = st.text_input("Instructor", value=s.get("instructor",""), key=f"i_{s['id']}")
                        new_capacity = st.number_input("Max capacity", value=s.get("max_capacity",1), min_value=1, key=f"c_{s['id']}")
                    with ec2:
                        new_active = st.checkbox("Active slot", value=s.get("active_slot", True), key=f"a_{s['id']}")
                    bc1, bc2 = st.columns(2)
                    with bc1:
                        if st.button("Save changes", key=f"save_{s['id']}"):
                            result, err = api_patch(f"/shifts/{s['id']}", {"instructor": new_instructor, "max_capacity": new_capacity, "active_slot": new_active})
                            if err:
                                st.error(err)
                            else:
                                st.success("Saved")
                                st.rerun()
                    with bc2:
                        if st.button("Delete shift", key=f"del_{s['id']}"):
                            result, err = api_delete(f"/shifts/{s['id']}")
                            if err:
                                st.error(err)
                            else:
                                st.success("Deleted")
                                st.rerun()

    with tab_create:
        st.markdown("### Create new shift")
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Class info</p>', unsafe_allow_html=True)
        fc1, fc2 = st.columns(2)
        with fc1:
            class_name = st.text_input("Class name *", placeholder="Yoga, Spinning, Pilates...")
            instructor = st.text_input("Instructor *", placeholder="Carlos García")
            day_of_week = st.selectbox("Day of week *", ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"])
        with fc2:
            start_time = st.time_input("Start time *")
            end_time = st.time_input("End time *")
            max_capacity = st.number_input("Max capacity *", min_value=1, value=10)
            active_slot = st.checkbox("Active slot", value=True)

        if st.button("Create shift"):
            if not class_name or not instructor:
                st.error("Class name and instructor are required.")
            elif start_time >= end_time:
                st.error("End time must be after start time.")
            else:
                payload = {
                    "class_name": class_name,
                    "instructor": instructor,
                    "day_of_week": day_of_week,
                    "start_time": str(start_time),
                    "end_time": str(end_time),
                    "max_capacity": int(max_capacity),
                    "active_slot": active_slot
                }
                result, err = api_post("/shifts/", payload)
                if err:
                    st.error(err)
                else:
                    st.success(f"Shift created — ID {result['id']}")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_avail:
        st.markdown("### Check availability for a shift")
        shifts_data, _ = api_get("/shifts/")
        if not shifts_data:
            st.warning("No shifts available.")
        else:
            shift_options = {f"{s['class_name']} · {s['day_of_week'].capitalize()} · {s['start_time']} (ID {s['id']})": s['id'] for s in shifts_data}
            selected = st.selectbox("Select shift", list(shift_options.keys()))
            check_date = st.date_input("Date to check", value=date.today())
            if st.button("Check availability"):
                avail, err = api_get(f"/shifts/{shift_options[selected]}/availability", params={"date": str(check_date)})
                if err:
                    st.error(err)
                else:
                    mc1, mc2, mc3 = st.columns(3)
                    mc1.metric("Max capacity", avail["max_capacity"])
                    mc2.metric("Active bookings", avail["active_bookings"])
                    mc3.metric("Available spots", avail["available_spots"])
                    if avail["is_available"]:
                        st.success("Class has available spots")
                    else:
                        st.error("Class is full")


elif module == "Reservations":
    st.markdown("# 📌 Reservations")
    tab_list, tab_create = st.tabs(["Search reservations", "Create reservation"])

    with tab_list:
        st.markdown("Search by member ID to see all their reservations.")
        member_id_filter = st.number_input("Member ID", min_value=1, value=1, step=1)
        if st.button("Search"):
            data, err = api_get(f"/reservations/member/{int(member_id_filter)}")
            if err:
                st.error(err)
            elif not data:
                st.info("No reservations found for this member.")
            else:
                st.markdown(f"**{len(data)} reservation(s)**")
                for r in data:
                    st.markdown(f"""
                    <div class="card">
                      <strong style="color:#6b4fbb">Reservation #{r.get('id')}</strong>
                      &nbsp;{status_pill(r.get('status',''))}<br>
                      <small style="color:#9b8ec4">
                        Shift ID: {r.get('shift_id')} &nbsp;|&nbsp;
                        Date: {r.get('date')} &nbsp;|&nbsp;
                        Member: {r.get('member_id')}
                        {f"&nbsp;|&nbsp; Queue position: {r.get('queue_position')}" if r.get('queue_position') else ""}
                      </small>
                    </div>
                    """, unsafe_allow_html=True)
                    if r.get("status") == "confirmed":
                        ac1, ac2 = st.columns(2)
                        with ac1:
                            if st.button("Cancel reservation", key=f"cancel_{r['id']}"):
                                result, err = api_patch(f"/reservations/{r['id']}/cancel")
                                if err:
                                    st.error(err)
                                else:
                                    st.success("Cancelled")
                                    st.rerun()
                        with ac2:
                            if st.button("Mark no-show", key=f"noshow_{r['id']}"):
                                result, err = api_patch(f"/reservations/{r['id']}/no-show")
                                if err:
                                    st.error(err)
                                else:
                                    st.success("Marked as no-show")
                                    st.rerun()

    with tab_create:
        st.markdown("### Book a shift for a member")
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        shifts_data, _ = api_get("/shifts/")
        if not shifts_data:
            st.warning("No shifts available. Create a shift first.")
        else:
            shift_options = {f"{s['class_name']} · {s['day_of_week'].capitalize()} · {s['start_time']} (ID {s['id']})": s['id'] for s in shifts_data}
            selected_shift = st.selectbox("Select shift *", list(shift_options.keys()))
            reservation_date = st.date_input("Date *", value=date.today())
            st.caption("Member ID is hardcoded to 1 until auth is implemented.")
            if st.button("Create reservation"):
                payload = {
                    "shift_id": shift_options[selected_shift],
                    "date": str(reservation_date)
                }
                result, err = api_post("/reservations/", payload)
                if err:
                    st.error(err)
                else:
                    st.success(f"Reservation created — ID {result['id']} · Status: {result['status']}")
        st.markdown('</div>', unsafe_allow_html=True)


elif module == "Members":
    st.markdown("# 👤 Members")
    tab_list, tab_create = st.tabs(["All members", "Register member"])

    with tab_list:
        data, err = api_get("/members/")
        if err:
            st.error(err)
        elif not data:
            st.info("No members registered yet.")
        else:
            st.markdown(f"**{len(data)} member(s)**")
            for m in data:
                initials = f"{m.get('first_name','?')[0]}{m.get('last_name','?')[0]}".upper()
                st.markdown(f"""
                <div class="card">
                  <div style="display:flex;align-items:center;gap:14px">
                    <div style="width:42px;height:42px;border-radius:50%;background:#e8e0f8;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:14px;color:#6b4fbb;flex-shrink:0">{initials}</div>
                    <div style="flex:1">
                      <strong style="color:#6b4fbb">{m.get('first_name','')} {m.get('last_name','')}</strong>
                      &nbsp;{status_pill("active" if m.get("is_active") else "inactive")}<br>
                      <small style="color:#9b8ec4">
                        📧 {m.get('email','')} &nbsp;|&nbsp;
                        📞 {m.get('phone') or '—'} &nbsp;|&nbsp;
                        Registered: {str(m.get('registration_date',''))[:10]}
                      </small>
                    </div>
                    <span style="font-size:11px;color:#b0a0d8">ID {m.get('id')}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    with tab_create:
        st.markdown("### Register new member")
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Personal info</p>', unsafe_allow_html=True)
        mc1, mc2 = st.columns(2)
        with mc1:
            first_name = st.text_input("First name *")
            last_name = st.text_input("Last name *")
            email = st.text_input("Email *", placeholder="member@example.com")
        with mc2:
            phone = st.text_input("Phone", placeholder="+34 600 000 000")
            birth_date = st.date_input("Birth date", value=None)

        if st.button("Register member"):
            if not first_name or not last_name or not email:
                st.error("First name, last name and email are required.")
            else:
                payload = {"first_name": first_name, "last_name": last_name, "email": email, "phone": phone or None}
                if birth_date:
                    payload["birth_date"] = str(birth_date)
                result, err = api_post("/members/", payload)
                if err:
                    st.error(err)
                else:
                    st.success(f"Member registered — ID {result['id']}")
        st.markdown('</div>', unsafe_allow_html=True)


elif module == "Memberships":
    st.markdown("# 💜 Memberships")
    tab_list, tab_create, tab_expiring = st.tabs(["All memberships", "Create membership", "Expiring soon"])

    with tab_list:
        fc1, fc2 = st.columns(2)
        with fc1:
            status_filter = st.selectbox("Status", ["All", "pending", "active", "expired", "cancelled"])
        with fc2:
            member_filter = st.number_input("Member ID (optional)", min_value=0, value=0, step=1)

        params = {}
        if status_filter != "All":
            params["status"] = status_filter
        if member_filter > 0:
            params["member_id"] = int(member_filter)

        data, err = api_get("/memberships/", params=params)
        if err:
            st.error(err)
        elif not data:
            st.info("No memberships found.")
        else:
            st.markdown(f"**{len(data)} membership(s)**")
            for m in data:
                st.markdown(f"""
                <div class="card">
                  <strong style="color:#6b4fbb">Membership #{m.get('id')}</strong>
                  &nbsp;{status_pill(m.get('status',''))}<br>
                  <small style="color:#9b8ec4">
                    Member ID: {m.get('member_id')} &nbsp;|&nbsp;
                    Plan ID: {m.get('plan_id')} &nbsp;|&nbsp;
                    {m.get('start_date','')} → {m.get('end_date','')}
                  </small>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Renew", key=f"renew_{m['id']}"):
                    result, err = api_post(f"/memberships/{m['id']}/renew", {})
                    if err:
                        st.error(err)
                    else:
                        st.success("Renewed")
                        st.rerun()

    with tab_create:
        st.markdown("### Assign a plan to a member")
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        plans_data, _ = api_get("/plans/")
        if not plans_data:
            st.warning("No plans available. Create a plan first.")
        else:
            plan_options = {f"{p.get('name')} · €{p.get('price')} · ID {p['id']}": p['id'] for p in plans_data}
            selected_plan = st.selectbox("Select plan *", list(plan_options.keys()))
            member_id = st.number_input("Member ID *", min_value=1, step=1)
            start_date = st.date_input("Start date *", value=date.today())

            if st.button("Create membership"):
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
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_expiring:
        st.markdown("### Memberships expiring soon")
        days = st.slider("Days ahead", 1, 60, 7)
        expiring, err2 = api_get("/memberships/expiring-soon", params={"days": days})
        if err2:
            st.error(err2)
        elif not expiring:
            st.success(f"No memberships expiring in the next {days} days.")
        else:
            st.warning(f"{len(expiring)} membership(s) expiring within {days} days")
            for m in expiring:
                st.markdown(f"""
                <div class="card" style="border-left:3px solid #f5b8cf">
                  <strong style="color:#c0436a">Membership #{m.get('id')}</strong><br>
                  <small style="color:#9b8ec4">
                    Member ID: {m.get('member_id')} &nbsp;|&nbsp;
                    Plan ID: {m.get('plan_id')} &nbsp;|&nbsp;
                    Expires: {m.get('end_date')}
                  </small>
                </div>
                """, unsafe_allow_html=True)


elif module == "Plans":
    st.markdown("# 📋 Plans")
    tab_list, tab_create = st.tabs(["All plans", "Create plan"])

    with tab_list:
        data, err = api_get("/plans/")
        if err:
            st.error(err)
        elif not data:
            st.info("No plans created yet.")
        else:
            cols = st.columns(min(len(data), 3))
            for i, p in enumerate(data):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="card" style="text-align:center;padding:24px 20px">
                      <p style="font-size:28px;font-weight:800;color:#6b4fbb;margin:0">€{p.get('price','')}</p>
                      <p style="font-size:16px;font-weight:800;color:#3b2f5e;margin:6px 0">{p.get('name','')}</p>
                      <p style="font-size:12px;color:#9b8ec4;margin:0">{p.get('description') or '—'}</p>
                      <p style="font-size:11px;color:#cdc0ef;margin:10px 0 0">ID {p.get('id')}</p>
                    </div>
                    """, unsafe_allow_html=True)

    with tab_create:
        st.markdown("### Create new plan")
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        pc1, pc2 = st.columns(2)
        with pc1:
            plan_name = st.text_input("Plan name *", placeholder="Monthly, Annual, Trial...")
            plan_price = st.number_input("Price (€) *", min_value=0.0, step=0.50, value=0.0)
        with pc2:
            plan_description = st.text_input("Description", placeholder="Optional short description")

        if st.button("Create plan"):
            if not plan_name:
                st.error("Plan name is required.")
            else:
                payload = {"name": plan_name, "price": plan_price, "description": plan_description or None}
                result, err = api_post("/plans/", payload)
                if err:
                    st.error(err)
                else:
                    st.success(f"Plan created — ID {result['id']}")
        st.markdown('</div>', unsafe_allow_html=True)


elif module == "Payments":
    st.markdown("# 💳 Payments")
    tab_list, tab_create = st.tabs(["All payments", "Register payment"])

    with tab_list:
        data, err = api_get("/payments/")
        if err:
            st.error(err)
        elif not data:
            st.info("No payments registered yet.")
        else:
            st.markdown(f"**{len(data)} payment(s)**")
            for p in data:
                st.markdown(f"""
                <div class="card">
                  <div style="display:flex;justify-content:space-between;align-items:center">
                    <div>
                      <strong style="color:#6b4fbb">Payment #{p.get('id')}</strong>
                      &nbsp;{status_pill(p.get('status',''))}<br>
                      <small style="color:#9b8ec4">
                        Amount: €{p.get('amount','')} &nbsp;|&nbsp;
                        Method: {p.get('payment_method','')} &nbsp;|&nbsp;
                        Membership: {p.get('membership_id')} &nbsp;|&nbsp;
                        Date: {str(p.get('payment_date',''))[:10]}
                        {f"&nbsp;|&nbsp; Ref: {p.get('reference')}" if p.get('reference') else ""}
                      </small>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("Export all payments as CSV"):
            import io, csv
            csv_data, err = api_get("/payments/export-csv")
            if err:
                st.error(err)
            else:
                st.download_button("Download CSV", data=str(csv_data), file_name="payments.csv", mime="text/csv")

    with tab_create:
        st.markdown("### Register a payment")
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Payment details</p>', unsafe_allow_html=True)
        pyc1, pyc2 = st.columns(2)
        with pyc1:
            membership_id = st.number_input("Membership ID *", min_value=1, step=1)
            amount = st.number_input("Amount (€) *", min_value=0.0, step=0.01)
        with pyc2:
            method = st.selectbox("Payment method *", ["cash", "card", "transfer", "bizum", "direct_debit", "other"])
            reference = st.text_input("Reference", placeholder="Optional transaction ref")
            notes = st.text_input("Notes", placeholder="Optional")

        if st.button("Register payment"):
            if amount <= 0:
                st.error("Amount must be greater than 0.")
            else:
                payload = {
                    "membership_id": int(membership_id),
                    "amount": amount,
                    "payment_method": method,
                    "reference": reference or "",
                    "notes": notes or ""
                }
                result, err = api_post("/payments/", payload)
                if err:
                    st.error(err)
                else:
                    st.success(f"Payment registered — ID {result['id']}")
        st.markdown('</div>', unsafe_allow_html=True)


elif module == "Attendance":
    st.markdown("# ✅ Attendance")
    tab_list, tab_create = st.tabs(["All records", "Register check-in"])

    with tab_list:
        data, err = api_get("/attendances/")
        if err:
            st.error(err)
        elif not data:
            st.info("No attendance records yet.")
        else:
            st.markdown(f"**{len(data)} record(s)**")
            for a in data:
                check_in = str(a.get('check_in', '—'))[:16]
                check_out = str(a.get('check_out', '—'))[:16] if a.get('check_out') else '—'
                st.markdown(f"""
                <div class="card">
                  <strong style="color:#6b4fbb">Attendance #{a.get('id')}</strong><br>
                  <small style="color:#9b8ec4">
                    Member ID: {a.get('member_id')} &nbsp;|&nbsp;
                    Reservation ID: {a.get('reservation_id')} &nbsp;|&nbsp;
                    Check-in: {check_in} &nbsp;|&nbsp;
                    Check-out: {check_out}
                  </small>
                </div>
                """, unsafe_allow_html=True)

    with tab_create:
        st.markdown("### Register member check-in")
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("Registers attendance for an existing confirmed reservation.")
        ac1, ac2 = st.columns(2)
        with ac1:
            reservation_id = st.number_input("Reservation ID *", min_value=1, step=1)
        with ac2:
            member_id_att = st.number_input("Member ID *", min_value=1, step=1)

        if st.button("Register check-in"):
            payload = {
                "reservation_id": int(reservation_id),
                "member_id": int(member_id_att)
            }
            result, err = api_post("/attendances/", payload)
            if err:
                st.error(err)
            else:
                st.success(f"Attendance registered — ID {result['id']}")
        st.markdown('</div>', unsafe_allow_html=True)