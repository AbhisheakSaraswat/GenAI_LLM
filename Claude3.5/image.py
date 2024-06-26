import base64
from app import client, MODEL_NAME, os

def get_completion(messages):
    response = client.messages.create(
        model = MODEL_NAME,
        max_tokens = 2000,
        temperature=0,
        messages= messages
    )
    return response.content[0].text

image = "Bill.png"
with open(image,"rb") as image_file:
    binary_data = image_file.read()
    base_64_encoded_data = base64.b64encode(binary_data)
    base_64_string = base_64_encoded_data.decode('utf-8')

messages = [
    {
        "role" : 'user',
        "content" : [
            {
                "type" : "image",
                "source" : {
                    "type" : "base64",
                    "media_type" : "image/png",
                    "data" : base_64_string
                }
            },
            {
                "type": "text",
                "text" : """Could you assist me with these queries: 
                1.) What exactly is the Consumer No.?
                2.) Would you be able to extract useful details and save them into the JSON format?
                 """
            }
        ]
    }
]
print(get_completion(messages))
