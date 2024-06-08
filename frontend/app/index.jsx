
import { Image, ScrollView, Text, View,  } from 'react-native';
import { Redirect, router} from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { images } from '../constants';
import CustomButton from '../components/custbtn';
import "expo-dev-client";

export default function App() {
  
  return (
    <SafeAreaView className="bg-[#7c3aed] h-full">
      <ScrollView contentContainerStyle={{ height: '100%'}}>
        <View className="w-full justify-center items-center h-full top-[150px]">
            <Image
              source = {images.cards}
              className="max-w-full w-full h-full"
              resizeMode="contain"
            />
            <View className="relative mt-5 bottom-[350px]">
              <Text className="text-3xl text-white font-bold text-center">
                  Scan for the Score  get the  Result
              </Text>
              <Text className="text-gray-100 text-sm font-pregular text-grey-100 mt-7 text-center">
              Targeted at educational institutions, teachers, and students, 
              the app offers a user-friendly interface that simplifies the 
              task of administering tests and processing results.
              </Text>

              <CustomButton
                  title="Continue with Email"
                  handlePress={() => router.push('/signin') }
                  contentContainerStyle="w-full mt-7"
              />
            </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

