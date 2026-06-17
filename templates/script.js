async function generateQuestion(){
    const notes = document.getElementById('notes').value;
    if(!notes){
        alert('Please paste some notes first');
        return;
    }

    document.getElementById('result').style.display = 'none';

    const response = await fetch('/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({notes: notes})
    });

    const data = await response.json();
    document.getElementById('question').textContent = data.question;
    document.getElementById('result').style.display = 'block';
}

async function giveFeedback(){
    const question = document.getElementById('question').textContent;
    const answer = document.getElementById('answer').value;

    const response = await fetch('/feedback',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({question: question, answer: answer}),
    });

    const data = await response.json();
    

    document.getElementById('feedback').innerHTML = data.feedback;

}

