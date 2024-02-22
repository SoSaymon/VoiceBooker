import React from "react";
import { ImSpinner9 } from "react-icons/im";

const Spinner = ({ className }) => {
  const classes = ` loading-spinner ${className}`
  return <>
    <ImSpinner9 className={classes} />
  </>;
};

export default Spinner;
