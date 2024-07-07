import React, { useEffect, useState } from "react";
import { api } from '../../Api';
import Cards from "./Cards";
import numberWithCommas from "../../lib/helpers/comma";

const CardDetails = ({ endpoint, title, icon, dataKey, subtitle="This is an estimate" }) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get(`${endpoint}`);
        setData(response.data);
      } catch (error) {
        console.error('Error fetching data: ', error);
      }
    };

    fetchData();
  }, [endpoint]);

  useEffect(() => {
    console.log(data);
  }, [data]);

  const renderData = (data) => {
    if (Array.isArray(data[dataKey])) {
      return <div className="text-2xl font-bold">{numberWithCommas(data[dataKey].length)}</div>;
    } else {
      return <div className="text-2xl font-bold">{numberWithCommas(data[dataKey])}</div>;
    }
  };

  return (
    <Cards title={title} icon={icon}>
      {data !== null ? (
        <>
          {renderData(data)}
          <p className="text-xs text-muted-foreground">
            {subtitle}
          </p>
        </>
      ) : (
        <div className="text-sm">Loading...</div>
      )}
    </Cards>
  );
};

export default CardDetails;
