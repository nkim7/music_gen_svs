// src/styles/global.js
import { StyleSheet } from 'react-native';
import colors from './colors';

export const globalStyles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: colors.white,  
  },
  label: {
    fontSize: 25,
    color: colors.textGray,  
    marginBottom: 10,
    fontWeight: '600',
  },
  input: {
    height: 50,
    borderColor: colors.borderGray,  
    borderWidth: 1,
    borderRadius: 20,  
    paddingHorizontal: 12,
    color: colors.black,
    backgroundColor: colors.lightGray,  
    marginBottom: 20,
  },
  button: {
    backgroundColor: colors.jade,
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginTop: 10,
  },
  buttonText: {
    color: colors.white,
    fontSize: 18,
    fontWeight: 'bold',
  },
});
