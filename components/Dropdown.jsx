import { View, Text } from 'react-native'
import React from 'react'
import { useState } from 'react';
import {  SelectList } from 'react-native-dropdown-select-list';

const DropDown = () => {
    const [selected, setSelected] = useState("");

    const data = [
      {key: '1', value: 'Tutor'},
      {key: '2', valjue: 'Student'},
    ];
  
  return (
    <View>
      <SelectList data={data} setSelected={setSelected}/>
    </View>
  )
}

export default DropDown