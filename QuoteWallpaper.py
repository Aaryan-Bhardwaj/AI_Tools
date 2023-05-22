import openai
import requests
import json
import ctypes
import os
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from io import BytesIO

def GetQuote(categories, languague = "english"):
    if languague == "english":        
        responseDict = json.loads(requests.get('https://api.quotable.io/tags').text)
        tagslugs = [tag['slug'] for tag in responseDict]
        tagnames = [tag['name'] for tag in responseDict]
        categoryString = ''
        for category in categories:
            if category in tagslugs or category in tagnames:
                categoryString = categoryString + ',' + category
        response = requests.get('https://api.quotable.io/quotes/random?tags=' + category + "&maxLength=128&limit=1")
        responseDict = json.loads(response.text)[0]
        return responseDict['content'], " - " + responseDict['author']
    elif languague == "hindi":
        for category in categories:
            if category in ['success', 'love', 'attitude', 'positive', 'motivational']:
                response = requests.get(f"https://hindi-quotes.vercel.app/random/{category}")
                responseDict = json.loads(response.text)        
                return responseDict['quote'], ""
    else:
        print("Invalid Language:")
        exit()
        
def GetPromptFromQuote(quote, category, apiKey):
    openai.api_key = apiKey
    
    messages = [
        {"role": "system", "content": f"Your task is to create a prompt that i can give to an image generator to get back an wallpaper that encapsulates the emotion and context of the quote. the wallpaper should have a dark but colorful asthetic, represent the theme of '{category[0]}' and not contain any text. the prompt should only describe image details and color pallet in the wallpaper, limited to 30 words."},
        {"role": "user", "content": f"quote: {quote}"}
    ]
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
    )
    return completion.choices[0].message.content

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

def ExtendImage(img, screenAspectRatio, prompt):
    def get_image(image_url):
        # Send a GET request to the URL and store the response
        response = requests.get(image_url)
        # Check if the request was successful
        if response.status_code == 200:
            # Write the image content to a buffer
            image_buffer = BytesIO(response.content)
            return Image.open(image_buffer)
        else:
            raise ValueError(f'Image could not be retrieved from {image_url}')
        
    h, w = img.size
    f = 3
    newWidth = int(w * screenAspectRatio)
    rectangle = np.zeros([h, newWidth, f], dtype='uint8')
    start = (newWidth - w) // 2
    rectangle[:,start:start + w] = np.array(img)

    left = rectangle[:, :h]
    right = rectangle[:, -h:]

    # Left part is all zeros
    mask_left = np.hstack([np.zeros([h, start, f+1]), 
                            255*np.ones([h, w - start , f+1])]).astype('uint8')
    mask_right = np.hstack([255*np.ones([h, w - start, f+1]), 
                            np.zeros([h, start, f+1])]).astype('uint8')

    left_buffer = BytesIO()
    mask_buffer = BytesIO()

    Image.fromarray(left).save(left_buffer, 'png')
    Image.fromarray(mask_left).save(mask_buffer, 'png')

    edit_top = openai.Image.create_edit(
        image=left_buffer.getvalue(),
        mask=mask_buffer.getvalue(),
        prompt=prompt,
        n=1,
        size='1024x1024'
    )
    image_left = get_image(edit_top['data'][0]['url'])
    
    right_buffer = BytesIO()
    mask_buffer = BytesIO()

    Image.fromarray(right).save(right_buffer, 'png')
    Image.fromarray(mask_right).save(mask_buffer, 'png')

    edit_top = openai.Image.create_edit(
        image=right_buffer.getvalue(),
        mask=mask_buffer.getvalue(),
        prompt=prompt,
        n=1,
        size='1024x1024'
    )
    image_right = get_image(edit_top['data'][0]['url'])
    
    img_final = Image.new('RGB', (newWidth, rectangle.shape[0]))
    img_final.paste(image_left, (0, 0))
    img_final.paste(image_right, (newWidth - w, 0))
    
    return img_final

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

def ProcessImage(image, message, author, prompt, extended):
    user32 = ctypes.windll.user32    
    screenAspectRatio = user32.GetSystemMetrics(0) / user32.GetSystemMetrics(1) # width / height
    image = Image.open(image)
    if extended:
        imageExtended = ExtendImage(image, screenAspectRatio, prompt)
        image = AddCaption(imageExtended.copy(), message, author)
        return image, imageExtended
    else:
        imagePadded = AddPaddingToWallpaper(image, screenAspectRatio)
        image = AddCaption(imagePadded.copy(), message, author)
        return image, imagePadded
        
def SaveImage(urls, name, quote, author, prompt, extended):
    if not os.path.exists(name.split('/')[0]):
        os.makedirs(name.split('/')[0])
    for i in range(len(urls)):
        imageSaveName = f"{name}.png"
        imageData = requests.get(urls[i]).content
        imageStream = io.BytesIO(imageData)
        image, imageNoCaption = ProcessImage(imageStream, quote, author, prompt, extended)
        count = 1
        while os.path.exists(imageSaveName):
            imageSaveName = f"{name}{count}.png"
            imageNoCaptionSaveName = f"{name}{count}_nocap.png"
            count += 1            
        image.save(imageSaveName)
        imageNoCaption.save(imageNoCaptionSaveName)
        
    return imageSaveName

def SetWallpaper(imageName):
    cwd = os.getcwd()
    ctypes.windll.user32.SystemParametersInfoW(20, 0, cwd+f"\{imageName}" , 0) 

imageName = 'Wallpapers/wallpaper'
gptAPIKey = ""
category = ['technology' ,'famous-quotes']  # hindi_categories: success, love, attitude, positive, motivational
languague = 'english' # english or hindi

quote, author = GetQuote(category, languague)
prompt = GetPromptFromQuote(quote, category, gptAPIKey)
image_url = GetImageURL(prompt, gptAPIKey, ImageCount=1, ImageSize='1024x1024')

print("Quote: " + quote +  author + "\n" + prompt)
imageName = SaveImage(image_url, imageName, quote, author, prompt, extended=True)
SetWallpaper(imageName)
