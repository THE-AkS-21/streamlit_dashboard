import streamlit as st
import pandas as pd
import io
import base64
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def export_controls(df: pd.DataFrame, file_prefix: str = "exported_data", export_type: str = "CSV"):
    """
    Export DataFrame in selected format.

    Args:
        df (pd.DataFrame): The filtered DataFrame to export.
        file_prefix (str): Base name for exported files.
        export_type (str): Export format - CSV, Excel, PDF, PNG.
    """
    if df.empty:
        st.warning("⚠️ No data to export.")
        return

    if export_type == "CSV":
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download CSV",
            data=csv_buffer.getvalue(),
            file_name=f"{file_prefix}.csv",
            mime="text/csv",
            use_container_width=True
        )

    elif export_type == "Excel":
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Data")
        st.download_button(
            label="Download Excel",
            data=excel_buffer.getvalue(),
            file_name=f"{file_prefix}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    elif export_type == "PDF":
        pdf_buffer = io.BytesIO()
        with PdfPages(pdf_buffer) as pdf:
            fig, ax = plt.subplots(figsize=(min(18, len(df.columns) * 1.2), min(12, len(df) * 0.4 + 1)))
            ax.axis('tight')
            ax.axis('off')
            table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1, 1.2)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
        st.download_button(
            label="Download PDF",
            data=pdf_buffer.getvalue(),
            file_name=f"{file_prefix}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    elif export_type == "PNG":
        fig, ax = plt.subplots(figsize=(min(18, len(df.columns) * 1.2), min(12, len(df) * 0.4 + 1)))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 1.2)

        png_buffer = io.BytesIO()
        fig.savefig(png_buffer, format="png", bbox_inches="tight", dpi=300)
        plt.close(fig)

        b64 = base64.b64encode(png_buffer.getvalue()).decode()
        href = f'<a href="data:image/png;base64,{b64}" download="{file_prefix}.png">🖼️ Download PNG</a>'
        st.markdown(href, unsafe_allow_html=True)
