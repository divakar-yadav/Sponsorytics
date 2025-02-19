import React, { useEffect } from "react";
import Highcharts from "highcharts";
import "./Dashboard.css";
import Header from "../../components/Header/Header";

const Dashboard = () => {
  const renderChart = (containerId, options) => {
    Highcharts.chart(containerId, options);
  };

  const generateBarChartOptions = (title, categories, data) => ({
    chart: {
      type: "bar",
      backgroundColor: "rgb(9 17 30)",
    },
    title: {
      text: title,
      style: { color: "white" },
    },
    xAxis: {
      categories: categories,
      labels: { style: { color: "white" } },
    },
    yAxis: {
      min: 0,
      labels: { style: { color: "white" } },
    },
    credits: { enabled: false },
    legend: { itemStyle: { color: "white", fontWeight: "bold" } },
    plotOptions: {
      series: {
        borderWidth: 0,
        dataLabels: { color: "white" },
      },
    },
    series: [{ name: title, data: data }],
  });

  const generatePieChartOptions = (title, data) => ({
    chart: {
      type: "pie",
      backgroundColor: "rgb(9 17 30)",
    },
    title: {
      text: title,
      style: { color: "white" },
    },
    credits: { enabled: false },
    plotOptions: {
      pie: {
        borderWidth: 0,
        dataLabels: { style: { color: "white" } },
      },
    },
    series: [{ name: "Share", data: data }],
  });

  const companies = ["Advocate Aurora Health", "Froedtert Health", "Ascension Wisconsin", "Quad", "Medical College of Wisconsin", "Kohl's", "GE Healthcare", "Goodwill Industries", "Rockwell Automation", "WEC Energy Group", "Harley-Davidson", "Milwaukee Tool", "Johnson Controls", "Robert W. Baird & Company", "ManpowerGroup", "Fiserv", "BMO Harris Bank", "Briggs & Stratton Corp.", "Children's Wisconsin", "Generac Holdings Inc.", "ProHealth Care"];

  const similarities = [0.503, 0.557, 0.204, 0.999, 0.813, 0.44, 0.155, 0.384, 0.318, 0.974, 0.559, 0.98, 0.462, 0.601, 0.685, 0.619, 0.662, 0.847, 0.362, 0.25, 0.117];

  const sponsorshipScores = similarities.map((sim, i) => ({ name: companies[i], y: sim * 100 }));

  const industryAlignment = [
    { name: "Healthcare", y: 30 },
    { name: "Finance", y: 20 },
    { name: "Manufacturing", y: 25 },
    { name: "Technology", y: 15 },
    { name: "Retail", y: 10 },
  ];

  const fundingCapacity = [
    { name: "GE Healthcare", y: 500 },
    { name: "Fiserv", y: 450 },
    { name: "Johnson Controls", y: 400 },
    { name: "Harley-Davidson", y: 350 },
    { name: "Kohl's", y: 300 },
  ];

  const milwaukeeVsNational = [
    { name: "Milwaukee-based", y: 40 },
    { name: "National", y: 60 },
  ];

  const untappedSponsors = [
    { name: "XYZ Corporation", y: 700 },
    { name: "ABC Industries", y: 650 },
    { name: "LMN Solutions", y: 600 },
  ];

  useEffect(() => {
    const charts = [];
    charts.push(renderChart("bar-chart-sponsorship", generateBarChartOptions("Sponsorship Likelihood Score", companies, similarities)));
    charts.push(renderChart("pie-chart-industry", generatePieChartOptions("Industry Alignment", industryAlignment)));
    charts.push(renderChart("bar-chart-funding", generateBarChartOptions("Funding Capacity", fundingCapacity.map(d => d.name), fundingCapacity.map(d => d.y))));
    // charts.push(renderChart("pie-chart-milwaukee", generatePieChartOptions("Milwaukee vs. National Sponsorship", milwaukeeVsNational)));
    charts.push(renderChart("bar-chart-untapped", generateBarChartOptions("Potential Untapped Sponsors", untappedSponsors.map(d => d.name), untappedSponsors.map(d => d.y))));
    
    return () => charts.forEach(chart => chart && chart.destroy && chart.destroy());
  }, []);

  return (
    <div className="dashboard-wrapper">
      <Header />
      <div className="dashboard-container">
        <div id="bar-chart-sponsorship" className="dashboard-chart"></div>
        <div id="pie-chart-industry" className="dashboard-chart"></div>
        <div id="bar-chart-funding" className="dashboard-chart"></div>
        {/* <div id="pie-chart-milwaukee" className="dashboard-chart"></div> */}
        <div id="bar-chart-untapped" className="dashboard-chart"></div>
      </div>
    </div>
  );
};

export default Dashboard;
