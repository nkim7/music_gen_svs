import React, { useState, useEffect } from 'react';
import { View, Text, ActivityIndicator, StyleSheet, Image } from 'react-native';


const images = [
  require('../../assets/loading_image_5.png'),
  require('../../assets/loading_image_1.png'),
  require('../../assets/loading_image_2.png'),
  require('../../assets/loading_image_3.png'),
  require('../../assets/loading_image_4.png'),

];

export default function LoadingPage() {
  const [currentImageIndex, setCurrentImageIndex] = useState(0); // 현재 이미지 인덱스 저장

  useEffect(() => {
    const intervalId = setInterval(() => {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);  // 10초마다 이미지 변경
    }, 10000); // 10000ms = 10초

    
    return () => clearInterval(intervalId);
  }, []);

  return (
    <View style={styles.container}>
        <ActivityIndicator size="large" color="#0000ff" style={styles.activityIndicator} />
      <Image 
        source={images[currentImageIndex]} 
        style={styles.loadingImage} 
      />
      
    
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
  loadingImage: {
    width: 1066, 
    height: 600, 
    marginBottom: 10, // 로딩 인디케이터와의 간격
  },
  activityIndicator: {
    marginBottom: 0, 
  },
  loadingText: {
    marginTop: 20,
    fontSize: 30,
    color: '#333',
  },
  
});
