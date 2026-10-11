"""
Configuration and constants for Sarvam AI Bulbul TTS and AudioReader.
"""

# Sarvam AI API endpoints
SARVAM_TTS_URL = "https://api.sarvam.ai/text-to-speech"

# Character limits
MAX_CHARS_PER_REQUEST = 2000  # API limit is 2,500; 2,000 provides safety buffer
CHUNK_SAFETY_MARGIN = 200

# Supported Indian Languages (BCP-47 codes)
SUPPORTED_LANGUAGES = [
    {"code": "en-IN", "name": "English (India)", "native": "English"},
    {"code": "hi-IN", "name": "Hindi", "native": "हिन्दी"},
    {"code": "bn-IN", "name": "Bengali", "native": "বাংলা"},
    {"code": "kn-IN", "name": "Kannada", "native": "ಕನ್ನಡ"},
    {"code": "ml-IN", "name": "Malayalam", "native": "മലയാളം"},
    {"code": "mr-IN", "name": "Marathi", "native": "मराठी"},
    {"code": "od-IN", "name": "Odia", "native": "ଓଡ଼ିଆ"},
    {"code": "pa-IN", "name": "Punjabi", "native": "ਪੰਜਾਬੀ"},
    {"code": "ta-IN", "name": "Tamil", "native": "தமிழ்"},
    {"code": "te-IN", "name": "Telugu", "native": "తెలుగు"},
    {"code": "gu-IN", "name": "Gujarati", "native": "ગુજરાતી"},
]

# Supported Models
SUPPORTED_MODELS = [
    {
        "id": "bulbul:v4-flash",
        "name": "Bulbul v4-Flash (Latest, High Fidelity)",
        "description": "Recommended for natural prosody, high speed, and 200+ voice personas",
    },
    {
        "id": "bulbul:v3",
        "name": "Bulbul v3 (Stable)",
        "description": "Standard stable model with classic Indian voice personas",
    },
]

# Universal voices for Bulbul v3 (supported across all 11 languages)
V3_UNIVERSAL_VOICES = [
    {"id": "shubh", "name": "Shubh", "gender": "Male", "tone": "Balanced & Natural (Default)"},
    {"id": "aditya", "name": "Aditya", "gender": "Male", "tone": "Confident & Clear"},
    {"id": "rahul", "name": "Rahul", "gender": "Male", "tone": "Casual & Conversational"},
    {"id": "amit", "name": "Amit", "gender": "Male", "tone": "Deep & Authoritative"},
    {"id": "dev", "name": "Dev", "gender": "Male", "tone": "Narrative"},
    {"id": "ritu", "name": "Ritu", "gender": "Female", "tone": "Warm & Expressive"},
    {"id": "priya", "name": "Priya", "gender": "Female", "tone": "Bright & Articulate"},
    {"id": "neha", "name": "Neha", "gender": "Female", "tone": "Professional"},
    {"id": "roopa", "name": "Roopa", "gender": "Female", "tone": "Storyteller & Melodious"},
    {"id": "kavya", "name": "Kavya", "gender": "Female", "tone": "Dynamic"},
]

# Language-specific persona catalog for Bulbul v4-Flash
V4_VOICES_BY_LANG = {
    "en-IN": [
        {"id": "shubh_en_narration", "name": "Shubh", "gender": "Male", "tone": "Audio Narration (Default)"},
        {"id": "simran_en_narration", "name": "Simran", "gender": "Female", "tone": "Natural Narration"},
        {"id": "aditi_en_stories", "name": "Aditi", "gender": "Female", "tone": "Storyteller"},
        {"id": "dev_en_conversational", "name": "Dev", "gender": "Male", "tone": "Conversational"},
        {"id": "ishita_en_stories", "name": "Ishita", "gender": "Female", "tone": "Expressive Stories"},
        {"id": "roopa_en_conversational", "name": "Roopa", "gender": "Female", "tone": "Warm & Conversational"},
        {"id": "shubh_en_audiobook", "name": "Shubh (Audiobook)", "gender": "Male", "tone": "Book Reader"},
        {"id": "amelia_en_conversational", "name": "Amelia", "gender": "Female", "tone": "International Accent"},
        {"id": "sophia_en_conversational", "name": "Sophia", "gender": "Female", "tone": "Warm & Gentle"},
    ],
    "hi-IN": [
        {"id": "simran_hi_narration", "name": "Simran", "gender": "Female", "tone": "Narration (Default)"},
        {"id": "shubh_hi_ads", "name": "Shubh", "gender": "Male", "tone": "Expressive Narration"},
        {"id": "roopa_hi_narration", "name": "Roopa", "gender": "Female", "tone": "Warm & Melodious"},
        {"id": "aditya_hi_conversational", "name": "Aditya", "gender": "Male", "tone": "Conversational"},
        {"id": "anand_hi_documentary", "name": "Anand", "gender": "Male", "tone": "Documentary & Deep"},
        {"id": "ritu_hi_conversation", "name": "Ritu", "gender": "Female", "tone": "Conversational"},
        {"id": "sanchita_hi_assistant", "name": "Sanchita", "gender": "Female", "tone": "Clear Assistant"},
        {"id": "shreya_hi_conversational", "name": "Shreya", "gender": "Female", "tone": "Bright & Lively"},
    ],
    "bn-IN": [
        {"id": "arnab_bn_conversation", "name": "Arnab", "gender": "Male", "tone": "Conversational"},
        {"id": "roopa_bn_conversational", "name": "Roopa", "gender": "Female", "tone": "Warm & Natural"},
        {"id": "bimal_bn_suspense", "name": "Bimal", "gender": "Male", "tone": "Dramatic & Deep"},
    ],
    "gu-IN": [
        {"id": "bhavik_gu_conversation", "name": "Bhavik", "gender": "Male", "tone": "Conversational"},
        {"id": "pooja_gu_conversational", "name": "Pooja", "gender": "Female", "tone": "Natural & Friendly"},
    ],
    "kn-IN": [
        {"id": "chaitra_kn_narration", "name": "Chaitra", "gender": "Female", "tone": "Narration"},
        {"id": "chetan_kn_conversation", "name": "Chetan", "gender": "Male", "tone": "Conversational"},
        {"id": "suchitra_kn_narration", "name": "Suchitra", "gender": "Female", "tone": "Expressive"},
    ],
    "mr-IN": [
        {"id": "mrunal_mr_narration", "name": "Mrunal", "gender": "Female", "tone": "Narration"},
        {"id": "nilesh_mr_conversation", "name": "Nilesh", "gender": "Male", "tone": "Conversational"},
        {"id": "neha_mr_narration", "name": "Neha", "gender": "Female", "tone": "Clear & Natural"},
        {"id": "soham_mr_narration", "name": "Soham", "gender": "Male", "tone": "Authoritative"},
        {"id": "rupali_mr_stories", "name": "Rupali", "gender": "Female", "tone": "Storyteller"},
    ],
    "pa-IN": [
        {"id": "harpreet_pa_narration", "name": "Harpreet", "gender": "Female", "tone": "Narration"},
        {"id": "anand_pa_conversation", "name": "Anand", "gender": "Male", "tone": "Conversational"},
        {"id": "jaspal_pa_banking", "name": "Jaspal", "gender": "Male", "tone": "Formal"},
    ],
    "ta-IN": [
        {"id": "gokul_ta_narration", "name": "Gokul", "gender": "Male", "tone": "Narration"},
        {"id": "vijay_ta_narration", "name": "Vijay", "gender": "Male", "tone": "Expressive"},
        {"id": "aravind_ta_ads", "name": "Aravind", "gender": "Male", "tone": "Energetic"},
    ],
    "te-IN": [
        {"id": "kavitha_te_narration", "name": "Kavitha", "gender": "Female", "tone": "Narration"},
        {"id": "tarun_te_narration", "name": "Tarun", "gender": "Male", "tone": "Conversational"},
        {"id": "pooja_te_conversation", "name": "Pooja", "gender": "Female", "tone": "Natural"},
    ],
}


def get_voices_for_selection(model_id: str, language_code: str):
    """
    Returns verified voices suitable for the chosen model and language.
    Gracefully falls back to universal Bulbul v3 personas if the language has no v4-flash voice.
    """
    if model_id == "bulbul:v4-flash":
        if language_code in V4_VOICES_BY_LANG:
            return V4_VOICES_BY_LANG[language_code]
        # For languages without specific v4 persona (like Odia or Malayalam), return V3 voices
        return V3_UNIVERSAL_VOICES

    # Default to V3 universal catalog
    return V3_UNIVERSAL_VOICES


# Sample preset texts for immediate testing
SAMPLE_TEXTS = {
    "en-IN": "Welcome to AudioReader! Powered by Sarvam AI Bulbul Text-to-Speech, this platform converts documents and text into natural, lifelike narration across eleven Indian languages.",
    "hi-IN": "ऑडियोरीडर में आपका स्वागत है! सर्वम एआई बुलबुल तकनीक की सहायता से, आप किसी भी दस्तावेज़ या पाठ को प्राकृतिक और स्पष्ट वाणी में परिवर्तित कर सकते हैं।",
    "od-IN": "ଅଡିଓରିଡରକୁ ସ୍ୱାଗତ! ସର୍ବମ୍ ଏଆଇ ବୁଲବୁଲ୍ ମଡେଲ ସାହାଯ୍ୟରେ, ଆପଣ ଯେକୌଣସି ପାଠ୍ୟକୁ ପ୍ରାକୃତିକ ସ୍ୱରରେ ରୂପାନ୍ତରିତ କରିପାରିବେ।",
    "bn-IN": "অডিওরিডারে আপনাকে স্বাগতম! সারভাম এআই বুলবুল মডেলের মাধ্যমে যেকোনো লেখাকে সুন্দর ও স্বাভাবিক কণ্ঠে রূপান্তর করুন।",
    "ta-IN": "ஆடியோ ரீடருக்கு உங்களை வரவேற்கிறோம்! சர்வக் ஏஐ புல்புல் மூலம் உங்கள் உரைகளை இயல்பான குரலாக மாற்றுங்கள்.",
}
