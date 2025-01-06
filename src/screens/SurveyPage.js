import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  Alert,
  TouchableOpacity,
  ScrollView,
} from 'react-native';

export default function SurveyPage({ navigation, route }) {
  const { mood, topic } = route.params; // Retrieve mood and topic passed as props
  const [newTopic, setNewTopic] = useState('');
  const [newMood, setNewMood] = useState('');
  const [likeSong, setLikeSong] = useState(null); // State for multiple-choice answer
  const [dummyAnswer2, setDummyAnswer2] = useState(''); // State for dummy Q2
  const [dummyAnswer3, setDummyAnswer3] = useState(''); // State for dummy Q3
  const [isLoading, setIsLoading] = useState(false); // For loading state

  const handleGenerateMusic = () => {
    if (!newTopic || !newMood) {
      Alert.alert('Error', 'Please provide both the new topic and mood.');
      return;
    }

    setIsLoading(true); 

    const BASE_URL = 'http://192.168.135.201:5000'; 

    fetch(`${BASE_URL}/generate-music`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        mood: newMood,
        topic: newTopic,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        Alert.alert('Success', 'Music generation started!');
        navigation.navigate('Music', { mood: newMood, topic: newTopic });
      })
      .catch((error) => {
        Alert.alert('Error', 'Failed to generate music. Please try again.');
        console.error('Music generation error:', error);
      })
      .finally(() => {
        setIsLoading(false); // Stop loading
      });
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Survey</Text>
      <Text style={styles.subtitle}>
        Previous Topic: {topic} | Previous Mood: {mood}
      </Text>

      {/* Question 1: Did you like the song? */}
      <View style={styles.inputContainer}>
        <Text style={styles.question}>1. Did you like the song?</Text>
        <View style={styles.choiceContainer}>
          <TouchableOpacity
            style={[
              styles.choiceButton,
              likeSong === 'Yes' && styles.selectedChoice,
            ]}
            onPress={() => setLikeSong('Yes')}
          >
            <Text style={styles.choiceText}>Yes</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[
              styles.choiceButton,
              likeSong === 'No' && styles.selectedChoice,
            ]}
            onPress={() => setLikeSong('No')}
          >
            <Text style={styles.choiceText}>No</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Dummy Question 2: What do you think about the topic? */}
      <View style={styles.inputContainer}>
        <Text style={styles.question}>2. What do you think about the topic?</Text>
        <TextInput
          style={styles.input}
          placeholder="Your thoughts on the topic"
          value={dummyAnswer2}
          onChangeText={setDummyAnswer2}
        />
      </View>

      {/* Dummy Question 3: How did you feel about the song? */}
      <View style={styles.inputContainer}>
        <Text style={styles.question}>3. How did you feel about the song?</Text>
        <TextInput
          style={styles.input}
          placeholder="Your feelings about the song"
          value={dummyAnswer3}
          onChangeText={setDummyAnswer3}
        />
      </View>

      {/* Functional Question: New Topic */}
      <View style={styles.inputContainer}>
        <Text style={styles.question}>
          4. What can you relate to from the previous topic? (New Topic)
        </Text>
        <TextInput
          style={styles.input}
          placeholder="Enter your new topic"
          value={newTopic}
          onChangeText={setNewTopic}
        />
      </View>

      {/* Functional Question: New Mood */}
      <View style={styles.inputContainer}>
        <Text style={styles.question}>
          5. What should be the mood of the new song? (New Mood)
        </Text>
        <TextInput
          style={styles.input}
          placeholder="Enter the mood for the new song"
          value={newMood}
          onChangeText={setNewMood}
        />
      </View>

      {/* Generate Music Button */}
      <TouchableOpacity
        style={styles.generateButton}
        onPress={handleGenerateMusic}
        disabled={isLoading} // Disable button while loading
      >
        <Text style={styles.generateButtonText}>
          {isLoading ? 'Generating...' : 'Generate'}
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
    color: '#333',
  },
  subtitle: {
    fontSize: 18,
    marginBottom: 20,
    color: '#555',
  },
  inputContainer: {
    marginBottom: 20,
  },
  question: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 10,
    color: '#333',
  },
  choiceContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  choiceButton: {
    flex: 1,
    padding: 15,
    marginHorizontal: 5,
    backgroundColor: '#ddd',
    borderRadius: 10,
    alignItems: 'center',
  },
  selectedChoice: {
    backgroundColor: '#0077b6',
  },
  choiceText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 10,
    backgroundColor: '#fff',
  },
  generateButton: {
    backgroundColor: '#0077b6',
    padding: 15,
    borderRadius: 25,
    alignItems: 'center',
    marginTop: 20,
  },
  generateButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});
