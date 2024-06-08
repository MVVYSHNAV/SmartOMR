import React, { useState, useEffect } from 'react';
import { View, TouchableOpacity, Text, StyleSheet } from 'react-native';
import { RNCamera } from 'react-native-camera';
import * as ImagePicker from 'react-native-image-picker';

const CameraScreen = () => {
  const [hasPermission, setHasPermission] = useState(null);
  const [type, setType] = useState(RNCamera.Constants.Type.back);
  const [image, setImage] = useState(null);

  useEffect(() => {
    (async () => {
      const { status } = await RNCamera.requestPermissions();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const takePicture = async () => {
    if (camera && hasPermission) {
      const data = await camera.takePictureAsync();
      processImage(data.uri);
    }
  };

  const toggleCameraType = () => {
    setType(
      type === RNCamera.Constants.Type.back
        ? RNCamera.Constants.Type.front
        : RNCamera.Constants.Type.back
    );
  };

  const selectImage = () => {
    ImagePicker.launchImageLibrary({ mediaType: 'photo', quality: 0.5 }, (response) => {
      if (response.assets) {
        setImage(response.assets[0].uri);
      }
    });
  };

  if (hasPermission === null) {
    return <View />;
  }

  if (hasPermission === false) {
    return (
      <View style={styles.container}>
        <Text style={styles.text}>We need your permission to show the camera</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <RNCamera
        ref={(ref) => {
          camera = ref;
        }}
        style={styles.camera}
        type={type}
        flashMode={RNCamera.Constants.FlashMode.auto}
        permissionDialogTitle={'Permission to use camera'}
        permissionDialogMessage={'We need your permission to use your camera'}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.button} onPress={toggleCameraType}>
            <Text style={styles.text}>Flip Camera</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button} onPress={takePicture}>
            <Text style={styles.text}>Take Picture</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button} onPress={selectImage}>
            <Text style={styles.text}>Select Image</Text>
          </TouchableOpacity>
        </View>
      </RNCamera>
      {image && (
        <View>
          <Text style={styles.text}>Selected Image:</Text>
          <Text style={styles.text}>{image}</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  camera: {
    flex: 1,
  },
  buttonContainer: {
    flex: 1,
    flexDirection: 'row',
    backgroundColor: 'transparent',
    margin: 64,
  },
  button: {
    flex: 1,
    alignSelf: 'flex-end',
    alignItems: 'center',
    margin: 16,
  },
  text: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
});

export default CameraScreen;
