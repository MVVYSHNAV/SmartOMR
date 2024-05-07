import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { Link } from 'expo-router';

export default function App() {
  return (
    <View  className="flex-1 items-center justify-center bg-grey" >
      <Text className="text-3xl font-pblack">SmartOMR </Text>
      <StatusBar style="auto" />
      <Link href="/home" style={{color: 'red'}}>  go to Home </Link>
    </View>
  );
}

