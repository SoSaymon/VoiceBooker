import React from "react";

const FormContainer = ({ children }) => {
    return <>
        <div className="container ">
            <div className="wrapper">
                <div className="login-box p-4 text-black">
                    {children}
                    <div className="circle-one d-none d-xl-block"></div>
                    <div className="circle-two d-none d-xl-block"></div>
                    <div className="circle-three d-none d-xl-block"></div>
                    <div className="circle-four d-none d-xl-block"></div>
                </div>
            </div>
        </div>
    </>;
};

export default FormContainer;
