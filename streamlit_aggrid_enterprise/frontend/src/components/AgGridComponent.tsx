import React, { useRef, useMemo } from "react";
import { AgGridReact } from "ag-grid-react";
import { ModuleRegistry } from "ag-grid-community";
import { IntegratedChartsModule } from "ag-grid-enterprise";
import { AgChartsEnterpriseModule } from "ag-charts-enterprise";



import "ag-grid-enterprise";
import "ag-grid-community/styles/ag-grid.css";
// import "ag-grid-community/styles/ag-theme-alpine.css";
// import "ag-grid-community/styles/ag-theme-quartz.css"; // Uncomment if you prefer Quartz

// Register AG Grid modules
ModuleRegistry.registerModules([
  IntegratedChartsModule.with(AgChartsEnterpriseModule),
]);

const AgGridApp = () => {
  const gridRef = useRef(null);

  const rowData = window.gridData || [];

  const columnDefs = useMemo(() => {
    if (rowData.length === 0) return [];

    return Object.keys(rowData[0]).map((key) => {
      const base = {
        field: key,
        sortable: true,
        resizable: true,
        filter: true,
        editable: false,
        minWidth: 120,
      };

      const lowerKey = key.toLowerCase();

      // CM2 Percentage Column
      if (lowerKey === "cm2percentage") {
        return {
          ...base,
          headerName: "CM2 %",
          cellStyle: percentageColorStyle([25, 20, 15, 10, 5], [
            "#006400",
            "#228B22",
            "#32CD32",
            "#FFA500",
            "#FF4C4C",
            "#8B0000",
          ]),
          cellRenderer: trendRenderer([25, 20, 15, 10, 5], ["★", "⬆", "↗", "➡", "↘", "⬇"]),
        };
      }

      // CM1 Percentage Column
      if (lowerKey === "cm1percentage") {
        return {
          ...base,
          headerName: "CM1 %",
          cellStyle: percentageColorStyle([50, 45, 40, 35, 30], [
            "#006400",
            "#228B22",
            "#32CD32",
            "#FFA500",
            "#FF4C4C",
            "#8B0000",
          ]),
          cellRenderer: trendRenderer([50, 45, 40, 35, 25], ["★", "⬆", "↗", "➡", "↘", "⬇"]),
        };
      }

      // GMGP Percentage Column
      if (lowerKey === "gmgppercentage") {
        return {
          ...base,
          headerName: "GMGP %",
          cellStyle: percentageColorStyle([55, 50, 45, 40, 35], [
            "#006400",
            "#228B22",
            "#32CD32",
            "#FFA500",
            "#FF4C4C",
            "#8B0000",
          ]),
          cellRenderer: trendRenderer([55, 50, 45, 40, 30], ["★", "⬆", "↗", "➡", "↘", "⬇"]),
        };
      }

      // Valuation Date
      if (lowerKey === "valuationdate") {
        return {
          ...base,
          valueFormatter: (params) => {
            const date = new Date(Number(params.value));
            return isNaN(date.getTime()) ? "Invalid Date" : date.toLocaleDateString("en-US", {
              year: "numeric",
              month: "short",
              day: "numeric",
            });
          },
          headerClass: "ag-header-bold",
        };
      }


      return {
        ...base,
        headerName: formatHeader(key),
      };
    });
  }, [rowData]);

  return (
    <div className="ag-theme-alpine" style={{ height: 600, width: "100%" }}>
      <AgGridReact
        ref={gridRef}
        rowData={rowData}
        columnDefs={columnDefs}
        defaultColDef={{
          editable: true,
          sortable: true,
          resizable: true,
          filter: true,
          enableRowGroup: true,
          enableValue: true,
          suppressHeaderMenuButton: true
        }}
        enableCharts={true}
        cellSelection={true}
        animateRows={true}
        suppressAggFuncInHeader={true}
        pagination={true}
        paginationPageSize={50}
        rowGroupPanelShow="always"
        pivotPanelShow="collapsed"
        sideBar={{
          toolPanels: [
            {
              id: "columns",
              labelDefault: "Columns",
              toolPanel: "agColumnsToolPanel",
            },
            {
              id: "filters",
              labelDefault: "Filters",
              toolPanel: "agFiltersToolPanel",
            },
          ],
          defaultToolPanel: "columns",
        }}
        popupParent={document.body}
      />
    </div>
  );
};

export default AgGridApp;

// ────── Utility Functions ──────

function percentageColorStyle(thresholds: number[], colors: string[]) {
  return (params) => {
    const val = params.value;
    for (let i = 0; i < thresholds.length; i++) {
      if (val >= thresholds[i]) {
        return { fontWeight: "bold", color: colors[i] };
      }
    }
    return { fontWeight: "bold", color: colors[colors.length - 1] };
  };
}

function trendRenderer(thresholds: number[], symbols: string[]) {
  return (params) => {
    const val = params.value;
    for (let i = 0; i < thresholds.length; i++) {
      if (val >= thresholds[i]) {
        return `${symbols[i]} ${val}%`;
      }
    }
    return `${symbols[symbols.length - 1]} ${val}%`;
  };
}

function formatHeader(key: string) {
  if (key.toLowerCase().endsWith("percentage")) {
    return key.slice(0, -10).replace(/_/g, " ").trim().toUpperCase() + " %";
  }
  return key.replace(/_/g, " ").trim().toUpperCase();
}
