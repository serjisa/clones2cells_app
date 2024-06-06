# clones2cells

Simple Streamlit application for interactive exploratory analysis of clonal embeddings.

## How to use it

To run *clones2cells* locally, firstly, install dependencies:

```bash
pip install streamlit plotly streamlit_plotly_events pandas
```

After that, run the following command from the terminal:

```bash
streamlit run https://raw.githubusercontent.com/serjisa/clones2cells_app/main/clones2cells_viewer.py
```

Streamlit clones2cells app should be opened after that — and here you will be able to select files that you got from `prepare_clones2cells` function from `scLiTr` package (one file for clonal embedding and one file for gene expression embedding).
