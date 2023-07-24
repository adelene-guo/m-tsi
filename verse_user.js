var number = 20;
var currentSong = 0;
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
       const songName = inputField.value.trim();

       if (songName !== "") {
           queue.push(songName);
           inputField.value = "";
           renderQueue();
       }
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