import React from "react";
import BarLoader from "react-spinners/BarLoader";

const Loader = ({ loading, fullPage = false }) => {
  const fullPageStyle = {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
  };

  const componentStyle = {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100%",
  };

  return (
    <div style={fullPage ? fullPageStyle : componentStyle}>
      <BarLoader color="#000" loading={loading} />
    </div>
  );
};

export default Loader;
