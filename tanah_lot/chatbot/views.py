from django.shortcuts import render, redirect
from django.http import JsonResponse
import os

from dotenv import load_dotenv
import google.generativeai as genai

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import KnowledgeItem

# ------------------- KONFIGURASI AWAL (LOAD .ENV DAN GEMINI) -------------------


dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"PERINGATAN: File .env tidak ditemukan di {dotenv_path}. Pastikan API key diatur.")

API_KEY_GEMINI = None
try:
    API_KEY_GEMINI = os.getenv("GEMINI_API_KEY")
    if not API_KEY_GEMINI:
        raise ValueError("GEMINI_API_KEY tidak ditemukan...")
    genai.configure(api_key=API_KEY_GEMINI)
except ValueError as e:
    print(f"Error konfigurasi Gemini: {e}")

model = None
if API_KEY_GEMINI:
    try:
        model = genai.GenerativeModel(
            'gemini-1.5-flash-latest',
            system_instruction=(
                "Anda adalah asisten virtual bernama TL-BOT yang khusus memberikan informasi tentang "
                "Tanah Lot di Bali, Indonesia. Jawablah pertanyaan hanya yang berkaitan dengan Tanah Lot, "
                "seperti sejarahnya, daya tariknya, fasilitas, waktu terbaik berkunjung, tips, legenda, "
                "pura di sana, ombak, matahari terbenam, dan hal-hal terkait objek wisata Tanah Lot. "
                "Jika pertanyaan di luar topik Tanah Lot, jawablah dengan sopan bahwa Anda hanya bisa "
                "membahas Tanah Lot. Jangan menjawab pertanyaan tentang topik lain meskipun Anda mengetahuinya."
            )
        )
    except Exception as e:
        print(f"Error saat inisialisasi model Gemini: {e}")

# ------------------- FUNGSI UNTUK LOGIKA RAG -------------------

def find_relevant_info_from_db(user_message):
    """
    Fungsi untuk mencari informasi relevan dari database KnowledgeItem.
    Ini adalah langkah 'Retrieval' dalam RAG.
    """
    user_message_lower = user_message.lower()
    
    knowledge_items = KnowledgeItem.objects.all()
    
    for item in knowledge_items:
        keywords = [k.strip().lower() for k in item.keywords.split(',')]
        for keyword in keywords:
            if keyword in user_message_lower:
                return item.information
                
    return None

# ------------------- VIEWS DJANGO -------------------

def chatbot_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('chatbot:chatbot')
    else:
        messages.warning(request, 'Anda harus login terlebih dahulu untuk mengakses chatbot.')
        return redirect('login:login')

# View ini adalah inti dari chatbot, sekarang dengan logika RAG
@login_required(login_url='/login/')
def chat_view(request):
    if model is None:
        error_msg = 'Model Gemini gagal dimuat. Periksa konfigurasi API Key, koneksi internet, dan instalasi library.'
        return render(request, 'chatbot.html', {'error_message': error_msg, 'chat_history': []})

    chat_history_session_key = 'gemini_chat_history_tl_bot'
    current_chat_history = request.session.get(chat_history_session_key, [])

    if request.method == 'POST':
        user_message_text = request.POST.get('message', '').strip()
        bot_response_text = "Maaf, terjadi kesalahan internal."

        if user_message_text:
            current_chat_history.append({'role': 'user', 'parts': [user_message_text]})
            
            # --- IMPLEMENTASI LOGIKA RAG ---
            # 1. Retrieval: Cari info relevan dari database lokal
            relevant_local_info = find_relevant_info_from_db(user_message_text)
            
            # 2. Augmentation: Siapkan prompt untuk Gemini
            final_prompt_to_gemini = user_message_text
            if relevant_local_info:
                print(f"DEBUG: Info lokal ditemukan: {relevant_local_info[:50]}...") # Log untuk debug
                context_for_prompt = (
                    f"Berdasarkan informasi spesifik berikut: '{relevant_local_info}'. "
                    f"Gunakan informasi ini untuk menjawab pertanyaan pengguna secara alami. Pertanyaannya adalah: '{user_message_text}'"
                )
                final_prompt_to_gemini = context_for_prompt
            else:
                print("DEBUG: Tidak ada info lokal yang relevan, menggunakan pengetahuan umum Gemini.")

            # 3. Generation: Kirim prompt ke Gemini
            try:
                gemini_chat_session = model.start_chat(history=current_chat_history[:-1]) 
                response = gemini_chat_session.send_message(final_prompt_to_gemini) # Kirim prompt yang sudah diperkaya
                bot_response_text = response.text
                current_chat_history.append({'role': 'model', 'parts': [bot_response_text]})

            except Exception as e:
                bot_response_text = f"Maaf, terjadi kesalahan saat menghubungi Gemini: {e}"
                print(f"Error saat berkomunikasi dengan Gemini: {e}")
                if not current_chat_history or current_chat_history[-1]['role'] != 'model':
                    current_chat_history.append({'role': 'model', 'parts': [bot_response_text]})
                else: 
                    current_chat_history[-1]['parts'] = [bot_response_text]

            request.session[chat_history_session_key] = current_chat_history

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'user_message': user_message_text,
                    'bot_message': bot_response_text,
                })
        else: 
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'user_message': '', 'bot_message': 'Silakan ketik sesuatu.'}, status=400)
    
    request.session.modified = True
    return render(request, 'chatbot.html', {'chat_history': current_chat_history})


@login_required(login_url='/login/')
def clear_chat_history(request):
    chat_history_session_key = 'gemini_chat_history_tl_bot'
    if chat_history_session_key in request.session:
        del request.session[chat_history_session_key]
    request.session.modified = True
   
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Riwayat percakapan telah dihapus.'})
    
    return redirect('chatbot:chatbot')