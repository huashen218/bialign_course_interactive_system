
# Human-AI Alignment Course (CSCI-SHU 205) - Building a Human-AI Interactive System 

<!-- AI Value Auditing System - Deployment Guide -->


This is a project template used for the (CSCI-SHU 205) Human-AI Alignment course at NYU Shanghai - Fall 2025 semester.

This guide explains how to set up and run the human-AI interactive Value Auditing System with both frontend and backend components.


## System Architecture

The system consists of:

1. **Python Backend**: A FastAPI server with a Python package structure for handling auditing logic
2. **React Frontend**: A responsive web interface displaying Human-Agent interactions and Value Auditing panels

## Prerequisites

- Python 3.7 or higher
- Node.js 14 or higher
- npm or yarn

## 1. Backend Setup

1. **Create a virtual environment and activate it**:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install the package in development mode**:

```bash
pip install -e .
```

3. **Run the backend server**:

```bash
value-auditor --reload
```

This will start the FastAPI server at http://localhost:8000 with auto-reload enabled for development.

## 2. Frontend Setup

### 2.1 Development 
1. **Create a new React app**:

```bash
npx create-react-app ai-value-auditor-frontend
cd ai-value-auditor-frontend
```

2. **Replace the default files**:

- Replace `src/App.js` with the provided React component code
- Replace `src/App.css` with the provided CSS styles

3. **Set up proxy for development**:

Add this line to your `package.json` file:

```json
"proxy": "http://localhost:8000"
```

4. **Install required dependencies**:

```bash
npm install
```

5. **Start the frontend development server**:

```bash
npm start
```

This will start the React development server at http://localhost:3000.


### 2.2 Production Deployment

For production deployment, you can:

(1) **Build the React frontend**:

```bash
npm run build
```

(2) **Configure the FastAPI backend to serve the static files**:

Update the `ai_value_auditor/server.py` file to serve the React build directory:

```python
# Add this near the end of the file, before the start_server function
app.mount("/", StaticFiles(directory="path/to/react/build", html=True), name="static")
```

(3) **Deploy using a production-ready server**:

```bash
uvicorn ai_value_auditor.server:app --host 0.0.0.0 --port 8000
```

## 3. Extending the System

### Adding Custom Auditing Logic

To enhance the auditing capabilities, modify the `ValueAuditor` class in `ai_value_auditor/auditor.py`:

```python
def audit_response(self, user_message: str, ai_response: str, task_id: int) -> Tuple[bool, Optional[str]]:
    # Add your custom auditing logic here
    # ...
```
