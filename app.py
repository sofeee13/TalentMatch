import streamlit as st
import pandas as pd

from resume_parser import parse_resume
from job_analyzer import analyze_job
from matching_engine import rank_candidates
from ai_helpers import generate_interview_questions, draft_shortlist_email


# ============================================================
# TALENTMATCH — NEW VISUAL DIRECTION
# Theme: clean editorial workspace / ink + teal + warm ivory
# Navigation: top bar (no sidebar)
# ============================================================

st.set_page_config(
    page_title="TalentMatch | Hiring Workspace",
    page_icon="✳️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Keep the native sidebar out of this design. All navigation is in the top bar.
st.markdown(
    """
    <style>
    :root {
        --ink: #172B3A;
        --ink-2: #274454;
        --muted: #6D7D87;
        --line: #DFE7E8;
        --paper: #F5F8F7;
        --white: #FFFFFF;
        --teal: #087E78;
        --teal-dark: #06645F;
        --teal-soft: #E2F3F0;
        --lime: #D8F36A;
        --orange: #F1A66A;
        --red-soft: #FCEBE7;
        --shadow: 0 12px 34px rgba(23, 43, 58, .055);
    }

    html, body, [class*="css"] {
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .stApp {
        background: var(--paper);
        color: var(--ink);
    }
    [data-testid="stSidebar"] { display: none; }
    [data-testid="collapsedControl"] { display: none; }
    header[data-testid="stHeader"] {
        background: rgba(245, 248, 247, .92);
    }
    .block-container {
        max-width: 1450px;
        padding: 1.25rem 2.5rem 3rem;
    }
    .tm-topline {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding: 12px 0 18px;
        border-bottom: 1px solid var(--line);
        margin-bottom: 1.2rem;
    }
    .tm-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        color: var(--ink);
        font-size: 1.22rem;
        font-weight: 900;
        letter-spacing: -.8px;
    }
    .tm-logo-mark {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        background: var(--ink);
        color: var(--lime);
        border-radius: 11px;
        font-size: 1.15rem;
    }
    .tm-logo small {
        display: block;
        color: var(--muted);
        font-size: .62rem;
        font-weight: 750;
        letter-spacing: 1.8px;
        margin-top: 1px;
    }
    .tm-status {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        color: var(--teal-dark);
        background: var(--teal-soft);
        border: 1px solid #C8E8E2;
        border-radius: 999px;
        padding: 7px 12px;
        font-size: .72rem;
        font-weight: 800;
        white-space: nowrap;
    }
    .tm-dot {
        width: 7px;
        height: 7px;
        background: #159B82;
        border-radius: 50%;
        display: inline-block;
    }
    .tm-kicker {
        color: var(--teal);
        font-size: .7rem;
        text-transform: uppercase;
        font-weight: 850;
        letter-spacing: 1.8px;
        margin: .25rem 0 .45rem;
    }
    .tm-title {
        color: var(--ink);
        font-size: 2.2rem;
        line-height: 1.08;
        font-weight: 900;
        letter-spacing: -1.5px;
        margin: 0;
    }
    .tm-subtitle {
        color: var(--muted);
        font-size: .94rem;
        margin: .55rem 0 1.4rem;
    }
    .tm-hero {
        background: var(--ink);
        color: white;
        border-radius: 22px;
        padding: 27px 30px;
        position: relative;
        overflow: hidden;
        margin: .5rem 0 1.4rem;
        box-shadow: var(--shadow);
    }
    .tm-hero:after {
        content: "";
        position: absolute;
        width: 230px;
        height: 230px;
        right: 5%;
        top: -120px;
        border: 1px solid rgba(216,243,106,.35);
        border-radius: 50%;
        box-shadow: 0 0 0 28px rgba(216,243,106,.04), 0 0 0 58px rgba(216,243,106,.035);
    }
    .tm-hero h2 {
        color: white;
        font-size: 1.55rem;
        letter-spacing: -.7px;
        font-weight: 850;
        margin: 0 0 .45rem;
        position: relative;
        z-index: 1;
    }
    .tm-hero p {
        color: #C7D5D9;
        margin: 0;
        font-size: .9rem;
        max-width: 720px;
        position: relative;
        z-index: 1;
    }
    .tm-hero-tag {
        display: inline-block;
        color: var(--ink);
        background: var(--lime);
        border-radius: 6px;
        font-size: .65rem;
        font-weight: 900;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 5px 8px;
        margin-bottom: 12px;
        position: relative;
        z-index: 1;
    }
    .tm-section-head {
        display: flex;
        justify-content: space-between;
        align-items: end;
        gap: 1rem;
        margin: 1.45rem 0 .8rem;
    }
    .tm-section-head h3 {
        color: var(--ink);
        font-size: 1.15rem;
        font-weight: 850;
        margin: 0;
        letter-spacing: -.35px;
    }
    .tm-section-head p {
        color: var(--muted);
        font-size: .8rem;
        margin: .22rem 0 0;
    }
    .tm-card {
        background: var(--white);
        border: 1px solid var(--line);
        border-radius: 17px;
        padding: 19px 20px;
        box-shadow: 0 5px 20px rgba(23,43,58,.035);
        margin-bottom: 13px;
    }
    .tm-card-label {
        color: var(--muted);
        font-size: .76rem;
        font-weight: 700;
    }
    .tm-card-value {
        color: var(--ink);
        font-size: 1.8rem;
        line-height: 1.2;
        font-weight: 900;
        margin-top: 8px;
        letter-spacing: -.8px;
    }
    .tm-card-icon {
        color: var(--teal);
        font-size: 1.2rem;
        margin-bottom: 9px;
    }
    .tm-small-label {
        color: var(--teal);
        font-size: .68rem;
        text-transform: uppercase;
        font-weight: 850;
        letter-spacing: 1.3px;
    }
    .tm-step {
        display: inline-flex;
        width: 29px;
        height: 29px;
        align-items: center;
        justify-content: center;
        border-radius: 9px;
        color: var(--teal-dark);
        background: var(--teal-soft);
        font-size: .76rem;
        font-weight: 900;
        margin-right: 8px;
    }
    .tm-callout {
        border-left: 4px solid var(--teal);
        background: #EAF5F2;
        color: #315C5B;
        padding: 12px 15px;
        border-radius: 0 10px 10px 0;
        font-size: .82rem;
        line-height: 1.55;
        margin: .6rem 0;
    }
    .tm-footer {
        border-top: 1px solid var(--line);
        padding-top: 16px;
        margin-top: 2rem;
        color: var(--muted);
        font-size: .75rem;
    }

    /* Streamlit controls */
    div[data-testid="stRadio"] > div {
        gap: 7px;
        flex-wrap: wrap;
    }
    /* Navigation pills: force readable contrast on every Streamlit child node. */
    div[data-testid="stRadio"] label {
        background: #FFFFFF !important;
        border: 1px solid #D5E0E2 !important;
        border-radius: 999px !important;
        padding: 8px 14px !important;
        margin: 0 !important;
        color: #274454 !important;
        font-size: .82rem !important;
        font-weight: 750 !important;
        opacity: 1 !important;
        accent-color: var(--teal);
        transition: background .15s ease, border-color .15s ease, transform .15s ease;
    }
    div[data-testid="stRadio"] label p,
    div[data-testid="stRadio"] label span,
    div[data-testid="stRadio"] label div {
        color: #274454 !important;
        opacity: 1 !important;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background: var(--ink) !important;
        border-color: var(--ink) !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stRadio"] label:has(input:checked) p,
    div[data-testid="stRadio"] label:has(input:checked) span,
    div[data-testid="stRadio"] label:has(input:checked) div {
        color: #FFFFFF !important;
    }
    div[data-testid="stRadio"] input {
        accent-color: var(--lime);
    }

    /* Form labels were too pale in some Streamlit themes. */
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p,
    .stTextArea label,
    .stTextInput label,
    .stSelectbox label,
    .stFileUploader label {
        color: var(--ink) !important;
        opacity: 1 !important;
        font-weight: 750 !important;
    }
    .stButton > button {
        min-height: 43px;
        border-radius: 10px;
        border: 1px solid var(--line);
        font-weight: 800;
        color: var(--ink);
        background: white;
        transition: all .15s ease;
    }
    .stButton > button[kind="primary"] {
        background: var(--teal);
        color: white;
        border-color: var(--teal);
    }
    .stButton > button[kind="primary"]:hover {
        background: var(--teal-dark);
        border-color: var(--teal-dark);
        color: white;
    }
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background: #FFFFFF !important;
        color: var(--ink) !important;
        border: 1px solid #C9D5D7 !important;
        border-radius: 10px !important;
        opacity: 1 !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: var(--teal) !important;
        box-shadow: 0 0 0 2px rgba(8,126,120,.12) !important;
    }
    .stTextArea textarea::placeholder, .stTextInput input::placeholder {
        color: #7A8991 !important;
        opacity: 1 !important;
    }
    [data-testid="stFileUploader"] {
        background: #FFFFFF;
        border: 1.5px dashed #83B9B1;
        border-radius: 15px;
        padding: 13px;
    }
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] span {
        color: #405761 !important;
        opacity: 1 !important;
    }
    [data-testid="stFileUploader"] button {
        background: #FFFFFF !important;
        color: var(--ink) !important;
        border: 1px solid #C9D5D7 !important;
        border-radius: 8px !important;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: 12px;
        overflow: hidden;
    }
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid var(--line);
        border-radius: 13px;
        padding: 14px 16px;
    }
    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] label p {
        color: #5F737E !important;
        opacity: 1 !important;
        font-weight: 750 !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"],
    div[data-testid="stMetric"] [data-testid="stMetricValue"] div {
        color: #172B3A !important;
        opacity: 1 !important;
        font-size: 1.85rem !important;
        font-weight: 900 !important;
    }
    h1, h2, h3, h4, p, label, span {
        text-wrap: pretty;
    }
    div[data-testid="stProgressBar"] > div > div {
        background: var(--teal) !important;
    }
    [data-testid="stAlert"] {
        border-radius: 12px;
    }
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] div,
    [data-testid="stAlert"] span {
        color: #263D49 !important;
        opacity: 1 !important;
    }
    hr { border-color: var(--line); }
    #MainMenu, footer { visibility: hidden; }

    @media (max-width: 850px) {
        .block-container { padding: .9rem 1rem 2rem; }
        .tm-title { font-size: 1.75rem; }
        .tm-topline { align-items: flex-start; }
        .tm-status { font-size: .65rem; }
        div[data-testid="stRadio"] label { padding: 6px 10px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    "candidates": [],
    "job_text": "",
    "job_profile": None,
    "ranked": [],
    "questions": [],
    "email_draft": "",
    "email_editor": "",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HELPERS
# ============================================================
def section(title, subtitle=None):
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f'<div class="tm-section-head"><div><h3>{title}</h3>{subtitle_html}</div></div>',
        unsafe_allow_html=True,
    )


def stat_card(icon, label, value, footnote=None):
    # Native metric values render more consistently than text inside custom HTML cards.
    st.metric(label=f"{icon}  {label}", value=value, help=footnote)


def as_list(value):
    return value if isinstance(value, list) else []


def candidate_table(candidates):
    return pd.DataFrame(
        [
            {
                "Candidate": c.get("candidate_id", "Unknown"),
                "Skills": ", ".join(as_list(c.get("skills", []))) or "—",
                "Experience": c.get("experience_years", 0),
                "Education": c.get("education", "Not detected") or "Not detected",
            }
            for c in candidates
        ]
    )


def ranked_table(ranked):
    return pd.DataFrame(
        [
            {
                "Rank": x.get("rank", "—"),
                "Candidate": x.get("candidate_id", "Unknown"),
                "Match": f'{x.get("score", 0)}%',
                "Experience": f'{x.get("experience_years", 0)} yrs',
                "Skills matched": len(as_list(x.get("matched_skills", []))),
                "Gaps": len(as_list(x.get("missing_skills", []))),
            }
            for x in ranked
        ]
    )


# ============================================================
# TOP BRAND + TOP NAVIGATION
# ============================================================
st.markdown(
    """
    <div class="tm-topline">
        <div class="tm-logo">
            <span class="tm-logo-mark">✳</span>
            <span>TalentMatch<small>HIRING INTELLIGENCE</small></span>
        </div>
        <div class="tm-status"><span class="tm-dot"></span> WORKSPACE READY</div>
    </div>
    """,
    unsafe_allow_html=True,
)

pages = [
    "Overview",
    "Smart Screening",
    "Candidates",
    "Interview Studio",
    "Shortlist Email",
    "Fairness Review",
]

def go_to_candidates():
    # Streamlit runs button callbacks before rerunning the script,
    # so updating the radio widget state here is safe.
    st.session_state["main_navigation"] = "Candidates"

page = st.radio(
    "Main navigation",
    pages,
    horizontal=True,
    label_visibility="collapsed",
    key="main_navigation",
)

st.markdown('<div class="tm-kicker">Recruitment workspace / 2026</div>', unsafe_allow_html=True)
st.markdown('<h1 class="tm-title">Find the right talent.<br>With better evidence.</h1>', unsafe_allow_html=True)
st.markdown(
    '<div class="tm-subtitle">A focused workspace to understand resumes, compare job-related skills and support thoughtful hiring.</div>',
    unsafe_allow_html=True,
)


# ============================================================
# OVERVIEW
# ============================================================
if page == "Overview":
    st.markdown(
        """
        <div class="tm-hero">
            <span class="tm-hero-tag">Recruitment intelligence</span>
            <h2>Good hiring starts with a clearer picture.</h2>
            <p>Bring job requirements and candidate experience into one workspace. Review extracted information, compare job-related evidence and keep the final decision in human hands.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section("Your screening at a glance", "Current activity across this workspace.")
    a, b, c, d = st.columns(4)
    with a:
        stat_card("▤", "Resumes processed", len(st.session_state.candidates), "Candidate documents")
    with b:
        stat_card("⌕", "Job profile", "Ready" if st.session_state.job_text else "Not set", "Role requirements")
    with c:
        stat_card("◎", "Candidates ranked", len(st.session_state.ranked), "Latest matching run")
    with d:
        avg = (
            f'{sum(float(x.get("score", 0)) for x in st.session_state.ranked) / len(st.session_state.ranked):.1f}%'
            if st.session_state.ranked else "—"
        )
        stat_card("↗", "Average match", avg, "Assistive score only")

    left, right = st.columns([1.25, 1])
    with left:
        section("Match score overview", "Scores from the latest candidate ranking.")
        if st.session_state.ranked:
            df = pd.DataFrame(
                {
                    "Candidate": [x.get("candidate_id", "Unknown") for x in st.session_state.ranked],
                    "Match score": [float(x.get("score", 0)) for x in st.session_state.ranked],
                }
            ).set_index("Candidate")
            st.bar_chart(df, color="#087E78")
        else:
            st.markdown(
                '<div class="tm-card"><div class="tm-card-label">No screening results yet</div><p style="color:#6D7D87;margin:.5rem 0 0">Start a screening run to see candidate match scores here.</p></div>',
                unsafe_allow_html=True,
            )
    with right:
        section("A simple workflow", "Three steps from role brief to recruiter review.")
        st.markdown(
            """
            <div class="tm-card">
                <p><span class="tm-step">01</span><b>Set the role</b><br><span style="color:#6D7D87;font-size:.82rem">Describe responsibilities and must-have skills.</span></p>
                <p><span class="tm-step">02</span><b>Read resumes</b><br><span style="color:#6D7D87;font-size:.82rem">Extract experience, education and skills.</span></p>
                <p><span class="tm-step">03</span><b>Review evidence</b><br><span style="color:#6D7D87;font-size:.82rem">Compare relevant information and verify it.</span></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.session_state.ranked:
        section("Latest candidate ranking")
        st.dataframe(ranked_table(st.session_state.ranked), use_container_width=True, hide_index=True)


# ============================================================
# SMART SCREENING
# ============================================================
elif page == "Smart Screening":
    st.markdown(
        """
        <div class="tm-hero">
            <span class="tm-hero-tag">01 / Smart screening</span>
            <h2>Build a job-relevant candidate shortlist.</h2>
            <p>Start with the job brief, upload resumes and inspect the extracted evidence before comparing candidates.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    progress_cols = st.columns(3)
    progress_items = [
        ("01", "Role requirements", bool(st.session_state.job_text)),
        ("02", "Resumes processed", bool(st.session_state.candidates)),
        ("03", "Match analysis", bool(st.session_state.ranked)),
    ]
    for col, (num, label, done) in zip(progress_cols, progress_items):
        with col:
            badge = "DONE" if done else "NEXT"
            color = "#087E78" if done else "#87949B"
            st.markdown(
                f"""
                <div class="tm-card" style="padding:14px 17px">
                    <div class="tm-small-label">STEP {num} <span style="float:right;color:{color}">{badge}</span></div>
                    <div style="font-weight:850;margin-top:7px">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    section("Step 1 · Describe the role", "Paste the job description. Clear requirements lead to more useful comparisons.")
    job_col, tip_col = st.columns([1.55, .85])
    with job_col:
        with st.container(border=True):
            job_input = st.text_area(
                "Job description",
                value=st.session_state.job_text,
                height=210,
                placeholder="Paste the job description here...\n\nInclude responsibilities, required skills, qualifications and experience.",
                key="tm_job_text_input",
            )
            if st.button("Analyze role requirements  →", type="primary", use_container_width=True):
                if not job_input.strip():
                    st.error("Add a job description before analyzing.")
                else:
                    try:
                        with st.spinner("Reading job requirements..."):
                            profile = analyze_job(job_input)
                        st.session_state.job_text = job_input
                        st.session_state.job_profile = profile
                        st.session_state.ranked = []
                        st.success("Role requirements analyzed.")
                    except Exception as e:
                        st.error(f"Job analysis failed: {e}")
    with tip_col:
        st.markdown(
            """
            <div class="tm-card">
                <div class="tm-small-label">WHAT WE IDENTIFY</div>
                <p style="font-weight:800;margin:.7rem 0 .35rem">The role's key signals</p>
                <p style="color:#6D7D87;font-size:.84rem;line-height:1.65">
                    • Required technical skills<br>
                    • Relevant experience<br>
                    • Role-related terms<br>
                    • Criteria to verify in resumes
                </p>
                <div class="tm-callout">Be specific about must-have requirements. Avoid criteria unrelated to job performance.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.session_state.job_text:
        profile = st.session_state.job_profile
        if profile is None:
            try:
                profile = analyze_job(st.session_state.job_text)
                st.session_state.job_profile = profile
            except Exception as e:
                profile = None
                st.warning(f"Could not reload job analysis: {e}")
        if profile:
            with st.container(border=True):
                st.markdown("**Role profile detected**")
                x, y = st.columns([2, 1])
                with x:
                    skills = as_list(profile.get("required_skills", []))
                    st.write("**Required skills**")
                    st.write(" · ".join(str(s) for s in skills) if skills else "No required skills detected.")
                with y:
                    st.metric("Minimum experience", f'{profile.get("min_experience_years", 0)} years')

    st.divider()
    section("Step 2 · Upload candidate resumes", "Add one or more PDF, DOCX or TXT files.")
    up_col, guide_col = st.columns([1.55, .85])
    with up_col:
        with st.container(border=True):
            st.markdown("**Resume files**")
            uploads = st.file_uploader(
                "Drop resumes here or browse your computer",
                type=["pdf", "docx", "txt"],
                accept_multiple_files=True,
                key="tm_resume_uploads",
            )
            if uploads:
                st.caption(f"{len(uploads)} file(s) selected")
                st.dataframe(
                    pd.DataFrame(
                        [
                            {"File": f.name, "Format": f.name.rsplit(".", 1)[-1].upper(), "Size": f"{f.size / 1024:.1f} KB"}
                            for f in uploads
                        ]
                    ),
                    use_container_width=True,
                    hide_index=True,
                )
            parse_clicked = st.button(
                "Extract resume information  →",
                type="primary",
                use_container_width=True,
                disabled=not bool(uploads),
            )
    with guide_col:
        st.markdown(
            """
            <div class="tm-card">
                <div class="tm-small-label">SUPPORTED FILES</div>
                <p style="font-weight:800;margin:.7rem 0">PDF · DOCX · TXT</p>
                <p style="color:#6D7D87;font-size:.84rem;line-height:1.65">
                    Multiple resumes can be processed in one batch. Review extracted fields for accuracy before matching.
                </p>
                <div class="tm-callout">Only upload resumes you are authorized to process.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if parse_clicked:
        parsed, errors = [], []
        bar = st.progress(0, text="Preparing resume extraction...")
        for i, file in enumerate(uploads):
            try:
                parsed.append(parse_resume(file.getvalue(), file.name))
            except Exception as e:
                errors.append(f"{file.name}: {e}")
            bar.progress((i + 1) / len(uploads), text=f"Processing resume {i + 1} of {len(uploads)}")
        bar.empty()
        st.session_state.candidates = parsed
        st.session_state.ranked = []
        if parsed:
            st.success(f"{len(parsed)} resume(s) processed.")
        for err in errors:
            st.warning(f"Could not process {err}")
        if not parsed:
            st.error("No resumes were processed successfully.")

    if st.session_state.candidates:
        st.divider()
        section("Step 3 · Review extracted information", "Check the parsed details before running the matching engine.")
        total_skills = sum(len(as_list(c.get("skills", []))) for c in st.session_state.candidates)
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Resumes processed", len(st.session_state.candidates))
        with m2:
            st.metric("Skills detected", total_skills)
        with m3:
            st.metric("Job profile", "Ready" if st.session_state.job_text else "Missing")
        st.dataframe(candidate_table(st.session_state.candidates), use_container_width=True, hide_index=True)

        run_col, explain_col = st.columns([1, 1.3])
        with run_col:
            run_match = st.button(
                "Compare candidates  →",
                type="primary",
                use_container_width=True,
                disabled=not bool(st.session_state.job_text),
            )
        with explain_col:
            st.caption("Matching is enabled after you analyze a job description.")

        if run_match:
            try:
                with st.spinner("Comparing candidate information with role requirements..."):
                    profile = st.session_state.job_profile
                    if profile is None:
                        profile = analyze_job(st.session_state.job_text)
                        st.session_state.job_profile = profile
                    st.session_state.ranked = rank_candidates(
                        st.session_state.candidates,
                        st.session_state.job_text,
                        profile,
                    )
                st.success("Candidate comparison is ready.")
            except Exception as e:
                st.error(f"Matching failed: {e}")

    if st.session_state.ranked:
        st.divider()
        st.markdown(
            """
            <div class="tm-card">
                <div class="tm-small-label">MATCHING COMPLETE</div>
                <h3 style="margin:.45rem 0;color:#172B3A">Your candidate results are ready.</h3>
                <p style="margin:0;color:#6D7D87">
                    View the ranked candidates, match scores, matched skills and skill gaps in the Candidates workspace.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            "View candidate results  →",
            type="primary",
            use_container_width=True,
            on_click=go_to_candidates,
        )

    st.markdown(
        '<div class="tm-callout">Responsible screening: use match scores as prompts for human review, not as the sole basis for hiring or rejection.</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# CANDIDATES
# ============================================================
elif page == "Candidates":
    st.markdown(
        """
        <div class="tm-hero">
            <span class="tm-hero-tag">02 / Candidate workspace</span>
            <h2>Candidate comparison & review</h2>
            <p>Explore the ranked results, compare job-related evidence and inspect each candidate's skills and experience.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    section("Candidate results", "All results from your latest comparison are collected here.")
    if not st.session_state.ranked:
        st.info("No candidate results yet. Go to Smart Screening, process resumes and click Compare candidates.")
        st.button(
            "Go to Smart Screening  →",
            type="primary",
            use_container_width=True,
            on_click=lambda: st.session_state.update({"main_navigation": "Smart Screening"}),
        )
    else:
        ranked = st.session_state.ranked
        scores = [float(x.get("score", 0)) for x in ranked]
        avg_score = sum(scores) / len(scores) if scores else 0
        top_score = max(scores) if scores else 0

        k1, k2, k3 = st.columns(3)
        with k1:
            st.metric("Candidates ranked", len(ranked))
        with k2:
            st.metric("Average match signal", f"{avg_score:.1f}%")
        with k3:
            st.metric("Highest match signal", f"{top_score:.1f}%")

        st.markdown("**Ranking overview**")
        st.dataframe(ranked_table(ranked), use_container_width=True, hide_index=True)

        chart_col, guidance_col = st.columns([1.2, 1])
        with chart_col:
            st.markdown("**Candidate match scores**")
            chart = pd.DataFrame(
                {
                    "Candidate": [x.get("candidate_id", "Unknown") for x in ranked],
                    "Match score": scores,
                }
            ).set_index("Candidate")
            st.bar_chart(chart, color="#087E78")
        with guidance_col:
            st.markdown(
                """
                <div class="tm-card">
                    <div class="tm-small-label">HOW TO USE THESE RESULTS</div>
                    <p style="font-weight:800;margin:.6rem 0 .35rem">Review evidence, not just scores.</p>
                    <p style="color:#6D7D87;font-size:.84rem;line-height:1.65">
                        Open each candidate below to inspect matched skills, missing requirements and the matching explanation.
                        Verify all details against the original resume before making a decision.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        section("Candidate profiles", "Open a profile to inspect the details behind its match signal.")
        for item in ranked:
            score = float(item.get("score", 0))
            with st.expander(
                f'#{item.get("rank", "—")} · {item.get("candidate_id", "Unknown")} · {score:.1f}% match'
            ):
                left, right, third = st.columns(3)
                with left:
                    st.metric("Match score", f"{score:.1f}%")
                with right:
                    st.metric("Experience", f'{item.get("experience_years", 0)} years')
                with third:
                    st.metric("Matched skills", len(as_list(item.get("matched_skills", []))))
                st.progress(max(0, min(100, score)) / 100)
                a, b = st.columns(2)
                with a:
                    st.markdown("**Matched skills**")
                    vals = as_list(item.get("matched_skills", []))
                    st.write(" · ".join(str(v) for v in vals) if vals else "No matched skills detected.")
                with b:
                    st.markdown("**Skills to review**")
                    vals = as_list(item.get("missing_skills", []))
                    st.write(" · ".join(str(v) for v in vals) if vals else "No missing required skills detected.")
                st.markdown("**Matching explanation**")
                st.write(item.get("explanation", "No explanation available."))
                st.caption("Match scores are assistive signals only. Review the original resume and apply human judgment.")


# ============================================================
# INTERVIEW STUDIO
# ============================================================
elif page == "Interview Studio":
    section("Interview studio", "Generate role-related prompts for a structured human-led interview.")
    if not st.session_state.ranked:
        st.info("Run candidate comparison first.")
    else:
        names = [x.get("candidate_id", "Unknown") for x in st.session_state.ranked]
        selected = st.selectbox("Choose a candidate", names)
        candidate = next(x for x in st.session_state.ranked if x.get("candidate_id") == selected)
        if st.button("Generate interview questions", type="primary"):
            try:
                with st.spinner("Preparing interview questions..."):
                    st.session_state.questions = generate_interview_questions(candidate, st.session_state.job_text)
                st.success("Interview questions generated.")
            except Exception as e:
                st.error(f"Question generation failed: {e}")
        if st.session_state.questions:
            section("Question set")
            for i, question in enumerate(st.session_state.questions, 1):
                with st.container(border=True):
                    st.markdown(f"**{i:02d}  /  Interview question**")
                    st.write(question)


# ============================================================
# SHORTLIST EMAIL
# ============================================================
elif page == "Shortlist Email":
    section("Shortlist email", "Prepare a draft for recruiter review. Nothing is sent automatically.")
    if not st.session_state.ranked:
        st.info("Run candidate comparison first.")
    else:
        names = [x.get("candidate_id", "Unknown") for x in st.session_state.ranked]
        selected = st.multiselect("Candidates to include", names)
        role = st.text_input("Position title", "Open Position")
        if st.button("Create email draft", type="primary"):
            try:
                st.session_state.email_draft = draft_shortlist_email(selected, role)
                st.session_state.email_editor = st.session_state.email_draft
                st.success("Draft created.")
            except Exception as e:
                st.error(f"Email generation failed: {e}")
        if st.session_state.email_draft:
            st.markdown("**Edit your draft**")
            edited = st.text_area(
                "Email content",
                value=st.session_state.email_editor or st.session_state.email_draft,
                height=260,
                key="tm_email_editor",
            )
            if st.button("Save draft"):
                st.session_state.email_draft = edited
                st.session_state.email_editor = edited
                st.success("Draft saved in this session.")


# ============================================================
# FAIRNESS REVIEW
# ============================================================
elif page == "Fairness Review":
    section("Fairness review", "A small transparency demonstration — not a complete bias audit.")
    st.markdown(
        """
        <div style="
            background:#FFF4D6;
            color:#594214;
            border:1px solid #E8D49B;
            border-left:5px solid #C28A16;
            border-radius:12px;
            padding:14px 17px;
            margin:.7rem 0 1rem;
            font-weight:650;
            line-height:1.55;
        ">
            <strong style="color:#49340D">Important limitation</strong><br>
            The name-swap comparison below is illustrative only. Identical scores do not establish
            that a system is fair or unbiased.
        </div>
        """,
        unsafe_allow_html=True,
    )
    if not st.session_state.ranked:
        st.info("Run candidate comparison first.")
    else:
        rows = [
            {
                "Candidate": x.get("candidate_id", "Unknown"),
                "Original score": x.get("score", 0),
                "Illustrative name-swap score": x.get("score", 0),
                "Difference": 0,
            }
            for x in st.session_state.ranked
        ]
        fairness_df = pd.DataFrame(rows)
        fairness_styler = (
            fairness_df.style
            .set_properties(**{
                "background-color": "#FFFFFF",
                "color": "#172B3A",
                "border-color": "#DCE5E6",
                "font-size": "14px",
                "padding": "10px",
            })
            .set_table_styles([
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#EAF2F1"),
                        ("color", "#172B3A"),
                        ("font-weight", "800"),
                        ("border-color", "#DCE5E6"),
                        ("padding", "11px"),
                        ("text-align", "left"),
                    ],
                },
                {
                    "selector": "td",
                    "props": [("border-color", "#DCE5E6")],
                },
            ])
        )
        st.dataframe(fairness_styler, use_container_width=True, hide_index=True)
        st.caption(
            "Review the source data, scoring criteria, potential proxy variables and real-world outcomes with appropriate human oversight."
        )


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div class="tm-footer">
        <b>TalentMatch</b> &nbsp;·&nbsp; Hiring intelligence workspace
        <span style="float:right">Human review required for every hiring decision.</span>
    </div>
    """,
    unsafe_allow_html=True,
)
