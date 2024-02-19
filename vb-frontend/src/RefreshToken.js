import createRefresh from "react-auth-kit/createRefresh"
import { REFRESH_TOKEN } from "./gqloperations/mutations"
import { client } from "./index";

export const refresh = createRefresh({
    interval : 10,
    refreshApiCallback : async (params) => {
try {
const response = await client.mutate({
    mutation: REFRESH_TOKEN,
    variables: { refreshToken: params.refreshToken }
})

const newAuthToken = response.data.refreshToken.token;

return {
    isSuccess: true,
    newAuthToken: newAuthToken,
    newAuthTokenExpireIn: 10, 
    newRefreshTokenExpiresIn: 60 
  };
} catch(error) {
    console.error("Token Refresh Failed:", error);
    return {
      isSuccess: false
    };
}
    }
})
