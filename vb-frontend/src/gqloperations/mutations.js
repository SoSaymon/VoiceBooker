import { gql } from '@apollo/client';

export const CREATE_USER = gql`
  mutation CreateUser($username: String!, $email: String!, $password: String!, $fullName: String!) {
    createUser(username: $username, email: $email, password: $password, fullName: $fullName) {
      ok
      user {
        id
        username        
        isActive
        isAdmin
        createdAt
        lastLogin
      }
    }
  }
`;


export const LOGIN_USER = gql`
mutation loginUser($email: String!, $password: String!){
    loginUser(email: $email, password: $password) {
        token
        refreshToken
        user {
            id
            username
            fullName
            isActive
            isAdmin
            createdAt
            lastLogin
        }
    }
}
`

export const REFRESH_TOKEN = gql`
mutation refreshToken{
  refreshToken{
      token
      refreshToken
      user {
          id
      }
  }
}
`
export const CREATE_FILE_UPLOAD = gql`
mutation createFileUpload($filename: String!, $fileType: String!, $title: String!, $author: String!, $summary: String!) {
  createFileUpload(filename: $filename, fileType: $fileType, title: $title, author: $author, summary: $summary) {
      ok
      fileUpload {
          id
          filename
          fileType
          userId
          createdAt
          deleteTime
          user {
              username
          }
          ebooks {
              id
              title
              author
              summary
          }
      }
  }
  }
`

//queries
export const GET_AUDIO_BOOK = gql`
query getAudiobookFilename($ebookId: Int!) {
  getAudiobookFilename(ebookId: $ebookId)
  }
`
