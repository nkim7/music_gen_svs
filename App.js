// App.js
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import InputPage from './src/screens/InputPage';
import OutputPage from './src/screens/OutputPage';
import WelcomePage from './src/screens/WelcomePage';
import LoadingPage from './src/screens/LoadingPage';
import ChatbotPage from './src/screens/ChatbotPage';
import SurveyPage from './src/screens/SurveyPage';

const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Input">
        <Stack.Screen name="Input" component={InputPage} />
        <Stack.Screen name="Music" component={OutputPage} />
        <Stack.Screen name="Loading" component={LoadingPage} />
        <Stack.Screen name="Welcome" component={WelcomePage} />
        <Stack.Screen name="Chatbot" component={ChatbotPage} />
        <Stack.Screen name="Survey" component={SurveyPage} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// import React from 'react';
// import ChatbotPage from './src/screens/ChatbotPage';

// export default function App() {
//   return <ChatbotPage />;
// }

