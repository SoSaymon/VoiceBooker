import React from "react";


const Button = ({children, onClick}) => {
  return <>
    <button onClick={onClick} className="form-btn py-2 mt-4">{children}</button>


};

export default Button;
