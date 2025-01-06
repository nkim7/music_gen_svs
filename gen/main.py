

import subprocess
from chord_gen import generate_tempo
from chatbot import chat_with_user
import os


import time

import sys
import math


def run_command(command, cwd=None):
    result = subprocess.run(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        output = result.stdout.decode('utf-8')
    except UnicodeDecodeError:
        output = result.stdout.decode('latin-1', errors='ignore')
    
    if result.returncode != 0:
        print(f"Error running command: {command}\n{result.stderr.decode('utf-8')}")
        return False
    else:
        print(output)
        return True

def calculate_measures(tempo, total_duration_in_seconds):
    
    measure_duration_in_seconds = 4 * (60 / tempo)
    

    num = total_duration_in_seconds / measure_duration_in_seconds
    
    # Round to the nearest multiple of 16
    if num % 16 < 8:
        num_measures = max(math.floor(num / 16) * 16, 16)
    else:
        num_measures = max(math.ceil(num / 16) * 16, 16)
    
    return num_measures

def main(mood, topic):
 
    # Specify mood, topic, and total duration of the music in seconds
    total_duration_in_seconds = 30

    # Generate the tempo based on the mood
    print('generating tempo')
    tempo = generate_tempo(mood, topic)
    print('tempo:   ', tempo)

    # Calculate the number of measures based on the tempo and total duration
    num_measures = calculate_measures(tempo, total_duration_in_seconds)
    print(f"Number of measures needed: {num_measures}")

    # 1. Run the MIDI generation with mood, tempo, and number of measures
    print('generating lyrics')
    lyrics_gen_script = f'python lyrics_gen.py "{topic}" "{mood}" "{tempo}" "{num_measures}"'
    if not run_command(lyrics_gen_script, cwd=r"C:\Users\nagyu\music-gen-app\music\gen"):
        raise Exception("Lyrics generation failed!")

    # 2. Generate the MIDI
    print('generating MIDI')
    midi_gen_script = f'python midi_gen.py "{topic}" "{mood}" "{tempo}" "{num_measures}"'
    if not run_command(midi_gen_script, cwd=r"C:\Users\nagyu\music-gen-app\music\gen"):
        raise Exception("MIDI generation failed!")

    # 3. Generate the UST file
    print('generating ust')
    ust_gen_command = f'python ust_gen.py "{topic}" "{tempo}"'
    if not run_command(ust_gen_command, cwd=r"C:\Users\nagyu\music-gen-app\music\gen"):
        raise Exception("UST generation failed!")

    # 4. Render the MIDI with instruments using FluidSynth
    print('rendering melody')
    fluidsynth_command_melody = (
        r'fluidsynth -ni "C:\Users\nagyu\FluidR3_GM\FluidR3_GM.sf2" '
        r'"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\melody_only.mid" '
        r'-F "C:\Users\nagyu\music-gen-app\music\gen\final_music\melody.wav"'
    )
    if not run_command(fluidsynth_command_melody):
        raise Exception("Melody rendering failed!")

    print('rendering accompaniment')
    fluidsynth_command_accompaniment = (
        r'fluidsynth -ni "C:\Users\nagyu\FluidR3_GM\FluidR3_GM.sf2" '
        r'"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\accompaniment_only.mid" '
        r'-F "C:\Users\nagyu\music-gen-app\music\gen\final_music\instrumental.wav"'
    )
    if not run_command(fluidsynth_command_accompaniment):
        raise Exception("Accompaniment rendering failed!")
        
    print('rendering intro')
    fluidsynth_command_accompaniment = (
        r'fluidsynth -ni "C:\Users\nagyu\FluidR3_GM\FluidR3_GM.sf2" '
        r'"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\intro_melody.mid" '
        r'-F "C:\Users\nagyu\music-gen-app\music\gen\final_music\intro_melody.wav"'
    )
    if not run_command(fluidsynth_command_accompaniment):
        raise Exception("Intro rendering failed!")
        
    print('rendering harmony intro')
    fluidsynth_command_accompaniment = (
        r'fluidsynth -ni "C:\Users\nagyu\FluidR3_GM\FluidR3_GM.sf2" '
        r'"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\intro_harmony.mid" '
        r'-F "C:\Users\nagyu\music-gen-app\music\gen\final_music\intro_harmony.wav"'
    )
    if not run_command(fluidsynth_command_accompaniment):
        raise Exception("Harmony intro rendering failed!")
        
    print('rendering outro')
    fluidsynth_command_accompaniment = (
        r'fluidsynth -ni "C:\Users\nagyu\FluidR3_GM\FluidR3_GM.sf2" '
        r'"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\outro_melody.mid" '
        r'-F "C:\Users\nagyu\music-gen-app\music\gen\final_music\outro_melody.wav"'
    )
    if not run_command(fluidsynth_command_accompaniment):
        raise Exception("Outro rendering failed!")
        
    print('rendering harmony outro')
    fluidsynth_command_accompaniment = (
        r'fluidsynth -ni "C:\Users\nagyu\FluidR3_GM\FluidR3_GM.sf2" '
        r'"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\outro_harmony.mid" '
        r'-F "C:\Users\nagyu\music-gen-app\music\gen\final_music\outro_harmony.wav"'
    )
    if not run_command(fluidsynth_command_accompaniment):
        raise Exception("Harmony outro rendering failed!")

    # 5. Generate vocal output using UTAU
    print('generating utau')
    utau_command = f'python utau.py'
    if not run_command(utau_command, cwd=r"C:\Users\nagyu\music-gen-app\music\gen"):
        raise Exception("UTAU generation failed!")

    # 6. Final merging of the generated audio
    print('final merging')
    merge_command = f'python merge.py "{tempo}" '
    if not run_command(merge_command, cwd=r"C:\Users\nagyu\music-gen-app\music\gen"):
        raise Exception("Final merging failed!")
    
    # previous_song_path = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\final_lyrics_with_syllables.json"

    # # Ensure the file exists
    # if not os.path.exists(previous_song_path):
    #     raise FileNotFoundError(f"The file {previous_song_path} does not exist. Ensure it is created before running the chatbot.")

    # # Start the chatbot
    # print("Starting chatbot interaction...")
    # mood, updated_topic = chat_with_user(topic, previous_song_path)

    # print(f"Chatbot interaction completed with mood: {mood} and topic: {updated_topic}.")
    # print("All steps completed successfully!")

    # start_new_song = input("You: ").strip()
    # if start_new_song == "Yes":
    #     main(mood, updated_topic)
    
    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <mood> <topic>")
        sys.exit(1)
    
    mood = sys.argv[1]
    topic = sys.argv[2]
    
    main(mood, topic)