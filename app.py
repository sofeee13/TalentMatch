
import streamlit as st
import pandas as pd

from resume_parser import parse_resume
from job_analyzer import analyze_job
from matching_engine import rank_candidates
from ai_helpers import generate_interview_questions, draft_shortlist_email


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="TalentMatch | AI Recruitment",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# DESIGN SYSTEM
# =========================================================

st.markdown("""
<style>

/* APP BACKGROUND */

.stApp {
    background: #F7F7FC;
    color: #28243D;
}

.block-container {
    padding: 2rem 2.5rem 3rem;
    max-width: 1500px;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #ECEAF4;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

.brand {
    font-size: 25px;
    font-weight: 800;
    color: #7565D9;
    letter-spacing: -1px;
}

.brand-subtitle {
    font-size: 11px;
    color: #9692A9;
    letter-spacing: 2px;
    margin-top: 5px;
    font-weight: 600;
}

.sidebar-footer {
    background: #F7F5FF;
    border-radius: 12px;
    padding: 13px;
    margin-top: 25px;
    font-size: 12px;
    color: #77718F;
    line-height: 1.6;
}

/* HEADER */

.top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.page-title {
    color: #28243D;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -1px;
}

.page-subtitle {
    color: #8B879D;
    font-size: 14px;
    margin-bottom: 28px;
}

/* SECTION HEADINGS */

.section-title {
    font-size: 21px;
    color: #28243D;
    font-weight: 750;
    margin-bottom: 5px;
}

.section-caption {
    color: #9290A2;
    font-size: 13px;
    margin-bottom: 18px;
}

/* HERO */

.hero-card {
    background: linear-gradient(115deg, #7565D9, #9989EA);
    border-radius: 18px;
    padding: 28px;
    color: white;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 25px;
    font-weight: 800;
    color: white;
}

.hero-description {
    color: #F0EDFF;
    font-size: 14px;
    margin-top: 8px;
}

/* METRIC CARDS */

.metric-card {
    background: white;
    border: 1px solid #ECEAF4;
    border-radius: 16px;
    padding: 21px;
    min-height: 125px;
    box-shadow: 0 4px 16px rgba(50, 40, 90, 0.035);
}

.metric-icon {
    font-size: 21px;
    margin-bottom: 12px;
}

.metric-label {
    color: #8B879D;
    font-size: 13px;
    font-weight: 500;
}

.metric-number {
    color: #7565D9;
    font-size: 29px;
    font-weight: 800;
    margin-top: 7px;
}

/* CONTENT CARDS */

.content-card {
    background: white;
    border: 1px solid #ECEAF4;
    border-radius: 15px;
    padding: 22px;
    margin-bottom: 16px;
}

/* BUTTONS */

.stButton > button {
    border-radius: 9px;
    min-height: 42px;
    font-weight: 650;
    border: 1px solid #E5E1F4;
}

.stButton > button[kind="primary"] {
    background: #7565D9;
    color: white;
    border: none;
}

.stButton > button[kind="primary"]:hover {
    background: #6252C5;
    color: white;
}

/* INPUTS */

.stTextInput input,
.stTextArea textarea {
    background: white;
    border-radius: 9px;
    border: 1px solid #E7E4F0;
}

[data-testid="stFileUploader"] {
    background: white;
    border: 1px dashed #B7ACEB;
    border-radius: 13px;
    padding: 15px;
}

/* TABLES */

[data-testid="stDataFrame"] {
    border: 1px solid #ECEAF4;
    border-radius: 12px;
    overflow: hidden;
}

/* DIVIDERS */

hr {
    border-color: #ECEAF4;
}

/* HIDE STREAMLIT DECORATIONS */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "candidates": [],
    "job_text": "",
    "job_profile": None,
    "ranked": [],
    "questions": [],
    "email_draft": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">👥 TalentMatch</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-subtitle">RECRUITMENT INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.caption("WORKSPACE")

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Screen Resumes",
            "Candidate Details",
            "Interview Questions",
            "Shortlist Email",
            "Fairness Checks"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("""
    <div class="sidebar-footer">
        🔒 <b>Privacy reminder</b><br>
        Use synthetic or consented resume data.
        Every hiring recommendation requires
        independent human review.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# COMMON HEADER
# =========================================================

st.markdown(
    '<div class="page-title">TalentMatch Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Your intelligent workspace for recruitment and candidate evaluation.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# REUSABLE METRIC CARD
# =========================================================

def metric_card(icon, label, value):

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-number">{value}</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# OVERVIEW
# =========================================================

if page == "Overview":

    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">Welcome to TalentMatch 👋</div>
        <div class="hero-description">
            Simplify resume screening, understand candidate skills
            and support better recruitment decisions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Recruitment Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-caption">Your recruitment activity at a glance.</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "📄",
            "Resumes Analyzed",
            len(st.session_state.candidates)
        )

    with c2:
        metric_card(
            "💼",
            "Job Description",
            "Added" if st.session_state.job_text else "Pending"
        )

    with c3:
        metric_card(
            "👥",
            "Candidates Ranked",
            len(st.session_state.ranked)
        )

    with c4:
        metric_card(
            "⭐",
            "Average Match",
            (
                f'{sum(x["score"] for x in st.session_state.ranked) / len(st.session_state.ranked):.1f}%'
                if st.session_state.ranked else "—"
            )
        )

    st.write("")

    left, right = st.columns([1.4, 1])

    with left:

        st.markdown(
            '<div class="section-title">Candidate Match Analysis</div>',
            unsafe_allow_html=True
        )

        if st.session_state.ranked:

            chart_data = pd.DataFrame({
                "Candidate": [
                    x["candidate_id"]
                    for x in st.session_state.ranked
                ],
                "Match Score": [
                    x["score"]
                    for x in st.session_state.ranked
                ]
            }).set_index("Candidate")

            st.bar_chart(
                chart_data,
                color="#8979E5"
            )

        else:
            st.info("Your candidate match chart will appear after ranking resumes.")

    with right:

        st.markdown(
            '<div class="section-title">Recruitment Workflow</div>',
            unsafe_allow_html=True
        )

        st.markdown("""
        <div class="content-card">
            <b>01 · Job Description</b><br>
            <small>Define the role and requirements.</small><br><br>

            <b>02 · Resume Upload</b><br>
            <small>Upload PDF, DOCX or TXT resumes.</small><br><br>

            <b>03 · Candidate Analysis</b><br>
            <small>Extract skills and experience.</small><br><br>

            <b>04 · Matching</b><br>
            <small>Compare candidate evidence with job requirements.</small><br><br>

            <b>05 · Recruiter Review</b><br>
            <small>Review recommendations and make independent decisions.</small>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.ranked:

        st.markdown(
            '<div class="section-title">Recent Candidate Rankings</div>',
            unsafe_allow_html=True
        )

        recent_data = pd.DataFrame([
            {
                "Rank": x["rank"],
                "Candidate": x["candidate_id"],
                "Match Score": f'{x["score"]}%',
                "Experience": f'{x["experience_years"]} years'
            }
            for x in st.session_state.ranked
        ])

        st.dataframe(
            recent_data,
            use_container_width=True,
            hide_index=True
        )

    st.caption(
        "TalentMatch provides assistive recommendations only. "
        "Recruiters remain responsible for all hiring decisions."
    )


# =========================================================
# SCREEN RESUMES
# =========================================================

elif page == "Screen Resumes":

    st.markdown(
        '<div class="section-title">Resume Screening</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-caption">Add a job description and upload resumes for analysis.</div>',
        unsafe_allow_html=True
    )

    st.markdown("#### 01 · Job Description")

    job_input = st.text_area(
        "Job description",
        value=st.session_state.job_text,
        height=190,
        placeholder="Enter job responsibilities, skills and experience requirements..."
    )

    if st.button("Save and Analyze Job", type="primary"):

        if not job_input.strip():

            st.error("Please enter a job description.")

        else:

            try:
                profile = analyze_job(job_input)

                st.session_state.job_text = job_input
                st.session_state.job_profile = profile
                st.session_state.ranked = []

                st.success("Job description analyzed successfully.")

            except Exception as e:
                st.error(f"Job analysis failed: {e}")

    if st.session_state.job_text:

        profile = st.session_state.job_profile

        if profile is None:
            profile = analyze_job(st.session_state.job_text)
            st.session_state.job_profile = profile

        with st.container(border=True):

            st.markdown("**Detected Job Requirements**")

            st.write(
                "Required skills:",
                ", ".join(profile["required_skills"]) or "None detected"
            )

            st.write(
                "Minimum experience:",
                f'{profile["min_experience_years"]} years'
            )

    st.divider()

    st.markdown("#### 02 · Upload Candidate Resumes")

    uploads = st.file_uploader(
        "Drag and drop resume files here",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if st.button("Parse Resumes", type="primary"):

        if not uploads:

            st.warning("Please upload at least one resume.")

        else:

            parsed = []

            progress = st.progress(0)

            for index, file in enumerate(uploads):

                try:

                    info = parse_resume(
                        file.getvalue(),
                        file.name
                    )

                    parsed.append(info)

                except Exception as e:

                    st.error(f"Could not read {file.name}: {e}")

                progress.progress((index + 1) / len(uploads))

            st.session_state.candidates = parsed
            st.session_state.ranked = []

            st.success(f"{len(parsed)} resume(s) processed.")

    if st.session_state.candidates:

        st.divider()

        st.markdown("#### 03 · Extracted Candidate Information")

        candidate_data = []

        for c in st.session_state.candidates:

            candidate_data.append({
                "Candidate": c["candidate_id"],
                "Skills": ", ".join(c["skills"]),
                "Experience": c["experience_years"],
                "Education": c["education"]
            })

        st.dataframe(
            pd.DataFrame(candidate_data),
            use_container_width=True,
            hide_index=True
        )

        if st.button(
            "✨ Match and Rank Candidates",
            type="primary",
            disabled=not bool(st.session_state.job_text)
        ):

            try:

                with st.spinner("Analyzing candidate matches..."):

                    profile = st.session_state.job_profile

                    if profile is None:
                        profile = analyze_job(st.session_state.job_text)

                    st.session_state.ranked = rank_candidates(
                        st.session_state.candidates,
                        st.session_state.job_text,
                        profile
                    )

                st.success("Candidate matching completed.")

            except Exception as e:

                st.error(f"Matching failed: {e}")


# =========================================================
# CANDIDATE DETAILS
# =========================================================

elif page == "Candidate Details":

    st.markdown(
        '<div class="section-title">Candidate Profiles</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-caption">Review candidate matches, skills and supporting evidence.</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.ranked:

        st.info("Run candidate matching first.")

    else:

        for item in st.session_state.ranked:

            with st.expander(
                f'#{item["rank"]}  |  {item["candidate_id"]}  |  {item["score"]}% match'
            ):

                c1, c2 = st.columns(2)

                with c1:
                    st.metric(
                        "Match Score",
                        f'{item["score"]}%'
                    )

                with c2:
                    st.metric(
                        "Experience",
                        f'{item["experience_years"]} years'
                    )

                st.progress(
                    max(0, min(100, float(item["score"]))) / 100
                )

                st.markdown("**Matched Skills**")

                if item["matched_skills"]:
                    for skill in item["matched_skills"]:
                        st.write(f"✓ {skill}")
                else:
                    st.write("No matched skills detected.")

                st.markdown("**Missing Required Skills**")

                if item["missing_skills"]:
                    for skill in item["missing_skills"]:
                        st.write(f"• {skill}")
                else:
                    st.write("No missing required skills detected.")

                st.markdown("**Match Explanation**")

                st.write(item["explanation"])

                st.caption(
                    "Scores are assistive estimates, not hiring decisions."
                )


# =========================================================
# INTERVIEW QUESTIONS
# =========================================================

elif page == "Interview Questions":

    st.markdown(
        '<div class="section-title">Interview Question Studio</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-caption">Generate role-related questions for recruiter review.</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.ranked:

        st.info("Rank candidates first.")

    else:

        names = [
            x["candidate_id"]
            for x in st.session_state.ranked
        ]

        selected = st.selectbox(
            "Select candidate",
            names
        )

        candidate = next(
            x for x in st.session_state.ranked
            if x["candidate_id"] == selected
        )

        if st.button(
            "Generate Interview Questions",
            type="primary"
        ):

            try:

                with st.spinner("Preparing interview questions..."):

                    st.session_state.questions = generate_interview_questions(
                        candidate,
                        st.session_state.job_text
                    )

                st.success("Questions generated.")

            except Exception as e:

                st.error(f"Question generation failed: {e}")

        if st.session_state.questions:

            st.markdown("#### Generated Questions")

            for i, question in enumerate(
                st.session_state.questions,
                1
            ):

                with st.container(border=True):

                    st.markdown(f"**Question {i}**")

                    st.write(question)


# =========================================================
# SHORTLIST EMAIL
# =========================================================

elif page == "Shortlist Email":

    st.markdown(
        '<div class="section-title">Shortlist Email Studio</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-caption">Prepare an email draft for recruiter review.</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.ranked:

        st.info("Rank candidates first.")

    else:

        selected = st.multiselect(
            "Select candidates for recruiter review",
            [
                x["candidate_id"]
                for x in st.session_state.ranked
            ]
        )

        role = st.text_input(
            "Position title",
            "Open Position"
        )

        if st.button(
            "Generate Email Draft",
            type="primary"
        ):

            try:

                st.session_state.email_draft = draft_shortlist_email(
                    selected,
                    role
                )

                st.success("Email draft generated.")

            except Exception as e:

                st.error(f"Email generation failed: {e}")

        if st.session_state.email_draft:

            st.markdown("#### Email Preview")

            st.text_area(
                "Review and edit the email",
                key="email_editor",
                value=st.session_state.email_draft,
                height=250
            )

            if st.button("Update Draft"):

                st.session_state.email_draft = st.session_state.email_editor

                st.success("Draft updated.")


# =========================================================
# FAIRNESS CHECKS
# =========================================================

elif page == "Fairness Checks":

    st.markdown(
        '<div class="section-title">Fairness and Transparency</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-caption">Inspect basic scoring transparency checks.</div>',
        unsafe_allow_html=True
    )

    st.info(
        "This prototype includes a basic name-swap demonstration. "
        "It is not a complete fairness or bias audit."
    )

    if not st.session_state.ranked:

        st.warning("Rank candidates first.")

    else:

        rows = []

        for x in st.session_state.ranked:

            rows.append({
                "Candidate ID": x["candidate_id"],
                "Original Score": x["score"],
                "Hypothetical Name-Swap Score": x["score"],
                "Difference": 0
            })

        fairness_df = pd.DataFrame(rows)

        st.markdown("#### Name-Swap Comparison")

        st.dataframe(
            fairness_df,
            use_container_width=True,
            hide_index=True
        )

        st.success(
            "This demonstration shows identical scores under a hypothetical name swap."
        )

        st.warning(
            "Identical scores in this demonstration do not prove that "
            "the overall system is unbiased. Review data, scoring criteria, "
            "potential proxies and outcomes with human oversight."
        )


# ==========================================================
# FOOTER
# ===============================================================

st.divider()

st.caption(
    "TalentMatch © 2026 | AI-assisted recruitment | "
    "Human review required for all hiring decisions."
)
