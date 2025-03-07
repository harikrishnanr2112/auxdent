# # from fastapi import FastAPI, File, UploadFile
# # import torch
# # from ultralytics import YOLO
# # from PIL import Image
# # import io

# # # Initialize FastAPI
# # app = FastAPI()

# # # Load the trained model
# # model = YOLO("best.pt")  # Make sure best.pt is in the same folder


# # @app.get("/")
# # def read_root():
# #     return {"message": "Welcome to the DentaAI API!"}

# # @app.post("/predict/")
# # async def predict(file: UploadFile = File(...)):
# #     # Read the image file
# #     image = Image.open(io.BytesIO(await file.read()))

# #     # Run the model on the image
# #     results = model(image)

# #     # Extract detected objects
# #     detections = []
# #     for result in results:
# #         for box in result.boxes:
# #             class_id = int(box.cls[0])  # Class index
# #             confidence = float(box.conf[0])  # Confidence score
# #             bbox = box.xyxy[0].tolist()  # Bounding box

# #             detections.append({
# #                 "class": model.names[class_id],  # Convert class index to name
# #                 "confidence": confidence,
# #                 "bbox": bbox
# #             })

# #     return {"detections": detections}





# from fastapi import FastAPI, File, UploadFile, HTTPException
# from roboflow import Roboflow
# from PIL import Image
# import io
# import openai  # For OpenAI GPT integration

# # Initialize FastAPI
# app = FastAPI()

# # Initialize Roboflow
# rf = Roboflow(api_key="YOUR_ROBOFLOW_API_KEY")
# project = rf.workspace().project("PROJECT_NAME")
# model = project.version(1).model  # Replace with your version number

# # Initialize OpenAI (or other AI API)
# openai.api_key = "YOUR_OPENAI_API_KEY"

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to the Dental X-ray Analysis API!"}

# @app.post("/analyze/")
# async def analyze(file: UploadFile = File(...)):
#     if not file.content_type.startswith("image/"):
#         raise HTTPException(status_code=400, detail="File must be an image")

#     try:
#         # Read the image file
#         image_bytes = await file.read()
#         image = Image.open(io.BytesIO(image_bytes))

#         # Save the image to a temporary file (Roboflow SDK requires a file path)
#         temp_image_path = "temp_image.jpg"
#         image.save(temp_image_path)

#         # Run the YOLO model on the image
#         predictions = model.predict(temp_image_path).json()

#         # Extract detected objects
#         detections = []
#         for prediction in predictions["predictions"]:
#             class_name = prediction["class"]
#             confidence = prediction["confidence"]
#             bbox = [prediction["x"], prediction["y"], prediction["width"], prediction["height"]]

#             # Generate a description using OpenAI GPT
#             prompt = f"Explain what {class_name} is in dental X-rays, the difficulties it may cause, and how to prevent or mitigate its effects."
#             response = openai.Completion.create(
#                 engine="text-davinci-003",  # Use the appropriate model
#                 prompt=prompt,
#                 max_tokens=150
#             )
#             description = response.choices[0].text.strip()

#             detections.append({
#                 "class": class_name,
#                 "confidence": confidence,
#                 "bbox": bbox,
#                 "description": description
#             })

#         return {"detections": detections}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))




from fastapi import FastAPI, File, UploadFile, HTTPException
from roboflow import Roboflow
from PIL import Image
import io
import google.generativeai as genai  # For Gemini AI integration

# Initialize FastAPI
app = FastAPI()

# Initialize Roboflow
rf = Roboflow(api_key="zmzK1BPZl9yKP1BPkO3x")
project = rf.workspace("dentex").project("dentex-3xe7e")
model = project.version(1).model  # Use the correct version number

# Initialize Gemini AI
genai.configure(api_key="AIzaSyCy7D1WYcj9ZVdioSBLyG_ZkSu1IJzhpag")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Dental X-ray Analysis API!"}

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read the image file
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # Save the image to a temporary file (Roboflow SDK requires a file path)
        temp_image_path = "temp_image.jpg"
        image.save(temp_image_path)

        # Run the Roboflow model on the image
        predictions = model.predict(temp_image_path).json()

        # Extract detected objects
        detections = []
        for prediction in predictions["predictions"]:
            class_name = prediction["class"]
            confidence = prediction["confidence"]
            bbox = [prediction["x"], prediction["y"], prediction["width"], prediction["height"]]

            # Generate a description using Gemini AI
            prompt = f"Explain what {class_name} is in dental X-rays, the difficulties it may cause, and how to prevent or mitigate its effects."
            response = genai.generate_text(prompt=prompt)
            description = response.result

            detections.append({
                "class": class_name,
                "confidence": confidence,
                "bbox": bbox,
                "description": description
            })

        return {"detections": detections}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))