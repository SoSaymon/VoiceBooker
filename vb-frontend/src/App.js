import React from "react";
import './App.css'
import { Routes, BrowserRouter, Route } from 'react-router-dom'
import Login from "./components/pages/Login";
import Home from "./components/pages/Home";
import Signup from "./components/pages/Signup";

const App = () => {
  return <>

    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Signup />} />
        <Route path="/signin" element={<Login />} />
        <Route path="/home" element={<Home />} />


        
      </Routes>

    </BrowserRouter>


  </>;
};

export default App;

