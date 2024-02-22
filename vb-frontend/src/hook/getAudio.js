import { useQuery } from "@apollo/client"
import { GET_AUDIO_BOOK } from "../gqloperations/mutations"
import useAuthUser from "react-auth-kit/hooks/useAuthUser"

const useGetAudio = (ebookId) => {
    const auth = useAuthUser()


    const { loading, error, data } = useQuery(GET_AUDIO_BOOK, {
        variables: { ebookId }, context: {
            headers: {
                Authorization: `Bearer ${auth?.user?.token}`
            }
        },
        pollInterval: 5000,
    })


    return { loading, error, data }
}



export default useGetAudio