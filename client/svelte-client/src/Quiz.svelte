<script>
    import { onMount } from 'svelte';
    let question = '';
    let answers = [];
    let selectedAnswer = '';
    let quizCompleted = false;
  
    async function getQuestion() {
        try {
            const response = await fetch('http://192.168.1.105:5000/get_question');
            if (response.ok) {
                const data = await response.json();
                if (data.type === 'question') {
                    question = data.question;
                    answers = data.answers;
                    quizCompleted = false;
                    console.log(`Received question: ${question}`);
                    console.log(`Possible answers: ${answers}`);
                } else if (data.type === 'end') {
                    question = data.message;
                    answers = [];
                    quizCompleted = true;
                    console.log(`Quiz completed: ${question}`);
                }
            } else {
                console.error('Failed to fetch question');
            }
        } catch (error) {
            console.error('Error fetching question:', error);
        }
    }
  
    async function submitAnswer() {
        if (selectedAnswer) {
            try {
                const response = await fetch('http://192.168.1.105:5000/submit_answer', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ answer: selectedAnswer })
                });
  
                if (response.ok) {
                    const data = await response.json();
                    if (data.type === 'question') {
                        question = data.question;
                        answers = data.answers;
                        console.log(`Received next question: ${question}`);
                        console.log(`Possible answers: ${answers}`);
                    } else if (data.type === 'end') {
                        question = data.message;
                        answers = [];
                        quizCompleted = true;
                        console.log(`Quiz completed: ${question}`);
                    }
                } else {
                    console.error('Failed to submit answer');
                }
            } catch (error) {
                console.error('Error submitting answer:', error);
            }
        }
    }
  
    onMount(() => {
        getQuestion();
    });
  
    // Define colors for each answer
    const colors = ['#DFFFEC', '#FF9797', '#F9DADA', '#D4C6FE'];
  </script>
  
  <main>
    {#if !quizCompleted}
      <h1 class="title">Quiz Question</h1>
      <p class="question">{question}</p>
      <div class="answers-container">
          {#each answers as answer, index}
              <div class="answer-block" style="background-color: {colors[index % colors.length]};">
                  <input type="radio" id={`answer${index}`} name="answer" value={answer} bind:group={selectedAnswer} />
                  <label for={`answer${index}`} class="answer-text">{answer}</label>
              </div>
          {/each}
      </div>
      <button class="submit-button" on:click={submitAnswer}>Submit Answer</button>
    {:else}
      <h1 class="title">{question}</h1>
    {/if}
  </main>
  