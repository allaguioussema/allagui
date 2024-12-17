from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
import cv2
import numpy as np
from tensorflow.keras.models import model_from_json
import mediapipe as mp
import base64
from PIL import Image
import io
import logging
from functools import lru_cache
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)

# Define labels
gender_list = ['Male', 'Female']
age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
emotion_dict = {0: "Surprise", 1: "Disgust", 2: "Fear", 3: "Happiness", 4: "Sadness", 5: "Anger", 6: "Neutral"}

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

@lru_cache(maxsize=1)
def load_models():
    """Load models with caching to prevent repeated loading"""
    try:
        # Load emotion model
        with open(r'C:\Users\Mongraal\PycharmProjects\JupyterProject\models\raf_model.json', 'r') as json_file:
            loaded_model_json = json_file.read()
        emotion_model = model_from_json(loaded_model_json)
        emotion_model.load_weights(r'C:\Users\Mongraal\PycharmProjects\JupyterProject\models\raf_model.weights.h5')

        # Load age and gender models
        age_net = cv2.dnn.readNetFromCaffe(
            r'C:\Users\Mongraal\Downloads\Documents\age_deploy.prototxt',
            r'C:\Users\Mongraal\Downloads\Documents\age_net.caffemodel'
        )

        gender_net = cv2.dnn.readNetFromCaffe(
            r'C:\Users\Mongraal\Downloads\Documents\gender_deploy.prototxt',
            r'C:\Users\Mongraal\Downloads\Documents\gender_net.caffemodel'
        )
        
        return emotion_model, age_net, gender_net
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        return None, None, None

def auth_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            try:
                username = User.objects.get(email=email).username
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('face_analyzer:home')
                else:
                    messages.error(request, 'Invalid credentials')
            except User.DoesNotExist:
                messages.error(request, 'User not found')
            
        elif action == 'signup':
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if password != confirm_password:
                messages.error(request, 'Passwords do not match')
                return redirect('face_analyzer:auth')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('face_analyzer:auth')
            
            try:
                username = email.split('@')[0]
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=full_name.split()[0],
                    last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
                )
                login(request, user)
                return redirect('face_analyzer:home')
            except Exception as e:
                messages.error(request, str(e))
    
    return render(request, 'face_analyzer/auth.html')

def logout_view(request):
    logout(request)
    return redirect('face_analyzer:auth')

@login_required(login_url='face_analyzer:auth')
def index(request):
    return render(request, 'face_analyzer/index.html')

def home(request):
    return render(request, 'face_analyzer/Home.html')

@login_required(login_url='face_analyzer:auth')
@csrf_exempt
def analyze_face(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
    # Load models only when needed
    emotion_model, age_net, gender_net = load_models()
    if not all([emotion_model, age_net, gender_net]):
        return JsonResponse({'error': 'Models not properly loaded. Please check server logs.'}, status=500)
    
    try:
        # Get the image data from the request
        image_data = request.POST.get('image')
        if not image_data:
            return JsonResponse({'error': 'No image data provided'}, status=400)
        
        # Remove the data URL prefix if present
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
            
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Process with MediaPipe
        results = face_mesh.process(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
        
        # Get detection options from request
        detect_emotion = request.POST.get('detect_emotion', 'true').lower() == 'true'
        detect_gender = request.POST.get('detect_gender', 'true').lower() == 'true'
        detect_age = request.POST.get('detect_age', 'true').lower() == 'true'

        # Initialize response data
        face_data = {}

        if results.multi_face_landmarks:
            # Process the first detected face
            face_landmarks = results.multi_face_landmarks[0]
            
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
                
            # Extract face ROI
            face_roi = cv_image[max(0, y_min-30):min(h, y_max+30),
                              max(0, x_min-30):min(w, x_max+30)]
            
            if face_roi.size > 0:
                # Analyze emotion if enabled
                if detect_emotion:
                    try:
                        emotion_roi = cv2.resize(face_roi, (224, 224))
                        emotion_roi = emotion_roi / 255.0  # Normalize to [0,1]
                        emotion_roi = np.expand_dims(emotion_roi, 0)
                        emotion_prediction = emotion_model.predict(emotion_roi)
                        emotion_label = emotion_dict[int(np.argmax(emotion_prediction[0]))]
                        emotion_scores = {emotion_dict[i]: float(score) for i, score in enumerate(emotion_prediction[0])}
                        face_data['emotion'] = emotion_label
                        face_data['emotion_scores'] = emotion_scores
                    except Exception as e:
                        face_data['emotion_error'] = str(e)
                
                # Analyze gender if enabled
                if detect_gender:
                    try:
                        blob = cv2.dnn.blobFromImage(face_roi, 1.0, (227, 227),
                                                   (78.4263377603, 87.7689143744, 114.895847746),
                                                   swapRB=False)
                        gender_net.setInput(blob)
                        gender_preds = gender_net.forward()
                        gender = gender_list[gender_preds[0].argmax()]
                        face_data['gender'] = gender
                    except Exception as e:
                        face_data['gender_error'] = str(e)
                
                # Analyze age if enabled
                if detect_age:
                    try:
                        blob = cv2.dnn.blobFromImage(face_roi, 1.0, (227, 227),
                                                   (78.4263377603, 87.7689143744, 114.895847746),
                                                   swapRB=False)
                        age_net.setInput(blob)
                        age_preds = age_net.forward()
                        age = age_list[age_preds[0].argmax()]
                        face_data['age'] = age
                    except Exception as e:
                        face_data['age_error'] = str(e)
            
            return JsonResponse(face_data)
        else:
            return JsonResponse({'error': 'No face detected'})
        
    except Exception as e:
        logger.error(f'Error in analyze_face: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url='face_analyzer:auth')
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

@login_required(login_url='face_analyzer:auth')
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
