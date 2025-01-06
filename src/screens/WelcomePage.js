import React from 'react';
import { View, Text, Image } from 'react-native';
import CustomButton from '../components/CustomButton';
import { globalStyles } from '../styles/global';

export default function WelcomePage({ navigation }) {
  const handleStart = () => {
    navigation.navigate('Input'); // Navigate to the InputPage
  };

  return (
    <View style={globalStyles.container}>
      {/* Add the welcome image */}
      <Text style={styles.welcomeText}>Welcome to Music Generator!</Text>
      <Text style={styles.subText}>Create music based on your mood and topic.</Text>
      <Image 
        source={require('../../assets/welcome_img.png')} 
        style={styles.welcomeImage} 
        resizeMode="contain" 
      />

      
      <CustomButton title="Start Generating Music" onPress={handleStart} />
    </View>
  );
}

const styles = {
  welcomeImage: {
    width: '100%',  
    height: 400,    
    marginBottom: 0,
  },
  welcomeText: {
    fontSize: 45,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
    color: '#333', 
  },
  subText: {
    fontSize: 25,
    color: '#666', 
    marginBottom: 0,
    textAlign: 'center',
  },
};
