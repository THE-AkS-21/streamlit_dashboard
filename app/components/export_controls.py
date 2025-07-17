import streamlit as st
import pandas as pd
import io
import base64
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def export_controls(df: pd.DataFrame, file_prefix: str = "exported_data", export_type: str = "CSV"):
    """
    Returns export content and metadata for custom trigger-based download.

    Args:
        df (pd.DataFrame): The DataFrame to export.
        file_prefix (str): Base filename (without extension).
        export_type (str): One of 'CSV', 'Excel', 'PDF', 'PNG'.

    Returns:
        Tuple[str, bytes, str, str]: filename, file content, mime type, HTML download link (if applicable)
    """
    if df.empty:
        st.warning("⚠️ No data to export.")
        return None

    file_name = f"{file_prefix}.{export_type.lower()}"
    content = None
    mime = None
    download_html = ""

    if export_type == "CSV":
        content = df.to_csv(index=False).encode()
        mime = "text/csv"

    elif export_type == "Excel":
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Data")
        content = buffer.getvalue()
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    elif export_type == "PDF":
        buffer = io.BytesIO()
        with PdfPages(buffer) as pdf:
            fig, ax = plt.subplots(figsize=(min(18, len(df.columns) * 1.2), min(12, len(df) * 0.4 + 1)))
            ax.axis('tight')
            ax.axis('off')
            table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1, 1.2)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
        content = buffer.getvalue()
        mime = "application/pdf"

    elif export_type == "PNG":
        fig, ax = plt.subplots(figsize=(min(18, len(df.columns) * 1.2), min(12, len(df) * 0.4 + 1)))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 1.2)

        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", bbox_inches="tight", dpi=300)
        plt.close(fig)
        content = buffer.getvalue()
        mime = "image/png"

    # Base64 download HTML link for PNG or fallback
    if content and export_type == "PNG":
        b64 = base64.b64encode(content).decode()
        download_html = f'<a href="data:{mime};base64,{b64}" download="{file_name}">🖼️ Download PNG</a>'

    return file_name, content, mime, download_html
