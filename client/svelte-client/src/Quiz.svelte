<script>
    import { onMount, onDestroy } from 'svelte';
    import CircularProgressbar from './CircularProgressbar.svelte';
    import ProgressBar from './ProgressBar.svelte';
    
    let question = '';
    let answers = [];
    let selectedAnswer = '';
    let quizCompleted = false;
    let timeLeft = 0;
    let timer;
    let isSubmitting = false;
    let feedback = '';
    let score = 0;
    let allScores = {};
    let isLoading = true;
    let currentQuestionIndex = 0;
    const totalQuestions = 5;

    async function getQuestion() {
        isLoading = true;
        try {
            const response = await fetch('http://192.168.1.105:5000/get_question');
            if (response.ok) {
                const data = await response.json();
                if (data.type === 'question') {
                    question = data.question;
                    answers = data.answers;
                    timeLeft = data.time_limit;
                    quizCompleted = false;
                    currentQuestionIndex++;
                    console.log(`Received question: ${question}`);
                    console.log(`Possible answers: ${answers}`);
                    startTimer();
                } else if (data.type === 'end') {
                    question = data.message;
                    answers = [];
                    quizCompleted = true;
                    score = data.score;
                    allScores = data.all_scores;
                    console.log(`Quiz completed: ${question}`);
                }
            } else {
                console.error('Failed to fetch question');
                feedback = 'Failed to fetch question. Please try again.';
            }
        } catch (error) {
            console.error('Error fetching question:', error);
            feedback = 'Error fetching question. Please try again.';
        } finally {
            isLoading = false;
        }
    }

    async function submitAnswer() {
        if (selectedAnswer && !isSubmitting) {
            isSubmitting = true;
            feedback = 'Submitting answer...';
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
                        timeLeft = data.time_limit;
                        selectedAnswer = '';
                        feedback = 'Answer submitted successfully!';
                        currentQuestionIndex++;
                        console.log(`Received next question: ${question}`);
                        console.log(`Possible answers: ${answers}`);
                        startTimer();
                    } else if (data.type === 'end') {
                        question = data.message;
                        answers = [];
                        quizCompleted = true;
                        score = data.score;
                        allScores = data.all_scores;
                        feedback = 'Quiz completed!';
                        console.log(`Quiz completed: ${question}`);
                    }
                } else {
                    console.error('Failed to submit answer');
                    feedback = 'Failed to submit answer. Please try again.';
                }
            } catch (error) {
                console.error('Error submitting answer:', error);
                feedback = 'Error submitting answer. Please try again.';
            } finally {
                isSubmitting = false;
            }
        }
    }

    function startTimer() {
        clearInterval(timer);
        timer = setInterval(() => {
            if (timeLeft > 0) {
                timeLeft--;
            } else {
                clearInterval(timer);
                submitAnswer();
            }
        }, 1000);
    }

    onMount(() => {
        getQuestion();
    });

    onDestroy(() => {
        clearInterval(timer);
    });

    const colors = ['#DFFFEC', '#FF9797', '#F9DADA', '#D4C6FE'];
</script>

<main>
    {#if isLoading}
        <div class="loading">
            <CircularProgressbar value={100} maxValue={100} text="Loading..." />
        </div>
    {:else if !quizCompleted}
        <h1 class="title">Quiz Question</h1>
        <ProgressBar current={currentQuestionIndex} total={totalQuestions} />
        <p class="question">{question}</p>
        <p class="timer">Time left: {timeLeft} seconds</p>
        <div class="answers-container">
            {#each answers as answer, index}
                <div class="answer-block" style="background-color: {colors[index % colors.length]};">
                    <input type="radio" id={`answer${index}`} name="answer" value={answer} bind:group={selectedAnswer} />
                    <label for={`answer${index}`} class="answer-text">{answer}</label>
                </div>
            {/each}
        </div>
        <button class="submit-button" on:click={submitAnswer} disabled={isSubmitting || !selectedAnswer}>
            {isSubmitting ? 'Submitting...' : 'Submit Answer'}
        </button>
        {#if feedback}
            <p class="feedback">{feedback}</p>
        {/if}
    {:else}
        <h1 class="title">Quiz Completed</h1>
        <p class="question">{question}</p>
        <p class="score">Your score: {score}</p>
        <h2>All Scores:</h2>
        <ul>
            {#each Object.entries(allScores) as [player, playerScore]}
                <li>{player}: {playerScore} points</li>
            {/each}
        </ul>
    {/if}
</main>

<style>
    .title {
        font-size: 24px;
        margin-bottom: 20px;
        text-align: center;
        color: black;
    }
    .question {
        font-size: 18px;
        margin-bottom: 15px;
    }
    .timer {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 15px;
        text-align: center;
    }
    .answers-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        gap: 20px;
        width: 100%;
        height: 30vh;
    }
    .answer-block {
        width: 150px;
        height: 150px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
    }
    .answer-block:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .answer-text {
        margin-top: 10px;
        text-align: center;
        font-weight: bold;
    }
    .submit-button {
        background-color: #030303;
        color: white;
        width: 200px;
        border: none;
        cursor: pointer;
    }
    input[type="radio"] {
        display: none;
    }
    input[type="radio"]:checked + .answer-text {
        color: #ffffff;
    }
    .submit-button:hover:not(:disabled) {
        background-color: #3e463f;
    }
    .submit-button:disabled {
        background-color: #cccccc;
        cursor: not-allowed;
    }
    .feedback {
        margin-top: 10px;
        font-style: italic;
        color: #666;
    }
    h2 {
        text-align: center;
    }
    li {
        text-align: center;
        list-style-type: none;
        color: rgb(0, 0, 0);
    }
    .score {
        font-size: 20px;
        font-weight: bold;
        margin-top: 20px;
        text-align: center;
    }
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 60vh;
    }
</style>