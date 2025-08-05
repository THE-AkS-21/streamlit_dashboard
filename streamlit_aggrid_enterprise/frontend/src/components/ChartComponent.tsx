// src/ChartApp.tsx
import React, { useEffect, useMemo, useState } from 'react';
import { AgCharts } from 'ag-charts-react';
import { AgChartOptions, AgCartesianSeriesOptions } from 'ag-charts-community';
import dayjs from 'dayjs';

// Define interfaces for clear type-checking
interface ChartDataPoint {
  valuationdate: string;
  [key: string]: any; // Allow any other keys for dynamic data
}

interface SeriesConfig {
  yKey: string;
  type: 'line' | 'bar' | 'area' | 'scatter';
  yName?: string;
  yAxisKey?: 'leftAxis' | 'rightAxis';
}

// A palette of colors for dynamic series
const COLOR_PALETTE = ['#2196f3', '#ef5350', '#66bb6a', '#ffca28', '#ab47bc', '#78909c'];

const ChartApp = () => {
  // --- 1. Read Data and Configuration from Window ---
  const rowData: any[] = (window as any).gridData || [];

  // Read series configuration from window, with a fallback to a default
  const seriesConfig: SeriesConfig[] = (window as any).chartConfig || [
    { yKey: 'units', type: 'bar', yName: 'Units', yAxisKey: 'leftAxis' },
    { yKey: 'asp', type: 'line', yName: 'ASP (₹)', yAxisKey: 'rightAxis' },
  ];

  const [chartData, setChartData] = useState<ChartDataPoint[]>([]);

  // --- 2. Process Raw Data (Unchanged) ---
  useEffect(() => {
    if (rowData?.length > 0) {
      const transformed = rowData.map((row) => {
        const point: ChartDataPoint = {
          valuationdate: row.valuationdate ? dayjs(Number(row.valuationdate)).format('YYYY-MM-DD') : 'N/A',
        };
        // Dynamically add all yKeys from the config to the data point
        seriesConfig.forEach(config => {
          point[config.yKey] = Number(row[config.yKey]) || 0;
        });
        return point;
      });
      setChartData(transformed);
    }
  }, [rowData, seriesConfig]);


  // --- 3. Dynamically Generate Chart Options ---
  const chartOptions = useMemo<AgChartOptions>(() => {
    // Generate series based on the config array
    const dynamicSeries: AgCartesianSeriesOptions[] = seriesConfig.map((config, index) => {
      const color = COLOR_PALETTE[index % COLOR_PALETTE.length];
      return {
        type: config.type,
        xKey: 'valuationdate',
        yKey: config.yKey,
        yName: config.yName || config.yKey, // Fallback yName to yKey
        yAxisKey: config.yAxisKey || 'leftAxis', // Default to left axis
        stroke: color, // For lines
        fill: color,   // For bars/areas
        marker: { enabled: config.type === 'line' },
        tooltip: {
          renderer: ({ datum }) => ({
            content: `${config.yName || config.yKey}: ${datum[config.yKey]}`,
          }),
        },
      };
    });

    // Generate axes based on which ones are needed by the series
    const requiredYAxes = new Set(seriesConfig.map(s => s.yAxisKey || 'leftAxis'));
    const dynamicAxes = [
      { // Bottom (X) axis is always required
        type: 'category',
        position: 'bottom',
        title: { text: 'Date' },
        label: { rotation: 45, avoidCollisions: true },
      },
    ];

    if (requiredYAxes.has('leftAxis')) {
      dynamicAxes.push({
        type: 'number',
        key: 'leftAxis',
        position: 'left',
        title: { text: 'Primary Value' },
      });
    }
    if (requiredYAxes.has('rightAxis')) {
      dynamicAxes.push({
        type: 'number',
        key: 'rightAxis',
        position: 'right',
        title: { text: 'Secondary Value (e.g., ASP)' },
      });
    }

    return {
      title: { text: 'Dynamic Chart' },
      data: chartData,
      series: dynamicSeries,
      axes: dynamicAxes,
      legend: { position: 'bottom' },
    };
  }, [chartData, seriesConfig]);

  return (
    <div style={{ height: 1000, width: '100%', marginTop: '2rem' }}>
      <AgCharts options={chartOptions} />
    </div>
  );
};

export default ChartApp;