const sessionHistory = [];


async function generateQuestion(){
    const notes = document.getElementById('notes').value;
    if(!notes){
        alert('Please paste some notes first');
        return;
    }

    document.getElementById('loading').style.display = 'block';
    document.getElementById('result').style.display = 'none';

    const response = await fetch('/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({notes: notes})
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    document.getElementById('loading').style.display = 'none';
    document.getElementById('question').textContent = '';
    document.getElementById('result').style.display = 'block';

    while(true) {
        const {done, value} = await reader.read();
        if(done) break;
        const chunk = decoder.decode(value);
        document.getElementById('question').textContent += chunk;
    }
}

async function giveFeedback(){
    const question = document.getElementById('question').textContent;
    const answer = document.getElementById('answer').value;
    document.getElementById('loadingFeedback').style.display = 'block';

    const response = await fetch('/feedback',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question: question, answer: answer}),
    });

    const data = await response.json();
    
    document.getElementById('loadingFeedback').style.display = 'none';
    document.getElementById('feedback').innerHTML = data.feedback;
    sessionHistory.push({question: question, answer: answer, feedback: data.feedback});

}

function showSummary(){
    let summaryText = "";

    sessionHistory.forEach(function(item){
        summaryText += "Q: " + item.question + "\nA: " + item.answer + "\n\n";
    });

    document.getElementById('summaryContent').textContent = summaryText;
}

