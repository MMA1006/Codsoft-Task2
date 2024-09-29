let gameOver = false; // Variable to track if the game is over

document.querySelectorAll('.cell').forEach(cell => {
    cell.addEventListener('click', function() {
        if (this.classList.contains('clicked') || gameOver) {
            return; // Prevent click if cell is already clicked or game is over
        }

        const row = this.getAttribute('data-row');
        const col = this.getAttribute('data-col');

        // Mark the clicked cell to prevent further clicks
        this.classList.add('clicked');

        fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ row: parseInt(row), col: parseInt(col) })
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);
            if (data.game_over) {
                document.getElementById('game-status').innerText = `Game Over! ${data.player} Wins!`;
                gameOver = true; // Set game over flag
            } else {
                document.getElementById('game-status').innerText = ''; // Clear status message
            }
        });
    });
});

document.getElementById('reset').addEventListener('click', () => {
    fetch('/reset', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        updateBoard(data.board);
        document.getElementById('game-status').innerText = ''; // Clear status message
        gameOver = false; // Reset game over flag
        // Remove 'clicked' class from all cells
        document.querySelectorAll('.cell').forEach(cell => cell.classList.remove('clicked'));
    });
});

function updateBoard(board) {
    const cells = document.querySelectorAll('.cell');
    cells.forEach((cell, index) => {
        cell.innerText = board[Math.floor(index / 3)][index % 3] || '';
        if (board[Math.floor(index / 3)][index % 3] !== null) {
            cell.classList.add('clicked'); // Mark cell if already filled
        } else {
            cell.classList.remove('clicked'); // Ensure 'clicked' is removed for empty cells
        }
    });
}
