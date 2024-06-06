import React, { useState } from 'react';
import { View, TouchableOpacity, Text } from 'react-native';
import { RNCamera } from 'react-native-camera';

const CameraScreen = () => {
  const [hasPermission, setHasPermission] = useState(null);
  const [type, setType] = useState(RNCamera.Constants.Type.back);

  const requestPermission = async () => {
    const permission = await RNCamera.requestPermissions();
    setHasPermission(permission === 'granted');
  };

  const takePicture = async () => {
    if (hasPermission) {
      const data = await camera.takePictureAsync();
      processImage(data.uri);
    }
  };

  return (
    <View>
      <RNCamera
        ref={(ref) => {
          camera = ref;
        }}
        style={{ flex: 1 }}
        type={type}
        flashMode={RNCamera.Constants.FlashMode.auto}
        permissionDialogTitle={'Permission to use camera'}
        permissionDialogMessage={'We need permission to use your camera'}>
        <View style={{ flex: 1, justifyContent: 'flex-end', alignItems: 'center' }}>
          <TouchableOpacity onPress={takePicture} style={{ flex: 0, backgroundColor: '#fff', borderRadius: 5, padding: 15, paddingHorizontal: 20, alignSelf: 'center', margin: 20 }}>
            <Text style={{ fontSize: 14 }}>Take Picture</Text>
          </TouchableOpacity>
        </View>
      </RNCamera>
    </View>
  );
};

export default CameraScreen;

// import { CameraView, useCameraPermissions } from 'expo-camera';
// import { useState } from 'react';
// import { Button, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
// import { ImagePicker } from 'react-native-image-picker';

// export default function App() {
//   const [facing, setFacing] = useState('back');
//   const [permission, requestPermission] = useCameraPermissions();
//   const [image, setImage] = useState(null);

//   if (!permission) {
//     // Camera permissions are still loading.
//     return <View />;
//   }

//   if (!permission.granted) {
//     // Camera permissions are not granted yet.
//     return (
//       <View style={styles.container}>
//         <Text style={{ textAlign: 'center' }}>We need your permission to show the camera</Text>
//         <Button onPress={requestPermission} title="grant permission" />
//       </View>
//     );
//   }

//   function toggleCameraFacing() {
//     setFacing(current => (current === 'back' ? 'front' : 'back'));
//   }

//   const selectImage = async () => {
//     const result = await ImagePicker.launchImageLibrary({
//       mediaType: 'photo',
//       quality: 0.5,
//     });

//     if (!result.didCancel) {
//       setImage(result.assets.uri);
//     }
//   };

//   return (
//     <View style={styles.container}>
//       <CameraView style={styles.camera} facing={facing}>
//         <View style={styles.buttonContainer}>
//           <TouchableOpacity style={styles.button} onPress={toggleCameraFacing}>
//             <Text style={styles.text}>Flip Camera</Text>
//           </TouchableOpacity>
//           <TouchableOpacity style={styles.button} onPress={selectImage}>
//             <Text style={styles.text}>Select Image</Text>
//           </TouchableOpacity>
//           {image && (
//             <View>
//               <Text style={styles.text}>Selected Image:</Text>
//               <Text style={styles.text}>{image}</Text>
//             </View>
//           )}
//         </View>
//       </CameraView>
//     </View>
//   );
// }

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     justifyContent: 'center',
//   },
//   camera: {
//     flex: 1,
//   },
//   buttonContainer: {
//     flex: 1,
//     flexDirection: 'row',
//     backgroundColor: 'transparent',
//     margin: 64,
//   },
//   button: {
//     flex: 1,
//     alignSelf: 'flex-end',
//     alignItems: 'center',
//     margin: 16,
//   },
//   text: {
//     fontSize: 24,
//     fontWeight: 'bold',
//     color: 'white',
//   },
// });