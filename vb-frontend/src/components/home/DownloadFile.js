import React, { useEffect, useState } from "react";
import { FiDownload } from "react-icons/fi";

import Spinner from "../../Spinner";


const DownloadFile = ({ loading, setstatus, url, fileName }) => {


  return (
    <>
      {loading ? (
        <div className="download-file-loading ">
          <Spinner className={'fs-1'} />
          <p className="main-desc fs-5 text-center">Please wait a moment your audio is generating...</p>
        </div>
      ) : (
        <div className="download-file-container">
          <h3 className="main-desc text-center">Download Your Personalized Audio Masterpiece </h3>
          <div>
            <button className="file-upload-btn me-4" onClick={() => setstatus("fileUpload")}>Upload again</button>
            <a href={url} download={'file.mp3'}>
              <button className="file-upload-btn mt-3">Download <FiDownload /></button>
            </a>
          </div>
        </div>
      )}
           
         
       
    </>
  );
};

export default DownloadFile;
