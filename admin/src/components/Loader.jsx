import React from "react";
import BarLoader from "react-spinners/BarLoader";

const override = {
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  height: "100vh",
};

const Loader = ({ loading }) => {
  return (
    <div style={override}>
      <BarLoader
        color="#4338ca"
        loading={loading}
        size={150}
      />
    </div>
  );
};

export default Loader;