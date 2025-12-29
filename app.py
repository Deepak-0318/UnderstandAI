import streamlit as st
from core.pipeline import run_pipeline

st.set_page_config(page_title="Understand AI", layout="wide")

st.title("🧠 Understand AI – Medical Consent Understanding Engine")
st.caption("Upload a medical consent PDF to detect confusion and verify understanding.")

uploaded_file = st.file_uploader(
    "Upload medical consent document (PDF)",
    type=["pdf"]
)

if uploaded_file:
    with st.spinner("Analyzing document..."):
        sentences, clarity = run_pipeline(uploaded_file)

    st.success("Analysis complete")

    # 🔢 Clarity Score
    st.subheader("📊 Clarity Score")
    st.metric(
        label="Final Clarity Score",
        value=clarity["clarity_score"]
    )

    st.divider()

    # 📄 Sentence-wise output
    st.subheader("📄 Sentence-wise Analysis")

    for s in sentences:
        if s.confusion_label == "HIGH":
            st.error(f"{s.sentence_id}: {s.text}")
        elif s.confusion_label == "MEDIUM":
            st.warning(f"{s.sentence_id}: {s.text}")
        else:
            st.success(f"{s.sentence_id}: {s.text}")

        if s.explanation:
            with st.expander("See explanation"):
                st.write(s.explanation)
