<script>
    import { onMount, onDestroy } from 'svelte';
    import ProgressBar from './ProgressBar.svelte';  

    let question = '';
    let answers = [];
    let selectedAnswer = '';
    let quizCompleted = false;
    let timeLeft = 0;
    let totalTime = 30;
    let timer;
    let isSubmitting = false;
    let feedback = '';
    let score = 0;
    let allScores = {};
    let isLoading = true;
    let currentQuestionIndex = 0;
    const totalQuestions = 5;  

    async function startNewGame() {
        isLoading = true;
        currentQuestionIndex = 0;
        quizCompleted = false;
        score = 0;
        selectedAnswer = ''; 
        await getQuestion(); 
        isLoading = false;
    }

    async function getQuestion() {
        try {
            const response = await fetch('http://192.168.1.105:5000/get_question');
            if (response.ok) {
                const data = await response.json();
                if (data.type === 'question') {
                    question = data.question;
                    answers = data.answers;
                    timeLeft = data.time_limit;
                    totalTime = data.time_limit;
                    quizCompleted = false;
                    currentQuestionIndex++;
                    selectedAnswer = '';  
                    startTimer();  
                } else if (data.type === 'end') {
                    question = data.message;
                    answers = [];
                    quizCompleted = true;
                    score = data.score;
                    allScores = data.all_scores;

                    await showScoresFor10Seconds();
                    await startNewGame();
                }
            } else {
                feedback = 'Failed to fetch question. Please try again.';
            }
        } catch (error) {
            feedback = 'Error fetching question. Please try again.';
        } finally {
            isLoading = false;
        }
    }

    async function showScoresFor10Seconds() {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve();
            }, 3000);  
        });
    }

    function startTimer() {
        clearInterval(timer);  
        timer = setInterval(() => {
            if (timeLeft > 0) {
                timeLeft--;
            } else {
                clearInterval(timer);
                autoSubmitAnswer();  
            }
        }, 1000);
    }

    function autoSubmitAnswer() {
        if (!selectedAnswer) {
            const randomIndex = Math.floor(Math.random() * answers.length);
            selectedAnswer = answers[randomIndex];
        }
        submitAnswer();  
    }

    async function submitAnswer() {
        if (isSubmitting) return;
        if (!selectedAnswer) {
            feedback = 'Please select an answer before submitting.';
            return;
        }
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
                    totalTime = data.time_limit;
                    selectedAnswer = ''; 
                    feedback = '';
                    startTimer();  
                } else if (data.type === 'end') {
                    question = data.message;
                    answers = [];
                    quizCompleted = true;
                    score = data.score;
                    allScores = data.all_scores;

                    await showScoresFor10Seconds();
                    await startNewGame();
                }
            } else {
                feedback = 'Failed to submit answer. Please try again.';
            }
        } catch (error) {
            feedback = 'Error submitting answer. Please try again.';
        } finally {
            isSubmitting = false;
        }
    }

    function selectAnswer(answer) {
        if (!isSubmitting) {
            selectedAnswer = answer;  
        }
    }

    function getColor(index) {
        const colors = ['#DFFFEC', '#FF9797', '#F9DADA', '#D4C6FE'];  
        return colors[index % colors.length];  
    }

    onMount(async () => {
        await getQuestion();
    });

    onDestroy(() => {
        clearTimeout(timer);
    });
</script>

<main>
    {#if isLoading}
        <div class="loading">Loading...</div>
    {:else}
        <div>
            {#if quizCompleted}
                <h2>Quiz completed! Your score: {score}</h2>
                <h3>All Players' Scores:</h3>
                <ul>
                    {#each Object.entries(allScores) as [player, playerScore]}
                        <li>{player}: {playerScore} points</li>
                    {/each}
                </ul>
                <button class="submit-button" on:click={startNewGame}>Start New Game</button>
            {:else}
                <h1 class="question">{question}</h1>
                <p class="timer">Time left: {timeLeft} seconds</p> 
                <ProgressBar current={currentQuestionIndex} total={totalQuestions} />  
                <div class="answers-container">
                    {#each answers as answer, index}
                        <button 
                            class="answer-block {selectedAnswer === answer ? 'selected' : ''}" 
                            style="background-color: {getColor(index)};"  
                            on:click={() => selectAnswer(answer)}>
                            <span class="answer-text">{answer}</span>
                        </button>
                    {/each}
                </div>
                <button 
                    class="submit-button" 
                    on:click={submitAnswer} 
                    disabled={!selectedAnswer || isSubmitting}>
                    {isSubmitting ? 'Submitting...' : 'Submit Answer'}
                </button>
                {#if feedback}
                    <p class="feedback">{feedback}</p>
                {/if}
            {/if}
        </div>
    {/if}
</main>

<style>
    .question {
        font-size: 18px;
        margin-bottom: 15px;
        text-align: center;
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
        margin-bottom: 20px;
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
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        text-align: center;
        border: 2px solid #D3D3D3; 
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .answer-block:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    .answer-block.selected {
        border: 3px solid #fdd1d9; 
    }
    .answer-text {
        font-weight: bold;
        text-align: center;
    }
    .submit-button {
        background-color: #201c1f;
        color: white;
        width: 200px;
        border: none;
        cursor: pointer;
        padding: 10px;
        font-size: 16px;
        margin: 0 auto;
        display: block;
    }
    .submit-button:hover:not(:disabled) {
        background-color: #52494e;
    }
    .submit-button:disabled {
        background-color: #cccccc;
        cursor: not-allowed;
    }
    .feedback {
        margin-top: 10px;
        font-style: italic;
        color: #666;
        text-align: center;
    }
    ul {
        text-align: center;
        list-style-type: none;
        padding: 0;
    }
    ul li {
        font-size: 16px;
        margin-bottom: 5px;
    }
    h2, h3 {
        text-align: center;
        margin-top: 20px;
    }
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 60vh;
    }
</style>
