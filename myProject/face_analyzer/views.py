from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import cv2
#import mediapipe as mp
import numpy as np
from tensorflow.keras.models import model_from_json
import mediapipe as mp
import base64
from PIL import Image
import io
import logging
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Initialize models
# Load emotion model using the paths from the notebook
with open(r'C:\Users\Mongraal\PycharmProjects\JupyterProject\models\raf_model.json', 'r') as json_file:
    loaded_model_json = json_file.read()
emotion_model = model_from_json(loaded_model_json)
emotion_model.load_weights(r'C:\Users\Mongraal\PycharmProjects\JupyterProject\models\raf_model.weights.h5')

# Load age and gender models using the paths from the notebook
age_net = cv2.dnn.readNetFromCaffe(
    r'C:\Users\Mongraal\Downloads\Documents\age_deploy.prototxt',
    r'C:\Users\Mongraal\Downloads\Documents\age_net.caffemodel'
)

gender_net = cv2.dnn.readNetFromCaffe(
    r'C:\Users\Mongraal\Downloads\Documents\gender_deploy.prototxt',
    r'C:\Users\Mongraal\Downloads\Documents\gender_net.caffemodel'
)

# Define labels
gender_list = ['Male', 'Female']
age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
emotion_dict = {0: "Anger", 1: "Disgust", 2: "Fear", 3: "Happiness", 4: "Sadness", 5: "Surprise", 6: "Neutral"}

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'face_analyzer/index.html')

@csrf_exempt
def analyze_face(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
    try:
        # Get the image file from the request
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image file provided'}, status=400)
        
        image_file = request.FILES['image']
        image_bytes = image_file.read()
        
        # Convert to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        cv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if cv_image is None:
            return JsonResponse({'error': 'Failed to decode image'}, status=400)
        
        # Get detection options from request
        detect_emotion = request.POST.get('detect_emotion') == 'true'
        detect_gender = request.POST.get('detect_gender') == 'true'
        detect_age = request.POST.get('detect_age') == 'true'

        # Process with MediaPipe
        results = face_mesh.process(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        
        if not results.multi_face_landmarks:
            return JsonResponse({'error': 'No face detected'}, status=400)
            
        # Process each detected face
        faces_data = []
        for face_landmarks in results.multi_face_landmarks:
            # Get face bounding box
            h, w = cv_image.shape[:2]
            x_min = w
            y_min = h
            x_max = y_max = 0
            for landmark in face_landmarks.landmark:
                x, y = int(landmark.x * w), int(landmark.y * h)
                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x)
                y_max = max(y_max, y)
                
            # Extract face ROI with padding
            padding = 30
            y_start = max(0, y_min - padding)
            y_end = min(h, y_max + padding)
            x_start = max(0, x_min - padding)
            x_end = min(w, x_max + padding)
            face_roi = cv_image[y_start:y_end, x_start:x_end]
            
            if face_roi.size == 0:
                continue
                
            face_data = {}
            
            # Only process requested detections
            if detect_emotion:
                try:
                    # Analyze emotion
                    emotion_roi = cv2.resize(face_roi, (224, 224))
                    emotion_roi = cv2.cvtColor(emotion_roi, cv2.COLOR_BGR2RGB)
                    emotion_roi = emotion_roi.astype('float32') / 255.0
                    emotion_roi = np.expand_dims(emotion_roi, 0)
                    emotion_prediction = emotion_model.predict(emotion_roi, verbose=0)
                    face_data['emotion'] = emotion_dict[int(np.argmax(emotion_prediction[0]))]
                    face_data['emotion_confidence'] = float(np.max(emotion_prediction[0]))
                except Exception as e:
                    face_data['emotion_error'] = str(e)
            
            if detect_gender or detect_age:
                try:
                    # Create blob for age and gender
                    blob = cv2.dnn.blobFromImage(face_roi, 1.0, (227, 227),
                                               (78.4263377603, 87.7689143744, 114.895847746),
                                               swapRB=False)
                    
                    if detect_gender:
                        # Gender prediction
                        gender_net.setInput(blob)
                        gender_preds = gender_net.forward()
                        face_data['gender'] = gender_list[gender_preds[0].argmax()]
                        face_data['gender_confidence'] = float(gender_preds[0].max())
                    
                    if detect_age:
                        # Age prediction
                        age_net.setInput(blob)
                        age_preds = age_net.forward()
                        face_data['age'] = age_list[age_preds[0].argmax()]
                        face_data['age_confidence'] = float(age_preds[0].max())
                except Exception as e:
                    if detect_gender:
                        face_data['gender_error'] = str(e)
                    if detect_age:
                        face_data['age_error'] = str(e)
            
            # Add bounding box
            face_data['bbox'] = {
                'x_min': int(x_min),
                'y_min': int(y_min),
                'x_max': int(x_max),
                'y_max': int(y_max)
            }
            faces_data.append(face_data)
            
        return JsonResponse({
            'success': True,
            'faces': faces_data,
            'faces_count': len(faces_data)
        })
        
    except Exception as e:
        logger.error(f'Error in analyze_face: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def compare_faces(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
    try:
        # Get both images from the request
        image1_data = request.POST.get('image1')
        image2_data = request.POST.get('image2')
        
        if not image1_data or not image2_data:
            return JsonResponse({'error': 'Both images are required'}, status=400)
            
        # Process both images
        images_data = []
        for image_data in [image1_data, image2_data]:
            if 'base64,' in image_data:
                image_data = image_data.split('base64,')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Process with MediaPipe
            results = face_mesh.process(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
            
            if not results.multi_face_landmarks:
                return JsonResponse({'error': f'No face detected in one of the images'}, status=400)
                
            # Get the first face landmarks
            face_landmarks = results.multi_face_landmarks[0]
            
            # Extract face features
            face_features = []
            for landmark in face_landmarks.landmark:
                face_features.extend([landmark.x, landmark.y, landmark.z])
                
            images_data.append(np.array(face_features))
            
        # Compare faces
        similarity = 1 - np.linalg.norm(images_data[0] - images_data[1])
        match_percentage = max(0, min(100, int(similarity * 100)))
        
        # Save comparison if user is authenticated
        if request.user.is_authenticated:
            # Save both images
            for i, image_data in enumerate([image1_data, image2_data], 1):
                if 'base64,' in image_data:
                    image_data = image_data.split('base64,')[1]
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
                
                image_name = f'face_comparisons/{request.user.username}_comparison_{i}.jpg'
                image_io = io.BytesIO()
                image.save(image_io, format='JPEG')
                image_content = ContentFile(image_io.getvalue())
                saved_path = default_storage.save(image_name, image_content)
            
        return JsonResponse({
            'success': True,
            'match_percentage': match_percentage,
        })
        
    except Exception as e:
        logger.error(f'Error in compare_faces: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)

def user_images(request):
    # Get user's saved images from media storage
    user_images = []
    image_dir = f'face_images/{request.user.username}'
    if default_storage.exists(image_dir):
        for image_name in default_storage.listdir(image_dir)[1]:  # [1] for files
            image_url = default_storage.url(f'{image_dir}/{image_name}')
            user_images.append({
                'url': image_url,
                'name': image_name
            })
    
    return JsonResponse({'images': user_images})
