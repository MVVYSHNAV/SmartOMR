import React, { useState } from 'react';
import { View, Text, ScrollView, Image, Dimensions } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Link } from 'expo-router';
import axios from 'axios';
import { images } from "../../constants";
import Formfield from '../../components/Formfield';
import CustomButton from '../../components/custbtn';

const BASE_URL = process.env.EXPO_PUBLIC_URL;

const SignUp = () => {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: ''
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const submit = async () => {
    if (!BASE_URL) {
      setErrorMessage("Server URL is not set.");
      return;
    }

    setIsSubmitting(true);
    setErrorMessage("We're experiencing technical issues. Please try again later");

    try {
      console.log("Submitting to:", BASE_URL);
      console.log("Form data:", form);

      const response = await axios.post(`${BASE_URL}/signup`, {
        username: form.username,
        email: form.email,
        password: form.password,
      });

      const data = response.data;
      console.log(data);

      if (data.success) {
        console.log("Sign up successful");
        // Handle successful sign-up, perhaps navigate to another screen
      } else {
        setErrorMessage(data.error || "Sign up failed");
        console.log("Sign up failed:", data.message);
      }
    } catch (error) {
      if (error.response) {
        console.log("Error response:", error.response.data);
        setErrorMessage(error.response.data.message || "An error occurred. Please try again.");
      } else if (error.request) {
        console.log("No response received:", error.request);
        setErrorMessage("No response from server. Please try again later.");
      } else {
        console.log("Error setting up request:", error.message);
        setErrorMessage("An error occurred. Please try again.");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

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
            Create an Account
          </Text>

          <Formfield
            title="Username"
            value={form.username}
            handleChangeText={(e) => setForm({ ...form, username: e })}
            otherStyles="mt-7"
          />

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
          title='Sign Up'
          handlePress={submit}
          containerStyles="mt-7"
          isLoading={isSubmitting}
          />

          <View className='justify-center pt-5 flex-row gap-2'>
            <Text className='text-lg text-gray-100 font-pregular'>
              Already have an account?
            </Text>
            <Link href="/signin" className='text-lg font-psemibold text-white'> Sign In</Link>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default SignUp;