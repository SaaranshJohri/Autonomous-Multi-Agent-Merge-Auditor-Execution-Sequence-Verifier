import streamlit as st
import requests


# =========================================================
# HELPER — DISPLAY CHANGES
# =========================================================

def show_changes(changes):

    if not changes:
        st.info("No changes detected.")
        return

    functions = changes.get(
        "functions",
        {}
    )

    classes = changes.get(
        "classes",
        {}
    )

    imports_added = changes.get(
        "imports_added",
        []
    )

    imports_removed = changes.get(
        "imports_removed",
        []
    )


    # =====================================================
    # FUNCTIONS
    # =====================================================

    st.markdown("**Functions**")

    added = functions.get(
        "added",
        []
    )

    removed = functions.get(
        "removed",
        []
    )

    modified = functions.get(
        "modified",
        []
    )


    if added:

        for name in added:

            st.markdown(
                f'<span class="change-added">'
                f'+ Added: {name}'
                f'</span>',
                unsafe_allow_html=True
            )


    if removed:

        for name in removed:

            st.markdown(
                f'<span class="change-removed">'
                f'- Removed: {name}'
                f'</span>',
                unsafe_allow_html=True
            )


    if modified:

        for name in modified:

            st.markdown(
                f'<span class="change-modified">'
                f'~ Modified: {name}'
                f'</span>',
                unsafe_allow_html=True
            )


    if not added and not removed and not modified:

        st.write("No function changes.")


    # =====================================================
    # CLASSES
    # =====================================================

    st.markdown("")
    st.markdown("**Classes**")

    class_added = classes.get(
        "added",
        []
    )

    class_removed = classes.get(
        "removed",
        []
    )

    class_modified = classes.get(
        "modified",
        []
    )


    for name in class_added:

        st.markdown(
            f'<span class="change-added">'
            f'+ Added class: {name}'
            f'</span>',
            unsafe_allow_html=True
        )


    for name in class_removed:

        st.markdown(
            f'<span class="change-removed">'
            f'- Removed class: {name}'
            f'</span>',
            unsafe_allow_html=True
        )


    for name in class_modified:

        st.markdown(
            f'<span class="change-modified">'
            f'~ Modified class: {name}'
            f'</span>',
            unsafe_allow_html=True
        )


    # =====================================================
    # IMPORTS
    # =====================================================

    st.markdown("")
    st.markdown("**Imports**")

    for name in imports_added:

        st.markdown(
            f'<span class="change-added">'
            f'+ {name}'
            f'</span>',
            unsafe_allow_html=True
        )


    for name in imports_removed:

        st.markdown(
            f'<span class="change-removed">'
            f'- {name}'
            f'</span>',
            unsafe_allow_html=True
        )


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MergeMind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background-color: #0e1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* =====================================================
       HEADER
       ===================================================== */

    .title {
        font-size: 44px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #9ca3af;
        font-size: 17px;
        margin-top: -5px;
        margin-bottom: 30px;
    }


    /* =====================================================
       SECTION
       ===================================================== */

    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }


    /* =====================================================
       CARDS
       ===================================================== */

    .info-card {
        padding: 18px;
        border-radius: 12px;
        background-color: #161b22;
        border: 1px solid #30363d;
        margin-bottom: 12px;
    }

    .function-card {
        padding: 16px;
        border-radius: 10px;
        background-color: #161b22;
        border: 1px solid #30363d;
        margin-bottom: 10px;
    }

    .function-name {
        font-size: 18px;
        font-weight: 700;
    }

    .muted {
        color: #8b949e;
        font-size: 14px;
    }


    /* =====================================================
       CODE VERSION CARDS
       ===================================================== */

    .version-header {
        padding: 12px 16px;
        border-radius: 10px 10px 0px 0px;
        background-color: #161b22;
        border: 1px solid #30363d;
        border-bottom: none;
        font-size: 17px;
        font-weight: 700;
    }

    .version-description {
        color: #8b949e;
        font-size: 13px;
        margin-top: 3px;
    }


    /* =====================================================
       PIPELINE
       ===================================================== */

    .pipeline-step {
        padding: 8px 12px;
        border-radius: 8px;
        background-color: #161b22;
        border: 1px solid #30363d;
        margin-bottom: 5px;
        font-size: 14px;
    }


    /* =====================================================
       STATUS
       ===================================================== */

    .status-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #161b22;
        border: 1px solid #30363d;
        margin-bottom: 15px;
    }


    /* =====================================================
       CONFLICT
       ===================================================== */

    .conflict-card {
        padding: 18px;
        border-radius: 12px;
        background-color: #1c1414;
        border: 1px solid #7f1d1d;
        margin-bottom: 15px;
    }

    .conflict-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .conflict-description {
        color: #d1d5db;
        font-size: 14px;
    }


    /* =====================================================
       SUCCESS
       ===================================================== */

    .success-card {
        padding: 18px;
        border-radius: 12px;
        background-color: #111c17;
        border: 1px solid #166534;
        margin-bottom: 15px;
    }


    /* =====================================================
       CHANGE BADGES
       ===================================================== */

    .change-added {
        color: #3fb950;
        font-weight: 600;
    }

    .change-removed {
        color: #f85149;
        font-weight: 600;
    }

    .change-modified {
        color: #d29922;
        font-weight: 600;
    }


    /* =====================================================
       CODE
       ===================================================== */

    code {
        font-size: 0.9rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="title">🧠 MergeMind</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Semantic Merge Analysis & Code Intelligence'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ Analysis")

    backend_url = st.text_input(
        "Backend URL",
        value="http://127.0.0.1:8000"
    )

    st.divider()

    st.subheader("Merge Pipeline")

    st.markdown(
        """
        <div class="pipeline-step">
        🟢 Source Versions
        </div>

        <div style="text-align:center;">↓</div>

        <div class="pipeline-step">
        🟢 AST Parsing
        </div>

        <div style="text-align:center;">↓</div>

        <div class="pipeline-step">
        🟢 Semantic Analysis
        </div>

        <div style="text-align:center;">↓</div>

        <div class="pipeline-step">
        🟢 Dependency Graph
        </div>

        <div style="text-align:center;">↓</div>

        <div class="pipeline-step">
        🟢 Conflict Detection
        </div>

        <div style="text-align:center;">↓</div>

        <div class="pipeline-step">
        ⚪ Visual Resolution
        </div>

        <div style="text-align:center;">↓</div>

        <div class="pipeline-step">
        ⚪ Validation
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.caption(
        "MergeMind v0.3.0"
    )


# =========================================================
# DEFAULT SAMPLE CODE
# =========================================================

base_code_default = '''import math


def calculate_tax(price):
    tax = price * 0.18
    return tax


def calculate_total(price):

    if price > 0:
        tax = calculate_tax(price)
        total = price + tax
        return total

    return 0
'''


developer_a_default = '''import math


def calculate_tax(price):
    tax = price * 0.18
    return tax


def calculate_total(price):

    if price > 0:
        tax = calculate_tax(price)

        discount = price * 0.10

        total = price + tax - discount

        return total

    return 0
'''


developer_b_default = '''import math


def calculate_tax(price):
    tax = price * 0.20
    return tax


def calculate_total(price):

    if price > 0:
        tax = calculate_tax(price)

        total = price + tax

        return total

    return 0
'''


# =========================================================
# SOURCE VERSIONS
# =========================================================

st.markdown(
    '<div class="section-title">🔀 Merge Sources</div>',
    unsafe_allow_html=True
)

st.caption(
    "Compare the original code with changes made by two developers."
)


# =========================================================
# FILENAMES
# =========================================================

name_col1, name_col2, name_col3 = st.columns(3)

with name_col1:

    base_filename = st.text_input(
        "Base filename",
        value="test.py"
    )

with name_col2:

    developer_a_filename = st.text_input(
        "Developer A filename",
        value="test.py"
    )

with name_col3:

    developer_b_filename = st.text_input(
        "Developer B filename",
        value="test.py"
    )


# =========================================================
# CODE EDITORS
# =========================================================

code_col1, code_col2, code_col3 = st.columns(3)


with code_col1:

    st.markdown(
        """
        <div class="version-header">
        🟦 BASE
        <div class="version-description">
        Original version of the code
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    base_code = st.text_area(
        "Base code",
        value=base_code_default,
        height=430,
        label_visibility="collapsed",
        key="base_code"
    )


with code_col2:

    st.markdown(
        """
        <div class="version-header">
        🟨 DEVELOPER A
        <div class="version-description">
        Changes from developer A
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    developer_a_code = st.text_area(
        "Developer A code",
        value=developer_a_default,
        height=430,
        label_visibility="collapsed",
        key="developer_a_code"
    )


with code_col3:

    st.markdown(
        """
        <div class="version-header">
        🟪 DEVELOPER B
        <div class="version-description">
        Changes from developer B
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    developer_b_code = st.text_area(
        "Developer B code",
        value=developer_b_default,
        height=430,
        label_visibility="collapsed",
        key="developer_b_code"
    )


# =========================================================
# ANALYZE MERGE BUTTON
# =========================================================

st.markdown("")

analyze_merge = st.button(
    "🔍 Analyze Merge",
    type="primary",
    use_container_width=True
)


# =========================================================
# MERGE ANALYSIS
# =========================================================

if analyze_merge:

    # -----------------------------------------------------
    # CLEAR OLD RESULT BEFORE NEW ANALYSIS
    # -----------------------------------------------------

    st.session_state.pop(
        "merge_analysis",
        None
    )

    with st.spinner(
        "Analyzing branches and detecting semantic conflicts..."
    ):

        try:

            response = requests.post(
                f"{backend_url.rstrip('/')}/merge",
                json={
                    "base_code": base_code,
                    "developer_a_code": developer_a_code,
                    "developer_b_code": developer_b_code,
                    "base_filename": base_filename,
                    "developer_a_filename": developer_a_filename,
                    "developer_b_filename": developer_b_filename
                },
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            if not data.get("success"):

                st.error(
                    data.get(
                        "error",
                        "Merge analysis failed."
                    )
                )

            else:

                merge_analysis = data.get(
                    "merge_analysis",
                    {}
                )

                st.session_state[
                    "merge_analysis"
                ] = merge_analysis

                st.success(
                    "Merge analysis completed."
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to the MergeMind backend."
            )

            st.info(
                "Make sure FastAPI is running with:"
            )

            st.code(
                "uvicorn main:app --reload"
            )

        except requests.exceptions.Timeout:

            st.error(
                "❌ Merge analysis timed out."
            )

        except requests.exceptions.HTTPError as e:

            st.error(
                f"❌ Backend returned an HTTP error: {e}"
            )

        except Exception as e:

            st.error(
                f"❌ Unexpected error: {e}"
            )


# =========================================================
# DISPLAY MERGE RESULTS
# =========================================================

if "merge_analysis" in st.session_state:

    merge_analysis = st.session_state[
        "merge_analysis"
    ]

    conflicts = merge_analysis.get(
        "conflicts",
        []
    )

    summary = merge_analysis.get(
        "summary",
        {}
    )

    developer_a = merge_analysis.get(
        "developer_a",
        {}
    )

    developer_b = merge_analysis.get(
        "developer_b",
        {}
    )

    developer_a_changes = developer_a.get(
        "changes",
        {}
    )

    developer_b_changes = developer_b.get(
        "changes",
        {}
    )


    # =====================================================
    # MERGE STATUS
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '📊 Merge Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    conflict_count = summary.get(
        "conflict_count",
        len(conflicts)
    )


    if conflict_count > 0:

        st.markdown(
            f"""
            <div class="conflict-card">

            <div class="conflict-title">
            🔴 {conflict_count}
            {'Conflict' if conflict_count == 1 else 'Conflicts'}
            Detected
            </div>

            <div class="conflict-description">
            MergeMind found changes that cannot currently
            be merged automatically.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="success-card">

            <div class="conflict-title">
            🟢 No Conflicts Detected
            </div>

            <div class="conflict-description">
            The changes from both developers can currently
            coexist without a detected structural conflict.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # SUMMARY METRICS
    # =====================================================

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:

        st.metric(
            "Conflicts",
            conflict_count
        )

    with metric2:

        modified_a = len(
            developer_a_changes
            .get("functions", {})
            .get("modified", [])
        )

        st.metric(
            "A Modified",
            modified_a
        )

    with metric3:

        modified_b = len(
            developer_b_changes
            .get("functions", {})
            .get("modified", [])
        )

        st.metric(
            "B Modified",
            modified_b
        )

    with metric4:

        added_a = len(
            developer_a_changes
            .get("functions", {})
            .get("added", [])
        )

        added_b = len(
            developer_b_changes
            .get("functions", {})
            .get("added", [])
        )

        st.metric(
            "Functions Added",
            added_a + added_b
        )


    # =====================================================
    # RESULT TABS
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '🔬 Merge Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    (
        conflict_tab,
        changes_tab,
        source_tab
    ) = st.tabs(
        [
            "🔴 Conflicts",
            "📝 Changes",
            "📄 Source Versions"
        ]
    )


    # =====================================================
    # CONFLICT TAB
    # =====================================================

    with conflict_tab:

        if not conflicts:

            st.info(
                "No conflicts were detected."
            )

        else:

            for index, conflict in enumerate(
                conflicts,
                start=1
            ):

                entity = conflict.get(
                    "entity",
                    "Unknown"
                )

                conflict_type = conflict.get(
                    "type",
                    "conflict"
                )

                description = conflict.get(
                    "description",
                    "Conflicting changes detected."
                )

                st.markdown(
                    f"""
                    <div class="conflict-card">

                    <div class="conflict-title">
                    🔴 Conflict #{index}
                    — {entity}
                    </div>

                    <div class="muted">
                    Type: {conflict_type}
                    </div>

                    <br>

                    <div class="conflict-description">
                    {description}
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # -----------------------------------------
                # THREE-WAY VIEW
                # -----------------------------------------

                base_version = conflict.get(
                    "base",
                    ""
                )

                developer_a_version = conflict.get(
                    "developer_a",
                    ""
                )

                developer_b_version = conflict.get(
                    "developer_b",
                    ""
                )


                view1, view2, view3 = st.columns(3)


                with view1:

                    st.markdown(
                        "**🟦 BASE**"
                    )

                    st.code(
                        base_version,
                        language="python"
                    )


                with view2:

                    st.markdown(
                        "**🟨 DEVELOPER A**"
                    )

                    st.code(
                        developer_a_version,
                        language="python"
                    )


                with view3:

                    st.markdown(
                        "**🟪 DEVELOPER B**"
                    )

                    st.code(
                        developer_b_version,
                        language="python"
                    )


                st.divider()


    # =====================================================
    # CHANGES TAB
    # =====================================================

    with changes_tab:

        st.subheader(
            "🟨 Developer A Changes"
        )

        show_changes(
            developer_a_changes
        )

        st.divider()

        st.subheader(
            "🟪 Developer B Changes"
        )

        show_changes(
            developer_b_changes
        )


    # =====================================================
    # SOURCE TAB
    # =====================================================

    with source_tab:

        source1, source2, source3 = st.tabs(
            [
                "🟦 Base",
                "🟨 Developer A",
                "🟪 Developer B"
            ]
        )


        with source1:

            st.code(
                st.session_state.get(
                    "base_code",
                    base_code_default
                ),
                language="python",
                line_numbers=True
            )


        with source2:

            st.code(
                st.session_state.get(
                    "developer_a_code",
                    developer_a_default
                ),
                language="python",
                line_numbers=True
            )


        with source3:

            st.code(
                st.session_state.get(
                    "developer_b_code",
                    developer_b_default
                ),
                language="python",
                line_numbers=True
            )


# =========================================================
# INITIAL STATE
# =========================================================

else:

    st.markdown(
        """
        <div class="info-card">

        <h3>🧠 Welcome to MergeMind</h3>

        <p style="color:#9ca3af;">

        MergeMind analyzes changes made by multiple
        developers and identifies structural conflicts
        before they reach the final codebase.

        </p>

        <p style="color:#9ca3af;">

        Start by providing three versions of your code:

        </p>

        <ul style="color:#9ca3af;">

        <li><b>Base</b> — original code</li>
        <li><b>Developer A</b> — first developer's changes</li>
        <li><b>Developer B</b> — second developer's changes</li>

        </ul>

        <p style="color:#9ca3af;">

        MergeMind will parse the three versions,
        compare their structures and identify conflicts.

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )