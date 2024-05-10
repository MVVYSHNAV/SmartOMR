import React, { useState } from 'react';
import { View, Text, ScrollView, Image, Dimensions } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { images } from '../../constants';
import Formfield from '../../components/Formfield'
import CustomButton from '../../components/custbtn'
import { Link } from 'expo-router'

const SignIn = () => {
  const [form, setForm] = useState({
    email: '',
    password: ''
  })

  const [isSubmitting, setIsSubmitting] = useState(false)

  const submit = () => {

  }

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#7c3aed' }}>
      <ScrollView>
        <View className="w-full flex justify-center min-h-[85vh] px-4 my-6" style={{
            minHeight: Dimensions.get("window").height - 100,
          alignItems: "center" }} >
          <Image
            source={images.logo}
            resizeMode="contain"
            className="w-[500px] h-[80px]"
          />

          <Text className="text-2xl font-semibold text-white mt-10 font-psemibold">
            Log in to SmartOMR
          </Text>

          <Formfield
            title="Email"
            value={form.email}
            handleChangeText={(e) => setForm({ ...form, email: e })}
            otherStyles="mt-7"
            keyboardType="email-address"
          />

          <Formfield
            title="Password"
            value={form.password}
            handleChangeText={(e) => setForm({ ...form, password: e })}
            otherStyles="mt-7"
          />
          <CustomButton 
          title='Sign In'
          handlePress={submit}
          containerStyles="mt-7"
          isLoading={isSubmitting}
          />

          <View className='justify-center pt-5 flex-row gap-2'>
            <Text className='text-lg text-gray-100 font-pregular'>
              Don't have account?
            </Text>
            <Link href="/sign-up" className='text-lg font-psemibold text-white'> Sign Up</Link>
          </View>
          </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default SignIn;
