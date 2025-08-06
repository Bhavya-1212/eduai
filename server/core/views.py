from .utils.chatbot import get_gemini_response
from django.shortcuts import render
from .forms import PromptForm, ChatForm
from diffusers import StableDiffusionPipeline
import torch
import fitz  # PyMuPDF
import os

# ✅ Load Stable Diffusion Model (CPU)
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32
)
pipe = pipe.to("cpu")

chat_history = []  # For keeping session-wide chat

def index(request):
    return render(request, 'core/index.html')

# ✅ Text to Image
def text_to_image(request):
    image_path = None

    if request.method == 'POST':
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            image = pipe(prompt).images[0]

            os.makedirs('media', exist_ok=True)
            image_path = 'media/generated_image.png'
            image.save(image_path)

            request.session['image_generated'] = True  # Track if image was created
    else:
        form = PromptForm()
        if request.session.get('image_generated'):
            try:
                os.remove('media/generated_image.png')
            except FileNotFoundError:
                pass
            request.session['image_generated'] = False  # Reset

    return render(request, 'core/text_to_image.html', {
        'form': form,
        'image_path': image_path
    })

# ✅ Education Chat using Gemini (with fallback)
def chat(request):
    global chat_history 

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            msg = form.cleaned_data['message']
            chat_history.append(('You', msg))

            try:
                bot_reply = get_gemini_response(msg)
            except Exception as e:
                bot_reply = f"❌ EduBot is unavailable. Error: {str(e)}"

            chat_history.append(('EduBot', bot_reply))
            form = ChatForm()  # Clear input after sending
    else:
        chat_history.clear()  # Reset on GET
        form = ChatForm()

    return render(request, 'core/chat.html', {
        'form': form,
        'chat': chat_history
    })
'''
def get_gemini_response(message):
    return "This is a dummy reply from EduBot."  # Test with dummy
    '''

 
