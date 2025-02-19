import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const companyLocations = [
  { name: "Company A", lat: 37.7749, lng: -122.4194 },
  { name: "Company B", lat: 40.7128, lng: -74.006 },
  { name: "Company C", lat: 34.0522, lng: -118.2437 },
];

const CompanyMap = () => {
  return (
    <MapContainer center={[37.7749, -122.4194]} zoom={4} style={{ height: "400px", width: "100%" }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      {companyLocations.map((company, index) => (
        <Marker key={index} position={[company.lat, company.lng]}>
          <Popup>{company.name}</Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default CompanyMap;
