import { View, Text, FlatList } from 'react-native'
import React from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'

const result = () => {
  return (
      <SafeAreaView>
        <FlatList>
          <Text  className="text-white px-4" >
            Result
          </Text>
        </FlatList>
      </SafeAreaView>
  )
}

export default result