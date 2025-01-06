import subprocess

# Paths
midi_file = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\melody_only.mid"
musescore_path = r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe"
output_file_pdf = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\melody_only.pdf"
plugin_name = r"C:\Program Files\MuseScore 3\plugins\linePerFourMeasures.qml"  
score_file = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\melody_only.mscz"  # MuseScore file output


def apply_plugin_to_midi(midi_path, output_score_path, musescore_exe, plugin_path):
    try:
    
        subprocess.run([musescore_exe, '--plugin', plugin_path, '-o', output_score_path, midi_path], check=True)
        print(f"MuseScore file created and plugin applied: {output_score_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during plugin application: {e}")


def convert_score_to_pdf(score_path, output_pdf_path, musescore_exe):
    try:

        subprocess.run([musescore_exe, '-o', output_pdf_path, score_path], check=True)
        print(f"PDF file created: {output_pdf_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during PDF export: {e}")

# Apply the plugin to the MIDI file and save it as an MSCZ score
apply_plugin_to_midi(midi_file, score_file, musescore_path, plugin_name)

# Convert the MSCZ score file to PDF
convert_score_to_pdf(score_file, output_file_pdf, musescore_path)
