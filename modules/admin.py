import streamlit as st
from database import (
    admin_login, SERVICES, get_waiting, current_token,
    serve_next, complete_current, get_all_queue
)

def admin_page():
    st.markdown('<div class="main-title">Admin Queue Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Control service counters, call tokens and monitor the live queue.</div>', unsafe_allow_html=True)

    if not st.session_state.get("admin_logged"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Sign in", type="primary", use_container_width=True):
            if admin_login(username.strip(), password):
                st.session_state["admin_logged"] = True
                st.rerun()
            else:
                st.error("Invalid credentials.")
        st.caption("Demo login: admin / admin123")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    service = st.selectbox("Counter / Service", SERVICES)
    current = current_token(service)
    waiting = get_waiting(service)

    a, b, c = st.columns(3)
    with a:
        st.metric("Currently Serving", f"#{current['token']}" if current else "None")
    with b:
        st.metric("Waiting", len(waiting))
    with c:
        st.metric("Estimated Queue Time", f"{len(waiting)*4} min")

    x, y = st.columns(2)
    with x:
        if st.button("Call Next Student", type="primary", use_container_width=True):
            token = serve_next(service)
            if token:
                st.success(f"Now serving token #{token}.")
                st.rerun()
            else:
                st.info("No students are waiting.")
    with y:
        if st.button("Complete Current", use_container_width=True):
            if complete_current(service):
                st.success("Current token completed.")
                st.rerun()
            else:
                st.info("No active token.")

    st.subheader("Waiting Queue")
    if waiting:
        data = [{
            "Token": f"#{r['token']}",
            "Student": r["student_name"],
            "Roll No": r["roll_no"],
            "Department": r["department"],
            "Joined": r["joined_at"].replace("T", " ")
        } for r in waiting]
        st.dataframe(data, use_container_width=True, hide_index=True)
    else:
        st.info("Queue is empty.")

    st.subheader("Recent Queue Activity")
    rows = get_all_queue()[:20]
    data = [{
        "Token": f"#{r['token']}",
        "Service": r["service"],
        "Student": r["student_name"],
        "Status": r["status"],
        "Joined": r["joined_at"].replace("T", " ")
    } for r in rows]
    st.dataframe(data, use_container_width=True, hide_index=True)
