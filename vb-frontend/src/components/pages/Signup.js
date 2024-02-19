
import React, { useState } from "react";
import FormContainer from "../FormContainer";
import Button from "../Button";
import { Link, useNavigate } from "react-router-dom";
import { useMutation } from "@apollo/client";
import { CREATE_USER } from "../../gqloperations/mutations";
import { toast } from "react-toastify";
import Spinner from "../../Spinner";

const Signup = () => {
    const navigate = useNavigate()
    const [createUser, { data, loading, error }] = useMutation(CREATE_USER)
    const [signupData, setSignupData] = useState({
        username: '',
        fullName: '',
        email: '',
        password: '',
    })

    //handle input change
    const handleChange = (e) => {
        const { value, id } = e.target;

        setSignupData((prev) => {
            return {
                ...prev,
                [id]: value
            }
        })
    }

    //handle register user
    const registerUser = () => {
        if (!signupData.email || !signupData.username || !signupData.password) {
            toast.error('All fields are required!')

        } else {
            createUser({
                variables: signupData
            }).then((response) => {
                // Log response
                //  console.log('Mutation response:', response);              
                setSignupData({
                    username: '',
                    fullName: '',
                    email: '',
                    password: '',
                })
                toast.success('User registered successfully!');
                navigate('/')

            }).catch((error) => {
                if (error) {
                    toast.error(error.message)
                } else {
                    toast.error('An error occurred while registering user. Please try again later.');
                }
            })
        }
    }


    // if (error) return <h1>erorr</h1>

    return <>
        <FormContainer>
            <h3 className="form-title ">Signup Account</h3>
            <p className="form-link">Already register? <Link to={'/'}>Sign in</Link></p>
            <div className="my-3 form-input">
                <label htmlFor="fullName">Full Name</label>
                <input type="text" id="fullName" value={signupData.fullName} placeholder="fullName..." onChange={handleChange} />
            </div>
            <div className="my-3 form-input">
                <label htmlFor="username">Username</label>
                <input type="text" id="username" value={signupData.username} placeholder="Username..." onChange={handleChange} />
            </div>
            <div className="my-3 form-input">
                <label htmlFor="email">Email</label>
                <input type="text" id="email" placeholder="Email..." value={signupData.email} onChange={handleChange} />
            </div>
            <div className="my-3 form-input">
                <label htmlFor="password">Password</label>
                <input type="password" id="password" placeholder="Password..." value={signupData.password} onChange={handleChange} />
            </div>

            <Button onClick={registerUser}>{loading ? <Spinner /> : 'Sign up'}</Button>



        </FormContainer>
    </>;
};

export default Signup;
