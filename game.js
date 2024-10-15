const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let player = {
  x: 400,
  y: 300,
  width: 50,
  height: 50,
  speed: 5,
  dx: 0,
  dy: 0
};

// Draw the player
function drawPlayer() {
  ctx.fillStyle = 'green';
  ctx.fillRect(player.x, player.y, player.width, player.height);
}

// Clear the canvas
function clear() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// Move the player
function movePlayer() {
  player.x += player.dx;
  player.y += player.dy;

  // Boundaries
  if (player.x < 0) player.x = 0;
  if (player.x + player.width > canvas.width) player.x = canvas.width - player.width;
  if (player.y < 0) player.y = 0;
  if (player.y + player.height > canvas.height) player.y = canvas.height - player.height;
}

// Keyboard event listeners
function keyDown(e) {
  if (e.key === 'ArrowRight' || e.key === 'd') {
    player.dx = player.speed;
  } else if (e.key === 'ArrowLeft' || e.key === 'a') {
    player.dx = -player.speed;
  } else if (e.key === 'ArrowUp' || e.key === 'w') {
    player.dy = -player.speed;
  } else if (e.key === 'ArrowDown' || e.key === 's') {
    player.dy = player.speed;
  }
}

function keyUp(e) {
  if (
    e.key === 'ArrowRight' ||
    e.key === 'ArrowLeft' ||
    e.key === 'ArrowUp' ||
    e.key === 'ArrowDown' ||
    e.key === 'd' ||
    e.key === 'a' ||
    e.key === 'w' ||
    e.key === 's'
  ) {
    player.dx = 0;
    player.dy = 0;
  }
}

// Update the game
function update() {
  clear();
  drawPlayer();
  movePlayer();

  requestAnimationFrame(update);
}

update();

document.addEventListener('keydown', keyDown);
document.addEventListener('keyup', keyUp);
