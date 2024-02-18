import React from "react";

const Container = ({ children }) => {
    return <>
        <div className="container container-flex" >
            {children}
        </div>

        {/* <div className="ellipse-one">
            <div className="ellipse-two"></div>
        </div> */}

        {/* circles */}
        <div className="circle-one d-none d-xl-block"></div>
        <div className="circle-two d-none d-xl-block"></div>
        <div className="circle-three d-none d-xl-block"></div>
        <div className="circle-four d-none d-xl-block"></div>

    </>;
};

export default Container;
