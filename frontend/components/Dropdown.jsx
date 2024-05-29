import { View, Text } from 'react-native'
import React, { useState } from 'react';
import { SelectList } from 'react-native-dropdown-select-list';

const DropDown = ({title}) => {
    const [selected, setSelected] = useState("");

    const data = [
      {key: '1', value: 'Tutor'},
      {key: '2', value: 'Student'},
    ];
  
  return (
    <View  className= {'space-y-3 justify-center mt-5 ${otherStyles}'}>
      <Text  className='text-base  text-gray-100 font-pmedium px-2' > {title}</Text>
      <View className='right-0 z-10 mt-2 w-80 origin-top-right rounded-md shadow-lg ring-1 ring-secondary ring-opacity-5 focus:outline-none'>
      
        <SelectList 
          setSelected={(selected) => setSelected(selected)} 
          data={data} 
          onSelect={(selected) => setSelected(selected)} 
          dropdownStyles={{ backgroundColor: 'black' }}
          dropdownItemStyles={{ backgroundColor: 'black' }}
          dropdownTextStyles={{ color: 'white' }}
          boxStyles={{ backgroundColor: 'black', borderColor: 'white' }}
          inputStyles={{ color: 'white', width: 60}}
        />
      </View>
    </View>
  )
}

export default DropDown