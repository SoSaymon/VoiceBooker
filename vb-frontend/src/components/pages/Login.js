import React from "react";
import FormContainer from "../FormContainer";
import { Link } from "react-router-dom";
import Button from "../Button";

const Login = () => {
    return <>
        <FormContainer>
            <h3 className="form-title ">Signin Account</h3>
            <p className="form-link">Does not have account? <Link to={'/'}>Sign up</Link></p>
            <div className="my-3 form-input">
                <label htmlFor="email">Email</label>
                <input type="text" id="email" placeholder="Email..." />
            </div>
            <div className="my-3 form-input">
                <label htmlFor="password">Password</label>
                <input type="password" id="password" placeholder="Password..." />
            </div>

            <Button>Sign in</Button>
        </FormContainer>
    </>;
};

export default Login;
