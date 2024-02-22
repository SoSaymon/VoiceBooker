import { useQuery } from "@apollo/client";
import React, { useEffect } from "react";
import { FiDownload } from "react-icons/fi";
import { Link } from "react-router-dom";
import { GET_AUDIO_BOOK } from "../../gqloperations/mutations";
import useAuthUser from "react-auth-kit/hooks/useAuthUser";
import Spinner from "../../Spinner";
import useGetAudio from "../../hook/getAudio";


const DownloadFile = ({ ebookId, setstatus }) => {
  const auth = useAuthUser()

  // console.log('auth', auth.user.token);
  const { loading, error, data } = useGetAudio(ebookId)
  console.log(error, data?.getAudiobookFilename);



  useEffect(() => {
    if (data?.getAudiobookFilename) {
      fetch(`http://localhost:8000/get-audiobook/${data?.getAudiobookFilename}`, {
        headers: {
          'Authorization': `Bearer ${auth?.user?.token}`
        },
      }).then((res) => {
        console.log(res);
      }).catch((err) => {
        console.log(err);
      })
    }

  }, [data?.getAudiobookFilename, auth?.user?.token])



  return <>
    {
      loading ? <div className="download-file-loading ">
        <Spinner className={'fs-1'} />
        <p className="main-desc fs-5 text-center">Please wait a moment your audio is generating...</p>
      </div> : <div className="download-file-container">
        <h3 className="main-desc text-center">Download Your Personalized Audio Masterpiece </h3>
        <div>
          <button className="file-upload-btn me-4" onClick={() => setstatus("fileUpload") }>Upload again</button>
          <a href={`http://localhost:8000/get-audiobook/${data?.getAudiobookFilename}`} download={data?.getAudiobookFilename}><button className="file-upload-btn mt-3 " >Download <FiDownload /></button></a>

        </div>
      </div>
    }

  </>;
};

export default DownloadFile;
