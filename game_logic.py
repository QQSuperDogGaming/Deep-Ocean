from js import document, window, localStorage
from math import sqrt
from random import randint

# Set up the game canvas
canvas = document.getElementById("gameCanvas")
context = canvas.getContext("2d")

# Audio setup (use Audio() directly without 'new')
background_music = window.Audio('assets/background-music.wav')
shoot_sound = window.Audio('assets/shoot-sound.wav')
explosion_sound = window.Audio('assets/explosion-sound.wav')

# Load background image
background_img = window.Image()
background_img.src = 'assets/background.png'

# Background scrolling speed and position
background_y1 = 0
background_y2 = -canvas.height
background_speed = 2

# Player setup
player_img = window.Image()
player_img.src = 'assets/player.png'
player_x = 370
player_y = 500
player_width = 64
player_height = 64
player_speed = 5
player_health = 100
bullet_width = 5
bullet_height = 20

# Enemy setup
enemy_img = window.Image()
enemy_img.src = 'assets/enemy.png'
enemy_width = 64
enemy_height = 64
num_of_enemies = 6
enemies = [{"x": randint(0, 800 - enemy_width), "y": randint(50, 150)} for _ in range(num_of_enemies)]
enemy_speed = 2

# Bullet setup
bullets = []
bullet_speed = 10

# Score and leaderboard
score = 0
leaderboard = []

# Track key states
keys = {"ArrowLeft": False, "ArrowRight": False, "Space": False}

# Health Bar Drawing
def draw_health_bar():
    context.fillStyle = "red"
    context.fillRect(10, 40, player_health * 2, 20)
    context.strokeStyle = "white"
    context.strokeRect(10, 40, 200, 20)

def draw_player():
    context.drawImage(player_img, player_x, player_y, player_width, player_height)

def draw_enemy(x, y):
    context.drawImage(enemy_img, x, y, enemy_width, enemy_height)

def draw_bullet(bullet):
    context.fillStyle = "yellow"
    context.fillRect(bullet["x"], bullet["y"], bullet_width, bullet_height)

def move_bullet():
    global bullets
    for bullet in bullets:
        bullet["y"] -= bullet_speed
    bullets = [bullet for bullet in bullets if bullet["y"] > 0]

def is_collision(enemy, bullet):
    distance = sqrt((enemy["x"] - bullet["x"]) ** 2 + (enemy["y"] - bullet["y"]) ** 2)
    return distance < 40

def handle_collision():
    global enemies, bullets, score
    for enemy in enemies:
        for bullet in bullets:
            if is_collision(enemy, bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                enemies.append({"x": randint(0, 800 - enemy_width), "y": randint(50, 150)})
                explosion_sound.play()
                score += 1
                break

def game_over():
    global player_health
    return player_health <= 0

def scroll_background():
    global background_y1, background_y2
    background_y1 += background_speed
    background_y2 += background_speed

    if background_y1 >= canvas.height:
        background_y1 = -canvas.height
    if background_y2 >= canvas.height:
        background_y2 = -canvas.height

    # Draw two instances of the background image to create a scrolling effect
    context.drawImage(background_img, 0, background_y1, canvas.width, canvas.height)
    context.drawImage(background_img, 0, background_y2, canvas.width, canvas.height)

def game_loop(*args):
    global player_x, player_health

    if game_over():
        save_score(score)
        end_game()
        return

    context.clearRect(0, 0, canvas.width, canvas.height)

    # Scroll and draw background
    scroll_background()

    # Move player
    if keys["ArrowLeft"]:
        player_x = max(0, player_x - player_speed)
    if keys["ArrowRight"]:
        player_x = min(canvas.width - player_width, player_x + player_speed)

    # Draw player and health bar
    draw_player()
    draw_health_bar()

    # Move and draw bullets
    move_bullet()
    for bullet in bullets:
        draw_bullet(bullet)

    # Move and draw enemies
    for enemy in enemies:
        enemy["x"] += enemy_speed if enemy["x"] < canvas.width - enemy_width else -enemy_speed
        if enemy["y"] >= player_y:  # Enemy reaches the player
            player_health -= 1
        draw_enemy(enemy["x"], enemy["y"])

    # Handle bullet-enemy collisions
    handle_collision()

    # Display score
    context.fillStyle = "white"
    context.font = "20px Arial"
    context.fillText(f"Score: {score}", 10, 20)

# Key press and release events
def on_key_down(event):
    keys[event.key] = True
    if event.key == " ":
        fire_bullet()

def on_key_up(event):
    keys[event.key] = False

# Bullet firing function
def fire_bullet(*args):
    global bullets
    bullets.append({"x": player_x + player_width // 2 - bullet_width // 2, "y": player_y})
    shoot_sound.play()

# Attach event listeners for key presses
window.addEventListener("keydown", on_key_down)
window.addEventListener("keyup", on_key_up)

# Save the score to localStorage
def save_score(score):
    leaderboard.append(score)
    leaderboard.sort(reverse=True)
    leaderboard = leaderboard[:5]  # Top 5 scores
    localStorage.setItem("leaderboard", str(leaderboard))

# Show leaderboard
def show_leaderboard():
    canvas.style.display = "none"
    document.getElementById("leaderboard").style.display = "block"
    document.getElementById("leaderboardList").innerHTML = "".join(
        [f"<li>{score}</li>" for score in leaderboard]
    )

# Game Over - show score and options to restart or go to main menu
def end_game():
    canvas.style.display = "none"
    document.getElementById("gameOverScreen").style.display = "block"
    document.getElementById("finalScore").innerText = str(score)

# Event listeners for menu buttons
def start_game():
    document.getElementById("mainMenu").style.display = "none"
    document.getElementById("gameOverScreen").style.display = "none"
    canvas.style.display = "block"
    background_music.play()
    window.setInterval(game_loop, 16)

def restart_game():
    global player_health, score, bullets, enemies
    player_health = 100
    score = 0
    bullets = []
    enemies = [{"x": randint(0, 800 - enemy_width), "y": randint(50, 150)} for _ in range(num_of_enemies)]
    start_game()

def go_to_menu():
    document.getElementById("gameOverScreen").style.display = "none"
    document.getElementById("mainMenu").style.display = "block"

def show_leaderboard_menu():
    document.getElementById("mainMenu").style.display = "none"
    show_leaderboard()

def back_to_menu():
    document.getElementById("leaderboard").style.display = "none"
    document.getElementById("mainMenu").style.display = "block"

# Load leaderboard from localStorage
leaderboard = eval(localStorage.getItem("leaderboard") or "[]")

# Main menu button event listeners
document.getElementById("startGame").addEventListener("click", start_game)
document.getElementById("viewLeaderboard").addEventListener("click", show_leaderboard_menu)
document.getElementById("restartGame").addEventListener("click", restart_game)
document.getElementById("goToMenu").addEventListener("click", go_to_menu)
document.getElementById("backToMenu").addEventListener("click", back_to_menu)
