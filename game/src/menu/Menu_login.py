import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 500
BG_COLOR = (240, 240, 245)
PRIMARY_COLOR = (70, 130, 180)
SECONDARY_COLOR = (100, 149, 237)
TEXT_COLOR = (50, 50, 50)
INPUT_BG = (255, 255, 255)
BORDER_COLOR = (200, 200, 200)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Login Screen")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.Font(None, 48)
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)

# Input boxes
username_box = pygame.Rect(150, 180, 300, 40)
password_box = pygame.Rect(150, 250, 300, 40)
login_button = pygame.Rect(200, 320, 200, 45)
signup_text_rect = pygame.Rect(200, 390, 200, 30)

# State
username = ""
password = ""
active_box = None
current_screen = "login"  # "login" or "signup"

# User database (in-memory for demo)
users = {}

def draw_text(text, font, color, x, y, center=False):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)

def draw_input_box(box, text, active, is_password=False):
    color = PRIMARY_COLOR if active else BORDER_COLOR
    pygame.draw.rect(screen, INPUT_BG, box)
    pygame.draw.rect(screen, color, box, 2)
    
    display_text = text
    if is_password and text:
        display_text = "*" * len(text)
    
    text_surf = font.render(display_text, True, TEXT_COLOR)
    screen.blit(text_surf, (box.x + 10, box.y + 8))

def draw_button(rect, text, hover=False):
    color = SECONDARY_COLOR if hover else PRIMARY_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=5)
    draw_text(text, font, (255, 255, 255), rect.centerx, rect.centery, center=True)

def draw_login_screen(mouse_pos):
    screen.fill(BG_COLOR)
    
    draw_text("Welcome Back", title_font, PRIMARY_COLOR, WIDTH // 2, 80, center=True)
    
    draw_text("Username:", small_font, TEXT_COLOR, 150, 160)
    draw_input_box(username_box, username, active_box == "username")
    
    draw_text("Password:", small_font, TEXT_COLOR, 150, 230)
    draw_input_box(password_box, password, active_box == "password", is_password=True)
    
    hover_login = login_button.collidepoint(mouse_pos)
    draw_button(login_button, "Login", hover_login)
    
    draw_text("Don't have an account?", small_font, TEXT_COLOR, WIDTH // 2, 390, center=True)
    hover_signup = signup_text_rect.collidepoint(mouse_pos)
    signup_color = SECONDARY_COLOR if hover_signup else PRIMARY_COLOR
    draw_text("Sign Up", small_font, signup_color, WIDTH // 2, 420, center=True)

def draw_signup_screen(mouse_pos):
    screen.fill(BG_COLOR)
    
    draw_text("Create Account", title_font, PRIMARY_COLOR, WIDTH // 2, 80, center=True)
    
    draw_text("Username:", small_font, TEXT_COLOR, 150, 160)
    draw_input_box(username_box, username, active_box == "username")
    
    draw_text("Password:", small_font, TEXT_COLOR, 150, 230)
    draw_input_box(password_box, password, active_box == "password", is_password=True)
    
    hover_signup = login_button.collidepoint(mouse_pos)
    draw_button(login_button, "Sign Up", hover_signup)
    
    draw_text("Already have an account?", small_font, TEXT_COLOR, WIDTH // 2, 390, center=True)
    hover_login = signup_text_rect.collidepoint(mouse_pos)
    login_color = SECONDARY_COLOR if hover_login else PRIMARY_COLOR
    draw_text("Login", small_font, login_color, WIDTH // 2, 420, center=True)

def handle_login():
    if username in users and users[username] == password:
        print(f"Login successful! Welcome {username}")
        # Add your game start logic here
    else:
        print("Invalid username or password")

def handle_signup():
    if username and password:
        if username in users:
            print("Username already exists")
        else:
            users[username] = password
            print(f"Account created for {username}")
    else:
        print("Please enter both username and password")

# Main loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if username_box.collidepoint(event.pos):
                active_box = "username"
            elif password_box.collidepoint(event.pos):
                active_box = "password"
            elif login_button.collidepoint(event.pos):
                if current_screen == "login":
                    handle_login()
                else:
                    handle_signup()
            elif signup_text_rect.collidepoint(event.pos):
                current_screen = "signup" if current_screen == "login" else "login"
                username = ""
                password = ""
                active_box = None
            else:
                active_box = None
        
        if event.type == pygame.KEYDOWN and active_box:
            if event.key == pygame.K_BACKSPACE:
                if active_box == "username":
                    username = username[:-1]
                else:
                    password = password[:-1]
            elif event.key == pygame.K_TAB:
                active_box = "password" if active_box == "username" else "username"
            elif event.key == pygame.K_RETURN:
                if current_screen == "login":
                    handle_login()
                else:
                    handle_signup()
            else:
                if active_box == "username":
                    username += event.unicode
                else:
                    password += event.unicode
    
    if current_screen == "login":
        draw_login_screen(mouse_pos)
    else:
        draw_signup_screen(mouse_pos)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()