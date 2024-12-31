# CYOA_python
Grade 11 CS Python Project - Choose Your own Adventure.

Here is a step-by-step procedure to run the app from a user's perspective, including setting up both the backend and frontend.

### Step-by-Step Procedure

#### 1. Clone the Repository

First, clone the repository containing the project files.

```sh
git clone <repository-url>
cd adventure-game
```

#### 2. Set Up the Backend

1. **Navigate to the Backend Directory**:
   ```sh
   cd backend
   ```

2. **Create a Virtual Environment**:
   Create and activate a virtual environment.
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install Dependencies**:
   Install the required Python packages.
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the Backend Server**:
   Start the Flask server.
   ```sh
   python cyoa.py
   ```

#### 3. Set Up the Frontend

1. **Navigate to the Frontend Directory**:
   Open a new terminal window and navigate to the frontend directory.
   ```sh
   cd frontend
   ```

2. **Install Node.js and npm**:
   Ensure you have Node.js and npm installed. You can download and install them from [nodejs.org](https://nodejs.org/).

3. **Install Dependencies**:
   Install the required npm packages.
   ```sh
   npm install
   ```

4. **Create an `.env` File**:
   Create an `.env` file in the root of the 

frontend

 directory with the following content:
   ```sh
   echo SKIP_PREFLIGHT_CHECK=true > .env
   ```

5. **Run the Frontend Application**:
   Start the React application.
   ```sh
   npm start
   ```

#### 4. Verify the Application

1. **Open the Application in a Browser**:
   Open your web browser and navigate to `http://localhost:3000`.

2. **Interact with the Game**:
   - You should see the initial game state with options to choose from.
   - Make choices and observe the game state updates.
   - If you encounter any issues, check the browser's console for errors and the terminal running the backend server for logs.
