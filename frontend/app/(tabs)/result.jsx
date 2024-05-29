import { View, Text, Image } from 'react-native'
import React from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import { images } from '../../constants'


const Result = () => {
  const [markedAnswers, setMarkedAnswers] = useState([]);

  const evaluateOMRSheet = async (imagePath) => {
    try {
      const result = await python.execute('omr_sheet_evaluator.py', 'evaluate_omr_sheet', imagePath);
      setMarkedAnswers(result);
    } catch (error) {
      console.error(error);
    }
  };
  return (
   <> <SafeAreaView className="bg-[#764CEE]">
      <View className="my-3 px-2 space-y-1">
      <View className="items-end">
                      <Image
                        source={images.logo}
                        className="w-20 h-10"
                        resizeMode='contain'
                      />
                    </View> 
      <View className="justify-center items-start flex-row mb-6">
        <Text className="text-white font-psemibold text-center text-lg px-10"> Result </Text>  
            </View>
      </View>
    </SafeAreaView>

    <View>
      <Text>Marked Answers:</Text>
      {markedAnswers.map((answer, index) => (
        <Text key={index}>{`Answer ${index + 1}: (${answer.x}, ${answer.y})`}</Text>
      ))}
    </View>
    </>
  )
}

export default Result