import streamlit as st
import requests



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

    /* ---------- GLOBAL ---------- */

    .stApp {
        background-color: #0e1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ---------- HEADER ---------- */

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


    /* ---------- SECTION ---------- */

    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }


    /* ---------- CARDS ---------- */

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


    /* ---------- PIPELINE ---------- */

    .pipeline-step {
        padding: 8px 12px;
        border-radius: 8px;
        background-color: #161b22;
        border: 1px solid #30363d;
        margin-bottom: 5px;
        font-size: 14px;
    }


    /* ---------- STATUS ---------- */

    .status-box {
        padding: 12px;
        border-radius: 10px;
        background-color: #161b22;
        border: 1px solid #30363d;
        margin-bottom: 15px;
    }


    /* ---------- CODE ---------- */

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
    'Code Intelligence & Semantic Merge Analysis'
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

    st.subheader("Analysis Pipeline")

    st.markdown(
        """
        <div class="pipeline-step">
        🟢 Source Code
        </div>

        <div style="text-align:center;">↓</div>

        <div class="pipeline-step">
        🟢 AST Parsing
        </div>

        <div style="text-align:center;">↓</div>

        <div class="pipeline-step">
        🟢 Dependency Graph
        </div>

        <div style="text-align:center;">↓</div>

        <div class="pipeline-step">
        ⚪ Conflict Detection
        </div>

        <div style="text-align:center;">↓</div>

        <div class="pipeline-step">
        ⚪ AI Auditing
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.caption(
        "MergeMind v0.2.0"
    )


# =========================================================
# SOURCE CODE INPUT
# =========================================================

st.markdown(
    '<div class="section-title">📄 Source Code</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 3])

with col1:

    filename = st.text_input(
        "Filename",
        value="test.py"
    )


with col2:

    st.write("")


# =========================================================
# DEFAULT SAMPLE CODE
# =========================================================

default_code = '''import math
from database import save_user


class User:

    def __init__(self, name):
        self.name = name

    def save(self):
        save_user(self.name)


def calculate_tax(price):
    tax = price * 0.18
    return tax


def calculate_total(price):

    if price > 0:
        tax = calculate_tax(price)
        total = price + tax
        return total

    return 0


def checkout(price):

    total = calculate_total(price)

    print(total)

    return total


user = User("Saaransh")

user.save()

checkout(100)
'''


code = st.text_area(
    "Python Code",
    value=default_code,
    height=400,
    label_visibility="collapsed"
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

analyze = st.button(
    "🔍 Analyze Code",
    type="primary",
    use_container_width=True
)


# =========================================================
# BACKEND ANALYSIS
# =========================================================

if analyze:

    with st.spinner(
        "Analyzing source code..."
    ):

        try:

            response = requests.post(
                f"{backend_url.rstrip('/')}/parse",
                json={
                    "filename": filename,
                    "code": code
                },
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            if not data.get("success"):

                st.error(
                    data.get(
                        "error",
                        "Analysis failed."
                    )
                )

                st.session_state.pop(
                    "analysis",
                    None
                )

                st.session_state.pop(
                    "graph",
                    None
                )

            else:

                # Store AST analysis
                st.session_state["analysis"] = (
                    data.get(
                        "ast_analysis",
                        {}
                    )
                )

                # Store dependency graph
                st.session_state["graph"] = (
                    data.get(
                        "dependency_graph",
                        {}
                    )
                )

                # Store source information
                st.session_state["filename"] = filename
                st.session_state["source_code"] = code

                st.success(
                    "Analysis completed successfully."
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
                "❌ Backend request timed out."
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
# DISPLAY RESULTS
# =========================================================

if "analysis" in st.session_state:

    analysis = st.session_state["analysis"]

    graph_data = st.session_state.get(
        "graph",
        {}
    )


    # =====================================================
    # EXTRACT DATA
    # =====================================================

    functions = analysis.get(
        "functions",
        []
    )

    classes = analysis.get(
        "classes",
        []
    )

    imports = analysis.get(
        "imports",
        []
    )

    calls = analysis.get(
        "function_calls",
        []
    )

    variables = analysis.get(
        "variables",
        []
    )

    assignments = analysis.get(
        "assignments",
        []
    )

    conditions = analysis.get(
        "conditions",
        []
    )

    loops = analysis.get(
        "loops",
        []
    )

    returns = analysis.get(
        "returns",
        []
    )

    nodes_data = graph_data.get(
        "nodes",
        []
    )

    edges_data = graph_data.get(
        "edges",
        []
    )


    # =====================================================
    # ANALYSIS STATUS
    # =====================================================

    st.markdown(
        '<div class="section-title">📊 Analysis Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="status-box">

        <b>Analyzed File:</b>
        {st.session_state.get("filename", "unknown.py")}

        &nbsp;&nbsp;•&nbsp;&nbsp;

        <b>Status:</b>
        🟢 Analysis Complete

        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # METRICS
    # =====================================================

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:

        st.metric(
            "Functions",
            len(functions)
        )

    with c2:

        st.metric(
            "Classes",
            len(classes)
        )

    with c3:

        st.metric(
            "Imports",
            len(imports)
        )

    with c4:

        st.metric(
            "Function Calls",
            len(calls)
        )

    with c5:

        st.metric(
            "Variables",
            len(variables)
        )


    # =====================================================
    # SECONDARY METRICS
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Assignments",
            len(assignments)
        )

    with c2:

        st.metric(
            "Conditions",
            len(conditions)
        )

    with c3:

        st.metric(
            "Loops",
            len(loops)
        )

    with c4:

        st.metric(
            "Graph Nodes",
            len(nodes_data)
        )


    # =====================================================
    # MAIN TABS
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '🔬 Code Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    (
        tab_structure,
        tab_graph,
        tab_relationships,
        tab_functions,
        tab_classes,
        tab_imports,
        tab_source
    ) = st.tabs(
        [
            "🧩 Structure",
            "🕸️ Dependency Graph",
            "🔗 Relationships",
            "⚙️ Functions",
            "🏛️ Classes",
            "📦 Imports",
            "📄 Source"
        ]
    )


    # =====================================================
    # TAB 1 — STRUCTURE
    # =====================================================

    with tab_structure:

        col1, col2 = st.columns(2)


        # -------------------------------------------------
        # FUNCTIONS
        # -------------------------------------------------

        with col1:

            st.subheader(
                "🔧 Functions"
            )

            if not functions:

                st.info(
                    "No functions detected."
                )

            for function in functions:

                arguments = function.get(
                    "arguments",
                    []
                )

                argument_names = [
                    arg.get(
                        "name",
                        "?"
                    )
                    for arg in arguments
                ]

                signature = (
                    f"{function['name']}"
                    f"("
                    f"{', '.join(argument_names)}"
                    f")"
                )

                st.markdown(
                    f"""
                    <div class="function-card">

                    <div class="function-name">
                    🔧 {signature}
                    </div>

                    <div class="muted">
                    Lines {function.get("line", "?")}
                    -
                    {function.get("end_line", "?")}
                    </div>

                    <div class="muted">
                    Arguments:
                    {function.get("argument_count", 0)}
                    &nbsp; • &nbsp;

                    Calls:
                    {len(function.get("calls", []))}
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # -------------------------------------------------
        # CLASSES
        # -------------------------------------------------

        with col2:

            st.subheader(
                "🏛️ Classes"
            )

            if not classes:

                st.info(
                    "No classes detected."
                )

            for cls in classes:

                st.markdown(
                    f"""
                    <div class="function-card">

                    <div class="function-name">
                    🏛️ {cls["name"]}
                    </div>

                    <div class="muted">
                    Lines {cls.get("line", "?")}
                    -
                    {cls.get("end_line", "?")}
                    </div>

                    <div class="muted">
                    Methods:
                    {len(cls.get("methods", []))}
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # =====================================================
    # TAB 2 — DEPENDENCY GRAPH
    # =====================================================

    with tab_graph:

        st.subheader("🕸️ Dependency Graph")

        st.caption(
            "Visual representation of relationships between "
            "functions, classes and methods."
        )

        # -------------------------------------------------
        # GRAPH DATA
        # -------------------------------------------------

        nodes_data = graph_data.get(
            "nodes",
            []
        )

        edges_data = graph_data.get(
            "edges",
            []
        )

        # -------------------------------------------------
        # GRAPH STATISTICS
        # -------------------------------------------------

        graph_col1, graph_col2, graph_col3 = st.columns(3)

        with graph_col1:
            st.metric(
                "Nodes",
                len(nodes_data)
            )

        with graph_col2:
            st.metric(
                "Relationships",
                len(edges_data)
            )

        with graph_col3:

            function_dependencies = sum(
                1
                for edge in edges_data
                if edge.get("type") == "calls"
            )

            st.metric(
                "Function Dependencies",
                function_dependencies
            )

        st.divider()

        # -------------------------------------------------
        # BUILD GRAPHVIZ DOT GRAPH
        # -------------------------------------------------

        dot_lines = []

        dot_lines.append(
            "digraph MergeMind {"
        )

        dot_lines.append(
            'rankdir=TB;'
        )

        dot_lines.append(
            'bgcolor="transparent";'
        )

        dot_lines.append(
            'node [shape=box, style="rounded,filled", '
            'fontname="Arial", fontsize=12];'
        )

        dot_lines.append(
            'edge [fontname="Arial", fontsize=10];'
        )

        # -------------------------------------------------
        # NODE DEFINITIONS
        # -------------------------------------------------

        for node in nodes_data:

            node_id = str(
                node.get("id", "unknown")
            )

            node_type = node.get(
                "type",
                "unknown"
            )

            # Escape characters for DOT
            safe_id = (
                node_id
                .replace("\\", "\\\\")
                .replace('"', '\\"')
            )

            # Display labels
            if node_type == "function":

                label = f"🔧 {node_id}"

            elif node_type == "class":

                label = f"🏛️ {node_id}"

            elif node_type == "method":

                label = f"⚙️ {node_id}"

            elif node_type == "import":

                label = f"📦 {node_id}"

            else:

                label = node_id

            safe_label = (
                label
                .replace("\\", "\\\\")
                .replace('"', '\\"')
            )

            # Different shapes for different code entities
            if node_type == "function":

                shape = "box"

            elif node_type == "class":

                shape = "box"

            elif node_type == "method":

                shape = "ellipse"

            elif node_type == "import":

                shape = "note"

            else:

                shape = "box"

            dot_lines.append(
                f'"{safe_id}" '
                f'[label="{safe_label}", '
                f'shape={shape}];'
            )

        # -------------------------------------------------
        # EDGE DEFINITIONS
        # -------------------------------------------------

        for edge in edges_data:

            source = str(
                edge.get(
                    "source",
                    ""
                )
            )

            target = str(
                edge.get(
                    "target",
                    ""
                )
            )

            edge_type = edge.get(
                "type",
                ""
            )

            safe_source = (
                source
                .replace("\\", "\\\\")
                .replace('"', '\\"')
            )

            safe_target = (
                target
                .replace("\\", "\\\\")
                .replace('"', '\\"')
            )

            safe_edge_type = (
                str(edge_type)
                .replace("\\", "\\\\")
                .replace('"', '\\"')
            )

            dot_lines.append(
                f'"{safe_source}" -> "{safe_target}" '
                f'[label="{safe_edge_type}"];'
            )

        dot_lines.append("}")

        dot_graph = "\n".join(
            dot_lines
        )

        # -------------------------------------------------
        # DISPLAY GRAPH
        # -------------------------------------------------

        if nodes_data:

            st.graphviz_chart(
                dot_graph,
                use_container_width=True
            )

        else:

            st.info(
                "No dependency relationships detected."
            )

        # -------------------------------------------------
        # GRAPH LEGEND
        # -------------------------------------------------

        st.divider()

        st.markdown("### 🧭 Graph Legend")

        legend_col1, legend_col2 = st.columns(2)

        with legend_col1:

            st.markdown(
                """
                **Nodes**

                🔧 Function  
                🏛️ Class  
                ⚙️ Method  
                📦 Import
                """
            )

        with legend_col2:

            st.markdown(
                """
                **Relationships**

                `calls` → Function calls another function

                `contains` → Class contains a method
                """
            )

    # =====================================================
    # TAB 3 — RELATIONSHIPS
    # =====================================================

    with tab_relationships:

        st.subheader(
            "🔗 Function Relationships"
        )

        has_relationship = False


        for function in functions:

            internal_calls = [
                call
                for call in function.get(
                    "calls",
                    []
                )
                if call.get(
                    "is_internal",
                    False
                )
            ]


            if internal_calls:

                has_relationship = True

                st.markdown(
                    f"### 🔧 {function['name']}"
                )

                for call in internal_calls:

                    st.write(
                        f"↳ calls "
                        f"**{call['name']}** "
                        f"at line "
                        f"**{call['line']}**"
                    )


        if not has_relationship:

            st.info(
                "No internal function relationships detected."
            )


        # -------------------------------------------------
        # EXTERNAL CALLS
        # -------------------------------------------------

        st.divider()

        st.subheader(
            "🌐 External / Built-in Calls"
        )

        external_calls = [
            call
            for call in calls
            if not call.get(
                "is_internal",
                False
            )
        ]


        if external_calls:

            for call in external_calls:

                st.write(
                    f"• `{call['name']}` "
                    f"— line {call['line']}"
                )

        else:

            st.info(
                "No external calls detected."
            )


    # =====================================================
    # TAB 4 — FUNCTIONS
    # =====================================================

    with tab_functions:

        st.subheader(
            "⚙️ Detailed Function Analysis"
        )


        if not functions:

            st.info(
                "No functions detected."
            )


        for function in functions:

            with st.expander(
                f"🔧 {function['name']}"
            ):

                # -----------------------------------------
                # LOCATION
                # -----------------------------------------

                st.write(
                    f"**Location:** "
                    f"Lines "
                    f"{function.get('line', '?')} "
                    f"- "
                    f"{function.get('end_line', '?')}"
                )


                # -----------------------------------------
                # ASYNC
                # -----------------------------------------

                st.write(
                    f"**Async Function:** "
                    f"{'Yes' if function.get('is_async') else 'No'}"
                )


                # -----------------------------------------
                # PARAMETERS
                # -----------------------------------------

                st.write(
                    "**Parameters**"
                )

                arguments = function.get(
                    "arguments",
                    []
                )

                if arguments:

                    for argument in arguments:

                        annotation = argument.get(
                            "annotation"
                        )

                        if annotation:

                            st.write(
                                f"- `{argument['name']}` "
                                f"→ `{annotation}`"
                            )

                        else:

                            st.write(
                                f"- `{argument['name']}`"
                            )

                else:

                    st.write(
                        "No parameters."
                    )


                # -----------------------------------------
                # CALLS
                # -----------------------------------------

                st.write(
                    "**Function Calls**"
                )

                function_calls = function.get(
                    "calls",
                    []
                )

                if function_calls:

                    for call in function_calls:

                        call_type = (
                            "Internal"
                            if call.get(
                                "is_internal"
                            )
                            else "External"
                        )

                        st.write(
                            f"- `{call['name']}` "
                            f"— line {call['line']} "
                            f"({call_type})"
                        )

                else:

                    st.write(
                        "No calls detected."
                    )


                # -----------------------------------------
                # RETURNS
                # -----------------------------------------

                st.write(
                    "**Return Statements**"
                )

                function_returns = function.get(
                    "returns",
                    []
                )

                if function_returns:

                    for ret in function_returns:

                        if ret.get(
                            "has_value"
                        ):

                            description = (
                                "returns a value"
                            )

                        else:

                            description = (
                                "empty return"
                            )

                        st.write(
                            f"- Line {ret['line']} "
                            f"→ {description}"
                        )

                else:

                    st.write(
                        "No return statements."
                    )


    # =====================================================
    # TAB 5 — CLASSES
    # =====================================================

    with tab_classes:

        st.subheader(
            "🏛️ Classes & Methods"
        )


        if not classes:

            st.info(
                "No classes detected."
            )


        for cls in classes:

            st.markdown(
                f"### 🏛️ {cls['name']}"
            )

            st.write(
                f"**Location:** "
                f"Lines {cls.get('line', '?')} "
                f"- "
                f"{cls.get('end_line', '?')}"
            )


            methods = cls.get(
                "methods",
                []
            )


            if methods:

                st.write(
                    "**Methods**"
                )

                for method in methods:

                    st.markdown(
                        f"""
                        <div class="function-card">

                        <b>⚙️ {method["name"]}</b>

                        <br>

                        <span class="muted">
                        Lines
                        {method.get("line", "?")}
                        -
                        {method.get("end_line", "?")}
                        </span>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.write(
                    "No methods detected."
                )


    # =====================================================
    # TAB 6 — IMPORTS
    # =====================================================

    with tab_imports:

        st.subheader(
            "📦 Imported Modules"
        )


        if imports:

            for imp in imports:

                if "module" in imp:

                    module = imp.get(
                        "module"
                    )

                    name = imp.get(
                        "name"
                    )

                    full_name = (
                        f"{module}.{name}"
                        if module
                        else name
                    )

                else:

                    full_name = imp.get(
                        "name",
                        "unknown"
                    )


                alias = imp.get(
                    "alias"
                )


                if alias:

                    display_name = (
                        f"{full_name} "
                        f"as {alias}"
                    )

                else:

                    display_name = full_name


                st.markdown(
                    f"""
                    <div class="function-card">

                    📦 <b>{display_name}</b>

                    <br>

                    <span class="muted">
                    Line {imp.get("line", "?")}
                    </span>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "No imports detected."
            )


    # =====================================================
    # TAB 7 — SOURCE CODE
    # =====================================================

    with tab_source:

        st.subheader(
            "📄 Analyzed Source"
        )

        st.caption(
            st.session_state.get(
                "filename",
                "unknown.py"
            )
        )

        st.code(
            st.session_state.get(
                "source_code",
                ""
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

        Paste Python source code above and click
        <b>Analyze Code</b> to generate an interactive
        representation of your code structure.

        </p>

        <p style="color:#9ca3af;">

        MergeMind currently analyzes:

        </p>

        <ul style="color:#9ca3af;">

        <li>Functions</li>
        <li>Classes and methods</li>
        <li>Imports</li>
        <li>Function calls</li>
        <li>Variables</li>
        <li>Assignments</li>
        <li>Conditions</li>
        <li>Loops</li>
        <li>Return statements</li>
        <li>Function dependencies</li>

        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )