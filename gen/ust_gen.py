import mido
from mido import MidiFile
import yaml
from collections import OrderedDict
import json
import re
import sys

# Set topic and tempo with default values
topic = sys.argv[1] if len(sys.argv) > 1 else "bears"
tempo = int(sys.argv[2]) if len(sys.argv) > 2 else 90


lyrics_json_path = r'C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\final_lyrics_with_syllables.json'
phoneme_yaml_path = r'C:\Users\nagyu\music-gen-app\music\gen\envccv.yaml'
ustx_output_path = r'C:\Users\nagyu\music-gen-app\music\gen\final_music\output.ustx'


class MyDumper(yaml.SafeDumper):
    def represent_scalar(self, tag, value, style=None):
        if value == "":
            return super(MyDumper, self).represent_scalar('tag:yaml.org,2002:str', value, style='"')
        return super(MyDumper, self).represent_scalar(tag, value, style)


def dict_representer(dumper, data):
    return dumper.represent_dict(data.items())


MyDumper.add_representer(OrderedDict, dict_representer)


def load_data_from_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    lyrics = [word for line in data['lyrics'] for word in line.split()]
    return lyrics, data['rhythm_sequence'], data['note_sequence']


def load_phoneme_dictionary(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        phoneme_data = yaml.safe_load(f)

    phoneme_dict = {entry['grapheme']: entry['phonemes'] for entry in phoneme_data['entries']}
    return phoneme_dict

def clean_lyric(lyric):
  
    lyric = lyric.lower() 
    lyric = re.sub(r'[,.]', '', lyric)  
    return lyric

# Create USTX data in YAML format
def create_ustx_data(lyrics, rhythm_sequence, note_sequence, phoneme_dict, bpm=tempo):
    ustx_data = OrderedDict({
        'name': topic,
        'comment': '',
        'output_dir': 'Vocal',
        'cache_dir': 'UCache',
        'ustx_version': '0.6',
        'resolution': 480,
        'bpm': bpm,
        'beat_per_bar': 4,
        'beat_unit': 4,
        'expressions': OrderedDict({
            'dyn': {
                'name': 'dynamics (curve)',
                'abbr': 'dyn',
                'type': 'Curve',
                'min': -240,
                'max': 120,
                'default_value': 0,
                'is_flag': False,
                'flag': ''
            },
            'pitd': {
                'name': 'pitch deviation (curve)',
                'abbr': 'pitd',
                'type': 'Curve',
                'min': -1200,
                'max': 1200,
                'default_value': 0,
                'is_flag': False,
                'flag': ''
            },
            'clr': {
                'name': 'voice color',
                'abbr': 'clr',
                'type': 'Options',
                'min': 0,
                'max': -1,
                'default_value': 0,
                'is_flag': False,
                'options': []
            },
            'eng': {
                'name': 'resampler engine',
                'abbr': 'eng',
                'type': 'Options',
                'min': 0,
                'max': 1,
                'default_value': 0,
                'is_flag': False,
                'options': ['', 'worldline']
            }
        }),
        'key': 0,
        'time_signatures': [
            {'bar_position': 0, 'beat_per_bar': 4, 'beat_unit': 4}
        ],
        'tempos': [
            {'position': 0, 'bpm': bpm}
        ],
        'tracks': [
            OrderedDict({
                'singer': 'Hanami -Dancing Fae- English VCCV',
                'phonemizer': 'OpenUtau.Plugin.Builtin.EnglishVCCVPhonemizer',
                'renderer_settings': {'renderer': 'WORLDLINE-R'},
                'track_name': 'Track1',
                'track_color': 'Blue',
                'mute': False,
                'solo': False,
                'volume': 0,
                'pan': 0,
                'track_expressions': [],
                'voice_color_names': ['']
            })
        ],
        'voice_parts': [
            OrderedDict({
                'duration': sum(rhythm_sequence) * 480, 
                'name': topic,
                'comment': '',
                'track_no': 0,
                'position': 0,
                'notes': []
            })
        ],
        'curves': [],
        'wave_parts': []
    })

    current_position = 0
    lyric_index = 0
    rhythm_index = 0
    note_index = 0
    first_note_adjusted = False 

    while lyric_index < len(lyrics):
        # Loop rhythm 
        rhythm = rhythm_sequence[rhythm_index % max(len(rhythm_sequence), 64)]
        note = note_sequence[note_index % max(len(note_sequence), 64)]

        # Define rhythm in ticks
        if rhythm == 0:
            duration = 480 
        else:
            duration = rhythm * 480  # 1 -> 480, 2 -> 2*480, etc.

        if note == '-':
          
            current_position += duration
        else:
            tone = note
            lyric = lyrics[lyric_index]
            lyric_index += 1

        
            clean_lyric_value = clean_lyric(lyric)

  
            if clean_lyric_value in phoneme_dict:
                phonemes = phoneme_dict[clean_lyric_value]
                phonemes_str = [str(p) for p in phonemes]
                lyric_with_phonemes = f"{lyric} [{' '.join(phonemes_str)}]"
            else:
                lyric_with_phonemes = lyric

  
            vibrato_length = 15 if (duration == 480 and tempo > 100) else 25

      
            if not first_note_adjusted:
                current_position += 60
                duration -= 60
                first_note_adjusted = True

            next_note = rhythm_sequence[(note_index + 1) % max(len(rhythm_sequence), 64)] if note_index + 1 < len(note_sequence) else None

            if next_note != 0:
              
                final_duration = duration - 60
            elif (duration == 480 or duration == 420) and next_note == 0:
            
                final_duration = duration + 60
            else:

                final_duration = duration


            phoneme_overrides = []

            # Check if the lyric_with_phonemes is "It's [i t s]"
            if lyric_with_phonemes == "It's [i t s]":
                phoneme_overrides = [
                    {'index': 1, 'offset': -167},
                    {'index': 2, 'phoneme': 's-'}
                ]
            elif lyric_with_phonemes == "it's [i t s]":
                phoneme_overrides = [
                    {'index': 1, 'offset': -167},
                    {'index': 2, 'phoneme': 's-'}
                ]
            elif lyric_with_phonemes == "that's [dh @ t s]":
                phoneme_overrides = [
                    {'index': 1, 'offset': -105},
                    {'index': 2, 'phoneme': 's-'}
                ]
            
            

            note_entry = OrderedDict({
                'position': current_position,
                'duration': final_duration,  
                'tone': tone,  
                'lyric': lyric_with_phonemes,
                'pitch': OrderedDict({
                    'data': [{'x': -40, 'y': 0, 'shape': 'io'}, {'x': 40, 'y': 0, 'shape': 'io'}],
                    'snap_first': True
                }),
                'vibrato': OrderedDict({
                    'length': vibrato_length,  
                    'period': 175,
                    'depth': 25,
                    'in': 10,
                    'out': 10,
                    'shift': 0,
                    'drift': 0,
                    'vol_link': 0
                }),
                'phoneme_expressions': [],
                'phoneme_overrides': phoneme_overrides  #
            })

            ustx_data['voice_parts'][0]['notes'].append(note_entry)

          
            current_position += duration


        rhythm_index += 1
        note_index += 1

    return ustx_data



lyrics, rhythm_sequence, note_sequence = load_data_from_json(lyrics_json_path)


phoneme_dict = load_phoneme_dictionary(phoneme_yaml_path)


ustx_data = create_ustx_data(lyrics, rhythm_sequence, note_sequence, phoneme_dict)

# Save the USTX file in YAML format
with open(ustx_output_path, 'w', encoding='utf-8') as f:
    yaml.dump(ustx_data, f, allow_unicode=True, default_flow_style=False, Dumper=MyDumper)

print(f"USTX file has been created at {ustx_output_path}.")
