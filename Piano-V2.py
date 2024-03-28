#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pygame
from pygame_screen_record import ScreenRecorder
import time
import numpy as np


# Initialize Pygame
pygame.init()
# Initialize Pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=1)
# Screen setup
screen_width, screen_height = 600*2, 400*2
screen = pygame.display.set_mode((screen_width, screen_height))


pygame.display.set_caption('Piano.')


num_keys = 88
num_white_keys = 7*num_keys//12+1
num_black_keys = num_keys-num_white_keys


# White key dimentions
piano_width = screen_width*5/6
key_width = piano_width/num_white_keys
key_height=key_width*5
# Black key dimentions
key_width_b = key_width*2/3
key_height_b = key_width_b*5


#Active keys
active_keys = []
color = None


white = (255,255,255)
black = (0,0,0)
green = (0,255,0)


letters = ['A', 'B','C','D','E','F','G']
piano_notes = []

indexes = [0,2,3,5,6]   #Indexes that have a black key
for i in range(num_white_keys):
    # ADD TO PIANO_NOTES LIST
    note = letters[i%len(letters)]
    octave = (i+5)//7                       #Complete the lower octave and get the octave
    piano_notes.append(f"{note}{octave}")
    if (i!= num_white_keys-1) and (i%7 in indexes):
        piano_notes.append(f"{note}{octave}#")
        
        
        
piano_freqs = {}
def frequency_of_key(key_number):
    # A4 is key 49, and its frequency is 440Hz
    a4_key_number = 49
    a4_frequency = 440.0
    # Calculate the number of half steps away from A4
    n = key_number - a4_key_number
    # Calculate the frequency
    frequency = a4_frequency * (2 ** (1/12)) ** n
    return frequency

# Example usage: Print the frequencies for all 88 keys
for key_number in range(num_keys):
    #print(f"Key {key_number}: {frequency_of_key(key_number)} Hz")
    piano_freqs[piano_notes[key_number]]=frequency_of_key(key_number)
    
active_key = None

def draw_piano(active_key, color):
    rects = []
    
    for i in range(num_white_keys):
        #Draw white keys
        key_left = (0.5*(screen_width-piano_width))+(i*key_width)
        rect = pygame.Rect(key_left,0,key_width,key_height)
        rect.center = (key_left+key_width/2,screen_height/2)
        pygame.draw.rect(screen, white, rect)
        if active_key==rect:
            pygame.draw.rect(screen, green, active_key)
        pygame.draw.rect(screen, black, rect, 2)
        rects.append(rect)
        


        #Draw black keys
        if (i!= num_white_keys-1) and (i%7 in indexes):
            key_left_b = key_left + key_width - key_width_b/2
            rect_b = pygame.Rect(key_left_b+1, 0, key_width_b, key_height_b)
            # Adjust the y position as needed, for example:
            rect_b.y = (screen_height - key_height) / 2
            pygame.draw.rect(screen, black, rect_b)
            if active_key==rect_b:
                pygame.draw.rect(screen, green, active_key)
                pygame.draw.rect(screen, black, active_key, 2)
            rects.append(rect_b)

            
        

    return rects


## NEW GENERATE_TONE FUNCTION TO MAKE TONES SOUND MORE LIKE A REAL PIANO
def generate_tone(frequency, duration, volume=0.5, sample_rate=44100):
    # Generate the time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate a more complex tone by adding harmonics
    # Fundamental frequency
    tone = np.sin(frequency * t * 2 * np.pi)
    # Add harmonics with decreasing amplitude
    harmonics_frequencies = [2, 3, 4, 5, 6]  # Harmonics
    harmonics_amplitudes = [0.5, 0.25, 0.125, 0.0625, 0.03125]  # Relative amplitudes
    
    for i, amp in zip(harmonics_frequencies, harmonics_amplitudes):
        tone += amp * np.sin(i * frequency * t * 2 * np.pi)
    
    # Apply volume
    tone *= volume * 32767 / np.max(np.abs(tone))
    
    # More sophisticated envelope: ADSR (Attack, Decay, Sustain, Release)
    attack_duration = int(sample_rate * 0.02)  # Attack
    decay_duration = int(sample_rate * 0.05)  # Decay
    sustain_level = 0.7  # Sustain level
    release_duration = int(sample_rate * 0.2)  # Release
    
    # Apply ADSR envelope
    env = np.ones_like(t)
    if attack_duration > 0:
        env[:attack_duration] = np.linspace(0, 1, attack_duration)
    if decay_duration > 0:
        env[attack_duration:attack_duration+decay_duration] = np.linspace(1, sustain_level, decay_duration)
    if release_duration > 0:
        env[-release_duration:] = np.linspace(sustain_level, 0, release_duration)
    
    tone *= env
    
    # Convert to bytes
    tone = tone.astype(np.int16).tobytes()
    
    # Create and return the Pygame sound object
    return pygame.mixer.Sound(buffer=tone)
            




# In[18]:


# MAIN GAME LOOP
run = True
while run:
    screen.fill('gray')
    keys = draw_piano(active_key, color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            color = screen.get_at((event.pos))
            for i in range(len(keys)):
                if keys[i].collidepoint(event.pos) :
                    note = piano_notes[i%len(piano_notes)]
                    if ("#" in note and color==black) or ("#" not in note and color==white):
                        active_key=keys[i]
                        # Change the color of the key
                        
                        # Generate
                        tone = generate_tone(piano_freqs[note], duration=0.5, volume=0.5, sample_rate=44100)
                        tone.play()
                        pygame.time.wait(int(0.25 * 30))
                        
                        # Print clicked key.
                        print(f"Clicked piano key: {note}")

    pygame.display.flip()
pygame.quit()


# In[90]:





# In[74]:





# In[75]:


piano_freqs


# In[ ]:




