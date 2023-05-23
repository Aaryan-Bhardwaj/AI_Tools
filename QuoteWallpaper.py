import openai
import requests
import json
import ctypes
import os
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from StableDiffusionAPI import get_image_url

def GetQuote(category, languague = "english"):
    if languague == "english":        
        responseDict = json.loads(requests.get('https://api.quotable.io/tags').text)
        tagslugs = [tag['slug'] for tag in responseDict]
        tagnames = [tag['name'] for tag in responseDict]

        if category in tagslugs or category in tagnames:
            response = requests.get('https://api.quotable.io/quotes/random?tags=' + category + "&limit=1")
            responseDict = json.loads(response.text)[0]
            return responseDict['content'], " - " + responseDict['author']
        else:
            print("Error:", response.status_code, response.text)
            return '', ''
    elif languague == "hindi":
        response = requests.get(f"https://hindi-quotes.vercel.app/random/{category}")
        responseDict = json.loads(response.text)        
        return responseDict['quote'], "" 
    else:
        print("Invalid Language:")
        exit()

def GetImageURL(Prompt, apiKey, ImageCount=1, ImageSize='512x512'):
    openai.api_key = apiKey
    
    response = openai.Image.create(
            prompt = Prompt,
            n = ImageCount,
            size = ImageSize,
            )
    
    urls = []
    for data in response['data']:
        urls.append(data['url'])

    return urls

def ProcessImage(image, message, author):
    user32 = ctypes.windll.user32    
    screenAspectRatio = user32.GetSystemMetrics(0) / user32.GetSystemMetrics(1) # width / height
    image = Image.open(image)

    image = AddPaddingToWallpaper(image, screenAspectRatio)
    image = AddCaption(image, message, author)
    
    return image

def AddCaption(image, message, author, fontColor='white', borderColor='black'):
    font = ImageFont.truetype("Amiko-Regular.ttf", size=int(image.size[1]/50))
    nSpaces = (font.getlength(message) - font.getlength(author)) // font.getlength(" ")
    textOverlay = message + '\n' + ' ' * int(nSpaces * 0.95) + author        
    W, H = (image.size[0], image.size[1])
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), textOverlay, font=font)
    textLocation = ((W-w)/2, (H-h)*7.3/8)

    # For borders
    borderWidth = 1
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            draw.text((
                    textLocation[0] + (borderWidth * x),
                    textLocation[1] + (borderWidth * y),
                ),
                textOverlay,
                font=font,
                fill=borderColor,
            )

    draw.text(textLocation, textOverlay, fill=fontColor, font=font)#'OpenSansCondensed-LightItalic.ttf')

    return image
        
def SaveImage(urls, name, quote, author):
    for i in range(len(urls)):
        imageSaveName = f"{name}.png" if i == 0 else f"{name}{i}.png"
        imageData = requests.get(urls[i]).content
        imageStream = io.BytesIO(imageData)
        image = ProcessImage(imageStream, quote, author)
        image.save(imageSaveName)

def AddPaddingToWallpaper(image, aspectRatio=(16//9), blurRadius=25):
    image = image.convert('RGBA')
    height = image.height
    newWidth = int(height * aspectRatio)
    paddingImg = image.resize((newWidth, height))
    paddingImg = paddingImg.filter(ImageFilter.GaussianBlur(blurRadius))
    resultImg = Image.new('RGBA', paddingImg.size)
    resultImg.paste(paddingImg, (0, 0))
    resultImg.paste(image, ((newWidth - height) // 2 ,0), mask=image)
    
    return resultImg

def GetPromptFromQuote(quote, category, apiKey):
    openai.api_key = apiKey
    
    messages = [
        {"role": "system", "content": f"Your task is to create a prompt that i can give to an image generator to get back an wallpaper that encapsulates the emotion and context of the quote. the wallpaper should have a darker asthetic, represent the theme {category} and not contain any text. the prompt should only describe image details and color pallet in the wallpaper, limited to 30 words."},
        {"role": "user", "content": f"quote: {quote}"}
    ]
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
    )
    return completion.choices[0].message.content

def getChatGPTPromptFromQuote(quote, category, accessToken):
    from revChatGPT.V1 import Chatbot

    chatbot = Chatbot(config={
    "access_token": accessToken
    })
    prompt = f"Your task is to create a prompt that i can give to an image generator to get back an wallpaper that encapsulates the emotion and context of the quote. the wallpaper should have a darker asthetic, represent the theme {category} and not contain any text. the prompt should only describe image details and color pallet in the wallpaper, limited to 30 words."
    prompt += f"quote: {quote}"
    response = ""
    for data in chatbot.ask(
    prompt
    ):
        response = data["message"]
    return response

    
def SetWallpaper(imageName):
    cwd = os.getcwd()
    ctypes.windll.user32.SystemParametersInfoW(20, 0, cwd+f"\{imageName}.png" , 0) 

# Get yours from https://chat.openai.com/api/auth/session -> accessToken
accessToken = ""

imageName = 'wallpaper'
gptAPIKey = ""
category = 'happiness'  # hindi_categories: success, love, attitude, positive, motivational
language = 'english' # english or hindi

quote, author = GetQuote(category, language)
# prompt = GetPromptFromQuote(quote, category, gptAPIKey)
# image_url = GetImageURL(prompt, gptAPIKey, ImageCount=1, ImageSize='1024x1024')
prompt = getChatGPTPromptFromQuote(quote, category, accessToken)
image_url = [get_image_url(prompt),]

print("Quote: " + quote +  author + "\n" + prompt)
SaveImage(image_url, imageName, quote, author)#, author)
SetWallpaper(imageName)
