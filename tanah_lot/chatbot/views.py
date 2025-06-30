from django.shortcuts import render, redirect
from django.http import JsonResponse
import google.generativeai as genai
import os
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
from django.contrib import messages


dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"PERINGATAN: File .env tidak ditemukan di {dotenv_path}. Pastikan API key diatur.")

# Konfigurasi API Key Gemini
API_KEY_GEMINI = None
try:
    API_KEY_GEMINI = os.getenv("GEMINI_API_KEY")
    if not API_KEY_GEMINI:
        raise ValueError("GEMINI_API_KEY tidak ditemukan. Pastikan sudah ada di file .env atau sebagai variabel lingkungan sistem.")
    genai.configure(api_key=API_KEY_GEMINI)
except ValueError as e:
    print(f"Error konfigurasi Gemini: {e}")
    # API_KEY_GEMINI sudah None by default jika error


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

def chatbot_redirect_view(request):
    # Periksa apakah pengguna sudah login
    if request.user.is_authenticated:
        # Jika sudah, langsung arahkan ke halaman chatbot yang sebenarnya
        return redirect('chatbot:chatbot')
    else:
        # Jika belum, tambahkan pesan error dan arahkan ke halaman login
        messages.warning(request, 'Anda harus login terlebih dahulu untuk mengakses chatbot.')
        return redirect('login:login') # Ganti 'login:login' jika nama URL login Anda berbeda
       
@login_required(login_url='/login/')
def chat_view(request):
    if model is None:
        error_msg = 'Model Gemini gagal dimuat. '
        if not API_KEY_GEMINI:
            error_msg += 'API Key Gemini tidak ditemukan atau tidak valid. '
        error_msg += 'Periksa konfigurasi API Key, koneksi internet, dan instalasi library (google-generativeai, pydantic, grpcio).'
        
        return render(request, 'error_page.html', {'error_message': error_msg})
       
        return render(request, 'chatbot/chatbot.html', {'error_message': error_msg, 'chat_history': []})


   
    # Format: [{'role': 'user', 'parts': ["Pesan pengguna"]}, {'role': 'model', 'parts': ["Balasan bot"]}]
    chat_history_session_key = 'gemini_chat_history_talbot'

   
    current_chat_history = request.session.get(chat_history_session_key, [])

    if request.method == 'POST':
        user_message_text = request.POST.get('message', '').strip()
        bot_response_text = "Maaf, terjadi kesalahan internal saat memproses permintaan Anda." 

        if user_message_text:
           
            current_chat_history.append({'role': 'user', 'parts': [user_message_text]})

            try:
              
                gemini_chat_session = model.start_chat(history=current_chat_history[:-1]) 
                
                response = gemini_chat_session.send_message(user_message_text)
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
           
    request.session.modified = True # Pastikan sesi disimpan
    return render(request, 'chatbot.html', {'chat_history': current_chat_history})


@login_required(login_url='/login/')
def clear_chat_history(request):
    """Menghapus riwayat percakapan dari sesi."""
    chat_history_session_key = 'gemini_chat_history_talbot'
    if chat_history_session_key in request.session:
        del request.session[chat_history_session_key]
    request.session.modified = True
   
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Riwayat percakapan telah dihapus.'})
    
    from django.shortcuts import redirect
    return redirect('chatbot:chatbot')