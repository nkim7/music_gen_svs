import json
import mido
from mido import Message, MidiFile, MidiTrack
import os
import random
import sys

# Load data from the JSON file
def load_data_from_json(json_file_path):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    return data['lyrics_with_plus'], data['chord_progression'], data['updated_syllable_distribution']


def update_selected_syllable_distribution(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    updated_syllable_distribution = []

    for measure in data['selected_syllable_distribution']:
        for submeasure in measure:
            total_beats = sum(submeasure)
            if total_beats < 4:
                submeasure.extend([0] * (4 - total_beats))
            updated_syllable_distribution.append(submeasure)

    data['updated_syllable_distribution'] = updated_syllable_distribution

    updated_json_path = r"C:\Users\nagyu\music_genfinal\demo_outputs\final_lyrics_with_syllables.json"
    with open(updated_json_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Updated JSON saved to {updated_json_path}")
    return updated_json_path

# Flatten the updated_syllable_distribution
def flatten_syllable_distribution(syllable_distribution):
    return [item for sublist in syllable_distribution for item in sublist]

# Repeat the flattened distribution based on repeat_times and save it back to the JSON file
def save_flattened_distribution(json_file_path, flattened_distribution, num_measures):
    repeat_times = num_measures // 16 
    repeated_distribution = flattened_distribution * repeat_times  
    
    with open(json_file_path, 'r+') as f:
        data = json.load(f)
        data['rhythm_sequence'] = repeated_distribution  
        f.seek(0)  # Move the file pointer to the beginning of the file
        json.dump(data, f, indent=4)  
        f.truncate()  # Truncate the file to remove any leftover content


def transform_rhythm_sequence(syllable_distribution, tempo):
    transformed_distribution = []

    for submeasure in syllable_distribution:
        # Rule 1: Change [1, 1, 0, 0] based on tempo conditions
        if submeasure == [1, 1, 0, 0]:
            if tempo > 100:

                if random.random() < 0.7:
                    transformed_distribution.append([1, 0, 1, 0])
                else:
                    transformed_distribution.append([2, 2])
            else:
                
                if random.random() < 0.3:
                    transformed_distribution.append([1, 0, 1, 0])
                else:
                    transformed_distribution.append([2, 2])
        # Rule 2: Change [1, 0, 0, 0] to [2, 0, 0]
        elif submeasure == [1, 0, 0, 0]:
            transformed_distribution.append([2, 0, 0])
        else:
            transformed_distribution.append(submeasure)

    return transformed_distribution


def load_chord_progression_from_json(json_file_path, limit=16):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    chord_progression_str = data.get('chord_progression', '')


    chord_progression = [chord for chord in chord_progression_str.split() if chord not in ['|', '']]


    return chord_progression[:limit]

def choose_restricted_note(previous_note, second_previous_note, available_notes):
    if previous_note is None:
        return random.choice(available_notes)
    
    possible_notes = [note for note in available_notes if abs(note - previous_note) <= 6]
    
    if not possible_notes:
        closest_note = min(available_notes, key=lambda note: abs(note - previous_note))
        return closest_note
    
    while True:
        note = random.choice(possible_notes)
        if note != previous_note or note != second_previous_note:
            return note

def generate_melody(chord_progression, syllable_distribution, num_measures):
    chords_mapping = {
        'C': [60, 64, 67],
        'G': [67, 59, 62],
        'Am': [69, 60, 64],
        'F': [65, 69, 60],
        'Dm': [62, 65, 69],
        'Em': [64, 67, 59],
        'D': [62, 66, 69],
        'A': [57, 61, 64],
        'Bdim': [59, 62, 65],
        'E': [64, 68, 59],
        'E7': [64, 68, 59, 62],
        'Fm': [65, 68, 61],
        'Bb': [58, 61, 66],
        'Eb': [63, 67, 70],
        'Ab': [68, 60, 63],
    }

    melody_notes = []
    note_sequence = []
    base_measures = 16
    chord_progression = load_chord_progression_from_json(r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\final_lyrics_with_syllables.json")


    if len(chord_progression) != len(syllable_distribution):
        print(f"Warning: Chord progression and syllable distribution lengths do not match. Chords: {len(chord_progression)}, Syllables: {len(syllable_distribution)}")
    
    previous_note = None
    second_previous_note = None

    for measure_idx, chord in enumerate(chord_progression):
        if measure_idx >= len(syllable_distribution):
            print(f"Warning: Measure index {measure_idx} exceeds the length of syllable_distribution.")
            break

        submeasure = syllable_distribution[measure_idx]
        print(f"Processing chord: {chord}, submeasure: {submeasure}")

        for note_type in submeasure:
            try:
                if note_type == 1:
                    note_duration = 480
                    note = choose_restricted_note(previous_note, second_previous_note, chords_mapping[chord])
                elif note_type == 2:
                    note_duration = 960
                    note = choose_restricted_note(previous_note, second_previous_note, chords_mapping[chord])
                elif note_type == 3:
                    note_duration = 1440
                    note = choose_restricted_note(previous_note, second_previous_note, chords_mapping[chord])
                elif note_type == 4:
                    note_duration = 1920
                    note = choose_restricted_note(previous_note, second_previous_note, chords_mapping[chord])
                elif note_type == 0:
                    note_duration = 480
                    note = 0
                else:
                    raise ValueError(f"Unexpected note_type value: {note_type}")

                if note > 0:
                    second_previous_note = previous_note
                    previous_note = note

                melody_notes.append((note, note_duration))
                note_sequence.append(note if note > 0 else '-')
            except KeyError as e:
                print(f"Error: Chord '{chord}' not found in chords_mapping.")
                raise e
            except Exception as e:
                print(f"Error processing submeasure {submeasure} at measure index {measure_idx}: {str(e)}")
                raise e

    full_melody = []
    full_note_sequence = []
    repeat_times = num_measures // base_measures

    print("repeat times:", repeat_times)

    for _ in range(repeat_times):
        full_melody.extend(melody_notes)
        full_note_sequence.extend(note_sequence)

    # intro_melody = melody_notes[:8] + melody_notes[-8:]
    # create_melody_midi_file(intro_melody, r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\intro_melody.mid", 100)

    return full_melody, full_note_sequence




def generate_lefthand(chord_progression, syllable_distribution, num_measures, tempo):
    chords_mapping = {
        'C': [60, 64, 67],   
        'G': [67, 71, 74],  
        'Am': [69, 72, 76], 
        'F': [65, 69, 72],  
        'Dm': [62, 65, 69], 
        'Em': [64, 67, 71], 
        'D': [62, 66, 69],  
        'A': [69, 73, 76],   
        'Bdim': [71, 74, 77],
        'E': [64, 68, 71],   
        'E7': [64, 68, 71, 74], 
        'Fm': [65, 68, 72],  
        'Bb': [70, 74, 77], 
        'Eb': [63, 67, 70], 
        'Ab': [68, 72, 75],  
    }

    left_hand_notes = []
    base_measures = 16
    chord_progression = load_chord_progression_from_json(r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\final_lyrics_with_syllables.json")

    pattern_groups = {
        1: 'harmony', 5: 'harmony',
        2: 'simple', 4: 'simple',
        3: 'arpeggio', 6: 'arpeggio', 7: 'arpeggio', 8: 'arpeggio'
    }


    previous_pattern_group = None


    if tempo <= 80:
        weights = [3, 7, 3, 7, 3, 0, 0, 0]  
    elif 80 < tempo <= 100:
        weights = [3, 1, 3, 1, 2, 3, 3, 3]  
    else:
        weights = [1, 1, 1, 1, 1, 1, 1, 1]  
    
    # extended_chord_progression = chord_progression[:4]
    # final_chord_progression = extended_chord_progression + chord_progression

    final_chord_progression = chord_progression

    print("final:", final_chord_progression)

    current_pattern = 1  # Initialize the pattern

    for measure_idx, chord in enumerate(final_chord_progression):
        
        # Change the accompaniment pattern every 8 measures, starting at 12, 20, 28, 36...
        # if (measure_idx >= 12) and ((measure_idx - 12) % 8 == 0):
        if measure_idx  % 8 == 0:
            available_patterns = [1, 2, 3, 4, 5, 6, 7, 8]  # Possible patterns
          
            if previous_pattern_group is not None:
                available_patterns = [p for p in available_patterns if pattern_groups[p] != previous_pattern_group]

       
            if len(available_patterns) < len(weights):
                current_weights = weights[:len(available_patterns)]
            else:
                current_weights = weights

            current_pattern = random.choices(available_patterns, weights=current_weights, k=1)[0]
            previous_pattern_group = pattern_groups[current_pattern]
            print(f"Switching to new pattern: {current_pattern} at measure {measure_idx}")


        if current_pattern == 1:
           
            root_note = chords_mapping[chord][0] - 12 
            fifth_note = root_note + 7  
            octave_note = root_note + 12 
            left_hand_notes.extend([
                (root_note, 240),   
                (fifth_note, 240),
                (octave_note, 480),  
                (octave_note, 960)   
            ])
        elif current_pattern == 2:
    
            root_note = chords_mapping[chord][0] - 12 
            fifth_note = chords_mapping[chord][2] - 12  
            for _ in range(2):  
                left_hand_notes.extend([
                    (root_note, 480),  
                    (fifth_note, 480)  
                ])
        elif current_pattern == 3:
         
            root_note = chords_mapping[chord][0] - 12  
            third_note = chords_mapping[chord][1] - 12  
            fifth_note = chords_mapping[chord][2] - 12  
            octave_note = chords_mapping[chord][0]  
            for _ in range(4): 
                left_hand_notes.extend([
                    (root_note, 240), 
                    (fifth_note, 240)  
                ])
        elif current_pattern == 4:
           
            root_note = chords_mapping[chord][0] - 12  
            for _ in range(4):  
                left_hand_notes.extend([
                    (root_note, 480), 
                ])
        elif current_pattern == 5:
     
            root_note = chords_mapping[chord][0] - 12  
            fifth_note = root_note + 7 
            octave_note = root_note + 12  
            left_hand_notes.extend([
                (root_note, 240), 
                (fifth_note, 120),  
                (octave_note, 120),
                (octave_note, 480),  
                (octave_note, 960)
            ])
        elif current_pattern == 6:
      
            root_note = chords_mapping[chord][0] - 12 
            fifth_note = root_note + 7 
            octave_note = root_note + 12  
            left_hand_notes.extend([
                (root_note, 240),    
                (fifth_note, 240),   
                (octave_note, 480),  
                (octave_note, 360),  
                (octave_note, 120),
                (octave_note, 480)
            ])
        elif current_pattern == 7:  
            root_note = chords_mapping[chord][0] - 12  
            fifth_note = root_note + 7  
            octave_note = root_note + 12  
            left_hand_notes.extend([
                (root_note, 240),    
                (fifth_note, 120),   
                (octave_note, 120),
                (octave_note, 360),  
                (octave_note, 120),
                (octave_note, 360),  
                (octave_note, 120),
                (octave_note, 480)
            ])
        elif current_pattern == 8:
  
            root_note = chords_mapping[chord][0] - 12  # Root note (1)
            fifth_note = root_note + 7  # Fifth note (5)
            octave_note = root_note + 12  # Octave note (8)
            left_hand_notes.extend([
                (root_note, 240),   
                (fifth_note, 240),  
                (octave_note, 480),  
                (octave_note, 240),  
                (octave_note, 120),
                (octave_note, 120),  
                (root_note, 480)
            ])

    full_left_hand = []
    repeat_times = num_measures // base_measures

    print("repeat times:", repeat_times)

    # intro_harmony = left_hand_notes[:8] + left_hand_notes[-8:]
    # create_accompaniment_midi_file(intro_harmony, r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\intro_harmony.mid", 100)


    for _ in range(repeat_times):
        full_left_hand.extend(left_hand_notes)

    return full_left_hand




def create_melody_midi_file(melody_notes, output_path, bpm):
    initial_midi = MidiFile()
    melody_track = MidiTrack()
    
    initial_midi.tracks.append(melody_track)

    tempo = mido.bpm2tempo(bpm)
    melody_track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    for note, duration in melody_notes:
        if note > 0:
            melody_track.append(Message('note_on', note=note, velocity=64, time=0))
            melody_track.append(Message('note_off', note=note, velocity=64, time=duration))
        else:
            melody_track.append(Message('note_off', note=0, velocity=0, time=duration))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    initial_midi.save(output_path)
    print(f'Melody MIDI file saved to {output_path}')


def create_accompaniment_midi_file(left_hand_notes, output_path, bpm):
    initial_midi = MidiFile()
    left_hand_track = MidiTrack()
    
    initial_midi.tracks.append(left_hand_track)

    tempo = mido.bpm2tempo(bpm)
    left_hand_track.append(mido.MetaMessage('set_tempo', tempo=tempo))

    for note, duration in left_hand_notes:
        if note > 0:
            left_hand_track.append(Message('note_on', note=note, velocity=64, time=0))
            left_hand_track.append(Message('note_off', note=note, velocity=64, time=duration))
        else:
            left_hand_track.append(Message('note_off', note=0, velocity=0, time=duration))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    initial_midi.save(output_path)
    print(f'Accompaniment MIDI file saved to {output_path}')


def save_note_sequence_to_json(json_file_path, note_sequence, num_measures):
    repeat_times = num_measures // 16  
    repeated_note_sequence = note_sequence * repeat_times

    with open(json_file_path, 'r+') as f:
        data = json.load(f)
        data['note_sequence'] = repeated_note_sequence  
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()




# Main Function 
def main():

    topic = sys.argv[1] if len(sys.argv) > 1 else "bears"
    mood = sys.argv[2] if len(sys.argv) > 2 else "happy and uplift"
    tempo = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    num_measures = int(sys.argv[4]) if len(sys.argv) > 4 else 16

 
    json_path = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\final_lyrics_with_syllables.json"

   
    lyrics_with_plus, chord_progression, updated_syllable_distribution = load_data_from_json(json_path)

   
    transformed_syllable_distribution = transform_rhythm_sequence(updated_syllable_distribution, tempo)

    flattened_distribution = flatten_syllable_distribution(transformed_syllable_distribution)
    save_flattened_distribution(json_path, flattened_distribution, num_measures)

    print("Final Chord Progression:")
    print(chord_progression)


    melody_notes, note_sequence = generate_melody(chord_progression, transformed_syllable_distribution, num_measures)


    melody_output_path = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\melody_only.mid"
    create_melody_midi_file(melody_notes, melody_output_path, tempo)


    def select_intro_melody(notes, direction="forward"):
        selected_notes = []
        total_duration = 0
        if direction == "forward":
            for note, duration in notes:
                selected_notes.append((note, duration))
                total_duration += duration
                if total_duration >= 3840:
                    break
        else:
            for note, duration in reversed(notes):
                selected_notes.insert(0, (note, duration))
                total_duration += duration
                if total_duration >= 3840:
                    break
        return selected_notes


    intro_melody = select_intro_melody(melody_notes, direction="forward")
    outro_melody = select_intro_melody(melody_notes, direction="backward")
    # intro_melody_back = select_intro_melody(melody_notes, direction="backward")
    # intro_melody = intro_melody_front + intro_melody_back
    # intro_melody = intro_melody_front
    intro_melody_output_path = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\intro_melody.mid"
    print("melody notes:", melody_notes)
    print("intro melody", intro_melody)
    create_melody_midi_file(intro_melody, intro_melody_output_path, tempo)
    outro_melody_output_path = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\outro_melody.mid"
    create_melody_midi_file(outro_melody, outro_melody_output_path, tempo)


    left_hand_notes = generate_lefthand(chord_progression, transformed_syllable_distribution, num_measures, tempo)

   
    accompaniment_output_path = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\accompaniment_only.mid"
    create_accompaniment_midi_file(left_hand_notes, accompaniment_output_path, tempo)


    intro_harmony = select_intro_melody(left_hand_notes, direction="forward")
    # intro_harmony_back = select_intro_melody(left_hand_notes, direction="backward")
    # intro_harmony = intro_harmony_front + intro_harmony_back
    outro_harmony = select_intro_melody(left_hand_notes, direction="backward")
    intro_harmony_output_path = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\intro_harmony.mid"
    create_accompaniment_midi_file(intro_harmony, intro_harmony_output_path, tempo)
    outro_harmony_output_path = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\outro_harmony.mid"
    create_accompaniment_midi_file(outro_harmony, outro_harmony_output_path, tempo)


    save_note_sequence_to_json(json_path, note_sequence, num_measures)

    print(f"Note sequence saved to JSON at {json_path}")

if __name__ == "__main__":
    main()
