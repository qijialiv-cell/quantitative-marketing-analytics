"""
apps/embedding_explorer/app.py
Semantic Similarity Explorer — Research Demo
University of Liverpool | Computational Marketing Research

Deployment: Hugging Face Spaces (Gradio)
Run locally: python app.py
"""

import gradio as gr
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

# Lazy-load the model to avoid blocking startup
_model = None

def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def compute_similarity(text_a: str, text_b: str) -> tuple:
    """
    Compute cosine similarity between two marketing texts.

    Parameters:
        text_a (str): First text (e.g. brand statement).
        text_b (str): Second text (e.g. customer review).

    Returns:
        tuple: (similarity_score_str, interpretation_str)
    """
    model = get_model()
    embs = model.encode([text_a, text_b])
    sim = float(cosine_similarity([embs[0]], [embs[1]])[0, 0])

    if sim > 0.85:
        label = "Very High — nearly identical meaning"
    elif sim > 0.65:
        label = "High — semantically similar"
    elif sim > 0.45:
        label = "Moderate — some overlap in meaning"
    elif sim > 0.25:
        label = "Low — somewhat related"
    else:
        label = "Very Low — unrelated"

    interpretation = (
        f"**Cosine Similarity: {sim:.3f}** — {label}\n\n"
        f"In marketing terms: "
        + ("These texts express closely aligned sentiments or topics." if sim > 0.65
           else "These texts cover different topics or sentiments.")
    )
    return f"{sim:.3f}", interpretation


def embed_and_plot(texts_raw: str) -> plt.Figure:
    """
    Embed a list of texts and plot them in 2D PCA space.

    Parameters:
        texts_raw (str): Newline-separated list of texts (max 20).

    Returns:
        matplotlib Figure
    """
    texts = [t.strip() for t in texts_raw.strip().split("\n") if t.strip()]
    texts = texts[:20]  # cap for performance

    model = get_model()
    embeddings = model.encode(texts)

    n = len(embeddings)
    if n < 2:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Enter at least 2 texts", ha="center", va="center")
        return fig

    pca = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(embeddings)

    fig, ax = plt.subplots(figsize=(9, 6), dpi=130)
    colors = plt.cm.tab10(np.linspace(0, 1, n))

    for i, (text, coord) in enumerate(zip(texts, coords)):
        ax.scatter(coord[0], coord[1], color=colors[i], s=120, zorder=3)
        label = text[:30] + "…" if len(text) > 30 else text
        ax.annotate(label, coord, fontsize=8, xytext=(6, 4), textcoords="offset points")

    ax.set_title("Embedding space — similar meanings appear closer together", fontweight="bold")
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


# ── Default example texts ─────────────────────────────────────────────────────
EXAMPLE_TEXTS = """\
Excellent product, really happy with the quality
Fantastic purchase, would highly recommend
Terrible experience, very disappointed
Product broke after one week, avoid
Love the sustainable brand values
The influencer campaign felt authentic
Average product, nothing special
Fast delivery, good value for money
""".strip()

# ── Gradio interface ──────────────────────────────────────────────────────────
with gr.Blocks(title="Semantic Similarity Explorer | UoL Marketing") as demo:
    gr.Markdown("""
    # Semantic Similarity Explorer
    **University of Liverpool | Computational Marketing Research**

    Explore how transformer-based text embeddings capture meaning in marketing text.
    Built on `sentence-transformers` (`all-MiniLM-L6-v2`).
    """)

    with gr.Tab("Pairwise Similarity"):
        gr.Markdown("Compare two marketing texts and measure how semantically similar they are.")
        with gr.Row():
            text_a = gr.Textbox(label="Text A (e.g. brand statement)", lines=3,
                                placeholder="We are committed to sustainable, ethical sourcing.")
            text_b = gr.Textbox(label="Text B (e.g. customer review)", lines=3,
                                placeholder="Love that this brand cares about the environment.")
        btn_sim = gr.Button("Compute Similarity", variant="primary")
        score_out = gr.Textbox(label="Similarity Score")
        interp_out = gr.Markdown()
        btn_sim.click(compute_similarity, inputs=[text_a, text_b], outputs=[score_out, interp_out])

    with gr.Tab("Embedding Space Visualiser"):
        gr.Markdown(
            "Enter one text per line (max 20). "
            "The plot shows how texts cluster in semantic space."
        )
        texts_in = gr.Textbox(label="Texts (one per line)", lines=10, value=EXAMPLE_TEXTS)
        btn_plot = gr.Button("Visualise Embeddings", variant="primary")
        plot_out = gr.Plot(label="PCA of embedding space")
        btn_plot.click(embed_and_plot, inputs=[texts_in], outputs=[plot_out])

    gr.Markdown("""
    ---
    **Interpretation guide:**
    - Points that appear *close together* share similar meanings
    - Points that appear *far apart* have different meanings
    - This is computed purely from the text — no keyword matching

    **Deployment:** Hugging Face Spaces | [GitHub](https://github.com)
    """)


if __name__ == "__main__":
    demo.launch()
