# Starlink AI - Industrial Property Analysis Agent

This project is a submission for the Starboard AI Agent Engineer take-home challenge. It is an intelligent agent system designed to integrate property data and perform comparable property analysis for the industrial real estate market.

**The system consists of a Python/Flask backend for data processing and a Next.js/TypeScript frontend for user interaction.**


---

### **🛠️ Tech Stack**

*   **Backend:** Python, Flask, Pandas
*   **Frontend:** Next.js, React, TypeScript, Tailwind CSS
*   **Core Logic:** Custom-built agents for data extraction and comparable property analysis.

---

## 🚀 How to Run This Project

To run this application, you will need to run the backend and frontend servers in two separate terminals.

### **1. Backend Server Setup**

The backend is responsible for all data analysis and API endpoints.

```bash
# 1. Navigate to the backend directory
cd backend

# 2. Create and activate a Python virtual environment
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
.\venv\Scripts\activate

# 3. Install the required Python packages
pip install -r requirements.txt

# 4. Run the Flask API server
python api.py
```
> ✅ The backend server should now be running on `http://127.0.0.1:5000`.

### **2. Frontend Server Setup**

The frontend provides the user interface to interact with the system.

```bash
# 1. In a new terminal, navigate to the frontend directory
cd frontend

# 2. Install the required Node.js packages
npm install

# 3. Run the Next.js development server
npm run dev
```
> ✅ The frontend application should now be running and accessible at `http://localhost:3000`.

---

## ⚙️ How to Use the Application

1.  Once both servers are running, open your web browser.
2.  Navigate to **`http://localhost:3000`**.
3.  Enter an industrial property address into the input field.
4.  Click the **"Find Comparables"** button.
5.  The system will process the request via the backend API and display the top comparable properties found in the dataset.
