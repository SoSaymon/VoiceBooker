# VoiceBooker

## Build Setup
1. Clone the repository
    ```bash
    git clone git@github.com:SoSaymon/VoiceBooker.git
    ```
2. create a virtual environment and activate it
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install the requirements
    ```bash
    pip install -r requirements.txt
    ```
4. Run the server
    ```bash
    uvicorn app.main:app
    ```
   

## API Documentation
### File Upload
- **http://localhost:8000/upload-ebook**
    - **Method**: POST
    - **Request**: 
        - **Headers**: 
            - Content-Type: multipart/form-data
            - Authorization: Bearer `<token>`
        - **Body**: 
            - file: `<file>`
    - **Response**: 
        - **Status Code**: 200
          - **Body**: 
              - filename: `<filename>`
              - file_type: `<file_type>`
              - email: `<email>`
- **http://localhost:8000/get-audiobook**
    - **Method**: GET
    - **Response**: 
        - **Status Code**: 200
          - **Body**:
            - file: `<file>` 


## File Upload

### How to upload a file
1. Send file via POST `/upload-ebook` endpoint
2. You will receive a response with the filename, file_type and email
3. Use the filename amd file_type to add the `FileUpload` via GrapQL mutation (see below)
    ```grqaphql
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
    ```

### How to get the audiobook

To be done in future, now the audiobook is not generated yet. It's only possible to download example audiobook from the `get-audiobook` endpoint. Do not forget to add the `Authorization` header with the `Bearer` token.