"""
Chase Leibowitz
M&TSI 2023
7/21/23

This script takes the user's favorite songs from the cloud from the downloadData script, uploads it to the GPT 3.5 Turbo API,
and then gets a return of similar songs. The script then cleans the data and prints it.
"""

import openai
import requests
from downloadData import df, len_data
print(df)

songs = df['Track Name'].to_string(index=False)
#print(songs)

# function to ask ChatGPT
def ask_GPT(input, key):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
    }

    data = {
        "model": "gpt-3.5-turbo",  # Change this to the desired model (e.g., "gpt-3.5-turbo")
        "messages": [{"role": "system", "content": "You are a DJ for an event. You will read the songs that are sent as the input and then create a playlist that is double the length of the songs inputted that will be in similar style and taste to the songs submitted. None of the songs you give will be the same as the ones I feed to you"},
                     {"role": "user", "content": input}]
    }

    response = requests.post(api_url, headers=headers, json=data)


    response_data = response.json()
    return response_data

key = "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"

response = ask_GPT(songs, key)
#print(response)

print('\n\ncreating AI playlist...\n')
assistant = response['choices'][0]['message']['content']


# print the new songs
print(assistant)


'''# chatGPT saved my ass with these 2 lines
#start_index = assistant.find("To complete the playlist, I have added the following songs that align with the style and taste of the songs you provided:\n\n")
#end_index = assistant.find("\n\nThis playlist should provide a similar style and taste to the songs you submitted, creating a cohesive and enjoyable listening experience for your event. Enjoy!")


start_index = assistant.find('1')


new_songs = assistant[start_index::]


#print(str(len_data))
#clean up api response to just get songs
#song_start = new_songs.find(str(len_data))
#cleaned_new_songs = new_songs[song_start::]

# print the songs
print("Here are your new songs:")
print(new_songs)




'''