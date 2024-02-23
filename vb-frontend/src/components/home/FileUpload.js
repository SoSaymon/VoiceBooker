import React, { useState } from "react";
import { IoMdCloudUpload } from "react-icons/io";
import wavyArrow from '../../wavy arrow-fotor-bg-remover-202402178119.png'
import Button from "../Button";
import { useMutation, useQuery } from "@apollo/client";
import { CREATE_FILE_UPLOAD, GET_AUDIO_BOOK } from "../../gqloperations/mutations";
import { toast } from "react-toastify";
import useAuthUser from 'react-auth-kit/hooks/useAuthUser';
import Spinner from "../../Spinner";
import DownloadFile from "./DownloadFile";

const FileUpload = () => {
    const [file, setfile] = useState(null);
    const [fileUploadError, setfileUploadError] = useState('');
    const [loading, setloading] = useState(false);
    const [status, setstatus] = useState('fileUpload');
    const [fileUrl, setfileUrl] = useState('');
    const [fileName, setfileName] = useState('');




    const auth = useAuthUser()
    // console.log(auth?.user?.token);
    // const [createFileUpload, { loading }] = useMutation(CREATE_FILE_UPLOAD)



    //handle file select
    const handleFileSelect = (e) => {
        setfile(e.target.files[0])
    }

    // post request to send uploaded file
    const handleUploadFile = async () => {
        setloading(true);

        try {
            const formData = new FormData();
            formData.append('pdf_file', file);
            setfileName(file?.name);

            const response = await fetch("https://ai-blinkist.onrender.com/upload-pdf/", {
                method: "POST",
                body: formData,
            });


            if (!response.ok) {
                throw new Error("Failed to upload file.");
            }

            const blob = await response.blob();         
            const url = URL.createObjectURL(blob);

            // console.log(blob, );
            console.log(url);
            setfileUrl(url);            
            setstatus("audioReady");
            setloading(false);
        } catch (err) {
            console.error("Upload failed:", err);
            setloading(false);
        }
    };






    return <>
        <div className="file-upload-container  p-5 mx-auto">
            {status === 'fileUpload' && <> <div className="file-upload-box mb-3 ">
                <input type="file" accept=".pdf,.epub" id="upload" hidden onChange={handleFileSelect} />
                <label htmlFor="upload" className="file-upload-label p-3">
                    <IoMdCloudUpload className="file-upload-icon mt-2" />
                    <h4 className="fw-bold text-center mt-3 file-upload-text ">Click to upload</h4>
                </label>
            </div>



                <div className="shadow d-none d-xl-block"></div>
                <img src={wavyArrow} alt="arrow" className=" arrow d-none d-xl-block" />
                {fileUploadError && <p className="text-center mt-3 text-danger">{fileUploadError}</p>}
                {file && <p className="file-deatils mt-1 ">{file.name}</p>}
                <button onClick={handleUploadFile} className="file-upload-btn fw-bold  float-end ">{loading ? <Spinner /> : 'Upload'}</button></>}

            {status === 'audioReady' && <>
                <div className="shadow d-none d-xl-block"></div>
                <DownloadFile url={fileUrl} setstatus={setstatus} fileName={fileName} />
            </>}
        </div>

    </>;
};

export default FileUpload;
