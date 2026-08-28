import streamlit as st
import pandas as pd
from database import get_all_queue
from io import BytesIO

def reports_page():
    st.markdown('<div class="main-title">Reports</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Export queue activity for project demonstrations and administration.</div>', unsafe_allow_html=True)

    rows = get_all_queue()
    if not rows:
        st.info("No queue records available.")
        return

    df = pd.DataFrame([dict(r) for r in rows])
    st.dataframe(df, use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV Report",
        data=csv,
        file_name="smart_queue_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    try:
        import openpyxl
        output = BytesIO()
        df.to_excel(output, index=False, engine="openpyxl")
        st.download_button(
            "Download Excel Report",
            data=output.getvalue(),
            file_name="smart_queue_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    except Exception:
        st.caption("Install openpyxl to enable Excel export.")
