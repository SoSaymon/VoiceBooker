import React, { useState } from "react";
import { IoMdCloudUpload } from "react-icons/io";
import wavyArrow from '../../wavy arrow-fotor-bg-remover-202402178119.png'
import Button from "../Button";
import { useMutation } from "@apollo/client";
import { CREATE_FILE_UPLOAD } from "../../gqloperations/mutations";
import { toast } from "react-toastify";
import useAuthUser from 'react-auth-kit/hooks/useAuthUser';
import Spinner from "../../Spinner";

const FileUpload = () => {
    const [file, setfile] = useState(null);
    const [fileUploadError, setfileUploadError] = useState('');
    const [author, setauthor] = useState('');
    const [title, setTitle] = useState('');
    const [summary, setsummary] = useState('');
   



    const auth = useAuthUser()
    // console.log(auth?.user?.token);

    const [createFileUpload, { loading }] = useMutation(CREATE_FILE_UPLOAD)



    //handle file select
    const handleFileSelect = (e) => {
        setfile(e.target.files[0])
    }
    // console.log(file);

    // post request to send uploaded file
    //http://localhost:8000/upload-ebook
    const handleUploadFile = () => {
        if (!file || !author || !title || !summary) {
            toast.error("All fields are required!");
        } else {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('filename', file?.name); // Append the filename
            formData.append('fileType', file?.type); // Append the fileType
            formData.append('title', title);
            formData.append('author', author);
            formData.append('summary', summary);

            fetch('http://localhost:8000/upload-ebook', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${auth?.user?.token}`
                },
                body: formData
            })
                .then((res) => {
                    if (res.ok) {
                        return res.json();
                    }
                    throw new Error('Network response was not ok.');
                })
                .then((data) => {
                    const { email, file_type, filename } = data
                    createFileUpload({
                        variables: {
                            filename,
                            fileType: file_type,
                            title,
                            author,
                            summary,

                        },
                        context: {
                            headers: {
                                Authorization: `Bearer ${auth?.user?.token}`
                            }
                        }

                    }).then((gqlRes) => {
                        toast.success('File uploaded Successfully!');
                        setTitle("");
                        setauthor("");
                        setsummary("");
                        setfile(null);
                    }).catch((err) => {
                        toast.error(err.message)
                        console.log('GQL error', err);
                    })


                })
                .catch((error) => {
                    toast.error(error.message);
                    console.error('Error uploading file:', error); // Handle error
                });
        }
    };

    return <>
        <div className="file-upload-container  p-5 mx-auto">
            <div className="file-upload-box">
                <input type="file" accept=".pdf,.epub" id="upload" hidden onChange={handleFileSelect} />
                <label htmlFor="upload" className="file-upload-label p-3">
                    <IoMdCloudUpload className="file-upload-icon mt-2" />
                    <h4 className="fw-bold text-center mt-3 file-upload-text ">Click to upload</h4>
                </label>
            </div>

            <div className="my-3  d-flex justify-between gap-3">
                <div className="w-100">
                    <label htmlFor="book">Book Title</label>
                    <br />
                    <input className="w-100 book-title " type="text" id="book" placeholder="Book title..." value={title} onChange={(e) => setTitle(e.target.value)} />
                </div>

                <div className="w-100">
                    <label htmlFor="author">Author</label>
                    <br />
                    <input className="w-100 author" type="text" id="author" placeholder="Author name..." value={author} onChange={(e) => setauthor(e.target.value)} />
                </div>
            </div>
            <label htmlFor="summary">Summary</label>
            <br />
            <textarea id="summary" cols="30" className="w-100 textarea mb-2" rows="3" placeholder="Summary..." value={summary} onChange={(e) => setsummary(e.target.value)}></textarea>

            <div className="shadow d-none d-xl-block"></div>
            <img src={wavyArrow} alt="arrow" className=" arrow d-none d-xl-block" />
            {fileUploadError && <p className="text-center mt-3 text-danger">{fileUploadError}</p>}
            {file && <p className="file-deatils mt-1 ">{file.name}</p>}
            <button onClick={handleUploadFile} className="file-upload-btn fw-bold float-end ">{loading ? <Spinner /> : 'Upload'}</button>
        </div>
    </>;
};

export default FileUpload;
