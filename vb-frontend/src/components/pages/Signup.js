import React from "react";
import FormContainer from "../FormContainer";
import Button from "../Button";
import { Link } from "react-router-dom";

const Signup = () => {
    return <>
        <FormContainer>
            <h3 className="form-title ">Signup Account</h3>
            <p className="form-link">Already register? <Link to={'/signin'}>Sign in</Link></p>
            <div className="my-3 form-input">
                <label htmlFor="email">Email</label>
                <input type="text" id="email" placeholder="Email..." />
            </div>
            <div className="my-3 form-input">
                <label htmlFor="password">Password</label>
                <input type="password" id="password" placeholder="Password..." />
            </div>
            <div className="my-3 form-input">
                <label htmlFor="cpassword">Confirm Password</label>
                <input type="password" id="cpassword" placeholder="Confirm password..."/>
            </div>

            <Button>Sign up</Button>
        </FormContainer>
    </>;
};

export default Signup;
