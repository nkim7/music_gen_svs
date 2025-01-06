# from pydub import AudioSegment
# import os
# import sys

# # Set file paths
# instrumental_path = r"C:\Users\nagyu\music-gen-app\music\gen\final_music\instrumental.wav"
# melody_path = r"C:\Users\nagyu\music-gen-app\music\gen\final_music\melody.wav"
# voice_path = r"C:\Users\nagyu\music-gen-app\music\gen\final_music\music_Track1.wav"
# output_path = r"C:\Users\nagyu\music-gen-app\music\gen\final_music\final_music.wav"
# intro_melody_path = r"C:\Users\nagyu\music-gen-app\music\gen\final_music\intro_melody.wav"
# intro_harmony_path = r"C:\Users\nagyu\music-gen-app\music\gen\final_music\intro_harmony.wav"


# # Function to load audio files
# def load_wav(file_path):
#     try:
#         return AudioSegment.from_wav(file_path)
#     except Exception as e:
#         print(f"Error occurred while loading the file: {e}")
#         return None

# # Function to calculate silence duration based on tempo and number of bars
# def calculate_silence_duration(tempo, num_bars):
#     # 1 beat length in seconds
#     beat_length = 60 / tempo
#     # 1 measure (4 beats) in seconds
#     measure_length = beat_length * 4
#     # Total time for `num_bars` measures
#     total_length = measure_length * num_bars
#     # Convert to milliseconds
#     return int(total_length * 1000)

# # Function to match lengths of audio files
# def match_audio_lengths(audio1, audio2):
#     if len(audio1) > len(audio2):
#         silence_to_add = AudioSegment.silent(duration=(len(audio1) - len(audio2)))
#         audio2 += silence_to_add
#     elif len(audio2) > len(audio1):
#         silence_to_add = AudioSegment.silent(duration=(len(audio2) - len(audio1)))
#         audio1 += silence_to_add
#     return audio1, audio2

# # Function to merge three audio files, with a delay on the third (voice) track based on the intro length
# def merge_three_wav_files(file1, file2, file3, file4, file5, output_file, silence_duration, outro_delay_duration):
#     if file1 and file2 and file3:
#         # Adjust volume of the first and second files
#         harmony = file1 + 8
#         melody = file2 + 4 
#         voice = file3 - 6
#         intro_melody = file4 + 8
#         intro_harmony = file5 + 8

        

#         # Add silence at the beginning of the third file (voice track)
#         silence = AudioSegment.silent(duration=silence_duration)  # Silence duration calculated based on tempo
#         harmony = silence + harmony
#         melody = silence + melody
#         voice = silence + voice  # Append silence at the start of the third audio

#         # Match lengths of the harmony and melody tracks
#         harmony, melody = match_audio_lengths(harmony, melody)
#         harmony, voice = match_audio_lengths(harmony, voice)

#         # Merge the first and second files
#         combined = harmony.overlay(melody)
#         # Merge the combined result with the third file (which now has the calculated delay)
#         combined = combined.overlay(voice)

#         # Prepare outro by adding 18 bars of silence before the outro plays
#         outro_silence = AudioSegment.silent(duration=outro_delay_duration)  # Delay for 18 bars
#         outro_melody = outro_silence + intro_melody
#         outro_harmony = outro_silence + intro_harmony

#         # Match lengths of the outro files
#         outro_melody, outro_harmony = match_audio_lengths(outro_melody, outro_harmony)

#         # Overlay the outro onto the combined track
#         combined = outro_melody.overlay(combined)
#         combined = combined.overlay(outro_harmony)

#         combined = combined.overlay(intro_melody)
#         combined = combined.overlay(intro_harmony)

#         # Ensure the final track is long enough to play the full outro
#         combined = match_audio_lengths(combined, outro_melody)[0]  # Ensure outro plays until the end

#         # Export the result as a new WAV file
#         combined.export(output_file, format="wav")
#         print(f"The merged file has been saved to {output_file}.")
#     else:
#         print("There was an issue loading the files.")

# def main():
#     # Get tempo from the command-line argument
#     tempo = int(sys.argv[1]) 
    
#     # Calculate the silence duration for 4 bars based on the tempo
#     silence_duration = calculate_silence_duration(tempo, num_bars=2)
    
#     # Calculate the delay duration for 18 bars (for the outro)
#     outro_delay_duration = calculate_silence_duration(tempo, num_bars=18)
    
#     # Load instrumental, melody, and voice files
#     instrumental_audio = load_wav(instrumental_path)
#     melody_audio = load_wav(melody_path)
#     voice_audio = load_wav(voice_path)
#     intro_melody_audio = load_wav(intro_melody_path)
#     intro_harmony_audio = load_wav(intro_harmony_path)

#     # Merge the three files and save the result as a new WAV file
#     merge_three_wav_files(instrumental_audio, melody_audio, voice_audio, intro_melody_audio, intro_harmony_audio, output_path, silence_duration, outro_delay_duration)

# if __name__ == "__main__":
#     main()



from pydub import AudioSegment
import os
import sys

# Set file paths
instrumental_path = r"C:\Users\nagyu\music-gen-app\music\gen\final_music\instrumental.wav"
melody_path = r"C:\Users\nagyu\music-gen-app\music\gen\final_music\melody.wav"
voice_path = r"C:\Users\nagyu\music-gen-app\music\gen\final_music\music_Track1.wav"
output_path = r"C:\Users\nagyu\music-gen-app\music\gen\final_music\final_music.wav"
intro_melody_path = r"C:\Users\nagyu\music-gen-app\music\gen\final_music\intro_melody.wav"
intro_harmony_path = r"C:\Users\nagyu\music-gen-app\music\gen\final_music\intro_harmony.wav"
outro_melody_path = r"C:\Users\nagyu\music-gen-app\music\gen\final_music\outro_melody.wav"
outro_harmony_path = r"C:\Users\nagyu\music-gen-app\music\gen\final_music\outro_harmony.wav"

# Function to load audio files
def load_wav(file_path):
    try:
        return AudioSegment.from_wav(file_path)
    except Exception as e:
        print(f"Error occurred while loading the file: {e}")
        return None


def calculate_silence_duration(tempo, num_bars):

    beat_length = 60 / tempo

    measure_length = beat_length * 4
 
    total_length = measure_length * num_bars

    return int(total_length * 1000)



# Function to match lengths of audio files
def match_audio_lengths(audio1, audio2):
    if len(audio1) > len(audio2):
        silence_to_add = AudioSegment.silent(duration=(len(audio1) - len(audio2)))
        audio2 += silence_to_add
    elif len(audio2) > len(audio1):
        silence_to_add = AudioSegment.silent(duration=(len(audio2) - len(audio1)))
        audio1 += silence_to_add
    return audio1, audio2



# Function to merge three audio files, with a delay on the third (voice) track based on the intro length
def merge_three_wav_files(file1, file2, file3, file4, file5, file6, file7,  output_file, silence_duration, outro_delay_duration):
    if file1 and file2 and file3:

        harmony = file1 + 8
        melody = file2 + 4 
        voice = file3 - 6
        intro_melody = file4 + 8
        intro_harmony = file5 + 8
        outro_melody = file6 + 8
        outro_harmony = file7 + 8

        

        # Add silence 
        silence = AudioSegment.silent(duration=silence_duration)  # Silence duration calculated based on tempo
        harmony = silence + harmony
        melody = silence + melody
        voice = silence + voice  # Append silence at the start of the third audio

        # Match lengths of the harmony and melody 
        harmony, melody = match_audio_lengths(harmony, melody)
        harmony, voice = match_audio_lengths(harmony, voice)

    
        combined = harmony.overlay(melody)
       
        combined = combined.overlay(voice)

   
        outro_silence = AudioSegment.silent(duration=outro_delay_duration)  # Delay for 18 bars
        outro_melody = outro_silence + outro_melody
        outro_harmony = outro_silence + outro_harmony

   
        outro_melody, outro_harmony = match_audio_lengths(outro_melody, outro_harmony)

        # Overlay the outro onto the combined track
        combined = outro_melody.overlay(combined)
        combined = combined.overlay(outro_harmony)

        combined = combined.overlay(intro_melody)
        combined = combined.overlay(intro_harmony)

        combined = match_audio_lengths(combined, outro_melody)[0]  

        combined.export(output_file, format="wav")
        print(f"The merged file has been saved to {output_file}.")
    else:
        print("There was an issue loading the files.")

def main():
 
    tempo = int(sys.argv[1]) 
    

    silence_duration = calculate_silence_duration(tempo, num_bars=2)
    

    outro_delay_duration = calculate_silence_duration(tempo, num_bars=18)

    instrumental_audio = load_wav(instrumental_path)
    melody_audio = load_wav(melody_path)
    voice_audio = load_wav(voice_path)
    intro_melody_audio = load_wav(intro_melody_path)
    intro_harmony_audio = load_wav(intro_harmony_path)
    outro_melody_audio = load_wav(outro_melody_path)
    outro_harmony_audio = load_wav(outro_harmony_path)


    merge_three_wav_files(instrumental_audio, melody_audio, voice_audio, intro_melody_audio, intro_harmony_audio, outro_melody_audio, outro_harmony_audio, output_path, silence_duration, outro_delay_duration)

if __name__ == "__main__":
    main()
