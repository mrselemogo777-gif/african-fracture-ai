import joblib
import numpy as np
import streamlit as st
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from PIL import Image

class ModelManager:
    def __init__(self):
        self.models = None
        self.extractor = None
        self.load()
    
    def load(self):
        try:
            self.models = {
                'clinical': joblib.load("clinical_model.pkl"),
                'scaler': joblib.load("scaler.pkl"),
                'xray': joblib.load("xray_model.pkl"),
                'pca': joblib.load("pca.pkl"),
                'ensemble': joblib.load("ensemble_meta_learner.pkl"),
                'clinical_accuracy': 0.841,
                'xray_accuracy': 0.686,
                'ensemble_accuracy': 0.848
            }
            self.extractor = EfficientNetB0(weights='imagenet', include_top=False, pooling='avg')
            return True
        except Exception as e:
            st.error(f"Error loading models: {e}")
            return False
    
    def predict_clinical(self, age, hr, bp_sys, bp_dia, pain):
        features = np.array([[age, hr, bp_sys, bp_dia, pain]])
        scaled = self.models['scaler'].transform(features)
        pred = self.models['clinical'].predict(scaled)[0]
        prob = max(self.models['clinical'].predict_proba(scaled)[0])
        return pred, prob
    
    def predict_xray(self, image):
        img = image.resize((224, 224))
        arr = np.array(img) / 255.0
        if len(arr.shape) == 2:
            arr = np.stack([arr] * 3, axis=-1)
        arr = preprocess_input(np.expand_dims(arr, axis=0).astype(float))
        features = self.extractor.predict(arr, verbose=0)
        pca_features = self.models['pca'].transform(features)
        pred = self.models['xray'].predict(pca_features)[0]
        prob = max(self.models['xray'].predict_proba(pca_features)[0])
        return pred, prob
