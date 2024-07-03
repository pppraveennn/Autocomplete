window.onload=function() {
    const searchButton = document.querySelector("#submit-guess");
    const searchBox = document.getElementById("guess");
    var score = 0;
    var turn = 1;
    const apiUrl = "http://127.0.0.1:8000/";

    async function getData(url) {
        let response = await fetch(url);
        let data = await response.json();
        return data;
    }


    function updateScore(data) {
        if (data.Error) {
            document.getElementById("output").innerHTML = data.Error;
        }
        else {
            if (data.Score == 1) {
                document.getElementById("output").innerHTML = 
                "You were " + String(data.Score) + ' letter away from the optimal guess, "' + data.Optimal + '"!';
            } 
            else {
                document.getElementById("output").innerHTML = 
                "You were " + String(data.Score) + ' letters away from the optimal guess, "' + data.Optimal + '"!';
            }
            score += data.Score;
            document.getElementById("score").innerHTML = "Score: " + String(score);
            if (turn === 10) {
                endGame();
            }
            else {
                turn += 1;
                document.getElementById("guess-number").innerHTML = "Guess #" + String(turn);
                setPhrase();
                document.getElementById("guess").value = ""
            }
            
        }
    }

    function setPhrase() {
        getData(apiUrl+"get-phrase").then(data => 
            document.getElementById("guess").setAttribute("placeholder", data.Phrase));
    }

    function submitGuess() {
        let guess = document.getElementById("guess").value;
        console.log(guess);
        let phrase = document.getElementById("guess").getAttribute("placeholder");
        document.getElementById("output").innerHTML = "loading..."
        getData(apiUrl+"get-score/?phrase="+phrase+"&guess="+guess).then(data =>
            updateScore(data)
        )
    }

    function endGame() {
        document.getElementById("guess-number").innerHTML = "Game over!";
        document.getElementById("guess").setAttribute("placeholder", "Game over!");
        document.getElementById("guess").value = "";
        searchButton.removeEventListener("click", submitOnClick);
        searchBox.removeEventListener("keydown", submitOnEnter);
        
    }

    function submitOnClick(event) {
        submitGuess();
    }

    function submitOnEnter(event) {
        if (event.key === "Enter") {
            submitGuess();
        }
    }

    setPhrase();
    searchButton.addEventListener("click", 
        submitOnClick
    )
    searchBox.addEventListener("keydown", 
        submitOnEnter
    )
    
}