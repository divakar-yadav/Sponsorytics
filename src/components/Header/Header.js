import React from "react";
import analytics from "../../assets/images/analytics.png"
import './Header.css';
const Header = () => {
  return (
    <header style={styles.header}>
      <h1 style={styles.title}>Sponsorytics</h1>
      <img src={analytics} className="analytics-icon"/>
    </header>
  );
};

const styles = {
  header: {
    backgroundColor: "#141b28",
    padding: "10px",
    textAlign: "center",
    color: "white",
    paddingLeft: "30px",
  },
  title: {
    margin: 0,
    fontSize: "24px"
  }
};

export default Header;