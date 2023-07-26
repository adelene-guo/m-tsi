var number = 0;
var currentSong = 0;
number++; // how to make the variable universal cross all accounts?

const songnames = [
    "Miss the Rage (feat. PlayBoi Carti)",
    "Moonlight Sonata",
    "Attention"
]
const singers = [
    "Trippie Redd",
    "Ludwig van Beethoven",
    "New Jeans"
]

document.getElementById("number").innerHTML = number;

//forever:
document.getElementById("songName").innerHTML = songnames[currentSong]+"<p style='color: #CC5500;'>"+singers[currentSong];
//when song is over:
currentSong+=1

function mixingOn(){
    var mixSwitch = document.getElementById("mixingOn")
    if (mixSwitch.checked == true){
        document.getElementById("mixingText").innerHTML = "mixing on";
    }
    else if (mixSwitch.checked == false){
            document.getElementById("mixingText").innerHTML = "mixing off";
    }
   }

   let queue = [];

   function addToQueue() {
       const inputField = document.getElementById("song-input");
       const inputField1 = document.getElementById("artist-input");
       const songName = inputField.value.trim();
       const artistName = inputField1.value.trim();

       if (songName !== "" && artistName !== "") {
           queue.push(songName +" by "+artistName);
           inputField.value = "";
           inputField1.value = "";
           renderQueue();
       }
       /*add song to spreadsheet

    try:
        search_result = sp.search(songName, limit=1, type='track')
        track = search_result['tracks']['items'][0]
        track_id = track['id']

        # Check for duplicates before adding
        if track_id not in added_track_ids:
            # Get audio features for the track
            audio_features = sp.audio_features(track_id)[0]

            # Append data to the dataframe
            track_df.loc[track_id] = {
                'ID': track_id,
                'Album Cover': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'Duration (ms)': track['duration_ms'],
                'Popularity': track['popularity'],
                'Danceability': audio_features['danceability'],
                'Energy': audio_features['energy'],
                'Valence': audio_features['valence'],
                'Key': audio_features['key'],
                'Tempo': audio_features['tempo'],
                'Time Signature': audio_features['time_signature']
            }

            sp.playlist_add_items(playlist_id, [track_id])
            added_track_ids.append(track_id)
            print("added: " + str(song))

        else:
            print(f"Duplicate song {song} skipped.")

    except IndexError:
        print(f"Couldn't find {song} on Spotify.")
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error searching for {song}. Error: {e}")
*/
       
   }

   function removeFromQueue(index) {
       queue.splice(index, 1);
       renderQueue();
   }

   function renderQueue() {
       const queueList = document.getElementById("queue-list");
       queueList.innerHTML = "";

       queue.forEach((song, index) => {
           const listItem = document.createElement("li");
           listItem.className = "queue-item";
           listItem.innerHTML = `
               <span>${song}</span>
               <button style="color:black;" onclick="removeFromQueue(${index})">Remove</button>
           `;
           queueList.appendChild(listItem);
       });
   }
   function clearQueue() {
    queue = [];
    renderQueue();
}