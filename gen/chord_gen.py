import openai


openai.api_key = "sk-robot-daniel-FOQfOlJ9dCGtSLaSTq2RT3BlbkFJ3fiAo6v08Aflm70zQmss"

def generate_chord_progression(mood, topic):

    prompt = (
        f"You are a music composition assistant. Generate a chord progression that perfectly fits the mood of '{mood}' and the topic of '{topic}'. "
        "The chord progression should be in the form of 4 chords per bar, with a total of 2 bars (4 * 2 structure). "
        "First bar is for verses and the other bar is for chorus."
        "Please use standard chords (e.g., C, G, Am, F) and ensure the progression flows well for the given mood. "
        "Output only the chords in sequence without any labels or additional text."
    )
    

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates music chord progressions."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.7
    )
    

    chord_progression = response['choices'][0]['message']['content'].strip()
    
    return chord_progression


def generate_tempo(mood, topic):

    prompt = (
        f"Given the mood '{mood}' and topic '{topic}', decide a suitable tempo in beats per minute (BPM). "
        "The tempo should match the emotional tone and energy level of the mood and the topic. "
        "Unless the mood specifically includes words like 'fast' or 'slow', try to keep the tempo between 60 and 120 BPM. "
        "Please provide only the BPM value as a number."
    )
    

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that decides appropriate tempos for different moods."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10,  
        temperature=0.7
    )
    

    tempo = int(response['choices'][0]['message']['content'].strip())
    
    return tempo

