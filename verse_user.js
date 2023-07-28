var number = 5;
var currentSong = 0; // how to make the variable universal cross all accounts?

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

/*
    function addSongToPlaylist() {
        const inputField = document.getElementById("song-input");
        const songName = inputField.value.trim();
    
        if (songName !== "") {
            const data = {
                song_name: songName
            };
    
            fetch('/add_song', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log(`Added ${songName} to playlist!`);
                    inputField.value = "";
                } else {
                    console.error('Error adding song:', data.error);
                }
            })
            .catch(error => {
                console.error('Error adding song:', error);
            });
        }
    }
    *\
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
       

let queue = [];

// Function to add a song to the queue
function addSong() {
    const songInput = document.getElementById('song-input');
    const artistInput = document.getElementById('artist-input');
    const songName = songInput.value.trim();
    const artistName = artistInput.value.trim();

    if (songName !== '') {
        queue.push(songName+" by "+artistName+"  ");
        songInput.value = '';
        artistInput.value = '';
        renderQueue();
    }
}

// Function to remove a song from the queue
function removeSong(index) {
    queue.splice(index, 1);
    renderQueue();
}

function clearQueue(){
    queue = [];
    renderQueue();
}

// Function to render the song queue
function renderQueue() {
    const songQueue = document.getElementById('queue-list');
    songQueue.innerHTML = '';

    queue.forEach((song, index) => {
        const listItem = document.createElement('li');
        listItem.textContent = song;

        const removeButton = document.createElement('button');
        removeButton.textContent = 'Remove';
        removeButton.style.color = "black";
        removeButton.onclick = () => removeSong(index);

        listItem.appendChild(removeButton);
        songQueue.appendChild(listItem);
    });
}