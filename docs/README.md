
# README for FastAPI Dockerized Application

This project provides a FastAPI application that processes PDB files and performs various computations. 
The app is dockerized for easy deployment and testing.

## 🚀 How to Build and Run the Docker Container

### 1. Clone the repository:
git clone https://github.com/auguNa/PDB_File_Processing.git
cd <repository_folder>

### 2. Build the Docker image:
To build the Docker image for the application, use the following command:

docker build -t <your_image_name> .

- Replace `<your_image_name>` with a name you want for the Docker image.
- This will build the image based on the `Dockerfile` in the current directory.

### 3. Run the Docker container:
Once the image is built, run the container using the command below:

docker run -d -p 8000:8000 -v $(pwd)/outputs:/app/outputs <your_image_name>

- `-d`: Runs the container in detached mode.
- `-p 8000:8000`: Maps port 8000 of the container to port 8000 on your local machine.
- `-v $(pwd)/outputs:/app/outputs`: Mounts the local `outputs` directory to `/app/outputs` inside the container.
- This ensures that metadata files are saved on your local machine.

### 4. Access the FastAPI application:
Once the container is running, you can access the FastAPI app by navigating to:

http://127.0.0.1:8000/docs

The `/docs` endpoint will provide interactive documentation where you can test the app's functionality.

## 📦 Dependencies

The application relies on the following Python dependencies, which are defined in `requirements.txt`:

- **FastAPI**: For building the web framework.
- **Uvicorn**: ASGI server for running FastAPI.
- **Pydantic**: Data validation and settings management.
- **Python-multipart**: File upload handling.
- **Requests**: For making HTTP requests (if needed).
- **Starlette**: Core FastAPI components.

To install dependencies manually (if not using Docker):

pip install -r requirements.txt

## 🐳 How to Use Docker Compose (Optional)

If you prefer to use Docker Compose for managing the container, follow these steps:

### 1. Run the application with Docker Compose:
docker-compose up --build

This will build the Docker image (if not already built) and start the container.

### 2. Access the FastAPI application:
After running the `docker-compose` command, the app will be accessible at:

http://127.0.0.1:8000/docs

## 🧪 Testing the Application Using FastAPI

Once the application is running, you can test it using the interactive Swagger UI:

1. Open your browser and go to: `http://127.0.0.1:8000/docs`
2. From the Swagger UI, you can interact with the available endpoints. The `POST /process-pdb/` endpoint allows you to upload a PDB file and get the processed result.

### Example Request:
- **URL**: `http://127.0.0.1:8000/process-pdb/`
- **Method**: `POST`
- **Body**: Upload a PDB file (e.g., `1bey.pdb`).

#### Expected Response:
```json
{
  "message": "Processing complete",
  "metadata": {
    "protein_id": "1bey.pdb",
    "processing_date": "2025-02-18 10:07:10",
    "extracted_chains": {
      "H": 20,
      "L": 20
    },
    "original_sequences": {
      "H": "QVLESGPRTaFCYMNWIKAH",
      "L": "CIQMTSPLAVGRaKNYWFEH"
    },
    "predicted_sequence": {
      "H": "QVLESGPRTaFCYMNWIKAH",
      "L": "CIQMTSPLAVGRaKNYWFEH"
    },
    "processing_time": 0.46,
    "embeddings": {
      "H": [
        [0.1996799260377884, ...],
        ...
      ]
    }
  }
}
```

#### File Save Location:
The metadata file `1bey.pdb_metadata.json` will be saved to the `outputs/` folder 
in the container or the local directory if using volume mapping.

---

## 📂 Directory Structure

Here’s a quick look at the structure of the project:

```
/app
├── /outputs           # Folder where metadata files will be saved
├── Dockerfile          # Docker configuration file
├── requirements.txt    # Project dependencies
├── main.py             # FastAPI application entry point
├── /pdb_files          # Folder where PDB files can be stored
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### If you have any further questions or issues, feel free to ask! 😄

---


