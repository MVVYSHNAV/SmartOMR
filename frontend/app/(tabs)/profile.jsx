import { View, Text, Image, TouchableOpacity, TextInput } from 'react-native'
import React, { useState } from 'react'
import { SafeAreaView } from 'react-native-safe-area-context'
import { images } from '../../constants'


const Profile = () => {
  const [name, setName] = useState('John Doe')
  const [email, setEmail] = useState('johndoe@example.com')
  const [editing, setEditing] = useState(false)

  const handleEdit = () => {
    setEditing(true)
  }

  const handleSave = () => {
    setEditing(false)
  }

  const handleNameChange = (text) => {
    setName(text)
  }

  const handleEmailChange = (text) => {
    setEmail(text)
  }

  return (
    <>
    <SafeAreaView className="bg-[#764CEE]">
      <View className="my-3 px-2 space-y-1">
      <View className=" items-end">
                      <Image
                        source={images.logo}
                        className="w-20 h-10"
                        resizeMode='contain'
                      />
                    </View> 
      <View className="justify-center items-start flex-row mb-6">
        <Text className="text-white font-psemibold text-center text-lg px-10">Profile</Text>
  
          </View>
      </View>
    </SafeAreaView>

    <View className="justify-center items-start flex-row mb-6">
          <Text className="text-white font-psemibold text-center text-lg px-10">Profile</Text>
          {editing ? (
            <TouchableOpacity onPress={handleSave}>
              <Text className="text-black font-psemibold text-center text-lg px-10">Save</Text>
            </TouchableOpacity>
          ) : (
            <TouchableOpacity onPress={handleEdit}>
              <Text className="text-black font-psemibold text-center text-lg px-10">Edit</Text>
            </TouchableOpacity>
          )}
        </View>
        <View className="px-4 py-2">
          <Text className="text-black font-psemibold text-lg">Name:</Text>
          {editing ? (
            <TextInput
              value={name}
              onChangeText={handleNameChange}
              className="bg-white px-2 py-1 rounded"
              placeholder="Enter name"
            />
          ) : (
            <Text className="text-black font-psemibold text-lg">{name}</Text>
          )}
        </View>
        <View className="px-4 py-2">
          <Text className="text-black font-psemibold text-lg">Email:</Text>
          {editing ? (
            <TextInput
              value={email}
              onChangeText={handleEmailChange}
              className="bg-white px-2 py-1 rounded"
              placeholder="Enter email"
            />
          ) : (
            <Text className="text-black font-psemibold text-lg">{email}</Text>
          )}
        </View>
    </>
    
  )
}

export default Profile