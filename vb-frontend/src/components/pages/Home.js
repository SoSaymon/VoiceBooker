import React from "react";
import Container from "../Container";
import Logo from "../home/Logo";
import HeroSection from "../home/HeroSection";
import FileUpload from "../home/FileUpload";

const Home = () => {
  return <>
     <Container>
      <Logo />
      <HeroSection />
      <FileUpload />

    </Container>
  </>;
};

export default Home;
