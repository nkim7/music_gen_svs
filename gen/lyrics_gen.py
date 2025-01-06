import openai
import re
import sys
import os
import json
import syllapy  # pyphen 대신 syllapy 사용
import time  


openai.api_key = "sk-robot-daniel-FOQfOlJ9dCGtSLaSTq2RT3BlbkFJ3fiAo6v08Aflm70zQmss"
MODEL = "gpt-3.5-turbo"


def generate_song_structure_with_chords(topic, mood, tempo, num_verses, model=MODEL, temperature=0.7, max_tokens=300):
    section_prompt = (
        "You are a highly creative and friendly assistant, tasked with writing simple and catchy educational lyrics "
        "for a 4/4 time signature song targeting children. "
        "Each verse and chorus must be short and concise, exactly 4 bars long in 4/4 time signature. "
        "Include the guitar chords above each line of lyrics. "
        "Use common chords for children's song to keep the structure simple and easy to play. "
        "Ensure that both verses and choruses are of similar length and structure, so they feel balanced and cohesive. "
        "Explicitly label the sections as 'Verse' and 'Chorus', and follow this format exactly:\n\n"
        "Verse:\n"
        "| C      | G      | Am     | F      |\n"
        "In a garden filled with colors bright,\n"
        "| C      | G      | Am     | F      |\n"
        "Blossoms dancing in the morning light,\n\n"
        "Chorus:\n"
        "| F      | C      | G      | Am     |\n"
        "Flowers, flowers, blooming everywhere,\n"
        "| F      | C      | G      | Am     |\n"
        "Sunshine glowing, filling up the air.\n\n"
        f"Write the song based on the mood '{mood}', but the lyrics should focus on teaching children about the topic '{topic}'. "
        "Please make the lyrics sufficiently long and in average have 3 words per chord."
        f"Ensure that the song is educational and simple for children to understand the topic '{topic}', with no need to include words that describe the mood explicitly. "
        f"Repeat this pattern until we have {num_verses} verses."
    )

    print(f"Prompt sent to OpenAI: {section_prompt}")  # Print the prompt

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": section_prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    print(f"Generated song structure: {response['choices'][0]['message']['content']}")  # Print the generated song structure
    return response['choices'][0]['message']['content'].strip()


def count_syllables_in_line(line):
    words = re.split(r'(\s+|,)', line)
    syllable_counts = []
    
    for word in words:
        if word == ',':
            continue  
        elif word.strip():  
            syllable_count = syllapy.count(word.strip())
            syllable_counts.append(syllable_count)
    
    print(f"Syllables for line '{line}': {syllable_counts}")  # Print syllable counts for each line
    return syllable_counts  

# Function to count the number of lines in lyrics
def count_lines_in_lyrics(lyrics):
    lines = [line for line in lyrics.split('\n') if line.strip()]
    print(f"Counted {len(lines)} lines in lyrics.")  # Print line count
    return len(lines)

# Function to write content to a file
def write_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"File saved: {filename}")  # Print file save message

# Function to calculate score for measures based on their deviation from the average
def calculate_score(measures):
    avg = sum(sum(m) for m in measures) / 4.0
    score = sum(abs(sum(m) - avg) for m in measures)
    print(f"Calculated score for measures: {score}")  # Print score
    return score

# Function to distribute syllables into 4 bars
def distribute_syllables(syllables):
    best_distribution = None
    best_score = float('inf')
    
    for i in range(1, len(syllables)):
        for j in range(i + 1, len(syllables)):
            for k in range(j + 1, len(syllables)):
                measures = [syllables[:i], syllables[i:j], syllables[j:k], syllables[k:]]
                score = calculate_score(measures)
                if score < best_score:
                    best_score = score
                    best_distribution = measures

    print(f"Best distribution: {best_distribution}")  
    return best_distribution

# Function to compare and select the longest syllable group from 4k, 4(k+1), 4(k+2), 4(k+3)
def select_longest_syllable_group(original_syllable_distribution):
    best_group = None
    for k in range(0, len(original_syllable_distribution), 4):
        group = original_syllable_distribution[k:k+4]
        if best_group is None:
            # Assign the first group
            best_group = group
        else:
            # Compare the groups and select the largest value
            for i in range(len(group)):
                for j in range(len(group[i])):
                    # Pad arrays to make them equal length before comparison
                    while len(best_group[i][j]) < len(group[i][j]):
                        best_group[i][j].append(0)
                    for idx, value in enumerate(group[i][j]):
                        # Update best_group by selecting the largest value from the original syllable distribution
                        best_group[i][j][idx] = max(best_group[i][j][idx], value)
    
    print(f"Selected longest syllable group: {best_group}")  # Print the final selected group
    return best_group

def extract_lyrics_and_syllables_as_dict(lyrics_with_chords):
    # Split lyrics into lines, ensuring we strip any trailing newlines or spaces
    lines = lyrics_with_chords.strip().split('\n')
    
    lyrics_data = {
        "lyrics": [],  
        "lyrics_with_plus": [],  
        "chord_progression": "",  
        "original_syllable_distribution": [], 
        "updated_syllable_distribution": [],  
        "selected_syllable_group": []  
    }
    
    chord_pattern = re.compile(r"\|.*?\|") 
    chord_progression = []
    i = 0
    

    while i < len(lines):
        line = lines[i].strip()


        if chord_pattern.search(line):
            chord_progression.append(line)
            if len(chord_progression) >= 4:  # 코드의 첫 4줄만 수집
                lyrics_data["chord_progression"] = " ".join(chord_progression)
            i += 1  # 코드 이후 가사가 올 것으로 기대하고 진행
        else:

            lyric_line = line.strip()
            if lyric_line and lyric_line.lower() not in ["verse:", "chorus:"]:
                lyrics_data["lyrics"].append(lyric_line)

      
                words = re.split(r'(\s+|,)', lyric_line)
                processed_line = ""
                for word in words:
                    if word.strip():  
                        syllable_count = syllapy.count(word.strip())
                        processed_line += word + ' +' * (syllable_count - 1)
                    else:
                        processed_line += word  
                lyrics_data["lyrics_with_plus"].append(processed_line.strip())

            i += 1  

 
    syllable_distribution = generate_syllable_distribution(lyrics_data["lyrics"])
    lyrics_data["original_syllable_distribution"] = syllable_distribution  # 원본 음절 분포 저장


    selected_syllable_group = select_longest_syllable_group(syllable_distribution)


    lyrics_data["updated_syllable_distribution"] = flatten_syllable_distribution(selected_syllable_group)
    lyrics_data["selected_syllable_group"] = selected_syllable_group

    return lyrics_data


def flatten_syllable_distribution(distribution):
    flattened_distribution = []
    for measure in distribution:
        for submeasure in measure:
            total_beats = sum(submeasure)
            if total_beats < 4:
                submeasure.extend([0] * (4 - total_beats))
            flattened_distribution.append(submeasure)
    
    print(f"Flattened syllable distribution: {flattened_distribution}")  # Print flattened syllable distribution
    return flattened_distribution

def generate_syllable_distribution(lyrics):
    syllable_distributions = []
    for line in lyrics:
        syllables = count_syllables_in_line(line)
        syllable_distributions.append(distribute_syllables(syllables))
    
    print(f"Syllable distributions: {syllable_distributions}")  # Print full syllable distributions
    return syllable_distributions




# Main execution loop 
while True:
    try:
        topic = sys.argv[1] if len(sys.argv) > 1 else "bears"
        mood = sys.argv[2] if len(sys.argv) > 2 else "happy and uplift"
        tempo = int(sys.argv[3]) if len(sys.argv) > 3 else 90
        num_measures = int(sys.argv[4]) if len(sys.argv) > 4 else 32

        print("num_measures: ", num_measures)

        print(f"Topic: {topic}, Mood: {mood}, Tempo: {tempo}, Measures: {num_measures}")  # Print input parameters

        num_verses = max(num_measures // 16, 1)
        expected_line_count = 10 * num_verses

        lyrics_with_chords = ""
        while True:
            lyrics_with_chords = generate_song_structure_with_chords(topic, mood, tempo, num_verses)
            line_count = count_lines_in_lyrics(lyrics_with_chords)

            print(f"Generated line count: {line_count}, Expected: {expected_line_count}")  # Print line count check

            if line_count == expected_line_count:
                break
            elif line_count == expected_line_count + 1:
                lyrics_with_chords = "\n".join(lyrics_with_chords.split("\n")[1:])
                line_count -= 1  
                if line_count == expected_line_count:
                    break
            print("Regenerating lyrics...")
            

        lyrics_with_chords_file_path = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\lyrics_with_chords.txt"
        write_to_file(lyrics_with_chords_file_path, lyrics_with_chords)

        lyrics_with_syllables = extract_lyrics_and_syllables_as_dict(lyrics_with_chords)

        final_lyrics_with_syllables_file_path = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\final_lyrics_with_syllables.json"
        lyrics_data = extract_lyrics_and_syllables_as_dict(lyrics_with_chords)
        with open(final_lyrics_with_syllables_file_path, 'w', encoding='utf-8') as f:
            json.dump(lyrics_data, f, ensure_ascii=False, indent=4)

        print(f"Processed lyrics with syllables have been successfully saved to {final_lyrics_with_syllables_file_path}.")
        
        break
        
    except Exception as e:
        print(f"An error occurred: {e}. Restarting the process in 5 seconds...")
        time.sleep(5)  # Wait 5 seconds before restarting
        continue
