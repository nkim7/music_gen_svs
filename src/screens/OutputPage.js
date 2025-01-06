import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Audio } from 'expo-av';
import { globalStyles } from '../styles/global';
import lyricsData from '../../gen/demo_outputs/final_lyrics_with_syllables.json'; 


export default function OutputPage({ route, navigation }) {
  const { mood, topic } = route.params;
  const [sound, setSound] = useState();
  const [isPlaying, setIsPlaying] = useState(false);
  const [position, setPosition] = useState(0);
  const [duration, setDuration] = useState(0);

  async function playSound() {
    const { sound } = await Audio.Sound.createAsync(
      require('../../gen/final_music/final_music.wav') 
      
    );
    setSound(sound);


    
    sound.setOnPlaybackStatusUpdate((status) => {
      if (status.isLoaded) {
        setPosition(status.positionMillis);
        setDuration(status.durationMillis);

        if (status.didJustFinish) {
          setIsPlaying(false);
        }
      }
    });

    await sound.playAsync();
    setIsPlaying(true);
  }

  async function stopSound() {
    if (sound) {
      await sound.stopAsync();
      setIsPlaying(false);
    }
  }

  useEffect(() => {
    return sound ? () => sound.unloadAsync() : undefined;
  }, [sound]);

  const handleButtonPress = () => {
    if (isPlaying) {
      stopSound();
    } else {
      playSound();
    }
  };

  const formatTime = (millis) => {
    const minutes = Math.floor(millis / 60000);
    const seconds = ((millis % 60000) / 1000).toFixed(0);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  };

  return (
    <View style={globalStyles.container}>
      <Text style={styles.title}>Your Music is Ready!</Text>

  
      <View style={styles.controlsContainer}>
        <TouchableOpacity style={styles.button} onPress={handleButtonPress}>
          <Text style={styles.buttonText}>{isPlaying ? 'Stop Music' : 'Play Music'}</Text>
        </TouchableOpacity>

        <View style={styles.timeContainer}>
          <Text style={styles.timeText}>{formatTime(position)}</Text>
          <Text style={styles.timeText}>{formatTime(duration)}</Text>
        </View>
      </View>

 
      <View style={styles.box}>
        <Text style={styles.subtitle}>Mood: {mood}</Text>
        <Text style={styles.subtitle}>Topic: {topic}</Text>

        <View style={styles.lyricsContainer}>
          {lyricsData.lyrics.map((line, index) => (
            <Text key={index} style={styles.lyricsText}>{line}</Text>
          ))}
        </View>
      </View>

      {/* Buttons */}
      <TouchableOpacity
        style={styles.newSongButton}
        onPress={() => navigation.navigate('Chatbot', { mood, topic })}>
        <Text style={styles.newSongButtonText}>Chatbot Mode</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.surveyButton}
        onPress={() => navigation.navigate('Survey', { mood, topic })}>
        <Text style={styles.surveyButtonText}>Survey Mode</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={[styles.homeButton, styles.homeButtonPosition]}
        onPress={() => navigation.navigate('Welcome')}>
        <Text style={styles.homeButtonText}>Home</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  box: {
    borderWidth: 2,
    borderColor: '#f4f1d4',
    backgroundColor: '#f4f1d4',
    borderRadius: 10,
    padding: 20,
    marginBottom: 30,
  },
  lyricsText: {
    fontSize: 18,
    color: '#333',
    textAlign: 'center',
    marginTop: 5,
  },
  subtitle: {
    fontSize: 20,
    color: '#333',
    textAlign: 'center',
    marginTop: 5,
    fontWeight: '600',
  },
  lyricsContainer: {
    paddingVertical: 10,
  },
  controlsContainer: {
    paddingTop: 20,
    alignItems: 'center',
    marginBottom: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 5,
    marginTop: 20,
    color: '#333',
  },
  button: {
    backgroundColor: '#00A86B',
    padding: 15,
    borderRadius: 25,
    alignItems: 'center',
    marginTop: 0,
  },
  buttonText: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
  timeContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '90%',
  },
  timeText: {
    color: '#333',
    fontSize: 14,
  },
  newSongButton: {
    backgroundColor: '#0077b6',
    padding: 15,
    borderRadius: 25,
    alignItems: 'center',
    marginTop: 20,
  },
  newSongButtonText: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
  surveyButton: {
    backgroundColor: '#f4a261',
    padding: 15,
    borderRadius: 25,
    alignItems: 'center',
    marginTop: 20,
  },
  surveyButtonText: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
  homeButton: {
    backgroundColor: '#61a5aa',
    padding: 15,
    borderRadius: 25,
    alignItems: 'center',
    marginTop: 20,
  },
  homeButtonPosition: {
    position: 'absolute',
    bottom: 20,
    left: 20,
  },
  homeButtonText: {
    color: '#FFF',
    fontSize: 18,
    fontWeight: 'bold',
  },
});
