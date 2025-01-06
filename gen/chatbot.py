import openai
import json
import random
import sys
from textblob import TextBlob  # For sentiment analysis
from transformers import pipeline  # For relevance checking with Hugging Face
from sentence_transformers import SentenceTransformer, util
import re
import sys
import io

# Set stdout and stderr to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Set OpenAI API key
openai.api_key = "sk-robot-daniel-FOQfOlJ9dCGtSLaSTq2RT3BlbkFJ3fiAo6v08Aflm70zQmss"

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
semantic_model = SentenceTransformer("all-MiniLM-L6-v2")


# Dynamic emoji mapping
EMOJI_MAP = {
    "sun": "☀️",
    "moon": "🌙",
    "rain": "🌧️",
    "flowers": "🌸",
    "butterflies": "🦋",
    "fire": "🔥",
    "water": "💧",
    "summer": "🌞",
    "winter": "❄️",
    "stars": "✨",
}


def check_relevance(user_response, topic, question):
  
    prompt = (
        f"Classify the user's response into one of the following categories:\n"
        f"- 'Answer_Not_Relevant': If the response is unrelated to the topic and question.\n"
        f"- 'Answer_Relevant': If the response is relevant to the topic and question.\n"
        f"- 'Question_Relevant_Answered': If the response is relevant to the topic AND have a relevant question.\n"
        f"- 'Question_Relevant_Unanswered': If the response is a relevant to the topic BUT the question is unanswered.\n"
        f"- 'Question_Irrelevant': If the response is an irrelevant question.\n"
        f"- 'Question_reasked': If the response is asking back the question or say I don't know.\n\n"
        f"### Examples ###\n"
        f"1. Topic: 'apple', Question asked: 'Do you like apples?'\n"
        f"   User Response: 'I love oranges.' -> Output: 'Answer_Not_Relevant'\n"
        f"2. Topic: 'apple', Question asked: 'Do you like apples?'\n"
        f"   User Response: 'Yes, I like them.' -> Output: 'Answer_Relevant'\n"
        f"   Topic: 'apple', Question asked: 'How did you feel about the song?'\n"
        f"   User Response: 'I like it.' -> Output: 'Answer_Relevant'\n"
        f"3. Topic: 'apple', Question asked: 'Do you like apples?'\n"
        f"   User Response: 'I like them. Do birds like them too?' -> Output: 'Question_Relevant_Answered'\n"
        f"4. Topic: 'apple', Question asked: 'Do you like apples?'\n"
        f"   User Response: 'Why are apples so popular?' -> Output: 'Question_Relevant_Unanswered'\n"
        f"5. Topic: 'apple', Question asked: 'Do you like apples?'\n"
        f"   User Response: 'Why is the sky blue?' -> Output: 'Question_Irrelevant'\n"
        f"5. Topic: 'apple', Question asked: 'Do you like apples?'\n"
        f"   User Response: 'Do I like apples? I don't know.' -> Output: 'Question_reasked'\n\n"
        f"### Analyze This ###\n"
        f"Topic: {topic}\n"
        f"Current Question: {question}\n"
        f"User Response: {user_response}\n\n"
        "Output one of: 'Answer_Not_Relevant', 'Answer_Relevant', 'Question_Relevant_Answered', 'Question_Relevant_Unanswered', 'Question_Irrelevant'."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an assistant that classifies user responses."},
            {"role": "user", "content": prompt}
        ]
    )

    classification = response['choices'][0]['message']['content'].strip()
    # print(question)
    # print(classification)
    return classification





# # (0, 0.2, 0.3, 0.2, 0.5, 0.1)
#params tried version

# def check_relevance(user_response, topic, question, polarity):
# 
#     # Define labels for zero-shot classification
#     positive_labels = [
#         f"Relevant positive answer to the question: '{question}'",
#         f"Positive response about the topic: {topic}",
#         "Off-topic"
#     ]
#     negative_labels = [
#         f"Relevant negative answer to the question: '{question}'",
#         f"Negative response about the topic: {topic}",
#         "Off-topic"
#     ]
    

#     labels = positive_labels if polarity == "positive" else negative_labels


#     result = classifier(user_response, labels)
#     relevance_scores = {label: score for label, score in zip(result["labels"], result["scores"])}
#     classification_relevance_score = relevance_scores[labels[0]]
#     off_topic_score = relevance_scores["Off-topic"]
#     classification_relevance = classification_relevance_score > off_topic_score

#     combined_context = f"Question: {question} Topic: {topic}"
#     embeddings = semantic_model.encode([user_response, combined_context], convert_to_tensor=True)
#     similarity_score = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()


#     response_length = len(user_response.split())
#     if response_length <= 0:  # For short, generic responses
#         similarity_threshold = 0.2
#     else:
#         similarity_threshold = 0.3 if polarity == "positive" else 0.5

#     # Final relevance decision logic

#     is_relevant = (
#         (classification_relevance and similarity_score > similarity_threshold) or
#         (((classification_relevance_score - off_topic_score) > 0.5) or ((similarity_score - similarity_threshold) > 0.1))
#     )


#     print(f"User Response: {user_response}")
#     print(f"Zero-Shot Classification Scores: {relevance_scores}")
#     print(f"Semantic Similarity Score: {similarity_score:.2f}")
#     print(f"Response Length: {response_length}")
#     print(f"Final Relevance Decision: {is_relevant}")


#     if not is_relevant:
#         reasons = []
#         if not classification_relevance:
#             reasons.append("Zero-shot classification marked the response as off-topic.")
#         if similarity_score <= similarity_threshold:
#             reasons.append("Semantic similarity score was below the threshold.")
        

#     return is_relevant


# (0, 0.2, 0.2, 0.2, 0.5, 0.1)

def reframe_question(original_question):

    original_question = original_question.lower()

    reframed_questions = [
        f"Hmm, let’s try again: {original_question}",
        f"That’s an interesting thought! But {original_question}",
        f"No worries! Let’s refocus: {original_question}"
    ]
    return random.choice(reframed_questions)

def handle_relevance_check(user_response, topic, question, max_attempts=3):

    attempt = 0

    while attempt < max_attempts:
        classification = check_relevance(user_response, topic, question)

        if classification == "Answer_Relevant":

            return user_response, topic, False

        elif classification == "Answer_Not_Relevant":

            print(reframe_question(question))
         
            attempt += 1
            user_response = input("You: ").strip()

        elif classification == "Question_Relevant_Answered":

            gpt_answer = answer_question_with_gpt(user_response, topic)
            print(f"{gpt_answer}")
            return gpt_answer, topic, True

        elif classification == "Question_Relevant_Unanswered":

            gpt_answer = answer_question_with_gpt(user_response, topic)
            print(f"{gpt_answer}\n")
            print(f"{question}")
            user_response = input("You: ").strip()
            attempt += 1

        elif classification == "Question_Irrelevant":
      
            print("Your question doesn't seem related to the topic. Let's focus on the current topic!")
            attempt += 1
            user_response = input("You: ").strip()

        elif classification == "Question_reasked":
 
            print("I want to know your opinion! Don't be scared and let me know what you think about it!")
            print(f"{question}")
            attempt += 1
            user_response = input("You: ").strip()


    print("We seem to be off track. Let's reset to a simpler topic like 'sunshine'!")
    topic = "sunshine"
    emoji = get_dynamic_emoji_with_gpt(topic)
    return "sunshine", topic, emoji

# use this when you use chatbot on Terminal
# def handle_relevance_check(user_response, topic, question, max_attempts=3):

#     attempt = 0

#     while attempt < max_attempts:
#         classification = check_relevance(user_response, topic, question)

#         if classification == "Answer_Relevant":
#             # User's response is relevant to the question and topic
#             return user_response, topic, False

#         elif classification in {"Answer_Not_Relevant", "Question_Irrelevant"}:
#             # Response is not relevant to the topic or is an irrelevant question
#             user_response = reframe_question(question)
#             attempt += 1

#         elif classification == "Question_Relevant_Answered":
#             # User has answered the question and asked a relevant follow-up
#             gpt_answer = answer_question_with_gpt(user_response, topic)
#             return gpt_answer, topic, True

#         elif classification == "Question_Relevant_Unanswered":
#             # User asked a relevant question but did not answer the current one
#             gpt_answer = answer_question_with_gpt(user_response, topic)
#             user_response = reframe_question(question)
#             attempt += 1

#         elif classification == "Question_reasked":
#             # User is uncertain or asking back the original question
#             user_response = reframe_question(question)
#             attempt += 1

#     print(classification)
#     # Fallback after max attempts: reset to a simple topic
#     fallback_topic = "sunshine"
#     fallback_emoji = get_dynamic_emoji_with_gpt(fallback_topic)
#     return user_response, fallback_topic, fallback_emoji





def answer_question_with_gpt(user_question, topic):
  
    prompt = (
        f"Answer the following question in a simple, friendly, and concise way. "
        f"Relate it to the topic '{topic}' if possible:\n"
        f"User Question: {user_question}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers user questions concisely for a 7 years old."},
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content'].strip()




def extract_topic_with_gpt(user_input):

    prompt = (
        "Extract the main topic or theme from the following user input for a song idea:\n"
        "Ensure the output is a concise, clear noun or noun phrase that represents the main idea.\n"
        "For example:\n"
        "- If the user says 'I want to sing about thunder,' the topic should be 'thunder.'\n"
        "- If the user says 'The   song is about big, brown, and furry bears that live in the forest. It talks about a mother bear who takes care of her little cub to keep it safe.,' the topic should be 'bears.'\n"
        "Avoid including unnecessary verbs or prepositions in the topic.\n"
        f"Input: {user_input}\n"
        "Output the main topic as a single phrase."
 
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts main topics from user input."},
            {"role": "user", "content": prompt}
        ]
    )
    topic = response['choices'][0]['message']['content'].strip()
    return topic



def extract_mood_with_gpt(user_input, topic, user_thoughts):

    prompt = (
        "Extract the mood or style described in the following user input for a song:\n"
        "Ensure the output is a concise list of adjectives that represent the mood or style. For example:\n"
        "- If the user says 'I want the song to be fast and adventurous,' the output should be 'fast and adventurous.'\n"
        "- If the user says 'It should feel calm and relaxing,' the output should be 'calm and relaxing.'\n"
        f"Context: The topic of the song is {topic} and is related to {user_thoughts}.\n"
        f"Mood input: {user_input}\n"
        "Output the mood or style as a concise phrase."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts moods or styles from user input."},
            {"role": "user", "content": prompt}
        ]
    )
    mood = response['choices'][0]['message']['content'].strip()
    return mood



def get_dynamic_emoji_with_gpt(topic):
 
    if topic.lower() in EMOJI_MAP:
        return EMOJI_MAP[topic.lower()]
    prompt = (
        f"Suggest an emoji that represents {topic} in a cheerful and child-friendly way."
        "Give me just the emoji(s)"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an assistant that matches topics to emojis."},
            {"role": "user", "content": prompt}
        ]
    )
    emoji = response['choices'][0]['message']['content'].strip()
    return emoji if emoji else "🎵"

def provide_fun_fact_with_gpt(topic, user_response=None):

    prompt = (
        f"Provide a simple and fun fact about {topic} suitable for a 10-year-old child. "
        "Make it cheerful, concise, and easy to understand."
    )
    if user_response:
        prompt += (
            f" Relate it to the user's response: '{user_response}'."
            "Keep the explanation friendly and encouraging."
        )
    else:
        prompt += " Ensure the fact is exciting and relevant to the topic."

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a friendly assistant providing fun facts. You don't yap."},
            {"role": "user", "content": prompt}
        ]
    )
    fun_fact = response['choices'][0]['message']['content'].strip()
    return fun_fact


def random_response(response_list):
  
    return random.choice(response_list)



def analyze_sentiment(response):
    
    response_lower = response.lower()

 
    yes_pattern = r"\byes\b[\s!.,]*"
    no_pattern = r"\bno\b[\s!.,]*"

    if re.search(yes_pattern, response_lower):

        return "positive"
    elif re.search(no_pattern, response_lower):

        return "negative"


    blob = TextBlob(response)
    polarity = blob.sentiment.polarity


    if polarity >= 0:  
        # print("positive!")
        # print(polarity)
        return "positive"
    elif polarity < -0.3:  
        # print("negative!")
        # print(polarity)
        return "negative"
    else:
        # print("neutral!")
        # print(polarity)
        return "neutral"

def summarize_lyrics(lyrics):

    prompt = (
        "Summarize the following song lyrics in a simple and friendly way for a 5-year-old:"
        f"\n\n{lyrics}\n\n"
        "Keep the summary cheerful and concise."
        "Start your answer with The or a."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a friendly assistant summarizing song lyrics for children."},
            {"role": "user", "content": prompt}
        ]
    )
    summary = response['choices'][0]['message']['content']
    return summary.strip()


#THE ORIGINAL
# def chat_with_user(topic, previous_song_path):


    with open(previous_song_path, 'r') as file:
        previous_song_data = json.load(file)


    lyrics = previous_song_data.get("lyrics", [])


 
    lyrics_summary = summarize_lyrics(" ".join(lyrics))
    emoji = get_dynamic_emoji_with_gpt(topic)


    greetings = [
        f"Our last song was about {topic}! {emoji}✨",
        f"Previously, we created a song about {topic}. Isn’t that exciting? ✨",
        f"Do you remember? The last song was all about {topic}! {emoji}"
    ]

 
    print("\n--- Chat with the Songwriting Chatbot ---")
    print(f"{random_response(greetings)}")
    print(f"{lyrics_summary}")

    # Step 1: Ask how the user felt about the song
    question = "How did you feel about the song? 😊"
    print(question)
    topic_summary = f"{topic} & {lyrics_summary}"
    user_feeling = input("You: ").strip()
    user_feeling, topic_summary, was_a_question = handle_relevance_check(user_feeling, topic_summary, question,  max_attempts=3)

    if not was_a_question:
   
        if analyze_sentiment(user_feeling) == "positive":
            print(f"I’m so glad you liked the song! Songs about {topic} can be so fun! {emoji}")
        else:
            print(f"That’s okay—songs are like experiments! Let’s make the next one even more fun! {emoji}")
    print(topic)

    # Step 2: Ask if they like the topic
    question = f"Do you like {topic}? Let me know why you think so! 😊"
    print(question)
    user_thoughts_on_topic = input("You: ").strip()
    sentiment_feeling = analyze_sentiment(user_thoughts_on_topic)
    user_thoughts_on_topic, topic, was_a_question = handle_relevance_check(user_thoughts_on_topic, topic, question,  max_attempts=3)

    # Provide a fun fact
    print(topic)
    fun_fact = provide_fun_fact_with_gpt(topic, user_response=user_thoughts_on_topic)
    print(f"{fun_fact} {emoji}")

    # Step 3: Handle feedback on the topic and switch if needed
    question = f"What do you think about {topic} now? {emoji}"
    print(question)
    user_feeling_renewed = input("You: ").strip()
    user_feeling_renewed, topic, was_a_question = handle_relevance_check(user_feeling_renewed, topic, question, 
                                                                max_attempts=3)
    sentiment_feeling = analyze_sentiment(user_feeling_renewed)

    if not was_a_question:
     
        if sentiment_feeling in ["negative", "neutral"]:
            print(f"Hmm, it seems like {topic} isn’t working for you. Do you have another topic in mind? {emoji}")
            new_topic_input = input("You: ").strip()

            # Directly extract the new topic
            topic = extract_topic_with_gpt(new_topic_input)
            emoji = get_dynamic_emoji_with_gpt(topic)
            print(f"Great! Let’s talk about {topic}! {emoji}")
        else:
            print(f"Glad to know your thoughts about {topic}! Let’s move on. {emoji}")

    # Step 4: Transition to related thoughts
    question = f"What comes to mind when you think of {topic}? Let's make a new song about them! {emoji}"
    print(question)
    user_thoughts = input("You: ").strip()
    sentiment_feeling = analyze_sentiment(user_thoughts)
    user_thoughts, topic, was_a_question = handle_relevance_check(user_thoughts, topic, question, max_attempts=3)

    user_thoughts = extract_topic_with_gpt(user_thoughts)
    emoji = get_dynamic_emoji_with_gpt(user_thoughts)

    if not was_a_question:
        # Step 5: Encourage storytelling and song creation
        print(f"Wow, that’s amazing! Stories about {topic} and {user_thoughts} make songs so magical! {emoji}")
        print(f"Songs can tell stories, teach lessons, or even share feelings. Isn’t that fun? {emoji}")

    # Step 6: Ask about the mood and tempo
    mood_questions = [
        "How should the song feel? Do you want it to be happy, calm, exciting, or something else? 🥳🎵",
        "What’s the vibe for this song? Calm, exciting, or maybe something in between? 🎶",
        "Should this song be cheerful, soothing, or adventurous? 🎵✨"
    ]
    question = f"{random_response(mood_questions)}"
    print(question)
    user_mood = input("You: ").strip()
    sentiment_feeling = analyze_sentiment(user_mood)
    user_mood, topic, was_a_question = handle_relevance_check(user_mood, topic, question,  max_attempts=3)

    # Step 7: Finalize the song mood and topic
    song_mood = extract_mood_with_gpt(user_mood, topic, user_thoughts)
    emoji = get_dynamic_emoji_with_gpt(song_mood)
    if not was_a_question:
        print(f"Got it! A {song_mood.lower()} song about {topic} with \"{user_thoughts}\" is coming right up! {emoji}")


    topic = f"{topic} & {user_thoughts}"
    emoji = get_dynamic_emoji_with_gpt(topic)
    print(f"Our final topic is '{topic}'. Let’s create something magical together! {emoji}")


    return song_mood, topic







# logic process
def handle_greeting(conversation_state, topic, emoji, lyrics_summary):
    responses = []

    responses.append("Welcome back! Let's start fresh. 😊")
    
    # Add the greeting and topic-specific details
    responses.append(f"Our last song was about {topic}! {emoji}✨")
    if lyrics_summary:
        responses.append(lyrics_summary)
    responses.append("How did you feel about the song? 😊")
    
    # Update the stage to feedback
    conversation_state["stage"] = "feedback"
    return responses, conversation_state



def handle_feedback(conversation_state, topic, emoji, user_message):
 
    responses = []

    sentiment = analyze_sentiment(user_message)


    if sentiment == "positive":
        responses.append(f"I’m so glad you like {topic}! Songs about {topic} can be so fun! {emoji}")
    else:
        responses.append(f"That’s okay—songs are like experiments! Let’s make the next one even more fun! {emoji}")

    responses.append(f"Do you like {topic}? Let me know why you think so! 😊")
    conversation_state["stage"] = "topic_feedback"
    
    return responses, conversation_state

def handle_topic_feedback(conversation_state, topic, emoji, user_message):

    responses = []

    fun_fact = provide_fun_fact_with_gpt(topic, user_message)
    responses.append(f"{fun_fact} {emoji}")
    responses.append(f"What do you think about {topic} now? {emoji}")
    conversation_state["stage"] = "topic_feedback_after_funfact"

    return responses, conversation_state

def handle_topic_feedback_after_funfact(conversation_state, topic, emoji, user_message):

    responses = []
    sentiment = analyze_sentiment(user_message)

    if sentiment in ["negative", "neutral"]:
        responses.append(f"Hmm, it seems like {topic} isn’t working for you. Do you have another topic in mind? {emoji}")
        conversation_state["stage"] = "story_creation"
    else:
        responses.append(f"Glad to know your thoughts about {topic}! {emoji}")
        responses.append(f"What comes to mind when you think of {topic}? Let’s make a new song about it! {emoji}")
        conversation_state["stage"] = "story_creation"

    return responses, conversation_state

def handle_story_creation(conversation_state, topic, emoji, user_message):
    responses = []
    new_topic = user_message.strip() 

    new_emoji = get_dynamic_emoji_with_gpt(new_topic)
    responses.append(f"Got it! A song about {new_topic} must be so fun! {new_emoji}")
    responses.append(f"What should be the mood of the new song? Happy? Sad?")
    conversation_state["topic"] = new_topic
    conversation_state["emoji"] = new_emoji
    conversation_state["stage"] = "finalize_mood"
    return responses, conversation_state


def handle_finalize_mood(conversation_state, topic, emoji, user_message):
    responses = []
    mood = user_message.strip() 

    responses.append(f"Got it! A {mood.lower()} song about {topic} is coming right up! {emoji}")
    conversation_state["final_topic"] = topic
    conversation_state["final_mood"] = mood
    conversation_state["stage"] = "end"


    try:
        result = trigger_song_generation(topic, mood)
        if result["status"] == "success":
            responses.append("Music generation has started! 🎶 Check back soon for your new song.")
        else:
            responses.append("Oops, there was an issue starting the music generation. Please try again.")
    except Exception as e:
        responses.append(f"Error during music generation: {str(e)}")

    return responses, conversation_state


def trigger_song_generation(topic, mood):

    import requests

    url = "http://127.0.0.1:5000/generate-music"  # Ensure this URL matches your Flask server
    payload = {"mood": mood, "topic": topic}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP response codes >= 400
        return {"status": "success", "message": response.json().get("message", "Music generation started!")}
    except requests.exceptions.RequestException as e:
        return {"status": "failure", "message": f"Error: {str(e)}"}

#FINAL
def chat_with_user(user_message, conversation_state, previous_song_path):

    responses = []


    if "stage" not in conversation_state:
        try:
            with open(previous_song_path, 'r') as file:
                previous_song_data = json.load(file)
            lyrics = previous_song_data.get("lyrics", [])
            conversation_state["lyrics_summary"] = summarize_lyrics(" ".join(lyrics))
        except FileNotFoundError:
            conversation_state["lyrics_summary"] = ""

        conversation_state["stage"] = "greeting"
        conversation_state["topic"] = extract_topic_with_gpt(conversation_state["lyrics_summary"])
        conversation_state["emoji"] = get_dynamic_emoji_with_gpt(conversation_state["topic"])
        responses.append("Welcome back! Let's start fresh. 😊")


    stage = conversation_state["stage"]
    topic = conversation_state.get("topic")
    emoji = conversation_state.get("emoji", "")
    lyrics_summary = conversation_state.get("lyrics_summary", "")

 
    if stage == "greeting":
        responses, conversation_state = handle_greeting(conversation_state, topic, emoji, lyrics_summary)
    elif stage == "feedback":
        responses, conversation_state = handle_feedback(conversation_state, topic, emoji, user_message)
    elif stage == "topic_feedback":
        responses, conversation_state = handle_topic_feedback(conversation_state, topic, emoji, user_message)
    elif stage == "topic_feedback_after_funfact":
        responses, conversation_state = handle_topic_feedback_after_funfact(conversation_state, topic, emoji, user_message)
    elif stage == "story_creation":
        responses, conversation_state = handle_story_creation(conversation_state, topic, emoji, user_message)
    elif stage == "finalize_mood":
        responses, conversation_state = handle_finalize_mood(conversation_state, topic, emoji, user_message)

    return responses, conversation_state







# previous_song_path = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\final_lyrics_with_syllables.json"
# mood, topic = chat_with_user("birds", previous_song_path)

if __name__ == "__main__":
    # Start the chatbot only when this file is executed directly
    previous_song_path = r"C:\Users\nagyu\music-gen-app\music\gen\demo_outputs\final_lyrics_with_syllables.json"
    if len(sys.argv) > 2:
        topic = sys.argv[2]
        print("!!!!! The topic is!!!", topic)
        mood, topic = chat_with_user(topic, previous_song_path)
    else:
        print("Usage: python chatbot.py <topic>")

