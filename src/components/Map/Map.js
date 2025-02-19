import React, { useEffect, useRef } from "react";
import Highcharts from "highcharts";
import HCMap from "highcharts/modules/map";
import worldMapData from "@highcharts/map-collection/custom/world.geo.json";

HCMap(Highcharts);

const Map = () => {
  const chartRef = useRef(null);

  useEffect(() => {
    if (!chartRef.current) {
      chartRef.current = Highcharts.mapChart("map-container", {
        chart: {
          map: worldMapData,
          backgroundColor: "rgb(9 17 30)",
        },
        title: {
          text: "Company Locations",
          style: { color: "white" },
        },
        mapNavigation: {
          enabled: true,
          buttonOptions: {
            theme: {
              fill: "#303030",
            },
          },
        },
        credits: {
          enabled: false,
        },
        series: [
          {
            name: "Companies",
            type: "mapbubble",
            joinBy: ["iso-a3", "code"],
            data: [
              { code: "USA", lat: 37.7749, lon: -122.4194, z: 10 },
              { code: "IND", lat: 28.6139, lon: 77.209 },
              { code: "GBR", lat: 51.5074, lon: -0.1278 },
            ],
            color: "#FF5733",
            dataLabels: {
              enabled: true,
              format: "{point.name}",
              style: { color: "white" },
            },
          },
        ],
      });
    }
  }, []);

  return <div id="map-container" style={{ height: "500px", width: "100%" }}></div>;
};

export default Map;
