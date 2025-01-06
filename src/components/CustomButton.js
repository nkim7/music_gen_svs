// src/components/CustomButton.js
import React from 'react';
import { TouchableOpacity, Text, StyleSheet } from 'react-native';
import colors from '../styles/colors';

export default function CustomButton({ title, onPress }) {
  return (
    <TouchableOpacity style={styles.button} onPress={onPress}>
      <Text style={styles.buttonText}>{title}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: colors.jade,
    padding: 15,
    borderRadius: 25,
    alignItems: 'center',
    marginTop: 0,
  },
  buttonText: {
    color: colors.white,
    fontSize: 25,
    fontWeight: 'bold',
  },
});
