import React, { useEffect, useState } from "react";
import { api } from '../../Api';
import Cards from "./Cards";
import Loader from "../Loader";
import numberWithCommas from "../../lib/helpers/comma";

const CardDetails = ({ endpoint, title, icon, dataKey, subtitle="This is an estimate" }) => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const response = await api.get(`${endpoint}`);
        setData(response.data);
      } catch (error) {
        console.error('Error fetching data: ', error);
      } finally {
        setIsLoading(false);
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
      {isLoading ? (
        <Loader loading={true} />
      ) : (
        data !== null ? (
          <>
            {renderData(data)}
            <p className="text-xs text-muted-foreground">
              {subtitle}
            </p>
          </>
        ) : (
          <div className="text-sm">Only admins can see this data.</div>
        )
      )}
    </Cards>
  );
};

export default CardDetails;
