import streamlit as st
import plotly.express as px
import plotly.subplots as sp
from streamlit_plotly_events import plotly_events
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="clones2cells web-viewer",
    page_icon="🔬",
    layout="wide",
)

locations = {
    "Control": {
        "Trunk": {
            "clone2vec": "clone2vec_control_trunk.csv",
            "All cells": "GEX_control_trunk_all.csv",
            "Neurons": "GEX_control_trunk_neurons.csv",
            "Mesenchyme": "GEX_control_trunk_mesenchyme.csv",
            "Other cells": "GEX_control_trunk_other.csv",
            "NC-derived cells": "GEX_control_trunk_NC.csv",
        },
        "Head": {
            "clone2vec": "clone2vec_control_head.csv",
            "All cells": "GEX_control_head_all.csv",
            "Neurons": "GEX_control_head_neurons.csv",
            "Mesenchyme": "GEX_control_head_mesenchyme.csv",
            "Other cells": "GEX_control_head_other.csv",
        },
    },
    "Perturbed and control": {
        "Trunk": {
            "clone2vec": "clone2vec_perturbed_trunk.csv",
            "All cells": "GEX_perturbed_trunk_all.csv",
            "Neurons": "GEX_perturbed_trunk_neurons.csv",
            "Mesenchyme": "GEX_perturbed_trunk_mesenchyme.csv",
            "Other cells": "GEX_perturbed_trunk_other.csv",
            "NC-derived cells": "GEX_perturbed_trunk_NC.csv",
        },
        "Head": {
            "clone2vec": "clone2vec_perturbed_head.csv",
            "All cells": "GEX_perturbed_head_all.csv",
            "Neurons": "GEX_perturbed_head_neurons.csv",
            "Mesenchyme": "GEX_perturbed_head_mesenchyme.csv",
            "Other cells": "GEX_perturbed_head_other.csv",
        },
    }
}

st.markdown("""
# *clones2cells* web-viewer

Supplementary web-application (*Erickson, Isaev et al.*) showing cells from different clones (and groups of clones) on gene expression embeddings.
Also here you can find links for the data download (.h5ad-containers) and CellxGene web-viewer so you can perform differential
expression analysis or any further statisctical testing.

**It's highly recommended to use Google Chrome or Mozilla Firefox, the app might be displayed incorrectly in other
browsers.**
""")

col1_0, col2_0 = st.columns(2)

with col1_0:
    perturbed = st.selectbox(
        "Which type of the data you want to analyse?",
        ("Control", "Perturbed and control"),
        index=None,
        placeholder="Select the dataset..."
    )

with col2_0:
    region = st.selectbox(
        "Which body region you want to analyse?",
        ("Trunk", "Head"),
        index=None,
        placeholder="Select the region...",
    )

if not ((perturbed is None) or (region is None)):

    col1_1, col2_1 = st.columns(2)

    with col1_1: 
        res = st.selectbox(
            "Please select the resolution of the clone2vec clusters",
            ("0.5", "1", "2")
        )

    with col2_1:
        if region == "Head":
            options = ("All cells", "Mesenchyme", "Neurons", "Other cells")
        else:
            options = ("All cells", "Mesenchyme", "Neurons", "NC-derived cells", "Other cells")
        embedding = st.selectbox(
            "Please select embedding of interest",
            options,
        )

    df_clone2vec = pd.read_csv(f"data/{locations[perturbed][region]['clone2vec']}", index_col=0)
    df_GEX = pd.read_csv(f"data/{locations[perturbed][region][embedding]}", index_col=0)

    leiden = f"leiden_{res}"

    if perturbed == "Control":
        annotation = (
            np.array(df_clone2vec.index) +
            " (Cluster " +
            np.array(df_clone2vec[leiden], dtype="str") + ")"
        )
    else:
        annotation = np.array(df_clone2vec["perturbation"], dtype="str")
        annotation[annotation == "nan"] = "w/o"
        annotation = (
            np.array(df_clone2vec.index) + " (" + annotation + " gRNA)"
        )

    col1_2, col2_2 = st.columns(2)
    with col1_2:
        col_but1_left, col_but2_left = st.columns(2)
        with col_but1_left:
            st.button("Download .h5ad-file (clonal)", use_container_width=True)
        with col_but2_left:
            st.button("Open in CellxGene viewer (clonal)", use_container_width=True)

        clone2vec_ax = px.scatter(
            df_clone2vec,
            x="UMAP1",
            y="UMAP2",
            title="<b>clone2vec UMAP</b>",
            height=600,
            width=700,
            color=leiden,
            color_continuous_scale="rainbow",
            text=annotation,
            #hover_data={"UMAP1": False, "UMAP2": False, "leiden_2": True}
        )

        clone2vec_ax.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            hovermode="closest",
        )

        clone2vec_ax.update_traces(
            marker={"size": 7},
            mode="markers",
            hovertemplate="%{text}",
        )

        clone2vec_ax.update_layout(
            title_x=0.45,
            title={"font": {"family": "Arial", "size": 18}},
        )

        clone2vec_ax.update(layout_coloraxis_showscale=False)

        selected_points = plotly_events(
            clone2vec_ax,
            click_event=True,
            select_event=True,
            hover_event=False,
            override_height=600,
        )

    with col2_2:
        col_but1_right, col_but2_right = st.columns(2)
        with col_but1_right:
            st.button("Download .h5ad-file (gene expression)", use_container_width=True)
        with col_but2_right:
            st.button("Open in CellxGene viewer (gene expression)", use_container_width=True)

        if len(selected_points) == 0:
            if perturbed == "Control":
                color = "celltype_l0"
                legend_title = "Cell type domain"
            else:
                color = "gRNA"
                legend_title = "gRNA"
            GEX_ax = px.scatter(
                df_GEX,
                x="UMAP1",
                y="UMAP2",
                title="Gene expression UMAP",
                height=600,
                width=600,
                text=df_GEX["celltype_l1"],
                color=color,
            )

            GEX_ax.update_traces(
                marker={"size": 3},
                mode="markers",
                hovertemplate="%{text}",
            )

            GEX_ax.update_layout(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                hovermode="closest",
            )

            GEX_ax.update_layout(
                title_x=0.45,
                title_y=0.93,
                title={"font": {"family": "Arial", "size": 18}},
                legend={"title": legend_title},
            )

            st.plotly_chart(GEX_ax)
        else:
            selected_points = [point["pointNumber"] for point in selected_points]
            selected_points = np.array(df_clone2vec.index[selected_points])
            selected_points = df_GEX.clone.isin(selected_points)
            df_GEX["selected"] = ["Selected" if i else "Other" for i in selected_points]
            df_GEX["size"] = [3 if i else 1 for i in selected_points]
            
            GEX_ax = px.scatter(
                df_GEX,
                x="UMAP1",
                y="UMAP2",
                title="Gene expression UMAP",
                height=600,
                width=600,
                text=df_GEX["celltype_l1"],
                color="selected",
                size="size",
                size_max=6,
                color_discrete_sequence=["lightgray", "black"],
                category_orders={"selected": ["Other", "Selected"]}
            )

            GEX_ax.update_traces(
                mode="markers",
                hovertemplate="%{text}",
                marker={"line": {"width": 0}}
            )

            GEX_ax.update_layout(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                hovermode="closest",
            )

            GEX_ax.update_layout(
                title_x=0.45,
                title_y=0.93,
                title={"font": {"family": "Arial", "size": 18}},
                legend={"title": "Selection"},
            )

            st.plotly_chart(GEX_ax)