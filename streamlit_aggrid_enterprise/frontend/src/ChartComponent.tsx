// src/components/ChartComponent.tsx
import dayjs from 'dayjs';
import React, { useEffect, useMemo, useState } from 'react';
import { AgCharts } from 'ag-charts-react';

type ChartDataPoint = {
  name: string;
  units: number;
  offtake: number;
  asp: number;
};

type ChartComponentProps = {
  rowData: any[];
  nameKey?: string; // Optional name/label key (e.g., 'sku', 'product')
};

const ChartComponent: React.FC<ChartComponentProps> = ({ rowData, nameKey = 'sku' }) => {
  const [chartData, setChartData] = useState<ChartDataPoint[]>([]);

  useEffect(() => {
    if (rowData?.length > 0) {
      const transformed = rowData.map((row) => ({
        valuationdate: row.valuationdate
        ? dayjs(Number(row.valuationdate)).format('YYYY-MM-DD')
        : 'N/A',
        name: row[nameKey] || row.name || 'N/A',
        units: Number(row.units) || 0,
        offtake: Number(row.offtake) || 0,
        asp: Number(row.asp) || 0,
      }));
      setChartData(transformed);
    }
  }, [rowData, nameKey]);

  const chartOptions = useMemo(() => ({
    title: {
      text: 'Units, Offtake, and ASP over Time',
      fontSize: 18,
    },
    data: chartData,
    series: [{
        type: 'bar',
        xKey: 'valuationdate',
        yKey: 'units',
        yName: 'Units',
        yAxisKey: 'leftAxis',
        fill: '#2196f3',
        tooltip: {
          renderer: ({ datum }) => ({ content: `Units: ${datum.units}` }),
        },
      },
      {
        type: 'bar',
        xKey: 'valuationdate',
        yKey: 'offtake',
        yName: 'Offtake',
        yAxisKey: 'leftAxis',
        fill: '#66bb6a',
        tooltip: {
          renderer: ({ datum }) => ({ content: `Offtake: ${datum.offtake}` }),
        },
      },
      {
        type: 'line',
        xKey: 'valuationdate',
        yKey: 'asp',
        yName: 'ASP (₹)',
        yAxisKey: 'rightAxis',
        stroke: '#ef5350',
        marker: { enabled: true },
        tooltip: {
          renderer: ({ datum }) => ({ content: `ASP: ₹${datum.asp}` }),
        },
      },
    ],

    axes: [
  {
    type: 'category',
    position: 'bottom',
    title: { text: 'Valuation Date' },
    label: {
      rotation: 45,
    },
  },
  {
    type: 'number',
    key: 'leftAxis',
    position: 'left',
    title: { text: 'Units & Offtake' },
  },
  {
    type: 'number',
    key: 'rightAxis',
    position: 'right',
    title: { text: 'ASP (₹)' },
  },
],

    legend: {
      position: 'bottom',
      item: { marker: { shape: 'circle' } },
    },
    padding: { top: 20, bottom: 40 },
  }), [chartData]);

  return (
    <div style={{ height: 1000, width: '100%', marginTop: '2rem' }}>
      <AgCharts options={chartOptions} />
    </div>
  );
};

export default ChartComponent;
