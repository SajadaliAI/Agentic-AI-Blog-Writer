from __future__ import annotations

import json
import os
import re
import zipfile
from datetime import date
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Optional, List, Iterator, Tuple

import pandas as pd
import streamlit as st

# -----------------------------
# Import your compiled LangGraph app
# -----------------------------
from bwa_backend import app

# -----------------------------
# Page Configuration & Advanced CSS Injection
# -----------------------------
st.set_page_config(
    page_title="AI Studio | Next-Gen Content Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom SaaS Dark Theme CSS
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Base Typography & Background */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: #090d16;
        color: #e2e8f0;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 95%;
    }

    /* Glassmorphic Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 28px 36px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(16px);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #818cf8, #c084fc, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.98rem;
        font-weight: 400;
    }

    /* Premium Metric Grid Cards */
    .metric-grid-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 16px 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        transition: all 0.25s ease;
    }
    .metric-grid-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }
    .metric-grid-label {
        font-size: 0.75rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .metric-grid-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f8fafc;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        color: #94a3b8;
        border: none !important;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4);
    }

    /* Button Enhancements */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        border: none;
        color: white;
        font-weight: 700;
        border-radius: 12px;
        padding: 0.65rem 1.2rem;
        box-shadow: 0 4px 18px rgba(99, 102, 241, 0.35);
        transition: all 0.25s ease;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 22px rgba(99, 102, 241, 0.55);
        transform: translateY(-2px);
    }

    /* Code & Log Box Styling */
    .stTextArea textarea {
        background-color: #0b0f19 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #38bdfe !important;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Inputs Styling */
    .stTextInput input, .stSelectbox select, .stDateInput input {
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        background: #0f172a !important;
        color: #f1f5f9 !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# -----------------------------
# Helpers
# -----------------------------
def safe_slug(title: str) -> str:
    s = title.strip().lower()
    s = re.sub(r"[^a-z0-9 _-]+", "", s)
    s = re.sub(r"\s+", "_", s).strip("_")
    return s or "blog"


def bundle_zip(md_text: str, md_filename: str, images_dir: Path) -> bytes:
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr(md_filename, md_text.encode("utf-8"))

        if images_dir.exists() and images_dir.is_dir():
            for p in images_dir.rglob("*"):
                if p.is_file():
                    z.write(p, arcname=str(p))
    return buf.getvalue()


def images_zip(images_dir: Path) -> Optional[bytes]:
    if not images_dir.exists() or not images_dir.is_dir():
        return None
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in images_dir.rglob("*"):
            if p.is_file():
                z.write(p, arcname=str(p))
    return buf.getvalue()


def try_stream(graph_app, inputs: Dict[str, Any]) -> Iterator[Tuple[str, Any]]:
    try:
        for step in graph_app.stream(inputs, stream_mode="updates"):
            yield ("updates", step)
        out = graph_app.invoke(inputs)
        yield ("final", out)
        return
    except Exception:
        pass

    try:
        for step in graph_app.stream(inputs, stream_mode="values"):
            yield ("values", step)
        out = graph_app.invoke(inputs)
        yield ("final", out)
        return
    except Exception:
        pass

    out = graph_app.invoke(inputs)
    yield ("final", out)


def extract_latest_state(current_state: Dict[str, Any], step_payload: Any) -> Dict[str, Any]:
    if isinstance(step_payload, dict):
        if len(step_payload) == 1 and isinstance(next(iter(step_payload.values())), dict):
            inner = next(iter(step_payload.values()))
            current_state.update(inner)
        else:
            current_state.update(step_payload)
    return current_state


# -----------------------------
# Markdown renderer with local image support
# -----------------------------
_MD_IMG_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)]+)\)")
_CAPTION_LINE_RE = re.compile(r"^\*(?P<cap>.+)\*$")


def _resolve_image_path(src: str) -> Path:
    src = src.strip().lstrip("./")
    return Path(src).resolve()


def render_markdown_with_local_images(md: str):
    matches = list(_MD_IMG_RE.finditer(md))
    if not matches:
        st.markdown(md, unsafe_allow_html=False)
        return

    parts: List[Tuple[str, str]] = []
    last = 0
    for m in matches:
        before = md[last : m.start()]
        if before:
            parts.append(("md", before))

        alt = (m.group("alt") or "").strip()
        src = (m.group("src") or "").strip()
        parts.append(("img", f"{alt}|||{src}"))
        last = m.end()

    tail = md[last:]
    if tail:
        parts.append(("md", tail))

    i = 0
    while i < len(parts):
        kind, payload = parts[i]

        if kind == "md":
            st.markdown(payload, unsafe_allow_html=False)
            i += 1
            continue

        alt, src = payload.split("|||", 1)

        caption = None
        if i + 1 < len(parts) and parts[i + 1][0] == "md":
            nxt = parts[i + 1][1].lstrip()
            if nxt.strip():
                first_line = nxt.splitlines()[0].strip()
                mcap = _CAPTION_LINE_RE.match(first_line)
                if mcap:
                    caption = mcap.group("cap").strip()
                    rest = "\n".join(nxt.splitlines()[1:])
                    parts[i + 1] = ("md", rest)

        if src.startswith("http://") or src.startswith("https://"):
            st.image(src, caption=caption or (alt or None), width="stretch")
        else:
            img_path = _resolve_image_path(src)
            if img_path.exists():
                st.image(str(img_path), caption=caption or (alt or None), width="stretch")
            else:
                st.warning(f"Image not found: `{src}` (looked for `{img_path}`)")

        i += 1


# -----------------------------
# Past blogs helpers
# -----------------------------
def list_past_blogs() -> List[Path]:
    cwd = Path(".")
    files = [p for p in cwd.glob("*.md") if p.is_file()]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files


def read_md_file(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def extract_title_from_md(md: str, fallback: str) -> str:
    for line in md.splitlines():
        if line.startswith("# "):
            t = line[2:].strip()
            return t or fallback
    return fallback


# -----------------------------
# Header Hero Section
# -----------------------------
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-title">🔮 Autonomous Blog Studio</div>
        <div class="hero-subtitle">Multi-Agent Content Strategy & High-Impact Writing Powered by LangGraph</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar Configuration
# -----------------------------
with st.sidebar:
    st.markdown("### ✍️ Prompt & Strategy")
    topic = st.text_area(
        "Article Topic / Key Focus",
        height=110,
        placeholder="Enter your blog idea or research topic...",
    )
    as_of = st.date_input("Knowledge Cutoff / As-of Date", value=date.today())
    
    st.write("")
    run_btn = st.button("🚀 Launch Generator", type="primary", width="stretch")

    st.divider()
    st.markdown("### 📚 Saved History")

    past_files = list_past_blogs()
    if not past_files:
        st.caption("No saved `.md` articles found.")
        selected_md_file = None
    else:
        options: List[str] = []
        file_by_label: Dict[str, Path] = {}
        for p in past_files[:50]:
            try:
                md_text = read_md_file(p)
                title = extract_title_from_md(md_text, p.stem)
            except Exception:
                title = p.stem
            label = f"📄 {title}"
            options.append(label)
            file_by_label[label] = p

        selected_label = st.selectbox(
            "Select past blog:",
            options=options,
            label_visibility="collapsed",
        )
        selected_md_file = file_by_label.get(selected_label)
        if st.button("📂 Load Selected File", width="stretch"):
            if selected_md_file:
                md_text = read_md_file(selected_md_file)
                st.session_state["last_out"] = {
                    "plan": None,
                    "evidence": [],
                    "image_specs": [],
                    "final": md_text,
                }
                st.toast("Article loaded to workspace!", icon="⚡")

if "last_out" not in st.session_state:
    st.session_state["last_out"] = None

# -----------------------------
# Main Navigation Tabs
# -----------------------------
tab_plan, tab_evidence, tab_preview, tab_images, tab_logs = st.tabs(
    ["📊 Content Blueprint", "🔎 Fact Research", "📝 Article Preview", "🎨 Visual Assets", "📟 Graph Logs"]
)

logs: List[str] = []

def log(msg: str):
    logs.append(msg)

# Streamlit Generation Execution
if run_btn:
    if not topic.strip():
        st.warning("⚠️ Please provide a blog topic to proceed.")
        st.stop()

    inputs: Dict[str, Any] = {
        "topic": topic.strip(),
        "mode": "",
        "needs_research": False,
        "queries": [],
        "evidence": [],
        "plan": None,
        "as_of": as_of.isoformat(),
        "recency_days": 7,
        "sections": [],
        "merged_md": "",
        "md_with_placeholders": "",
        "image_specs": [],
        "final": "",
    }

    status = st.status("🔮 Agents are orchestrating content...", expanded=True)
    progress_area = st.empty()

    current_state: Dict[str, Any] = {}
    last_node = None

    for kind, payload in try_stream(app, inputs):
        if kind in ("updates", "values"):
            node_name = None
            if isinstance(payload, dict) and len(payload) == 1 and isinstance(next(iter(payload.values())), dict):
                node_name = next(iter(payload.keys()))
            if node_name and node_name != last_node:
                status.write(f"⚡ **Executing Node:** `{node_name}`")
                last_node = node_name

            current_state = extract_latest_state(current_state, payload)

            summary = {
                "mode": current_state.get("mode"),
                "needs_research": current_state.get("needs_research"),
                "queries": current_state.get("queries", [])[:5] if isinstance(current_state.get("queries"), list) else [],
                "evidence_count": len(current_state.get("evidence", []) or []),
                "tasks": len((current_state.get("plan") or {}).get("tasks", [])) if isinstance(current_state.get("plan"), dict) else None,
                "images": len(current_state.get("image_specs", []) or []),
                "sections_done": len(current_state.get("sections", []) or []),
            }
            progress_area.json(summary)
            log(f"[{kind}] {json.dumps(payload, default=str)[:1200]}")

        elif kind == "final":
            out = payload
            st.session_state["last_out"] = out
            status.update(label="✨ Content Orchestration Complete!", state="complete", expanded=False)
            log("[final] process finished")

# -----------------------------
# Workspace Views
# -----------------------------
out = st.session_state.get("last_out")
if out:
    # --- 1. Content Blueprint ---
    with tab_plan:
        plan_obj = out.get("plan")
        if not plan_obj:
            st.info("No structural plan available for this article.")
        else:
            if hasattr(plan_obj, "model_dump"):
                plan_dict = plan_obj.model_dump()
            elif isinstance(plan_obj, dict):
                plan_dict = plan_obj
            else:
                plan_dict = json.loads(json.dumps(plan_obj, default=str))

            st.markdown(f"#### 📌 Draft Title: *{plan_dict.get('blog_title')}*")
            st.write("")

            # Metric Cards
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(
                    f"""<div class="metric-grid-card">
                        <div class="metric-grid-label">Target Audience</div>
                        <div class="metric-grid-value">{plan_dict.get("audience", "General")}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f"""<div class="metric-grid-card">
                        <div class="metric-grid-label">Content Tone</div>
                        <div class="metric-grid-value">{plan_dict.get("tone", "Professional")}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            with c3:
                st.markdown(
                    f"""<div class="metric-grid-card">
                        <div class="metric-grid-label">Format Style</div>
                        <div class="metric-grid-value">{plan_dict.get("blog_kind", "Technical Blog")}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

            st.write("")
            st.markdown("##### 📋 Article Outline & Subtasks")
            tasks = plan_dict.get("tasks", [])
            if tasks:
                df = pd.DataFrame(
                    [
                        {
                            "ID": t.get("id"),
                            "Section Title": t.get("title"),
                            "Target Words": t.get("target_words"),
                            "Research": "✅ Yes" if t.get("requires_research") else "❌ No",
                            "Citations": "✅ Yes" if t.get("requires_citations") else "❌ No",
                            "Code Snippets": "✅ Yes" if t.get("requires_code") else "❌ No",
                            "Tags": ", ".join(t.get("tags") or []),
                        }
                        for t in tasks
                    ]
                ).sort_values("ID")
                st.dataframe(df, width="stretch", hide_index=True)

                with st.expander("🛠️ View Complete Plan Schema JSON"):
                    st.json(tasks)

    # --- 2. Fact Research ---
    with tab_evidence:
        st.markdown("### 🔎 Verified Web Sources & Citations")
        evidence = out.get("evidence") or []
        if not evidence:
            st.info("No external evidence gathered (or closed-book mode).")
        else:
            rows = []
            for e in evidence:
                if hasattr(e, "model_dump"):
                    e = e.model_dump()
                rows.append(
                    {
                        "Resource Title": e.get("title"),
                        "Published Date": e.get("published_at"),
                        "Domain/Source": e.get("source"),
                        "URL Link": e.get("url"),
                    }
                )
            st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

    # --- 3. Article Preview ---
    with tab_preview:
        final_md = out.get("final") or ""
        if not final_md:
            st.warning("No markdown draft ready.")
        else:
            plan_obj = out.get("plan")
            if hasattr(plan_obj, "blog_title"):
                blog_title = plan_obj.blog_title
            elif isinstance(plan_obj, dict):
                blog_title = plan_obj.get("blog_title", "blog")
            else:
                blog_title = extract_title_from_md(final_md, "blog")

            md_filename = f"{safe_slug(blog_title)}.md"
            bundle = bundle_zip(final_md, md_filename, Path("images"))

            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button(
                    "⬇️ Download Raw Markdown (.md)",
                    data=final_md.encode("utf-8"),
                    file_name=md_filename,
                    mime="text/markdown",
                    width="stretch",
                )
            with col_b:
                st.download_button(
                    "📦 Download Zip Archive (MD + Assets)",
                    data=bundle,
                    file_name=f"{safe_slug(blog_title)}_bundle.zip",
                    mime="application/zip",
                    width="stretch",
                )

            st.divider()
            render_markdown_with_local_images(final_md)

    # --- 4. Visual Assets ---
    with tab_images:
        st.markdown("### 🖼️ Generated Media & Placeholders")
        specs = out.get("image_specs") or []
        images_dir = Path("images")

        if not specs and not images_dir.exists():
            st.info("No images generated for this blog post.")
        else:
            if specs:
                st.markdown("**Image Specifications & Prompts:**")
                st.json(specs)

            if images_dir.exists():
                files = [p for p in images_dir.iterdir() if p.is_file()]
                if not files:
                    st.warning("Image directory exists but is empty.")
                else:
                    cols = st.columns(2)
                    for idx, p in enumerate(sorted(files)):
                        with cols[idx % 2]:
                            st.image(str(p), caption=p.name, width="stretch")

                z = images_zip(images_dir)
                if z:
                    st.download_button(
                        "⬇️ Download Image Assets (.zip)",
                        data=z,
                        file_name="images.zip",
                        mime="application/zip",
                        width="stretch",
                    )

    # --- 5. System Logs ---
    with tab_logs:
        st.markdown("### 📟 Stream & Graph Logs")
        if "logs" not in st.session_state:
            st.session_state["logs"] = []
        if logs:
            st.session_state["logs"].extend(logs)

        st.text_area(
            "Graph Telemetry",
            value="\n\n".join(st.session_state["logs"][-80:]),
            height=480,
            disabled=True,
        )
else:
    st.info("💡 Enter your blog focus topic in the sidebar and press **Launch Generator** to start.")    