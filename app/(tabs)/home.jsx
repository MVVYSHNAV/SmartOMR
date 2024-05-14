import { View, Text, FlatList, Image } from 'react-native'
import React from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import { images } from '../../constants'

const Home = () => {
  return (
    <>
    <SafeAreaView className="bg-[#764CEE]"> 
      
      <View className="my-1 px-2 space-y-6">
        <View className="justify-between items-start flex-row mb-6">
            <View>
              <Text className="font-psemibold mt-10  px-5 text-sm text-gray-100 ">
                Welcome to
              </Text >
              <Text  className="font-pbold text-lg px-5 text-white" > 
               SmartOMR
              </Text>
            </View>
                  <View className="mt-1.5">
                      <Image
                        source={images.logo}
                        className="w-20 h-10"
                        resizeMode='contain'
                      />
                    </View>
        </View>
      </View>
    </SafeAreaView>
    <View className="justify-between  mb-6" >
      <Text className="text-sm font-psemi mt-5 px-4 text-gray-400 text-center">
       "Excellence is not a skill. It is an attitude."
      </Text>
      <Text className="text-2xl font-psemibold mt-10 px-10 text-gray-600 ">
        Recent
      </Text>
      <FlatList>
        data={[{id:1}, {id:2}, {id:3}]}
        keyExtractor{({item}) => item.$id}
        renderItem={({ item }) => (
          <Text className="text-3xl text-black">
              {item.id}
          </Text>
        )}
      </FlatList>
    </View>
    
    </>
  )
}

export default Home