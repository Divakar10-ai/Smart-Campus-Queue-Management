import streamlit as st
from database import (
    SERVICES, create_student, student_login, generate_token,
    get_student_active, cancel_queue, add_feedback
)
from config import DEPARTMENTS, YEARS

def student_page():
    st.markdown('<div class="main-title">Student Queue Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Join a campus service queue and track your position in real time.</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Get Token", "My Queue", "Account"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        name = st.text_input("Student name")
        roll = st.text_input("Roll number")
        department = st.selectbox("Department", DEPARTMENTS)
        service = st.selectbox("Select service", SERVICES)
        if st.button("Generate Queue Token", use_container_width=True, type="primary"):
            if not name.strip() or not roll.strip():
                st.error("Enter your name and roll number.")
            else:
                active = get_student_active(roll.strip())
                if active:
                    st.warning(f"You already have active token #{active['token']} for {active['service']}.")
                else:
                    token, wait, queue_id = generate_token(
                        service, name.strip(), roll.strip(), department
                    )
                    st.session_state["last_queue_id"] = queue_id
                    st.session_state["last_roll"] = roll.strip()
                    st.session_state["last_token"] = token
                    st.session_state["last_service"] = service
                    st.success("Token generated successfully.")
                    st.markdown(f'<div class="token">TOKEN #{token}</div>', unsafe_allow_html=True)
                    st.info(f"Estimated waiting time: about {wait} minutes.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        roll = st.text_input("Enter roll number to track", key="track_roll")
        if st.button("Check Queue", use_container_width=True):
            row = get_student_active(roll.strip())
            if not row:
                st.info("No active queue entry found.")
            else:
                st.markdown(f'<div class="token">#{row["token"]}</div>', unsafe_allow_html=True)
                waiting = 0
                # Approximate position is based on earlier active queue records.
                from database import connect
                conn = connect()
                waiting = conn.execute("""
                    SELECT COUNT(*) AS c FROM queue
                    WHERE service=? AND status='Waiting' AND id<=?
                """, (row["service"], row["id"])).fetchone()["c"]
                conn.close()
                st.metric("People before/including you", waiting)
                st.write(f"**Service:** {row['service']}")
                st.write(f"**Status:** {row['status']}")
                st.write(f"**Estimated wait:** {row['estimated_minutes']} minutes")
                if row["status"] == "Waiting":
                    if st.button("Cancel Token", key=f"cancel_{row['id']}"):
                        cancel_queue(row["id"])
                        st.success("Token cancelled.")
                        st.rerun()

    with tab3:
        create, login = st.columns(2)
        with create:
            st.subheader("Create student account")
            n = st.text_input("Name", key="reg_name")
            r = st.text_input("Roll number", key="reg_roll")
            d = st.selectbox("Department", DEPARTMENTS, key="reg_dept")
            y = st.selectbox("Year", YEARS)
            p = st.text_input("Password", type="password", key="reg_pass")
            if st.button("Create Account"):
                if not all([n.strip(), r.strip(), p]):
                    st.error("Fill all required fields.")
                else:
                    ok, msg = create_student(n.strip(), r.strip(), d, y, p)
                    (st.success if ok else st.error)(msg)

        with login:
            st.subheader("Student login")
            r2 = st.text_input("Roll number", key="login_roll")
            p2 = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login"):
                row = student_login(r2.strip(), p2)
                if row:
                    st.session_state["student"] = dict(row)
                    st.success(f"Welcome, {row['name']}.")
                else:
                    st.error("Invalid roll number or password.")

    if st.session_state.get("last_queue_id"):
        st.divider()
        st.subheader("Service feedback")
        rating = st.slider("Rate your queue experience", 1, 5, 5)
        comment = st.text_area("Optional comment")
        if st.button("Submit Feedback"):
            add_feedback(st.session_state["last_queue_id"], rating, comment)
            st.success("Thank you for your feedback.")
