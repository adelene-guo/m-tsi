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