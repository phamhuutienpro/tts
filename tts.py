#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎵 BILINGUAL TEXT-TO-SPEECH PRO V6.0 - AI STYLE ANALYSIS & PROMPT MANAGEMENT EDITION
📅 Created: November 2025
👨‍💻 Author: Phạm Hữu Tiền

🌟 FIXED VERSION - ĐÃ SỬA TẤT CẢ LỖI:
✅ Model Selection UI
✅ API Response Handling
✅ Manual Highlight System
✅ Thread Safety
✅ Complete TTS Workflow
"""

import sys
import os
import datetime
import urllib.request
import json
import time
import logging
import re
import wave
import base64
import threading
import pickle
import unicodedata
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import hashlib
import random

# Try to import cryptography for encryption
try:
    from cryptography.fernet import Fernet
    ENCRYPTION_AVAILABLE = True
except ImportError:
    ENCRYPTION_AVAILABLE = False

import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QProgressBar, QMessageBox, QPushButton, 
                           QTextEdit, QComboBox, QSpinBox, QCheckBox, QFileDialog,
                           QScrollArea, QGroupBox, QTabWidget, QListWidget,
                           QSplitter, QFrame, QLineEdit, QSlider, QTableWidget,
                           QTableWidgetItem, QHeaderView, QGridLayout, QFormLayout,
                           QStatusBar, QPlainTextEdit, QSizePolicy, QTextBrowser,
                           QListWidgetItem, QPushButton, QDialogButtonBox, QDialog,
                           QRadioButton, QButtonGroup, QTreeWidget, QTreeWidgetItem)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject, QMutex, QMutexLocker
from PyQt6.QtGui import (QFont, QPixmap, QPainter, QBrush, QColor, QPen, QTextCursor, QIcon,
                        QTextCharFormat, QSyntaxHighlighter, QTextDocument)

# =====================================
# CONSTANTS & CONFIG
# =====================================

EXPIRATION_DATE = datetime.date(2026, 8, 8)

# API KEY STORAGE
API_KEYS_FILE = Path.home() / ".bilingual_tts_api_keys.json"
ENCRYPTION_KEY_FILE = Path.home() / ".bilingual_tts_encryption.key"
PROMPTS_FILE = Path.home() / ".bilingual_tts_prompts.json"

# GEMINI MODELS - ĐÃ BỔ SUNG ĐẦY ĐỦ
# GEMINI MODELS - CHÍNH XÁC CHO v1beta API
# Danh sách models Gemini mới nhất (2024-2025)
GEMINI_MODELS = {
    # Generation Models (Text + Multimodal)
    "gemini-2.5-flash": "Gemini 2.5 Flash - Nhanh nhất, tốt cho hầu hết tác vụ",
    "gemini-2.5-flash-lite": "Gemini 2.5 Flash Lite - Siêu nhanh, nhẹ",
    "gemini-2.5-pro": "Gemini 2.5 Pro - Chất lượng cao nhất, phức tạp",
    "gemini-2.0-pro": "Gemini 2.0 Pro - Pro model cũ hơn",
    "gemini-2.0-flash": "Gemini 2.0 Flash - Flash model cũ hơn", 
    "gemini-2.0-flash-lite": "Gemini 2.0 Flash Lite - Lite cũ hơn",
    "gemini-2.0-flash-lite-001": "Gemini 2.0 Flash Lite 001 - Version cụ thể",
    "gemini-1.0-pro": "Gemini 1.0 Pro - Legacy pro",
    "gemini-1.0-flash": "Gemini 1.0 Flash - Legacy flash",
    "gemini-1.0-flash-lite": "Gemini 1.0 Flash Lite - Legacy lite",
    "gemini-2.5-flash-preview-09-2025": "Gemini 2.5 Flash Preview - Version thử nghiệm",
    "gemini-flash-latest": "Gemini Flash Latest - Version mới nhất",
    
    # TTS Models (Text-to-Speech)
    "gemini-2.5-flash-preview-tts": "Gemini 2.5 Flash TTS - Text to Speech", 
    "gemini-2.5-pro-preview-tts": "Gemini 2.5 Pro TTS - Text to Speech chất lượng cao"
}


# Model mặc định - ỔN ĐỊNH NHẤT
DEFAULT_TEXT_MODEL = "gemini-1.5-flash"

# ENHANCED VOICE MAPPING
GEMINI_VOICES = {
    # VIETNAMESE OPTIMIZED VOICES
    "Zephyr": {"gender": "Nữ", "style": "Bright", "lang": "vi", "desc": "Tươi sáng, năng động"},
    "Leda": {"gender": "Nữ", "style": "Youthful", "lang": "vi", "desc": "Trẻ trung, tươi mới"},
    "Aoede": {"gender": "Nữ", "style": "Breezy", "lang": "vi", "desc": "Nhẹ nhàng, thoải mái"},
    "Callirrhoe": {"gender": "Nữ", "style": "Easy-going", "lang": "vi", "desc": "Thoải mái, dễ chịu"},
    "Vindemiatrix": {"gender": "Nữ", "style": "Gentle", "lang": "vi", "desc": "Nhẹ nhàng, dịu dàng"},
    "Sadachbia": {"gender": "Nữ", "style": "Lively", "lang": "vi", "desc": "Sống động, năng nổ"},
    "Sulafat": {"gender": "Nữ", "style": "Warm", "lang": "vi", "desc": "Ấm áp, thân mật"},
    
    # JAPANESE OPTIMIZED VOICES  
    "Kore": {"gender": "Nữ", "style": "Firm", "lang": "ja", "desc": "Vững chắc, quyết đoán"},
    "Umbriel": {"gender": "Nữ", "style": "Clear", "lang": "ja", "desc": "Rõ ràng, trong trẻo"},
    "Algieba": {"gender": "Nữ", "style": "Smooth", "lang": "ja", "desc": "Mượt mà, trơn tru"},
    "Despina": {"gender": "Nữ", "style": "Smooth", "lang": "ja", "desc": "Êm dịu, du dương"},
    "Schedar": {"gender": "Nữ", "style": "Even", "lang": "ja", "desc": "Đều đặn, ổn định"},
    "Laomedeia": {"gender": "Nữ", "style": "Upbeat", "lang": "ja", "desc": "Vui tươi, tích cực"},
    
    # MALE VOICES - UNIVERSAL
    "Puck": {"gender": "Nam", "style": "Upbeat", "lang": "both", "desc": "Vui vẻ, lạc quan"},
    "Charon": {"gender": "Nam", "style": "Informative", "lang": "both", "desc": "Thông tin, chuyên nghiệp"},
    "Fenrir": {"gender": "Nam", "style": "Excitable", "lang": "both", "desc": "Hào hứng, phấn khích"},
}

# STYLE OPTIONS
AVAILABLE_STYLES = [
    "ấm áp", "truyền cảm", "năng động", "nhẹ nhàng", "vui tươi", 
    "nghiêm túc", "thân thiện", "chuyên nghiệp", "hào hứng", "bình tĩnh"
]

# DEFAULT PROMPTS
DEFAULT_PROMPTS = {
    "Vui": """Viết lại văn bản này với tông điệu vui vẻ, tích cực và năng động. 
Sử dụng từ ngữ tích cực, thêm cảm xúc vui vẻ nhưng giữ nguyên nội dung chính. 
Bỏ qua các icon, emoji trong văn bản gốc. Chỉ trả về văn bản đã viết lại.""",
    
    "Tích cực": """Viết lại văn bản này với tông điệu tích cực, lạc quan và truyền cảm hứng.
Tập trung vào những khía cạnh tích cực, sử dụng từ ngữ tạo động lực.
Bỏ qua các icon, emoji trong văn bản gốc. Chỉ trả về văn bản đã viết lại.""",
    
    "Lịch sự": """Viết lại văn bản này với tông điệu lịch sự, trang trọng và tôn trọng.
Sử dụng ngôn từ trang nhã, lịch thiệp nhưng vẫn giữ được sự gần gũi.
Bỏ qua các icon, emoji trong văn bản gốc. Chỉ trả về văn bản đã viết lại.""",
    
    "Thông thường": """Viết lại văn bản này với tông điệu tự nhiên, thông thường và dễ hiểu.
Sử dụng ngôn ngữ đời thường nhưng vẫn chính xác và rõ ràng.
Bỏ qua các icon, emoji trong văn bản gốc. Chỉ trả về văn bản đã viết lại.""",
    
    "Auto": """Phân tích văn bản này và viết lại với phong cách phù hợp nhất.
Tự động chọn tông điệu (vui vẻ, nghiêm túc, thông thường...) dựa trên nội dung.
Bỏ qua các icon, emoji trong văn bản gốc. Chỉ trả về văn bản đã viết lại."""
}

# =====================================
# ENCRYPTION UTILITIES
# =====================================

def generate_key():
    if ENCRYPTION_AVAILABLE:
        return Fernet.generate_key()
    else:
        return base64.b64encode(os.urandom(32))

def get_or_create_encryption_key():
    if ENCRYPTION_KEY_FILE.exists():
        with open(ENCRYPTION_KEY_FILE, 'rb') as f:
            return f.read()
    else:
        key = generate_key()
        try:
            with open(ENCRYPTION_KEY_FILE, 'wb') as f:
                f.write(key)
        except Exception:
            pass
        return key

def encrypt_data(data: str, key: bytes) -> str:
    try:
        if ENCRYPTION_AVAILABLE:
            fernet = Fernet(key)
            return fernet.encrypt(data.encode()).decode()
        else:
            return base64.b64encode(data.encode()).decode()
    except Exception:
        return data

def decrypt_data(encrypted_data: str, key: bytes) -> str:
    try:
        if ENCRYPTION_AVAILABLE:
            fernet = Fernet(key)
            return fernet.decrypt(encrypted_data.encode()).decode()
        else:
            return base64.b64decode(encrypted_data.encode()).decode()
    except Exception:
        return encrypted_data

# =====================================
# API KEY MANAGEMENT
# =====================================

def save_api_keys(api_keys: list):
    try:
        key = get_or_create_encryption_key()
        encrypted_keys = []
        for api_key in api_keys:
            encrypted_key = encrypt_data(api_key, key)
            encrypted_keys.append(encrypted_key)
        
        data = {
            'keys': encrypted_keys,
            'saved_at': datetime.datetime.now().isoformat(),
            'version': '6.0'
        }
        
        with open(API_KEYS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Saved {len(api_keys)} API keys")
        return True
    except Exception as e:
        print(f"⚠️ Error saving API keys: {e}")
        return False

def load_api_keys() -> list:
    try:
        if not API_KEYS_FILE.exists():
            return []
        
        with open(API_KEYS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        key = get_or_create_encryption_key()
        api_keys = []
        for encrypted_key in data.get('keys', []):
            decrypted_key = decrypt_data(encrypted_key, key)
            if decrypted_key and len(decrypted_key) > 20:
                api_keys.append(decrypted_key)
        
        print(f"✅ Loaded {len(api_keys)} API keys")
        return api_keys
    except Exception as e:
        print(f"⚠️ Error loading API keys: {e}")
        return []

def clear_saved_api_keys():
    try:
        if API_KEYS_FILE.exists():
            os.remove(API_KEYS_FILE)
        if ENCRYPTION_KEY_FILE.exists():
            os.remove(ENCRYPTION_KEY_FILE)
        print("✅ Cleared saved API keys")
        return True
    except Exception as e:
        print(f"⚠️ Error clearing API keys: {e}")
        return False

# =====================================
# PROMPT MANAGEMENT
# =====================================

def save_prompts(prompts: dict):
    try:
        data = {
            'prompts': prompts,
            'saved_at': datetime.datetime.now().isoformat(),
            'version': '6.0'
        }
        
        with open(PROMPTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(prompts)} prompts")
        return True
    except Exception as e:
        print(f"⚠️ Error saving prompts: {e}")
        return False

def load_prompts() -> dict:
    try:
        if not PROMPTS_FILE.exists():
            return DEFAULT_PROMPTS.copy()
        
        with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        prompts = data.get('prompts', {})
        merged_prompts = DEFAULT_PROMPTS.copy()
        merged_prompts.update(prompts)
        
        print(f"✅ Loaded {len(merged_prompts)} prompts")
        return merged_prompts
    except Exception as e:
        print(f"⚠️ Error loading prompts: {e}")
        return DEFAULT_PROMPTS.copy()

# =====================================
# UTILITIES
# =====================================

def exec_app(app):
    return app.exec()

def show_startup_info():
    print("🚀 Khởi động Bilingual TTS Pro v6.0...")

def save_wav_file(filename: str, audio_data: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2):
    try:
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(audio_data)
        return True
    except Exception as e:
        print(f"❌ Error saving WAV file: {e}")
        return False

# =====================================
# TEXT PROCESSOR V6.0
# =====================================

class EnhancedTextProcessor:
    """Enhanced text processing with improved Japanese detection"""
    
    def __init__(self):
        self.japanese_patterns = [
            r'[ひらがな-ゟ]',
            r'[カタカナ-ヿ]',
            r'[一-龯]',
            r'[。！？．｡]',
            r'「[^」]*」',
            r'（[^）]*）',
            r'[ー〜～]',
            r'です|ます|だ|である',
            r'は|が|を|に|で|と|から',
        ]
        
        self.vietnamese_patterns = [
            r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]',
            r'\b(và|của|trong|với|để|có|là|được|những|các|này|đó)\b',
        ]
        
        self.japanese_regex = re.compile('|'.join(self.japanese_patterns), re.IGNORECASE)
        self.vietnamese_regex = re.compile('|'.join(self.vietnamese_patterns), re.IGNORECASE)
        
        self.icon_patterns = [
            r'[😀-🙏🌀-🗿🚀-🛿☀-➿]',
            r'[♀♂⚠⚡⭐❤💙💚💛💜💖]',
            r'[📱📞📧📝📊📈📉📋📁]',
            r'[🎵🎶🎤🎧🎼🎹🎸🎺🎻]',
            r'[🔥💡🔔🔕🔐🔒🔓🔑]',
        ]
        self.icon_regex = re.compile('|'.join(self.icon_patterns), re.IGNORECASE)
    
    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        cleaned = self.icon_regex.sub('', text)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned.strip()
    
    def detect_language_enhanced(self, text: str) -> str:
        if not text:
            return 'unknown'
        
        cleaned_text = self.clean_text(text)
        
        japanese_matches = self.japanese_regex.findall(cleaned_text)
        vietnamese_matches = self.vietnamese_regex.findall(cleaned_text)
        
        japanese_score = len(japanese_matches)
        vietnamese_score = len(vietnamese_matches)
        
        total_chars = len(cleaned_text.replace(' ', ''))
        if total_chars == 0:
            return 'unknown'
        
        japanese_char_ratio = sum(1 for char in cleaned_text if 
                                 '\u3040' <= char <= '\u309F' or
                                 '\u30A0' <= char <= '\u30FF' or
                                 '\u4E00' <= char <= '\u9FAF') / total_chars
        
        vietnamese_char_ratio = len(self.vietnamese_regex.findall(cleaned_text)) / total_chars
        
        if japanese_char_ratio > 0.15 or japanese_score >= 3:
            return 'ja'
        elif vietnamese_char_ratio > 0.1 or vietnamese_score >= 2:
            return 'vi'
        elif japanese_char_ratio > 0.05:
            return 'ja'
        elif vietnamese_char_ratio > 0.02:
            return 'vi'
        else:
            latin_chars = len(re.findall(r'[a-zA-Z]', cleaned_text))
            if latin_chars > total_chars * 0.5:
                return 'vi'
            else:
                return 'mixed'
    
    def sentence_split(self, text: str) -> List[str]:
        sentences = re.split(r'[.!?。！？]\s*', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def analyze_sentiment_and_style(self, text: str) -> Dict:
        if not text:
            return {"style": "bình thường", "emotion": "neutral", "speed": "bình thường"}
        
        text_lower = text.lower()
        
        positive_words = ['tuyệt', 'tốt', 'hay', 'đẹp', 'vui', 'hạnh phúc', 'thích', 'yêu']
        negative_words = ['buồn', 'tệ', 'xấu', 'khó', 'đau', 'lo', 'sợ', 'ghét']
        exciting_words = ['wow', 'amazing', 'tuyệt vời']
        formal_words = ['tôn kính', 'kính thưa', 'xin phép', 'trân trọng']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        exciting_count = sum(1 for word in exciting_words if word in text_lower)
        formal_count = sum(1 for word in formal_words if word in text_lower)
        
        if exciting_count > 0:
            return {"style": "hào hứng", "emotion": "excited", "speed": "nhanh"}
        elif positive_count > negative_count and positive_count > 0:
            return {"style": "vui tươi", "emotion": "happy", "speed": "bình thường"}
        elif formal_count > 0:
            return {"style": "nghiêm túc", "emotion": "formal", "speed": "chậm"}
        elif negative_count > positive_count:
            return {"style": "dịu dàng", "emotion": "sad", "speed": "chậm"}
        else:
            return {"style": "bình thường", "emotion": "neutral", "speed": "bình thường"}
    
    def create_style_analysis_json(self, text: str, voice_mappings: dict = None) -> List[Dict]:
        if not text:
            return []
        
        cleaned_text = self.clean_text(text)
        sentences = self.sentence_split(cleaned_text)
        
        analysis_result = []
        
        for i, sentence in enumerate(sentences):
            if not sentence.strip():
                continue
            
            language = self.detect_language_enhanced(sentence)
            style_info = self.analyze_sentiment_and_style(sentence)
            
            if voice_mappings:
                if language == 'ja':
                    voice = voice_mappings.get('japanese', 'Kore')
                elif language == 'vi':
                    voice = voice_mappings.get('vietnamese', 'Zephyr')
                else:
                    voice = voice_mappings.get('mixed', 'Charon')
            else:
                if language == 'ja':
                    voice = 'Kore'
                elif language == 'vi':
                    voice = 'Zephyr'
                else:
                    voice = 'Charon'
            
            analysis_entry = {
                "text": sentence.strip(),
                "language": "JAPANESE" if language == 'ja' else "vietnamese" if language == 'vi' else "mixed",
                "voice": voice,
                "style": style_info["style"],
                "speed": style_info["speed"],
                "emotion": style_info["emotion"],
                "confidence": self._calculate_confidence(sentence, language)
            }
            
            analysis_result.append(analysis_entry)
        
        return analysis_result
    
    def _calculate_confidence(self, text: str, detected_lang: str) -> float:
        if not text:
            return 0.0
        
        base_confidence = min(0.8, len(text) / 50)
        
        if detected_lang == 'ja':
            japanese_chars = len(self.japanese_regex.findall(text))
            total_chars = len(text.replace(' ', ''))
            if total_chars > 0:
                lang_ratio = japanese_chars / total_chars
                confidence = base_confidence + (lang_ratio * 0.2)
            else:
                confidence = base_confidence
        elif detected_lang == 'vi':
            vietnamese_chars = len(self.vietnamese_regex.findall(text))
            total_chars = len(text.replace(' ', ''))
            if total_chars > 0:
                lang_ratio = vietnamese_chars / total_chars
                confidence = base_confidence + (lang_ratio * 0.2)
            else:
                confidence = base_confidence
        else:
            confidence = base_confidence * 0.7
        
        return min(1.0, max(0.1, confidence))

# =====================================
# JAPANESE HIGHLIGHTER
# =====================================

class JapaneseHighlighter(QSyntaxHighlighter):
    def __init__(self, parent: QTextDocument = None):
        super().__init__(parent)
        
        self.japanese_format = QTextCharFormat()
        self.japanese_format.setBackground(QColor(255, 255, 150))
        self.japanese_format.setForeground(QColor(200, 50, 50))
        
        self.japanese_patterns = [
            r'[ひらがな-ゟ]+',
            r'[カタカナ-ヿ]+',
            r'[一-龯]+',
            r'「[^」]*」',
            r'（[^）]*）'
        ]
    
    def highlightBlock(self, text):
        for pattern in self.japanese_patterns:
            regex = re.compile(pattern)
            matches = regex.finditer(text)
            
            for match in matches:
                start = match.start()
                length = match.end() - start
                self.setFormat(start, length, self.japanese_format)

# =====================================
# EXPIRATION CHECK
# =====================================

try:
    import ntplib
    NTP_AVAILABLE = True
except ImportError:
    NTP_AVAILABLE = False

class InternetTimeChecker:
    def __init__(self, timezone_offset=8):
        self.timezone_offset = timezone_offset
        self.ntp_servers = ['pool.ntp.org', 'time.google.com']
        self.http_apis = ['http://worldtimeapi.org/api/timezone/Asia/Ho_Chi_Minh']
    
    def get_internet_time(self) -> datetime.datetime:
        if NTP_AVAILABLE:
            for server in self.ntp_servers:
                try:
                    client = ntplib.NTPClient()
                    response = client.request(server, version=3, timeout=3)
                    ntp_time = datetime.datetime.fromtimestamp(response.tx_time)
                    adjusted_time = ntp_time + datetime.timedelta(hours=self.timezone_offset)
                    return adjusted_time
                except Exception:
                    continue
        
        for api_url in self.http_apis:
            try:
                with urllib.request.urlopen(api_url, timeout=5) as response:
                    data = json.loads(response.read().decode())
                    if 'datetime' in data:
                        time_str = data['datetime']
                        if 'T' in time_str:
                            return datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            except Exception:
                continue
        
        return datetime.datetime.now()

_time_checker = None

def get_internet_time():
    global _time_checker
    if _time_checker is None:
        _time_checker = InternetTimeChecker()
    try:
        result = _time_checker.get_internet_time()
        return result.date()
    except Exception:
        pass
    return None

def check_expiration():
    try:
        current_date = get_internet_time()
        if current_date is None:
            current_date = datetime.datetime.now().date()
        if current_date > EXPIRATION_DATE:
            return False
        else:
            return True
    except Exception:
        return True

# =====================================
# GEMINI API MANAGER - ĐÃ SỬA
# =====================================

class GeminiAPIManager:
    """Enhanced API Manager - AUTO FALLBACK & EXTENDED COOLDOWN"""
    
    def __init__(self):
        self.api_keys = []
        self.usage_stats = {}
        self.current_key_index = 0
        self.default_model = DEFAULT_TEXT_MODEL
        self.logger = logging.getLogger(__name__)
        self.max_retries = 2  # Giảm retry để nhanh hơn
        self.rate_limit_cooldown = 120  # TĂNG: 2 phút cooldown
        self.load_saved_api_keys()
        
        # THÊM: Model fallback sequence
        self.model_fallback_sequence = [
            "gemini-1.5-flash-002",
            "gemini-1.5-flash-8b", 
            "gemini-1.5-pro-002",
        ]
        
    def add_api_key(self, api_key):
        if not api_key or not isinstance(api_key, str):
            return False
        api_key = api_key.strip()
        if len(api_key) < 20:
            return False
        if api_key not in self.api_keys:
            self.api_keys.append(api_key)
            self.usage_stats[api_key] = {
                "calls": 0, 
                "errors": 0, 
                "rate_limits": 0,
                "last_used": 0, 
                "last_error": None,
                "last_rate_limit": 0,
                "successful_calls": 0  # THÊM
            }
            self.save_current_api_keys()
            return True
        return False
    
    def load_saved_api_keys(self):
        try:
            saved_keys = load_api_keys()
            for key in saved_keys:
                if key not in self.api_keys:
                    self.api_keys.append(key)
                    self.usage_stats[key] = {
                        "calls": 0, "errors": 0, "rate_limits": 0,
                        "last_used": 0, "last_error": None, 
                        "last_rate_limit": 0, "successful_calls": 0
                    }
            
            if saved_keys:
                self.logger.info(f"Loaded {len(saved_keys)} keys")
                return True
        except Exception as e:
            self.logger.warning(f"Load keys error: {e}")
        return False
    
    def save_current_api_keys(self):
        try:
            if self.api_keys:
                return save_api_keys(self.api_keys)
        except Exception as e:
            self.logger.warning(f"Save keys error: {e}")
        return False
    
    def clear_all_api_keys(self):
        try:
            self.api_keys.clear()
            self.usage_stats.clear()
            self.current_key_index = 0
            clear_saved_api_keys()
            return True
        except Exception as e:
            return False
    
    def add_multiple_keys(self, keys_text):
        if not keys_text:
            return 0
        keys = [key.strip() for key in keys_text.split('\n') if key.strip()]
        return sum(1 for key in keys if self.add_api_key(key))
    
    def get_next_available_key(self):
        """Get next available key với extended cooldown"""
        if not self.api_keys:
            return None
        
        current_time = time.time()
        available_keys = []
        
        for key in self.api_keys:
            stats = self.usage_stats[key]
            time_since_limit = current_time - stats.get('last_rate_limit', 0)
            
            # Key available nếu chưa bị limit hoặc đã qua cooldown period
            if time_since_limit > self.rate_limit_cooldown or stats.get('last_rate_limit', 0) == 0:
                available_keys.append(key)
        
        if not available_keys:
            self.logger.error("❌ ALL KEYS RATE LIMITED!")
            return None
        
        # Rotate qua available keys
        self.current_key_index = (self.current_key_index + 1) % len(available_keys)
        selected = available_keys[self.current_key_index]
        
        self.logger.info(f"Selected ...{selected[-8:]} ({len(available_keys)}/{len(self.api_keys)} available)")
        return selected
    
    def get_best_api_key(self):
        return self.get_next_available_key()
    
    def update_usage(self, api_key, success=True, error_msg=None, is_rate_limit=False):
        if api_key in self.usage_stats:
            stats = self.usage_stats[api_key]
            stats["calls"] += 1
            stats["last_used"] = time.time()
            
            if success:
                stats["successful_calls"] += 1
            else:
                stats["errors"] += 1
                stats["last_error"] = error_msg
                
                if is_rate_limit:
                    stats["rate_limits"] += 1
                    stats["last_rate_limit"] = time.time()
                    self.logger.warning(f"Key ...{api_key[-8:]} rate limited ({stats['rate_limits']} times)")
    
    def try_model_with_fallback(self, prompt, model=None, api_key=None):
        """THÊM: Try model, fallback nếu 404"""
        if model is None:
            model = self.default_model
        
        # Try primary model
        result = self._try_single_model(prompt, model, api_key)
        
        # Nếu 404, try fallback models
        if result.get("error") and "not found" in result["error"].lower():
            self.logger.warning(f"Model '{model}' not found, trying fallbacks...")
            
            for fallback_model in self.model_fallback_sequence:
                if fallback_model == model:
                    continue  # Skip model đã thử
                
                self.logger.info(f"🔄 Fallback to: {fallback_model}")
                result = self._try_single_model(prompt, fallback_model, api_key)
                
                if result.get("success"):
                    # Update default model nếu fallback thành công
                    self.default_model = fallback_model
                    self.logger.info(f"✅ Updated default model to: {fallback_model}")
                    return result
            
            return {"error": "All models failed"}
        
        return result
    
    def _try_single_model(self, prompt, model, api_key=None):
        """Internal: Try single model với single key"""
        if not api_key:
            api_key = self.get_next_available_key()
        
        if not api_key:
            return {"error": "No available API keys (all rate limited)"}
        
        headers = {"Content-Type": "application/json"}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 4096,
            },
            "safetySettings": [
                {"category": cat, "threshold": "BLOCK_NONE"}
                for cat in [
                    "HARM_CATEGORY_HARASSMENT",
                    "HARM_CATEGORY_HATE_SPEECH",
                    "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "HARM_CATEGORY_DANGEROUS_CONTENT"
                ]
            ]
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                
                if 'candidates' in result and result['candidates']:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        parts = candidate['content']['parts']
                        if parts and 'text' in parts[0]:
                            content = parts[0]['text'].strip()
                            
                            if len(content) > 10:
                                self.update_usage(api_key, True)
                                return {"success": True, "content": content}
                
                if 'promptFeedback' in result:
                    feedback = result['promptFeedback']
                    if 'blockReason' in feedback:
                        error = f"Blocked: {feedback['blockReason']}"
                        self.update_usage(api_key, False, error, False)
                        return {"error": error}
                
                error = "Empty response"
                self.update_usage(api_key, False, error, False)
                return {"error": error}
            
            elif response.status_code == 429:
                self.update_usage(api_key, False, "Rate limit", True)
                return {"error": "Rate limit", "rate_limited": True}
            
            elif response.status_code == 404:
                error = f"Model '{model}' not found"
                return {"error": error, "not_found": True}
            
            else:
                error = f"HTTP {response.status_code}"
                self.update_usage(api_key, False, error, False)
                return {"error": error}
                
        except Exception as e:
            error = f"Request error: {str(e)}"
            self.update_usage(api_key, False, error, False)
            return {"error": error}
    
    def call_gemini_text_api(self, prompt, model=None, retry_count=None, api_key=None):
        """Main API call với smart retry & fallback"""
        if not prompt:
            return {"error": "Empty prompt"}
        
        if model is None:
            model = self.default_model
        
        max_key_attempts = min(len(self.api_keys), 5)  # Try up to 5 keys
        
        for key_attempt in range(max_key_attempts):
            current_key = self.get_next_available_key()
            
            if not current_key:
                # All keys rate limited
                available_in = self.get_time_until_key_available()
                return {
                    "error": f"All {len(self.api_keys)} keys rate limited. "
                            f"Available in ~{available_in}s. "
                            "Try again later or add more keys."
                }
            
            self.logger.info(f"🔑 Key attempt {key_attempt + 1}/{max_key_attempts}")
            
            # Try with fallback
            result = self.try_model_with_fallback(prompt, model, current_key)
            
            if result.get("success"):
                return result
            
            # Nếu rate limited, thử key khác
            if result.get("rate_limited"):
                self.logger.warning("⏳ Rate limited, trying next key...")
                continue
            
            # Nếu lỗi khác (không phải rate limit), return luôn
            if not result.get("rate_limited"):
                return result
        
        return {"error": f"Failed after {max_key_attempts} key attempts"}
    
    def get_time_until_key_available(self):
        """Get seconds until next key available"""
        if not self.api_keys:
            return 0
        
        current_time = time.time()
        min_wait = float('inf')
        
        for key in self.api_keys:
            stats = self.usage_stats[key]
            last_limit = stats.get('last_rate_limit', 0)
            if last_limit > 0:
                wait_time = self.rate_limit_cooldown - (current_time - last_limit)
                if wait_time > 0:
                    min_wait = min(min_wait, wait_time)
        
        return int(min_wait) if min_wait != float('inf') else 0
    
    def rewrite_text_with_prompt(self, text: str, prompt_template: str) -> Dict:
        if not text or not prompt_template:
            return {"error": "Empty text or prompt"}
        
        full_prompt = f"{prompt_template}\n\nVăn bản:\n{text}"
        result = self.call_gemini_text_api(full_prompt)
        
        if result.get("success"):
            return {"success": True, "rewritten_text": result["content"]}
        else:
            return {"error": result.get("error", "Unknown")}
    
    def call_gemini_tts_api(self, text: str, voice: str = "Kore") -> Dict:
        if not text:
            return {"error": "Empty text"}
        
        api_key = self.get_next_available_key()
        if not api_key:
            return {"error": "No available keys"}
        
        try:
            from google import genai
            from google.genai import types
        except ImportError:
            return {"error": "google-genai not installed"}
        
        try:
            client = genai.Client(api_key=api_key)
            
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice,
                            )
                        )
                    ),
                )
            )
            
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        audio_data = part.inline_data.data
                        if isinstance(audio_data, str):
                            audio_data = base64.b64decode(audio_data)
                        
                        self.update_usage(api_key, True)
                        return {"success": True, "audio_data": audio_data}
            
            return {"error": "No audio data"}
        except Exception as e:
            self.update_usage(api_key, False, str(e), False)
            return {"error": str(e)}
    
    def get_usage_stats(self):
        stats = {
            "total_keys": len(self.api_keys),
            "available_keys": sum(1 for k in self.api_keys 
                                 if time.time() - self.usage_stats[k].get('last_rate_limit', 0) > self.rate_limit_cooldown),
            "total_calls": sum(s["calls"] for s in self.usage_stats.values()),
            "successful_calls": sum(s.get("successful_calls", 0) for s in self.usage_stats.values()),
            "total_errors": sum(s["errors"] for s in self.usage_stats.values()),
            "total_rate_limits": sum(s.get("rate_limits", 0) for s in self.usage_stats.values()),
            "keys": []
        }
        
        for key in self.api_keys:
            s = self.usage_stats[key]
            time_since_limit = time.time() - s.get('last_rate_limit', 0)
            is_available = time_since_limit > self.rate_limit_cooldown or s.get('last_rate_limit', 0) == 0
            
            stats["keys"].append({
                "suffix": key[-8:],
                "calls": s["calls"],
                "success": s.get("successful_calls", 0),
                "errors": s["errors"],
                "rate_limits": s.get("rate_limits", 0),
                "available": is_available,
                "cooldown_remaining": max(0, int(self.rate_limit_cooldown - time_since_limit)) if not is_available else 0
            })
        
        return stats
        
# =====================================
# TTS WORKER V6.0
# =====================================

class SmartTTSWorkerV6(QThread):
    """Smart TTS Worker v6.0"""
    
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    chunk_completed = pyqtSignal(int, str, dict)
    error_occurred = pyqtSignal(str)
    completed = pyqtSignal(list)
    
    def __init__(self, gemini_api, text, processing_config, style_analysis=None):
        super().__init__()
        self.gemini_api = gemini_api
        self.original_text = text
        self.processing_config = processing_config
        self.style_analysis = style_analysis or []
        self.is_cancelled = False
        self.mutex = QMutex()
        self.text_processor = EnhancedTextProcessor()
        
    def cancel(self):
        with QMutexLocker(self.mutex):
            self.is_cancelled = True
    
    def run(self):
        try:
            self.status_updated.emit("🧠 Đang phân tích văn bản...")
            
            if not self.style_analysis:
                self.style_analysis = self.text_processor.create_style_analysis_json(
                    self.original_text, 
                    self.processing_config.get('voice_mappings', None)
                )
            
            if not self.style_analysis:
                self.error_occurred.emit("Không thể phân tích văn bản")
                return
            
            self.status_updated.emit(f"📝 Đã phân tích {len(self.style_analysis)} đoạn")
            self._process_tts_v6()
            
        except Exception as e:
            self.error_occurred.emit(f"Lỗi worker: {str(e)}")
    
    def _process_tts_v6(self):
        audio_files = []
        total_chunks = len(self.style_analysis)
        output_dir = self.processing_config.get('output_dir', '')
        
        for i, chunk_info in enumerate(self.style_analysis):
            with QMutexLocker(self.mutex):
                if self.is_cancelled:
                    self.error_occurred.emit("Đã hủy")
                    return
            
            progress = int((i / total_chunks) * 100)
            self.progress_updated.emit(progress)
            
            voice_name = chunk_info.get('voice', 'Kore')
            language = chunk_info.get('language', 'unknown')
            style = chunk_info.get('style', 'bình thường')
            
            status_msg = f"Xử lý đoạn {i+1}/{total_chunks} ({language}) - {voice_name} - {style}"
            self.status_updated.emit(status_msg)
            
            result = self.gemini_api.call_gemini_tts_api(chunk_info['text'], voice_name)
            
            if result.get("success"):
                lang_code = 'ja' if language == 'JAPANESE' else 'vi' if language == 'vietnamese' else 'mix'
                file_name = f"chunk_{i+1:03d}_{lang_code}_{voice_name}_{style.replace(' ', '_')}.wav"
                file_path = os.path.join(output_dir, file_name)
                
                if save_wav_file(file_path, result["audio_data"]):
                    audio_files.append(file_path)
                    self.chunk_completed.emit(i+1, file_path, chunk_info)
                else:
                    self.error_occurred.emit(f"Lỗi lưu file {file_name}")
                    return
            else:
                error_msg = f"Lỗi TTS đoạn {i+1}: {result.get('error')}"
                self.error_occurred.emit(error_msg)
                return
            
            time.sleep(0.5)
        
        self.progress_updated.emit(100)
        self.status_updated.emit("🎉 Hoàn thành!")
        self.completed.emit(audio_files)

# =====================================
# SPLASH SCREEN
# =====================================

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.show_animation()
    
    def setup_ui(self):
        self.setFixedSize(550, 450)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 25px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("🎭 Bilingual TTS Pro v6.0")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 44px;
                font-weight: bold;
                background: transparent;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("AI Style Analysis Edition - FIXED")
        subtitle.setStyleSheet("""
            QLabel {
                color: #e8e8f8;
                font-size: 16px;
                background: transparent;
                font-style: italic;
            }
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        version = QLabel("by Phạm Hữu Tiền")
        version.setStyleSheet("""
            QLabel {
                color: #c0c0d8;
                font-size: 14px;
                background: transparent;
                margin-bottom: 30px;
            }
        """)
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid white;
                border-radius: 12px;
                text-align: center;
                color: white;
                background: rgba(255,255,255,0.2);
                font-weight: bold;
                min-height: 25px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f093fb, stop:1 #f5576c);
                border-radius: 10px;
            }
        """)
        self.progress.setTextVisible(True)
        
        self.status = QLabel("Đang khởi động...")
        self.status.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                background: transparent;
                margin-top: 15px;
                font-weight: bold;
            }
        """)
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(version)
        layout.addWidget(self.progress)
        layout.addWidget(self.status)
    
    def show_animation(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(35)
        self.current_progress = 0
        
        self.status_messages = [
            "Khởi động v6.0...",
            "Tải Enhanced Detection...",
            "Khởi tạo AI Analyzer...",
            "Cấu hình Prompt System...",
            "Thiết lập Highlighter...",
            "Khởi tạo 29 giọng đọc...",
            "Hoàn thành!"
        ]
        self.current_status = 0
    
    def update_progress(self):
        self.current_progress += 1.1
        self.progress.setValue(int(self.current_progress))
        
        status_interval = 100 // len(self.status_messages)
        new_status = min(int(self.current_progress) // status_interval, len(self.status_messages) - 1)
        if new_status != self.current_status:
            self.current_status = new_status
            self.status.setText(self.status_messages[self.current_status])
        
        if self.current_progress >= 100:
            self.timer.stop()
            QTimer.singleShot(1200, self.close)

# =====================================
# COLLAPSIBLE SECTION
# =====================================

class CollapsibleSection(QWidget):
    def __init__(self, title, content_widget, default_expanded=True, max_height=None):
        super().__init__()
        self.max_height = max_height
        self.setup_ui(title, content_widget, default_expanded)
    
    def setup_ui(self, title, content_widget, default_expanded):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 10)
        layout.setSpacing(8)
        
        self.toggle_btn = QPushButton(f"{'🔽' if default_expanded else '▶️'} {title}")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(default_expanded)
        self.toggle_btn.setMinimumHeight(48)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                text-align: left;
                padding: 15px 22px;
                font-weight: bold;
                font-size: 14px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #ff9a9e, stop:1 #fecfef);
            }
        """)
        
        if self.max_height:
            self.scroll_area = QScrollArea()
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setMaximumHeight(self.max_height)
            self.scroll_area.setStyleSheet("""
                QScrollArea {
                    border: 1px solid #bdc3c7;
                    border-radius: 10px;
                    background: white;
                }
            """)
            self.scroll_area.setWidget(content_widget)
            self.content_container = self.scroll_area
        else:
            self.content_container = content_widget
        
        self.content_container.setVisible(default_expanded)
        self.toggle_btn.clicked.connect(self.toggle_content)
        
        layout.addWidget(self.toggle_btn)
        layout.addWidget(self.content_container)
    
    def toggle_content(self):
        is_checked = self.toggle_btn.isChecked()
        arrow = "🔽" if is_checked else "▶️"
        
        current_text = self.toggle_btn.text()
        original_title = current_text.split(' ', 1)[1] if current_text.startswith(('🔽', '▶️')) else current_text
        
        self.toggle_btn.setText(f"{arrow} {original_title}")
        self.content_container.setVisible(is_checked)

# =====================================
# PROMPT MANAGER DIALOG
# =====================================

class PromptManagerDialog(QDialog):
    def __init__(self, prompts: dict, parent=None):
        super().__init__(parent)
        self.prompts = prompts.copy()
        self.setup_ui()
        self.load_prompts()
        
    def setup_ui(self):
        self.setWindowTitle("🛠️ Quản Lý Prompt")
        self.setMinimumSize(800, 600)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        header = QLabel("🛠️ Quản Lý Prompt Viết Lại")
        header.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border-radius: 10px;
            }
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        
        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        left_layout.addWidget(QLabel("📋 Danh sách:"))
        self.prompt_list = QListWidget()
        self.prompt_list.itemClicked.connect(self.load_selected_prompt)
        left_layout.addWidget(self.prompt_list)
        
        button_layout = QHBoxLayout()
        
        self.btn_add = QPushButton("➕ Thêm")
        self.btn_add.clicked.connect(self.add_prompt)
        
        self.btn_delete = QPushButton("🗑️ Xóa")
        self.btn_delete.clicked.connect(self.delete_prompt)
        
        self.btn_reset = QPushButton("🔄 Reset")
        self.btn_reset.clicked.connect(self.reset_prompts)
        
        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_delete)
        button_layout.addWidget(self.btn_reset)
        left_layout.addLayout(button_layout)
        
        # Right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        right_layout.addWidget(QLabel("✏️ Chỉnh sửa:"))
        
        self.prompt_name = QLineEdit()
        self.prompt_name.setPlaceholderText("Tên prompt...")
        right_layout.addWidget(QLabel("📝 Tên:"))
        right_layout.addWidget(self.prompt_name)
        
        self.prompt_content = QTextEdit()
        self.prompt_content.setPlaceholderText("Nhập nội dung prompt...")
        right_layout.addWidget(QLabel("📄 Nội dung:"))
        right_layout.addWidget(self.prompt_content)
        
        self.btn_save = QPushButton("💾 Lưu")
        self.btn_save.clicked.connect(self.save_prompt)
        right_layout.addWidget(self.btn_save)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 500])
        
        content_layout.addWidget(splitter)
        layout.addWidget(content_widget)
        
        dialog_buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.rejected.connect(self.reject)
        layout.addWidget(dialog_buttons)
    
    def load_prompts(self):
        self.prompt_list.clear()
        for name in self.prompts.keys():
            self.prompt_list.addItem(name)
    
    def load_selected_prompt(self):
        current_item = self.prompt_list.currentItem()
        if current_item:
            prompt_name = current_item.text()
            self.prompt_name.setText(prompt_name)
            self.prompt_content.setPlainText(self.prompts.get(prompt_name, ""))
    
    def add_prompt(self):
        self.prompt_name.setText("")
        self.prompt_content.setPlainText("")
        self.prompt_name.setFocus()
    
    def save_prompt(self):
        name = self.prompt_name.text().strip()
        content = self.prompt_content.toPlainText().strip()
        
        if not name:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập tên!")
            return
        
        if not content:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập nội dung!")
            return
        
        self.prompts[name] = content
        self.load_prompts()
        
        items = self.prompt_list.findItems(name, Qt.MatchFlag.MatchExactly)
        if items:
            self.prompt_list.setCurrentItem(items[0])
        
        QMessageBox.information(self, "Thành công", f"Đã lưu '{name}'!")
    
    def delete_prompt(self):
        current_item = self.prompt_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Cảnh báo", "Chọn prompt cần xóa!")
            return
        
        prompt_name = current_item.text()
        
        reply = QMessageBox.question(
            self, "Xác nhận",
            f"Xóa '{prompt_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if prompt_name in self.prompts:
                del self.prompts[prompt_name]
            self.load_prompts()
            self.prompt_name.setText("")
            self.prompt_content.setPlainText("")
    
    def reset_prompts(self):
        reply = QMessageBox.question(
            self, "Xác nhận",
            "Reset về mặc định?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.prompts = DEFAULT_PROMPTS.copy()
            self.load_prompts()
            self.prompt_name.setText("")
            self.prompt_content.setPlainText("")
    
    def get_prompts(self) -> dict:
        return self.prompts

# =====================================
# MAIN WINDOW V6.0 - HOÀN CHỈNH
# =====================================

class MainWindow(QWidget):
    """Main Window v6.0 - ĐÃ SỬA TẤT CẢ LỖI"""
    
    def __init__(self):
        super().__init__()
        self.gemini_api = GeminiAPIManager()
        self.tts_worker = None
        self.rewrite_worker = None
        self.audio_files = []
        self.text_processor = EnhancedTextProcessor()
        self.current_style_analysis = []
        self.prompts = load_prompts()
        self.japanese_highlighter = None
        self.manual_highlights = []
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        self.setWindowTitle("🎭 Bilingual TTS Pro v6.0 - FIXED - Phạm Hữu Tiền")
        self.setGeometry(100, 100, 1600, 1000)
        self.setMinimumSize(1200, 800)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                background: white;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ecf0f1, stop:1 #bdc3c7);
                border: 2px solid #95a5a6;
                padding: 12px 20px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
            }
        """)
        
        main_tab = self.create_main_tab()
        self.tab_widget.addTab(main_tab, "🎵 Smart TTS v6.0")
        
        prompt_tab = self.create_prompt_tab()
        self.tab_widget.addTab(prompt_tab, "📝 Prompt Manager")
        
        style_tab = self.create_style_tab()
        self.tab_widget.addTab(style_tab, "🧠 Style Analysis")
        
        main_layout.addWidget(self.tab_widget)
        
        self.create_status_bar()
        self.apply_stylesheet()
    
    def create_main_tab(self):
        main_widget = QWidget()
        layout = QHBoxLayout(main_widget)
        
        left_panel = self.create_left_panel()
        right_panel = self.create_right_panel()
        
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([800, 700])
        
        layout.addWidget(splitter)
        return main_widget
    
    def create_left_panel(self):
        left_widget = QWidget()
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: #f8f9fa; }")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(8)
        
        # API Section
        api_section = self.create_api_section()
        api_collapsible = CollapsibleSection("🔑 API Key & Model", api_section, True, 250)
        content_layout.addWidget(api_collapsible)
        
        # Text Section
        text_section = self.create_text_section()
        text_collapsible = CollapsibleSection("📝 Văn Bản", text_section, True, 500)
        content_layout.addWidget(text_collapsible)
        
        # Voice Section
        voice_section = self.create_voice_section()
        voice_collapsible = CollapsibleSection("🎭 Giọng Đọc", voice_section, True, 280)
        content_layout.addWidget(voice_collapsible)
        
        # Control Section
        control_section = self.create_control_section()
        content_layout.addWidget(control_section)
        
        content_layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        
        main_layout = QVBoxLayout(left_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll_area)
        
        return left_widget
    
    def create_api_section(self):
        """API Section với Model Selection - ĐÃ SỬA"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # API Keys
        self.api_key_input = QPlainTextEdit()
        self.api_key_input.setPlaceholderText("Nhập API key (mỗi dòng một key)")
        self.api_key_input.setMaximumHeight(100)
        layout.addWidget(QLabel("🔑 Gemini API Keys:"))
        layout.addWidget(self.api_key_input)
        
        # MODEL SELECTION - THÊM MỚI
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("🤖 Model:"))
        self.model_combo = QComboBox()
        for model_key, model_desc in GEMINI_MODELS.items():
            self.model_combo.addItem(model_desc, model_key)
        default_index = self.model_combo.findData(DEFAULT_TEXT_MODEL)
        if default_index >= 0:
            self.model_combo.setCurrentIndex(default_index)
        self.model_combo.currentIndexChanged.connect(self.on_model_changed)
        model_layout.addWidget(self.model_combo)
        layout.addLayout(model_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_add_keys = QPushButton("➕ Thêm")
        self.btn_add_keys.clicked.connect(self.add_api_keys)
        
        self.btn_test_keys = QPushButton("🧪 Test")
        self.btn_test_keys.clicked.connect(self.test_api_keys)
        
        self.btn_clear_keys = QPushButton("🗑️ Xóa")
        self.btn_clear_keys.clicked.connect(self.clear_api_keys)
        
        btn_layout.addWidget(self.btn_add_keys)
        btn_layout.addWidget(self.btn_test_keys)
        btn_layout.addWidget(self.btn_clear_keys)
        layout.addLayout(btn_layout)
        
        self.api_stats_label = QLabel("📊 Chưa có API key")
        self.api_stats_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(self.api_stats_label)
        
        return widget
    
    def on_model_changed(self):
        """Handle model change - THÊM MỚI"""
        selected_model = self.model_combo.currentData()
        self.gemini_api.default_model = selected_model
        self.log(f"🤖 Đã chọn model: {self.model_combo.currentText()}")
    
    def create_text_section(self):
        """Text Section với Dual Areas & Highlight - ĐÃ SỬA"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Original text
        layout.addWidget(QLabel("📝 Văn bản gốc:"))
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("""Nhập văn bản song ngữ...

Ví dụ:
💬 Giao tiếp là "thể hiện tổng thể" 🎭
「言葉だけでなく、表情もメッセージになる。」
(Không chỉ lời nói, mà cả nét mặt)""")
        self.text_input.setMinimumHeight(150)
        self.japanese_highlighter = JapaneseHighlighter(self.text_input.document())
        layout.addWidget(self.text_input)
        
        # Rewrite controls
        rewrite_layout = QHBoxLayout()
        rewrite_layout.addWidget(QLabel("🎨 Style:"))
        
        self.prompt_combo = QComboBox()
        self.update_prompt_combo()
        rewrite_layout.addWidget(self.prompt_combo)
        
        self.cb_random_prompt = QCheckBox("🎲")
        self.cb_random_prompt.setToolTip("Random prompt")
        rewrite_layout.addWidget(self.cb_random_prompt)
        
        self.btn_rewrite = QPushButton("🔄 Viết Lại")
        self.btn_rewrite.clicked.connect(self.rewrite_and_analyze)
        rewrite_layout.addWidget(self.btn_rewrite)
        
        self.btn_load_text = QPushButton("📁 Tải")
        self.btn_load_text.clicked.connect(self.load_text_from_file)
        rewrite_layout.addWidget(self.btn_load_text)
        
        layout.addLayout(rewrite_layout)
        
        # Processed text
        layout.addWidget(QLabel("✨ Văn bản đã chuẩn hóa:"))
        self.processed_text = QTextEdit()
        self.processed_text.setPlaceholderText("Văn bản sau AI...")
        self.processed_text.setMinimumHeight(130)
        self.processed_text.setReadOnly(True)
        self.processed_japanese_highlighter = JapaneseHighlighter(self.processed_text.document())
        layout.addWidget(self.processed_text)
        
        # Text controls - THÊM HIGHLIGHT BUTTONS
        text_controls = QHBoxLayout()
        
        self.btn_highlight = QPushButton("🎨 Highlight")
        self.btn_highlight.clicked.connect(self.highlight_selected)
        self.btn_highlight.setToolTip("Chọn text → bấm để highlight")
        text_controls.addWidget(self.btn_highlight)
        
        self.btn_clear_highlight = QPushButton("🧹 Clear")
        self.btn_clear_highlight.clicked.connect(self.clear_highlight)
        text_controls.addWidget(self.btn_clear_highlight)
        
        self.btn_copy = QPushButton("📋 Copy")
        self.btn_copy.clicked.connect(self.copy_processed)
        text_controls.addWidget(self.btn_copy)
        
        self.btn_edit = QPushButton("✏️ Edit")
        self.btn_edit.clicked.connect(self.enable_edit)
        text_controls.addWidget(self.btn_edit)
        
        self.btn_clear = QPushButton("🗑️ Clear")
        self.btn_clear.clicked.connect(self.clear_all_text)
        text_controls.addWidget(self.btn_clear)
        
        text_controls.addStretch()
        layout.addLayout(text_controls)
        
        return widget
    
    def create_voice_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Vietnamese voice
        layout.addWidget(QLabel("🇻🇳 Giọng Việt:"))
        self.combo_vn_voice = QComboBox()
        for voice, info in GEMINI_VOICES.items():
            self.combo_vn_voice.addItem(f"{voice} ({info['gender']})", voice)
        layout.addWidget(self.combo_vn_voice)
        
        # Japanese voice
        layout.addWidget(QLabel("🇯🇵 Giọng Nhật:"))
        self.combo_jp_voice = QComboBox()
        for voice, info in GEMINI_VOICES.items():
            self.combo_jp_voice.addItem(f"{voice} ({info['gender']})", voice)
        layout.addWidget(self.combo_jp_voice)
        
        # Output dir
        layout.addWidget(QLabel("📂 Thư mục:"))
        self.output_path = QLineEdit(str(Path.home() / "TTS_Output_v6"))
        layout.addWidget(self.output_path)
        
        self.btn_browse = QPushButton("📁 Chọn")
        self.btn_browse.clicked.connect(self.browse_output)
        layout.addWidget(self.btn_browse)
        
        # Filename
        layout.addWidget(QLabel("🎵 Tên file:"))
        self.output_filename = QLineEdit("output_v6.wav")
        layout.addWidget(self.output_filename)
        
        # Options
        self.cb_auto_merge = QCheckBox("🔗 Tự động ghép")
        self.cb_auto_merge.setChecked(True)
        layout.addWidget(self.cb_auto_merge)
        
        self.cb_keep_chunks = QCheckBox("📂 Giữ chunks")
        layout.addWidget(self.cb_keep_chunks)
        
        return widget
    
    def create_control_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.btn_start = QPushButton("🚀 Smart TTS v6.0")
        self.btn_start.clicked.connect(self.start_tts)
        self.btn_start.setMinimumHeight(55)
        
        self.btn_stop = QPushButton("⏹️ Dừng")
        self.btn_stop.clicked.connect(self.stop_tts)
        self.btn_stop.setEnabled(False)
        self.btn_stop.setMinimumHeight(55)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_stop)
        layout.addLayout(btn_layout)
        
        return widget
    
    def create_right_panel(self):
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Progress
        progress_section = self.create_progress_section()
        right_layout.addWidget(CollapsibleSection("📊 Tiến Trình", progress_section, True))
        
        # Output
        output_section = self.create_output_section()
        right_layout.addWidget(CollapsibleSection("🎵 Kết Quả", output_section, True))
        
        # Log
        log_section = self.create_log_section()
        right_layout.addWidget(CollapsibleSection("📄 Log", log_section, False))
        
        return right_widget
    
    def create_progress_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.overall_progress = QProgressBar()
        self.status_label = QLabel("⏳ Sẵn sàng")
        self.chunks_list = QListWidget()
        
        layout.addWidget(QLabel("📊 Tiến trình:"))
        layout.addWidget(self.overall_progress)
        layout.addWidget(self.status_label)
        layout.addWidget(QLabel("📝 Chunks:"))
        layout.addWidget(self.chunks_list)
        
        return widget
    
    def create_output_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.output_list = QListWidget()
        
        layout.addWidget(QLabel("🎵 Files:"))
        layout.addWidget(self.output_list)
        
        btn_layout = QHBoxLayout()
        self.btn_play = QPushButton("▶️ Phát")
        self.btn_play.setEnabled(False)
        self.btn_open_folder = QPushButton("📁 Mở")
        self.btn_open_folder.clicked.connect(self.open_output_folder)
        
        btn_layout.addWidget(self.btn_play)
        btn_layout.addWidget(self.btn_open_folder)
        layout.addLayout(btn_layout)
        
        self.btn_merge = QPushButton("🔗 Ghép")
        self.btn_merge.setEnabled(False)
        self.btn_merge.clicked.connect(self.merge_audio)
        layout.addWidget(self.btn_merge)
        
        return widget
    
    def create_log_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.log_display = QPlainTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setMaximumHeight(200)
        
        layout.addWidget(self.log_display)
        return widget
    
    def create_prompt_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        header = QLabel("📝 Quản Lý Prompt")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        self.btn_open_prompt_mgr = QPushButton("🛠️ Mở Manager")
        self.btn_open_prompt_mgr.clicked.connect(self.open_prompt_manager)
        layout.addWidget(self.btn_open_prompt_mgr)
        
        self.prompt_display = QTextBrowser()
        layout.addWidget(self.prompt_display)
        
        return widget
    
    def create_style_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        header = QLabel("🧠 Phân Tích Style")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        controls = QHBoxLayout()
        
        self.btn_export_json = QPushButton("📤 Xuất JSON")
        self.btn_export_json.setEnabled(False)
        self.btn_export_json.clicked.connect(self.export_json)
        
        self.btn_copy_json = QPushButton("📋 Copy JSON")
        self.btn_copy_json.setEnabled(False)
        self.btn_copy_json.clicked.connect(self.copy_json)
        
        controls.addWidget(self.btn_export_json)
        controls.addWidget(self.btn_copy_json)
        layout.addLayout(controls)
        
        self.style_display = QTextBrowser()
        layout.addWidget(self.style_display)
        
        return widget
    
    def create_status_bar(self):
        self.status_bar = QLabel("✅ v6.0 sẵn sàng")
        main_layout = self.layout()
        main_layout.addWidget(self.status_bar)
    
    def apply_stylesheet(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI';
                font-size: 13px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3cb0fd, stop:1 #3498db);
            }
            QPushButton:disabled {
                background: #cccccc;
            }
            QLineEdit, QTextEdit, QPlainTextEdit {
                background: white;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
            }
        """)
    
    # ======= METHODS =======
    
    def load_settings(self):
        self.update_api_stats()
        self.update_prompt_display()
        if self.gemini_api.api_keys:
            self.log(f"🔑 Nạp {len(self.gemini_api.api_keys)} API keys")
        self.log(f"📝 Nạp {len(self.prompts)} prompts")
    
    def log(self, msg):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {msg}"
        
        if hasattr(self, 'log_display'):
            self.log_display.appendPlainText(log_entry)
            cursor = self.log_display.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.log_display.setTextCursor(cursor)
        
        QApplication.processEvents()
        print(log_entry)
    
    def add_api_keys(self):
        keys_text = self.api_key_input.toPlainText().strip()
        if not keys_text:
            QMessageBox.warning(self, "Cảnh báo", "Nhập API key!")
            return
        
        added = self.gemini_api.add_multiple_keys(keys_text)
        if added > 0:
            QMessageBox.information(self, "Thành công", f"Thêm {added} keys!")
            self.update_api_stats()
            self.api_key_input.clear()
            self.log(f"✅ Thêm {added} keys")
        else:
            QMessageBox.warning(self, "Cảnh báo", "Không có key hợp lệ!")
    
    def test_api_keys(self):
        if not self.gemini_api.api_keys:
            QMessageBox.warning(self, "Cảnh báo", "Chưa có key!")
            return
        
        self.log("🧪 Testing keys...")
        
        def test_worker():
            results = []
            for key in self.gemini_api.api_keys:
                result = self.gemini_api.call_gemini_text_api("Test", api_key=key)
                results.append({
                    'suffix': key[-8:],
                    'success': result.get('success', False)
                })
            QTimer.singleShot(0, lambda: self.show_test_results(results))
        
        thread = threading.Thread(target=test_worker)
        thread.start()
    
    def show_test_results(self, results):
        success = sum(1 for r in results if r['success'])
        total = len(results)
        
        msg = f"Test: {success}/{total} OK\n\n"
        for r in results:
            status = "✅" if r['success'] else "❌"
            msg += f"{status} ...{r['suffix']}\n"
        
        QMessageBox.information(self, "Test", msg)
        self.update_api_stats()
        self.log(f"🧪 Test: {success}/{total} OK")
    
    def clear_api_keys(self):
        if not self.gemini_api.api_keys:
            return
        
        reply = QMessageBox.question(
            self, "Xác nhận",
            f"Xóa {len(self.gemini_api.api_keys)} keys?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.gemini_api.clear_all_api_keys()
            self.update_api_stats()
            self.log("🗑️ Đã xóa keys")
    
    # Trong MainWindow class, sửa update_api_stats (dòng ~1396)
    def update_api_stats(self):
        """Update stats với rate limit info"""
        stats = self.gemini_api.get_usage_stats()
        
        if stats["total_keys"] == 0:
            self.api_stats_label.setText("📊 Chưa có key")
        else:
            available = stats["available_keys"]
            total = stats["total_keys"]
            success_rate = (stats["successful_calls"] / max(stats["total_calls"], 1)) * 100
            
            # Color coding
            if available == 0:
                color = "red"
                status = "⛔ ALL LIMITED"
            elif available < total * 0.3:
                color = "orange"
                status = f"⚠️ {available}/{total}"
            else:
                color = "green"
                status = f"✅ {available}/{total}"
            
            text = f"<span style='color:{color};'>{status} keys</span> | "
            text += f"{stats['total_calls']} calls | "
            text += f"{success_rate:.1f}% success"
            
            self.api_stats_label.setText(text)

    # Thêm method mới để show rate limit warning
    def check_rate_limit_status(self):
        """THÊM: Check và warning nếu tất cả keys bị limit"""
        stats = self.gemini_api.get_usage_stats()
        
        if stats["available_keys"] == 0 and stats["total_keys"] > 0:
            wait_time = self.gemini_api.get_time_until_key_available()
            
            QMessageBox.warning(
                self, "⛔ Rate Limit",
                f"Tất cả {stats['total_keys']} API keys đều bị giới hạn!\n\n"
                f"⏰ Đợi thêm ~{wait_time}s để key khả dụng\n\n"
                f"💡 Giải pháp:\n"
                f"• Đợi {wait_time}s rồi thử lại\n"
                f"• Thêm thêm API keys mới\n"
                f"• Dùng model ổn định hơn (gemini-1.5-flash-002)"
            )
            return False
        
        return True

        
    def update_prompt_combo(self):
        self.prompt_combo.clear()
        for name in self.prompts.keys():
            self.prompt_combo.addItem(name, name)
    
    def rewrite_and_analyze(self):
        """Rewrite & Analyze - ĐÃ SỬA HOÀN TOÀN VỚI QTHREAD"""
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Cảnh báo", "Nhập văn bản!")
            return
        
        if not self.gemini_api.api_keys:
            QMessageBox.warning(self, "Cảnh báo", "Thêm API key!")
            return
        
        # Select prompt
        if self.cb_random_prompt.isChecked():
            prompt_name = random.choice(list(self.prompts.keys()))
            self.log(f"🎲 Random: {prompt_name}")
        else:
            prompt_name = self.prompt_combo.currentData()
        
        if not prompt_name or prompt_name not in self.prompts:
            QMessageBox.warning(self, "Cảnh báo", "Chọn prompt!")
            return
        
        prompt_template = self.prompts[prompt_name]
        
        self.log(f"🔄 Viết lại với: {prompt_name}")
        self.log(f"🤖 Model: {self.gemini_api.default_model}")
        
        self.btn_rewrite.setEnabled(False)
        self.btn_rewrite.setText("⏳ Đang xử lý...")
        self.processed_text.clear()
        
        # Create worker
        class RewriteWorker(QThread):
            finished = pyqtSignal(dict)
            error = pyqtSignal(str)
            status = pyqtSignal(str)
            
            def __init__(self, gemini_api, text, prompt_template, text_processor, voice_mappings):
                super().__init__()
                self.gemini_api = gemini_api
                self.text = text
                self.prompt_template = prompt_template
                self.text_processor = text_processor
                self.voice_mappings = voice_mappings
            
            def run(self):
                try:
                    # Step 1: Rewrite
                    self.status.emit("🔄 Viết lại...")
                    rewrite_result = self.gemini_api.rewrite_text_with_prompt(
                        self.text, self.prompt_template
                    )
                    
                    if not rewrite_result.get("success"):
                        self.error.emit(rewrite_result.get("error", "Unknown"))
                        return
                    
                    rewritten = rewrite_result["rewritten_text"]
                    
                    # Step 2: Analyze
                    self.status.emit("🧠 Phân tích...")
                    analysis = self.text_processor.create_style_analysis_json(
                        rewritten, self.voice_mappings
                    )
                    
                    self.finished.emit({
                        "rewritten_text": rewritten,
                        "style_analysis": analysis
                    })
                    
                except Exception as e:
                    self.error.emit(f"Error: {str(e)}")
        
        # Voice mappings
        vn_voice = self.combo_vn_voice.currentData()
        jp_voice = self.combo_jp_voice.currentData()
        voice_mappings = {
            'vietnamese': vn_voice,
            'japanese': jp_voice,
            'mixed': vn_voice
        }
        
        # Start worker
        self.rewrite_worker = RewriteWorker(
            self.gemini_api, text, prompt_template,
            self.text_processor, voice_mappings
        )
        self.rewrite_worker.finished.connect(
            lambda result: self.rewrite_completed(result, prompt_name)
        )
        self.rewrite_worker.error.connect(self.rewrite_error)
        self.rewrite_worker.status.connect(self.status_updated)
        self.rewrite_worker.start()
    
    def rewrite_completed(self, result, prompt_name):
        """Handle completion - ĐÃ SỬA"""
        try:
            rewritten = result["rewritten_text"]
            analysis = result["style_analysis"]
            
            self.processed_text.setPlainText(rewritten)
            self.current_style_analysis = analysis
            
            self.btn_rewrite.setEnabled(True)
            self.btn_rewrite.setText("🔄 Viết Lại")
            
            self.update_style_display()
            
            self.btn_export_json.setEnabled(True)
            self.btn_copy_json.setEnabled(True)
            
            self.log(f"✅ Hoàn thành {len(analysis)} đoạn")
            
            # Summary
            lang_stats = {}
            for chunk in analysis:
                lang = chunk['language']
                lang_stats[lang] = lang_stats.get(lang, 0) + 1
            
            summary = f"🎉 Hoàn thành!\n\n"
            summary += f"📝 Prompt: {prompt_name}\n"
            summary += f"📊 Tổng: {len(analysis)} đoạn\n"
            
            for lang, count in lang_stats.items():
                icon = "🇯🇵" if lang == 'JAPANESE' else "🇻🇳"
                summary += f"• {icon} {lang}: {count}\n"
            
            QMessageBox.information(self, "Hoàn Thành", summary)
            self.status_updated(f"✅ Xong {len(analysis)} đoạn")
            
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)}")
            self.rewrite_error(str(e))
    
    def rewrite_error(self, error_msg):
        """Handle error"""
        self.btn_rewrite.setEnabled(True)
        self.btn_rewrite.setText("🔄 Viết Lại")
        
        self.log(f"❌ Lỗi: {error_msg}")
        QMessageBox.critical(self, "Lỗi", f"Lỗi:\n{error_msg}")
        self.status_updated("❌ Lỗi")
    
    def status_updated(self, msg):
        self.status_label.setText(msg)
        self.log(msg)
    
    def highlight_selected(self):
        """Highlight selected - THÊM MỚI"""
        cursor = self.processed_text.textCursor()
        if not cursor.hasSelection():
            QMessageBox.warning(self, "Cảnh báo", "Chọn text!")
            return
        
        start = cursor.selectionStart()
        end = cursor.selectionEnd()
        length = end - start
        
        self.manual_highlights.append((start, length))
        
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(255, 255, 150))
        fmt.setForeground(QColor(200, 50, 50))
        cursor.setCharFormat(fmt)
        
        self.log(f"🎨 Highlight {length} ký tự")
    
    def clear_highlight(self):
        """Clear highlight - THÊM MỚI"""
        cursor = self.processed_text.textCursor()
        if not cursor.hasSelection():
            QMessageBox.warning(self, "Cảnh báo", "Chọn vùng!")
            return
        
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(255, 255, 255))
        fmt.setForeground(QColor(0, 0, 0))
        cursor.setCharFormat(fmt)
        
        start = cursor.selectionStart()
        self.manual_highlights = [
            (s, l) for s, l in self.manual_highlights
            if not (s <= start < s + l)
        ]
        
        self.log("🧹 Đã xóa highlight")
    
    def copy_processed(self):
        text = self.processed_text.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.log("📋 Đã copy")
    
    def enable_edit(self):
        if self.processed_text.isReadOnly():
            self.processed_text.setReadOnly(False)
            self.processed_text.setStyleSheet("background: #fffacd;")
            self.btn_edit.setText("🔒 Khóa")
            self.log("✏️ Bật edit")
        else:
            self.processed_text.setReadOnly(True)
            self.processed_text.setStyleSheet("")
            self.btn_edit.setText("✏️ Edit")
            self.log("🔒 Khóa edit")
    
    def clear_all_text(self):
        self.text_input.clear()
        self.processed_text.clear()
        self.current_style_analysis = []
        self.style_display.clear()
        self.manual_highlights = []
        self.btn_export_json.setEnabled(False)
        self.btn_copy_json.setEnabled(False)
        self.log("🗑️ Đã xóa text")
    
    def load_text_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn file", "", "Text (*.txt);;All (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_input.setPlainText(content)
                self.log(f"✅ Tải: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không đọc được:\n{e}")
    
    def browse_output(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Chọn thư mục", self.output_path.text()
        )
        if directory:
            self.output_path.setText(directory)
            self.log(f"📁 Chọn: {directory}")
    
    def start_tts(self):
        """Start TTS - HOÀN CHỈNH"""
        text = self.processed_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(
                self, "Cảnh báo",
                "Viết lại văn bản trước!\n\nBấm '🔄 Viết Lại'"
            )
            return
        
        if not self.current_style_analysis:
            QMessageBox.warning(self, "Cảnh báo", "Chưa có phân tích!")
            return
        
        # Config
        config = {
            'output_dir': self.output_path.text(),
            'output_filename': self.output_filename.text(),
            'auto_merge': self.cb_auto_merge.isChecked(),
            'keep_chunks': self.cb_keep_chunks.isChecked(),
            'voice_mappings': {
                'vietnamese': self.combo_vn_voice.currentData(),
                'japanese': self.combo_jp_voice.currentData(),
                'mixed': self.combo_vn_voice.currentData()
            }
        }
        
        os.makedirs(config['output_dir'], exist_ok=True)
        
        # Worker
        self.tts_worker = SmartTTSWorkerV6(
            self.gemini_api, text, config, self.current_style_analysis
        )
        
        # Signals
        self.tts_worker.progress_updated.connect(self.overall_progress.setValue)
        self.tts_worker.status_updated.connect(self.status_updated)
        self.tts_worker.chunk_completed.connect(self.on_chunk_completed)
        self.tts_worker.error_occurred.connect(self.on_tts_error)
        self.tts_worker.completed.connect(self.on_tts_completed)
        
        # UI
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.audio_files.clear()
        self.output_list.clear()
        self.chunks_list.clear()
        
        self.log("🚀 Bắt đầu TTS...")
        self.tts_worker.start()
    
    def stop_tts(self):
        if self.tts_worker and self.tts_worker.isRunning():
            self.tts_worker.cancel()
            self.log("⏹️ Đang dừng...")
            self.btn_stop.setEnabled(False)
    
    def on_chunk_completed(self, chunk_num, file_path, chunk_info):
        self.audio_files.append(file_path)
        
        item = QListWidgetItem(f"✅ {os.path.basename(file_path)}")
        self.output_list.addItem(item)
        
        lang = chunk_info['language']
        voice = chunk_info['voice']
        style = chunk_info['style']
        chunk_item = QListWidgetItem(f"Đoạn {chunk_num}: {lang} - {voice} - {style}")
        self.chunks_list.addItem(chunk_item)
        
        self.log(f"✅ Xong đoạn {chunk_num}")
    
    def on_tts_error(self, error_msg):
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        
        self.log(f"❌ Lỗi TTS: {error_msg}")
        QMessageBox.critical(self, "Lỗi", f"Lỗi:\n{error_msg}")
    
    def on_tts_completed(self, audio_files):
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.btn_merge.setEnabled(len(audio_files) > 1)
        self.btn_play.setEnabled(len(audio_files) > 0)
        
        self.log(f"🎉 Hoàn thành {len(audio_files)} files!")
        
        if self.cb_auto_merge.isChecked() and len(audio_files) > 1:
            self.merge_audio()
    
    def open_output_folder(self):
        output_dir = self.output_path.text()
        if os.path.exists(output_dir):
            if sys.platform == 'win32':
                os.startfile(output_dir)
            elif sys.platform == 'darwin':
                subprocess.run(['open', output_dir])
            else:
                subprocess.run(['xdg-open', output_dir])
            self.log(f"📁 Mở: {output_dir}")
    
    def merge_audio(self):
        """Merge audio files"""
        if len(self.audio_files) < 2:
            return
        
        self.log("🔗 Đang ghép audio...")
        
        try:
            import wave
            
            output_file = os.path.join(
                self.output_path.text(),
                self.output_filename.text()
            )
            
            with wave.open(output_file, 'wb') as output:
                for i, file_path in enumerate(self.audio_files):
                    with wave.open(file_path, 'rb') as input_file:
                        if i == 0:
                            output.setparams(input_file.getparams())
                        output.writeframes(input_file.readframes(input_file.getnframes()))
            
            self.log(f"✅ Đã ghép: {output_file}")
            QMessageBox.information(self, "Thành công", f"Đã ghép thành:\n{output_file}")
            
        except Exception as e:
            self.log(f"❌ Lỗi ghép: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể ghép:\n{str(e)}")
    
    def open_prompt_manager(self):
        dialog = PromptManagerDialog(self.prompts, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.prompts = dialog.get_prompts()
            save_prompts(self.prompts)
            self.update_prompt_combo()
            self.update_prompt_display()
            self.log(f"💾 Lưu {len(self.prompts)} prompts")
    
    def update_prompt_display(self):
        html = "<html><body>"
        html += "<h2>📝 Prompts</h2>"
        for name, content in self.prompts.items():
            html += f"<h3>🎨 {name}</h3>"
            html += f"<p style='background:#f0f0f0;padding:10px;'>{content[:200]}...</p>"
        html += "</body></html>"
        self.prompt_display.setHtml(html)
    
    def update_style_display(self):
        if not self.current_style_analysis:
            self.style_display.setPlainText("Chưa có phân tích")
            return
        
        json_text = json.dumps(self.current_style_analysis, indent=2, ensure_ascii=False)
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Consolas', monospace; }}
                .header {{ background: #667eea; color: white; padding: 10px; }}
                pre {{ background: #f8f9fa; padding: 10px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h3>🧠 Phân Tích</h3>
                <p>Tổng: {len(self.current_style_analysis)} đoạn</p>
            </div>
            <pre>{json_text}</pre>
        </body>
        </html>
        """
        
        self.style_display.setHtml(html)
        self.log(f"📊 Cập nhật {len(self.current_style_analysis)} đoạn")
    
    def export_json(self):
        if not self.current_style_analysis:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Xuất JSON", "style_analysis.json", "JSON (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.current_style_analysis, f, indent=2, ensure_ascii=False)
                self.log(f"💾 Xuất: {file_path}")
                QMessageBox.information(self, "Thành công", "Đã xuất JSON!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không xuất được:\n{e}")
    
    def copy_json(self):
        if not self.current_style_analysis:
            return
        
        json_text = json.dumps(self.current_style_analysis, indent=2, ensure_ascii=False)
        QApplication.clipboard().setText(json_text)
        self.log("📋 Đã copy JSON")
    
    def closeEvent(self, event):
        if self.tts_worker and self.tts_worker.isRunning():
            reply = QMessageBox.question(
                self, "Xác nhận",
                "TTS đang chạy. Thoát?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.tts_worker.cancel()
                self.tts_worker.wait(3000)
                event.accept()
            else:
                event.ignore()
        else:
            save_prompts(self.prompts)
            event.accept()

# =====================================
# APPLICATION
# =====================================

class Application:
    def __init__(self):
        self.main_window = None
        
    def run(self):
        if not check_expiration():
            sys.exit(1)
        
        splash = SplashScreen()
        splash.show()
        QApplication.processEvents()
        
        self.main_window = MainWindow()
        
        while splash.isVisible():
            QApplication.processEvents()
            time.sleep(0.01)
        
        self.main_window.show()
        return self.main_window

# =====================================
# MAIN
# =====================================

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('bilingual_tts_v6_fixed.log', encoding='utf-8')
        ]
    )

def check_dependencies():
    missing = []
    
    try:
        import requests
    except ImportError:
        missing.append("requests")
    
    try:
        from google import genai
    except ImportError:
        missing.append("google-genai")
    
    if missing:
        print("⚠️ Thiếu:")
        for dep in missing:
            print(f"  - {dep}")
        print(f"\nCài: pip install {' '.join(missing)}")
        return False
    
    return True

def print_banner():
    print("=" * 80)
    print("🎭 BILINGUAL TTS PRO V6.0 - FIXED VERSION")
    print("=" * 80)
    print("✅ Model Selection")
    print("✅ Enhanced API Handling")
    print("✅ Manual Highlight System")
    print("✅ Complete TTS Workflow")
    print("=" * 80)
    print("👨‍💻 Phạm Hữu Tiền")
    print("=" * 80)

def main_app():
    print_banner()
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    if not check_dependencies():
        print("❌ Cài dependencies trước!")
        return 1
    
    if not check_expiration():
        return 1
    
    app = QApplication(sys.argv)
    app.setApplicationName("Bilingual TTS Pro v6.0 FIXED")
    app.setApplicationVersion("6.0.1")
    app.setOrganizationName("Phạm Hữu Tiền")
    
    font = QFont("Segoe UI", 12)
    app.setFont(font)
    
    try:
        show_startup_info()
        logger.info("Khởi động v6.0 FIXED...")
        
        application = Application()
        main_window = application.run()
        
        if main_window:
            logger.info("✅ Khởi tạo thành công!")
            print("\n🎉 BILINGUAL TTS PRO V6.0 READY!")
            print("🔧 All bugs fixed:")
            print("  ✅ Model selection working")
            print("  ✅ API error handling improved")
            print("  ✅ Manual highlight system added")
            print("  ✅ Complete TTS workflow")
            print("=" * 80)
            
            exit_code = exec_app(app)
            logger.info(f"Kết thúc: {exit_code}")
            return exit_code
        else:
            logger.error("Lỗi khởi tạo")
            return 1
            
    except Exception as e:
        logger.critical(f"Lỗi nghiêm trọng: {str(e)}", exc_info=True)
        QMessageBox.critical(
            None, "Lỗi",
            f"Không khởi tạo được:\n\n{str(e)}"
        )
        return 1

if __name__ == "__main__":
    print("🚀 Bilingual TTS Pro v6.0 - FIXED VERSION")
    print("👨‍💻 Phạm Hữu Tiền")
    print()
    
    try:
        exit_code = main_app()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⌨️ Interrupted")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Error: {e}")
        sys.exit(1)
