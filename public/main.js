var canvas = document.createElement('canvas');
var ctx = canvas.getContext('2d');

var selectedTeamA = document.getElementById("inputGroupSelectTeamA")
var selectedTeamB = document.getElementById("inputGroupSelectTeamB")

var resultBox = document.getElementById("resultBox")
var modelDesc = document.getElementById("model-descrp")

var SimulateButton1 = document.getElementById("simulate-btn-1")
var SimulateButton2 = document.getElementById("simulate-btn-2")
var SimulateButton3 = document.getElementById("simulate-btn-3")

SimulateButton1.style.display = "none"
SimulateButton2.style.display = "none"
SimulateButton3.style.display = "none"

var rad1 = document.getElementById("gridRadios1")
var rad2 = document.getElementById("gridRadios2")
var rad3 = document.getElementById("gridRadios3")

rad1.addEventListener('click', ()=> {
    SimulateButton1.style.display = "block"
    SimulateButton2.style.display = "none"
    SimulateButton3.style.display = "none"
    modelDesc.innerHTML = "Model 1 is based on simple Monte Carlo simulation (uses team score, and opponent team score)."
})

rad2.addEventListener('click', ()=> {
    SimulateButton2.style.display = "block"
    SimulateButton1.style.display = "none"
    SimulateButton3.style.display = "none"
    modelDesc.innerHTML = "Model 2 also uses Monte Carlo simulation, but this time, the model utilizes advanced stats to calculate team/opponent team score."
})

rad3.addEventListener('click', ()=> {
    SimulateButton3.style.display = "block"
    SimulateButton1.style.display = "none"
    SimulateButton2.style.display = "none"
    modelDesc.innerHTML = "Model 3 trains naive bayes model by using in season advance stats (win/lose are the classifications). The trained naive bayes model predicts win/lose rate based on the randomly generated advanced stats."
})

// function showSimulateBtn() {
//     if (selectedTeamA.value != 'Choose...' && selectedTeamB.value != 'Choose...') {
//         SimulateButton1.style.display = "block"
//     }
// }

selectedTeamA.addEventListener('change', () => {
        var oldPic = document.getElementById("teamApic")
        if (oldPic) {
            oldPic.remove()
        }
        var img = document.createElement("img");
        img.setAttribute("id", "teamApic")
    
        img.src = "./pics/"+selectedTeamA.value+".png";
        var src = document.getElementById("forPic");
        src.appendChild(img);
        document.getElementById("teamApic").style.maxWidth = "200px"
        // showSimulateBtn()
    }
)

selectedTeamB.addEventListener('change', () => {
    var oldPicB = document.getElementById("teamBpic")
    if (oldPicB) {
        oldPicB.remove()
    }
    var img = document.createElement("img");
    img.setAttribute("id", "teamBpic")

    img.src = "./pics/"+selectedTeamB.value+".png";
    var src = document.getElementById("forPicB");
    src.appendChild(img);
    document.getElementById("teamBpic").style.maxWidth = "200px"
    // showSimulateBtn()
}
)

SimulateButton1.addEventListener('click', ()=> {
    resultBox.innerHTML = "Waiting for results"
    $.ajax({
        type: 'POST', // added,
        url: '/',
        contentType: 'application/json',
        data: JSON.stringify({"model":"1", teamA: selectedTeamA.value, teamB: selectedTeamB.value}),
        // data: '{"data": "TEST"}',
        //dataType: 'jsonp' - removed
        //jsonpCallback: 'callback' - removed
        success: (data)=> {
            retData = JSON.parse(data)
            var res = retData.split("\n")
            var teamAwinRate = parseFloat(res[0]) * 100
            var teamBwinRate = parseFloat(res[1]) * 100 
            var tieRate = parseFloat(res[2]) * 100 
            resultBox.innerHTML = selectedTeamA.value + " win rate: " + Math.round(teamAwinRate) + "%<br />"
            resultBox.innerHTML += selectedTeamB.value + " win rate: " + Math.round(teamBwinRate) + "%<br />"
            resultBox.innerHTML += "Tie rate: " + Math.round(tieRate) + "%<br />"

        }
        });
})


SimulateButton2.addEventListener('click', ()=> {
    resultBox.innerHTML = "Waiting for results"
    $.ajax({
        type: 'POST', // added,
        url: '/',
        contentType: 'application/json',
        data: JSON.stringify({"model":"2", teamA: selectedTeamA.value, teamB: selectedTeamB.value}),
        // data: '{"data": "TEST"}',
        //dataType: 'jsonp' - removed
        //jsonpCallback: 'callback' - removed
        success: (data)=> {
            retData = JSON.parse(data)
            var res = retData.split("\n")
            var teamAwinRate = parseFloat(res[0]) * 100
            var teamBwinRate = parseFloat(res[1]) * 100 
            var tieRate = parseFloat(res[2]) * 100 
            resultBox.innerHTML = selectedTeamA.value + " win rate: " + Math.round(teamAwinRate) + "%<br />"
            resultBox.innerHTML += selectedTeamB.value + " win rate: " + Math.round(teamBwinRate) + "%<br />"
            resultBox.innerHTML += "Tie rate: " + Math.round(tieRate) + "%<br />"
        }
        });
})

SimulateButton3.addEventListener('click', ()=> {
    resultBox.innerHTML = "Waiting for results"
    $.ajax({
        type: 'POST', // added,
        url: '/',
        contentType: 'application/json',
        data: JSON.stringify({"model":"3", teamA: selectedTeamA.value, teamB: selectedTeamB.value}),

        success: (data)=> {
            retData = JSON.parse(data)
            var res = retData.split("\n")
            var gamesPlayed = res[0]
            var gamesWon = res[1]
            var winRate = parseFloat(res[2]) * 100
            // var teamAwinRate = parseFloat(res[0]) * 100
            // var teamBwinRate = parseFloat(res[1]) * 100 
            // var tieRate = parseFloat(res[2]) * 100 
            resultBox.innerHTML = selectedTeamA.value + " is likely to win " + gamesWon + "/" + gamesPlayed + " games<br />"
            resultBox.innerHTML += selectedTeamA.value + " win rate is " + Math.round(winRate) + "%"
            // resultBox.innerHTML = selectedTeamA.value + " win rate: " + Math.round(teamAwinRate) + "%<br />"
            // resultBox.innerHTML += selectedTeamB.value + " win rate: " + Math.round(teamBwinRate) + "%<br />"
            // resultBox.innerHTML += "Tie rate: " + Math.round(tieRate) + "%<br />"
        }
        });
})