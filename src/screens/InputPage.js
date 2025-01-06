import React, { useState, useEffect } from 'react';
import { View, TextInput, Text, Alert, Image, StyleSheet, ScrollView, KeyboardAvoidingView, TouchableWithoutFeedback, Keyboard, Platform, TouchableOpacity, Modal } from 'react-native';
import CustomButton from '../components/CustomButton';
import { globalStyles } from '../styles/global';

export default function InputPage({ navigation }) {
  const [mood, setMood] = useState('');
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);  
  const [keyboardHeight, setKeyboardHeight] = useState(0);  
  const [isVisible, setIsVisible] = useState(false); 


  useEffect(() => {
    const keyboardDidShowListener = Keyboard.addListener('keyboardDidShow', (event) => {
      setKeyboardHeight(event.endCoordinates.height); 
    });
    const keyboardDidHideListener = Keyboard.addListener('keyboardDidHide', () => {
      setKeyboardHeight(0); 
    });

    return () => {
      keyboardDidShowListener.remove();
      keyboardDidHideListener.remove();
    };
  }, []);

  const handleSubmit = () => {
   
    if (!mood || !topic) {
      Alert.alert('Error', 'Please fill in both mood and topic');
      return;
    }

    setLoading(true);  

   
    navigation.navigate('Loading'); 

    const BASE_URL = process.env.EXPO_PUBLIC_BACKEND_URL || "http://192.168.135.201:5000";

   
    fetch(`${BASE_URL}/generate-music`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        mood: mood,
        topic: topic,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        setLoading(false);
        console.log('Navigating to Music with:', { mood, topic });
        navigation.navigate('Music', { mood, topic });
      })
      .catch((error) => {
        setLoading(false);
        Alert.alert('Error', 'Failed to start music generation.');
      });
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'position' : undefined}  
      style={styles.container}
    >
      <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        <View style={[styles.scrollViewContent, { paddingBottom: keyboardHeight }]}>
        
          <Text style={styles.title}>Let's Start Creating Music!</Text>

   
          <Text style={styles.instructions}>
            To generate music, we need your mood and a topic. Please fill in both fields below.
          </Text>

          {/* 이미지 */}
          <Image
            source={require('../../assets/input_img.png')}  
            style={styles.image}  
          />

          {/* 감정 입력 필드 */}
          <View style={styles.labelContainer}>
            <Text style={globalStyles.label}>Enter Mood:</Text>

            {/* 아이콘과 팝업 */}
            <TouchableOpacity
              onPressIn={() => setIsVisible(true)} 
              onPressOut={() => setIsVisible(false)} 
            >
              {/* 아이콘을 Image로 표시 */}
              <Image
                source={require('../../assets/info_icon.png')} 
                style={styles.infoIcon}  
              />
            </TouchableOpacity>
          </View>

          <TextInput
            style={[globalStyles.input, { fontSize: 20 }]}
            placeholder="Enter your mood"
            placeholderTextColor="#A0A0A0"
            value={mood}
            onChangeText={setMood}
            editable={!loading}
          />

          {/* 주제 입력 필드 */}
          <Text style={globalStyles.label}>Enter Topic:</Text>
          <TextInput
            style={[globalStyles.input, { fontSize: 20 }]}
            placeholder="Enter the topic"
            placeholderTextColor="#A0A0A0"
            value={topic}
            onChangeText={setTopic}
            editable={!loading}
          />

          {/* 제출 버튼 */}
          <CustomButton
            title={loading ? 'Submitting...' : 'Submit'}
            onPress={handleSubmit}
            disabled={loading}
          />

       
          {keyboardHeight > 0 && <View style={{ height: keyboardHeight * 0.4 }} />}  
      

      
          <Modal
            transparent={true}
            visible={isVisible}
            onRequestClose={() => setIsVisible(false)}
          >
            <View style={styles.modalOverlay}>
              <View style={styles.modalContent}>
                <Text style={styles.popup}>You can choose any mood or topic you like! 🌈 {'\n'} It could be a word, a sentence, or even an explanation. {'\n'} Feel free to get creative! {'\n'} (Maybe it can also make a song about topology)🤪</Text>
              </View>
            </View>
          </Modal>

        </View>
      </TouchableWithoutFeedback>
    </KeyboardAvoidingView>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',  
  },
  scrollViewContent: {
    flexGrow: 1,
    justifyContent: 'center',  
    paddingHorizontal: 20,  
    paddingVertical: 20
  },
  image: {
    width: '100%',
    height: 300,
    resizeMode: 'contain',
    marginBottom: 0,
  },
  title: {
    fontSize: 35,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 5,
    marginTop: 20,
    color: '#333',
  },
  instructions: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 20,
    color: '#333',
  },
  popup: {
    fontSize: 25,
    textAlign: 'center',
    color: '#333',
    fontWeight: '450'
  },
  labelContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  infoIcon: {
    width: 40,  // 아이콘 너비
    height: 40,  // 아이콘 높이
    marginLeft: 10,  // 텍스트와의 간격
    marginBottom: 8,
  },
  modalOverlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',  // 반투명 배경
  },
  modalContent: {
    width: 800,
    padding: 20,
    backgroundColor: 'white',
    borderRadius: 10,
  },
});
