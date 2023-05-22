import openai
import requests
import json
import ctypes
import os
from PIL import Image, ImageDraw, ImageFont

def FetchQuote(category, apiKey):
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': apiKey})
    if response.status_code == requests.codes.ok:
        responseDict = json.loads(response.text)
        return len(responseDict[0]['quote']), responseDict[0]['quote'], responseDict[0]['author']
    else:
        print("Error:", response.status_code, response.text)
        return '', ''
    
def GetQuote(category, apiKey):
    '''
        categories: 'age', 'alone', 'amazing', 'anger', 'architecture', 'art', 'attitude', 'beauty', 'best', 'birthday', 'business', 'car', 'change', 'communications', 'computers', 'cool', 
            'courage', 'dad', 'dating', 'death', 'design', 'dreams', 'education', 'environmental', 'equality', 'experience', 'failure', 'faith', 'family', 'famous', 'fear', 'fitness', 'food', 
            'forgiveness', 'freedom', 'friendship', 'funny', 'future', 'god', 'good', 'government', 'graduation', 'great', 'happiness', 'health', 'history', 'home', 'hope', 'humor', 'imagination', 
            'inspirational', 'intelligence', 'jealousy', 'knowledge', 'leadership', 'learning', 'legal', 'life', 'love', 'marriage', 'medical', 'men', 'mom', 'money', 'morning', 'movies', 'success'
    '''
    size = 100
    while size > 84:
        size, quote, author = FetchQuote(category, apiKey)
    return quote, " - " + author

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

def AddCaption(message, author, file, fontColor):
    message = message + '\n' + ' ' * (len(message) - len(author)) + author    
    image = Image.open(file)
    font = ImageFont.truetype("Amiko-Regular.ttf", size=int(image.size[0]/50))
    W, H = (image.size[0], image.size[1])
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), message, font=font)
    print(image.size)
    draw.text(((W-w)/2, (H-h)*7.5/8), message, fill=fontColor, font=font)#'OpenSansCondensed-LightItalic.ttf')
    image.save(file)
        
def SaveImage(urls, name, quote, author):
    for i in range(len(urls)):
        imageSaveName = f"{name}.png" if i == 0 else f"{name}{i}.png"
        image = requests.get(urls[i])
        with open(imageSaveName, "wb") as f:
            f.write(image.content)
        AddCaption(quote, author, imageSaveName, 'white')
        
def GetPromptFromQuote(quote, category, apiKey):
    openai.api_key = apiKey
    
    messages = [
        {"role": "system", "content": f"Your task is to create a prompt that i can give to an image generator to get back an wallpaper that encasulates the emotion and context of the quote. the wallpaper should have a darker asthetic, represent the theme {category} and contain no text. the propmt should only describe image details and color pallet in the wallpaper, limited to 30 words."},
        {"role": "user", "content": f"quote: {quote}"}
    ]
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
    )
    return completion.choices[0].message.content

def SetWallpaper(imageName):
    cwd = os.getcwd()
    ctypes.windll.user32.SystemParametersInfoW(20, 0, cwd+f"\{imageName}.png" , 0)
    
def GetQuoteHindi(category):
    '''
      categories: success, love, attitude, positive, motivational
    '''
    response = requests.get(f"https://hindi-quotes.vercel.app/random/{category}")
    responseDict = json.loads(response.text)
    
    return responseDict['quote'], ""   

imageName = 'wallpaper'
gptAPIKey = ""
category = 'motivational'
           
quote, author = GetQuoteHindi(category)
quote, author = GetQuote(category = 'change', apiKey = '') # Get yours from: https://api-ninjas.com/
prompt = GetPromptFromQuote(quote, category, gptAPIKey)
image_url = GetImageURL(prompt, gptAPIKey, ImageCount=1, ImageSize='1024x1024')

print("Quote: " + quote +  author + "\n" + prompt)
SaveImage(image_url, imageName, quote, author)#, author)
SetWallpaper(imageName)
