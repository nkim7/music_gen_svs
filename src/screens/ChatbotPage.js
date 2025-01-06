import React, { useState, useEffect } from "react";
import {
  View,
  TextInput,
  Button,
  Text,
  ScrollView,
  StyleSheet,
  ActivityIndicator,
} from "react-native";
import { useNavigation } from "@react-navigation/native";

export default function ChatbotPage() {
  const [userMessage, setUserMessage] = useState(""); 
  const [chatHistory, setChatHistory] = useState([]);
  const [conversationState, setConversationState] = useState({}); 
  const [loading, setLoading] = useState(false); 

  const navigation = useNavigation();

  
  const BASE_URL = "http://192.168.135.201:5000";

 
  useEffect(() => {
    console.log("DEBUG: Fetching initial message...");
    setLoading(true);
    fetch(`${BASE_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: "",
        conversation_state: {},
        is_restart: true,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("DEBUG: Initial response from server:", data);
        const botResponses = data.responses || ["Welcome to the chatbot!"];
        setConversationState(data.conversation_state || {});
        setChatHistory(botResponses.map((text) => ({ sender: "Bot", text })));
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching initial message:", error);
        setChatHistory([
          {
            sender: "Bot",
            text: "Unable to connect to the chatbot. Please try again later.",
          },
        ]);
        setLoading(false);
      });
  }, []);

  
  const sendMessage = () => {
    if (!userMessage.trim()) return;

   
    setChatHistory((prev) => [...prev, { sender: "You", text: userMessage }]);
    setLoading(true);

    console.log("DEBUG: Sending message to server:", userMessage);
    console.log("DEBUG: Current conversation state:", conversationState);

    fetch(`${BASE_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: userMessage,
        conversation_state: conversationState,
        is_restart: false,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("DEBUG: Server response:", data);

        const botResponses = data.responses || ["Bot didn't respond."];
        setConversationState(data.conversation_state || {}); 
        setChatHistory((prev) => [
          ...prev,
          ...botResponses.map((text) => ({ sender: "Bot", text })),
        ]);
        setLoading(false);

      
        if (data.conversation_state?.stage === "end") {
          navigation.navigate("Music", {
            mood: data.conversation_state.final_mood,
            topic: data.conversation_state.final_topic,
          });
        }
      })
      .catch((error) => {
        console.error("Error sending message:", error);
        setChatHistory((prev) => [
          ...prev,
          {
            sender: "Bot",
            text: "Oops! Something went wrong. Please try again.",
          },
        ]);
        setLoading(false);
      });

    setUserMessage(""); 
  };

  return (
    <View style={styles.container}>
      {/* Chat History */}
      <ScrollView style={styles.chatContainer}>
        {chatHistory.map((msg, index) => (
          <View
            key={index}
            style={
              msg.sender === "You" ? styles.userMessage : styles.botMessage
            }
          >
            <Text style={styles.messageText}>{msg.text}</Text>
          </View>
        ))}
        {loading && (
          <ActivityIndicator size="small" color="#0000ff" style={styles.loader} />
        )}
      </ScrollView>

      {/* Input Field and Send Button */}
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="Type your message here..."
          value={userMessage}
          onChangeText={setUserMessage}
          onSubmitEditing={sendMessage} 
        />
        <Button title="Send" onPress={sendMessage} disabled={loading} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f5f5f5" },
  chatContainer: { flex: 1, padding: 10 },
  userMessage: {
    alignSelf: "flex-end",
    backgroundColor: "#d1e7dd",
    padding: 10,
    marginBottom: 5,
    borderRadius: 10,
    maxWidth: "80%",
  },
  botMessage: {
    alignSelf: "flex-start",
    backgroundColor: "#f8d7da",
    padding: 10,
    marginBottom: 5,
    borderRadius: 10,
    maxWidth: "80%",
  },
  messageText: { fontSize: 16, color: "#333" },
  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    padding: 10,
    backgroundColor: "#fff",
    borderTopWidth: 1,
    borderTopColor: "#ddd",
  },
  input: {
    flex: 1,
    borderColor: "#ddd",
    borderWidth: 1,
    padding: 10,
    borderRadius: 10,
    marginRight: 10,
    backgroundColor: "#fff",
  },
  loader: { marginTop: 10 },
});
