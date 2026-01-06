import streamlit as st
import time
from core.pipeline import run_pipeline

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Understand AI",
    layout="wide"
)

st.title("🧠 Understand AI – Medical Consent Understanding Engine")
st.caption(
    "Upload a medical consent PDF. The analysis runs automatically — no buttons, no setup."
)

# -------------------------------
# Session State (prevents reruns)
# -------------------------------
if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None
    st.session_state.results = None

# -------------------------------
# File Upload (single obvious action)
# -------------------------------
uploaded_file = st.file_uploader(
    "📄 Upload medical consent document (PDF)",
    type=["pdf"],
    help="Upload once. Results appear automatically."
)

# -------------------------------
# Helper: Clarity Score Hero Card
# -------------------------------
# -------------------------------
# Helper: Clarity Score (FIXED – NO HTML)
# -------------------------------
def render_clarity_score(clarity):
    final_score = clarity.get("clarity_score", 0.0)
    before_score = clarity.get("initial_score")

    st.subheader("📊 Clarity Score")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.metric(
            label="Final Clarity Score",
            value=final_score,
            delta=(final_score - before_score) if before_score is not None else None
        )

    with col2:
        # Progress bar is safe and intuitive
        st.progress(min(final_score / 100.0, 1.0))

    if before_score is not None:
        st.caption(f"Before: {before_score} → After: {final_score}")

# -------------------------------
# Helper: Confusion Distribution Chart
# -------------------------------
def render_confusion_distribution(sentences):
    counts = {
        "High Confusion 🟥": 0,
        "Medium Confusion 🟨": 0,
        "Clear 🟩": 0
    }

    for s in sentences:
        if s.confusion_label == "HIGH":
            counts["High Confusion 🟥"] += 1
        elif s.confusion_label == "MEDIUM":
            counts["Medium Confusion 🟨"] += 1
        else:
            counts["Clear 🟩"] += 1

    st.subheader("📊 Confusion Distribution")
    st.caption("How confusing the document is at a glance.")
    st.bar_chart(counts)

# -------------------------------
# Helper: Before vs After Comparison
# -------------------------------
def render_before_after(sentences):
    st.subheader("🔁 Before vs After Understanding")
    st.caption("Original medical language compared with clarified explanations.")

    for s in sentences:
        if not s.explanation or not s.explanation.strip():
            continue

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown(
                f"""
                <div style="
                    background-color:#0f172a;
                    padding:16px;
                    border-radius:10px;
                    border-left:6px solid #ef4444;
                    color:#e5e7eb;
                    font-size:15px;
                    line-height:1.6;
                ">
                    <div style="font-size:13px;color:#94a3b8;margin-bottom:6px;">
                        BEFORE · S{s.sentence_id}
                    </div>
                    {s.text}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div style="
                    background-color:#020617;
                    padding:16px;
                    border-radius:10px;
                    border-left:6px solid #22c55e;
                    color:#d1fae5;
                    font-size:15px;
                    line-height:1.6;
                ">
                    <div style="font-size:13px;color:#86efac;margin-bottom:6px;">
                        AFTER · S{s.sentence_id}
                    </div>
                    {s.explanation}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br/>", unsafe_allow_html=True)

# -------------------------------
# Helper: Sentence Heatmap + Expandable Panel
# -------------------------------
def render_sentence(sentence_id, text, label, explanation):
    style_map = {
        "HIGH": {"bg": "#ffebee", "border": "#e53935"},
        "MEDIUM": {"bg": "#fff8e1", "border": "#f9a825"},
        "LOW": {"bg": "#e8f5e9", "border": "#43a047"},
    }

    styles = style_map.get(label, style_map["LOW"])

    st.markdown(
        f"""
        <div style="
            background-color:{styles['bg']};
            border-left:6px solid {styles['border']};
            padding:14px 16px;
            border-radius:8px;
            margin-bottom:6px;
            font-size:15px;
            line-height:1.65;
            color:#111;
        ">
            <strong>SS{sentence_id}.</strong> {text}
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("🔍 Explain / Why confusing?"):
        if explanation and explanation.strip():
            st.markdown(
                f"<div style='font-size:14px;line-height:1.6;color:#222;'>{explanation}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div style='font-size:14px;font-style:italic;color:#666;'>Explanation not available yet.</div>",
                unsafe_allow_html=True
            )

# -------------------------------
# One-Click Auto-Run Pipeline
# -------------------------------
if uploaded_file:
    if st.session_state.last_uploaded_file != uploaded_file.name:
        st.session_state.last_uploaded_file = uploaded_file.name

        with st.status("Analyzing document…", expanded=True) as status:
            time.sleep(0.6)
            status.update(label="Detecting confusion…")

            time.sleep(0.6)
            status.update(label="Verifying understanding…")

            sentences, clarity = run_pipeline(uploaded_file)

            status.update(label="Analysis complete", state="complete")

        st.session_state.results = (sentences, clarity)

# -------------------------------
# Render Results (single flow)
# -------------------------------
if st.session_state.results:
    sentences, clarity = st.session_state.results

    render_clarity_score(clarity)

    st.divider()
    render_confusion_distribution(sentences)

    st.divider()
    render_before_after(sentences)

    st.divider()
    st.subheader("📄 Sentence-wise Analysis")

    for s in sentences:
        render_sentence(
            sentence_id=s.sentence_id,
            text=s.text,
            label=s.confusion_label,
            explanation=s.explanation
        )
