###  RUN 1 DOCKERFILE
### FROM agrigorev/zoomcamp-model:2025

### # 1. Copy the dependency file and install dependencies
### # We use 'pip install .' to install dependencies from pyproject.toml
### COPY pyproject.toml .
### RUN pip install .

### # 2. Copy the FastAPI script (app.py)
### # Make sure your main application file is named 'app.py'
### COPY app.py .

# 3. Define the command to run the FastAPI app with uvicorn
# 'app' refers to the module (app.py), and 'app' refers to the FastAPI variable (app = FastAPI())
### CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

### Second run to fix one error:

FROM agrigorev/zoomcamp-model:2025

# Set the working directory (already done by base image, but good practice)
# WORKDIR /code

# 1. Copy the dependency file and install dependencies
COPY pyproject.toml .
RUN pip install .

# 2. Copy the FastAPI script (app.py)
COPY app.py .

# 3. *** NEW STEP: Copy the pipeline_v1.bin model file ***
# Make sure 'pipeline_v1.bin' is in the same directory as your Dockerfile
COPY pipeline_v1.bin . 

# 4. Define the command to run the FastAPI app with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]