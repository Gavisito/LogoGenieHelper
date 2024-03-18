document.addEventListener('DOMContentLoaded', (event) => {
    const questions = document.querySelectorAll('.question');

    questions.forEach(question => {
        question.addEventListener('click', () => {
            const answerId = question.getAttribute('id').replace('q', 'a');
            const answer = document.getElementById(answerId);
            if (answer.style.display === 'none' || answer.style.display === '') {
                answer.style.display = 'block';
            } else {
                answer.style.display = 'none';
            }
        });
    });
});