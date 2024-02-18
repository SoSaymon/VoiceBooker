import React from "react";

const Button = ({children}) => {
  return <>
    <button className="form-btn py-2 mt-4">{children}</button>
  </>;
};

export default Button;
