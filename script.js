window.onload=function() {
    const searchButton = document.querySelector("#submit-guess");
    const searchBox = document.getElementById("guess");
    var score = 0;
    var turn = 1;
    var phraseList;
    var currPhrase;
    var nextPhrase;
    var rankings;
    // const apiUrl = "https://autocomplete-piu1.onrender.com/";
    const apiUrl = "http://127.0.0.1:8000/";

    async function getData(url) {
        let response = await fetch(url);
        let data = await response.json();
        return data;
    }

    async function postData(url, data) {
        await fetch(url, {
            method: "POST",
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify(data)});
    }

    function hideLeaderboard() {
        document.getElementById("lb").style.display = "none";
    }

    function showLeaderboard() {
        getData(apiUrl+"get-leaderboard").then(data => 
            rankings = data);
        setTimeout(() =>  {
            for (let i = 1; i <= 10; i++) {
                let doc = rankings[String(i)];
                if (doc) {
                    let date = doc.Month+"/"+doc.Day+"/"+doc.Year;
                    document.getElementById("score"+String(i)).innerHTML = doc.Score;
                    document.getElementById("date"+String(i)).innerHTML = date;
                }
            }
        }, 1000);
        let rank;
        getData(apiUrl+"get-rank?score="+score).then(data => document.getElementById("rank").innerHTML += data.Rank+"!");
        document.getElementById("lb").style.display = "block";
    }

    function numSpaces(phrase) {
        let count = 0;
        for (let i = 0; i < phrase.length; i++) {
            if (phrase.charAt(i) === " ") {
                count++;
            }
        }
        return count;
    }

    function phraseLength(phrase) {
        return phrase.length - numSpaces(phrase);
    }

    function vaildGuess(phrase, guess) {
        return (phrase.toLowerCase().search(guess.toLowerCase()) != -1);
    }

    function updateScore(guess) {
        let delta = Math.max(phraseLength(currPhrase.Optimal) - phraseLength(guess), 
                    phraseLength(guess) - phraseLength(currPhrase.Optimal))
    
        if (delta == 0) {
            document.getElementById("output").innerHTML = 
            "You had the optimal guess!";
        }
        else if (delta == 1) {
            document.getElementById("output").innerHTML = 
            "You were " + String(delta) + ' letter away from the optimal guess, "' + currPhrase.Optimal + '"!';
        } 
        else {
            document.getElementById("output").innerHTML = 
            "You were " + String(delta) + ' letters away from the optimal guess, "' + currPhrase.Optimal + '"!';
        }
        score += delta;
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
    

    function getPhrases() {
        getData(apiUrl+"get-phrase-list").then(data => 
            phraseList = data);
    }

    function setPhrase() {
        currPhrase = phraseList[String(turn)];
        document.getElementById("guess").setAttribute("placeholder", currPhrase.Phrase);
    }

    function submitGuess() {
        let guess = document.getElementById("guess").value;
        let phrase = currPhrase.Phrase;
        if (!vaildGuess(phrase, guess)) {
            document.getElementById("output").innerHTML = "Your guess must be a part of the search phrase!";
        }
        else {
            document.getElementById("output").innerHTML = "Searching Autocomplete...";
            updateScore(guess);
        }
        
    }

    async function endGame() {
        document.getElementById("guess-number").innerHTML = "Game over!";
        document.getElementById("guess").setAttribute("placeholder", "Game over!");
        document.getElementById("guess").value = "";
        document.getElementById("score").innerHTML = "Final " + document.getElementById("score").innerHTML
        searchButton.removeEventListener("click", submitOnClick);
        searchBox.removeEventListener("keydown", submitOnEnter);
        await postData(apiUrl+"post-score", {score: score});
        showLeaderboard();
    }

    function submitOnClick(event) {
        if (document.getElementById("guess").value.length != 0) {
            submitGuess();
        }
        
    }

    function submitOnEnter(event) {
        if (event.key === "Enter") {
            if (document.getElementById("guess").value.length != 0) {
                submitGuess();
            }
            
        }
    }

    hideLeaderboard();
    getPhrases();
    setTimeout(() => setPhrase(), 1000);
    searchButton.addEventListener("click", 
        submitOnClick
    )
    searchBox.addEventListener("keydown", 
        submitOnEnter
    )
    
}