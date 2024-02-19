import React, { useState } from "react";
import FormContainer from "../FormContainer";
import { Link, useNavigate } from "react-router-dom";
import Button from "../Button";
import { useMutation } from "@apollo/client";
import { toast } from "react-toastify";
import { LOGIN_USER } from "../../gqloperations/mutations";
import useSignIn from 'react-auth-kit/hooks/useSignIn';
import Spinner from "../../Spinner";


const Login = () => {
    const [loginUser, {loading}] = useMutation(LOGIN_USER)
    const signIn = useSignIn()
    const navigate = useNavigate()
    const [loginData, setLoginData] = useState({
        email: '',
        password: '',
    })


    // handle input change
    const handleChange = (e) => {
        const { value, id } = e.target;

        setLoginData((prev) => {
            return {
                ...prev,
                [id]: value
            }
        })

    }


    // handle login user
    const signinUser = () => {

        // console.log(loginData)
        if (!loginData.email || !loginData.password) {
            toast.error("All fields are required!")
        } else {
            loginUser({ variables: loginData }).then((response) => {
                // console.log(response.data);
                signIn({
                    auth: {
                        token: response.data.loginUser.token,
                        type: 'Bearer',
                    },
                    refresh: response.data.loginUser.refreshToken,
                    userState: {
                        email: loginData.email
                    }
                })

                //navigate to home on successfully login
                navigate('/home')

            }).catch((error) => {
                toast.error(error.message)
                console.log(error);
            })
        }       
    }

   //registred user credentials
  //email : malikaleeza886@gmail.com
 //password :1234A@oig 

    return <>
        <FormContainer>
            <h3 className="form-title ">Signin Account</h3>
            <p className="form-link">Does not have account? <Link to={'/signup'}>Sign up</Link></p>
            <div className="my-3 form-input">
                <label htmlFor="email">Email</label>
                <input type="text" id="email" placeholder="Email..." value={loginData.email} onChange={handleChange} />
            </div>
            <div className="my-3 form-input">
                <label htmlFor="password">Password</label>
                <input type="password" id="password" placeholder="Password..." value={loginData.password} onChange={handleChange} />
            </div>

            <Button onClick={signinUser}>{loading ? <Spinner /> : 'Sign in'}</Button>
            
        </FormContainer>
    </>;
};

export default Login;
