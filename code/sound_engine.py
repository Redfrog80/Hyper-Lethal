import sys
import pygame
from pygame.locals import *
 
 #IMPORTANT! Apparently PyGame can't handle .aif files so I'm replacing everything with .wav.
 
def update(dt):
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
def draw(screen):
  screen.fill((0, 0, 0))
  pygame.display.flip()
def runPyGame():
  pygame.init()
  fps = 60.0
  fpsClock = pygame.time.Clock()
  width, height = 640, 480
  screen = pygame.display.set_mode((width, height))
  
  ######################################################################################
  
  # MUSIC STUFF
  
  pygame.mixer.init()
  
  # Loads sounds and sets volume
  laser_sounds = pygame.mixer.Sound("sounds/LaserShot1.wav") or pygame.mixer.Sound("sounds/LaserShot3.wav")
  laser_sounds.set_volume(1)
  
  glitch_sound = pygame.mixer.Sound("sounds/Glitch_downshifter.wav")
  glitch_sound.set_volume(1)
  
  death_sound = pygame.mixer.Sound("sounds/Death1.wav") or pygame.mixer.Sound("sounds/Death2.wav")
  death_sound.set_volume(1)
  
  alert_sound = pygame.mixer.Sound("sounds/SynthAlert.wav")
  alert_sound.set_volume(1)
  
  UI_sound = pygame.mixer.Sound("sounds/UIClick.wav")
  UI_sound.set_volume(1)
  
  #Loads and plays the loading screen music
  def Loading_Music():
    pygame.mixer.music.load("sounds/loading_screen.wav")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1)
  
  #Stops existing music and plays battle music
  def Battle_Music():
    pygame.mixer.music.stop
    pygame.mixer.music.load("sounds/battle_music.wav") # Don't worry this is just a placeholder lol
    pygame.mixer.music.play(-1)
  
  # Use these to pause and unpause the music
  def pauseMusic():
    ############
    pygame.mixer.music.pause()
  def unpauseMusic():
    global pause
    pygame.mixer.music.unpause()
    pause = False
  
  #These are commands we can use when we need to call sounds
  
  #Loading_Music()
  #Battle_Music()
  #pygame.mixer.Sound.play(laser_sounds) # to play the sound, automatically creates a new channel so sounds don't overlap
  #pygame.mixer.Sound.play(UI_sound)
  #pygame.mixer.Sound.play(alert_sound)
  #pygame.mixer.Sound.play(glitch_sound)
  #pygame.mixer.Sound.play(death_sound)

################################################################################
  x = 0
  # Main game loop.
  dt = 1/fps # dt is the time since last frame.
  while True:
    update(dt)
    x += 1/60
    print(f"seconds passed: {x}")
    draw(screen)
    dt = fpsClock.tick(fps)
runPyGame()