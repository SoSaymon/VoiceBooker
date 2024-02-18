import React from "react";
import { IoMdCloudUpload } from "react-icons/io";
import wavyArrow from '../../wavy arrow-fotor-bg-remover-202402178119.png'

const FileUpload = () => {
    return <>
        <div className="file-upload-container  p-5 mx-auto">
            <div className="file-upload-box">
                <input type="file" accept=".pdf,.epub" id="upload" hidden />
                <label htmlFor="upload" className="file-upload-label p-3">
                    <IoMdCloudUpload className="file-upload-icon mt-2" />
                    <h4 className="fw-bold text-center mt-3 file-upload-text ">Click to upload</h4>
                </label>
            </div>
            <div className="shadow d-none d-xl-block"></div>
            <img src={wavyArrow} alt="arrow" className=" arrow d-none d-xl-block" />
        </div>
    </>;
};

export default FileUpload;
