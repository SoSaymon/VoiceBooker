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