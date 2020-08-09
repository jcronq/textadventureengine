import React, {useState, useEffect} from 'react';
import {Text, Box} from 'ink';

const GameTerminal = (props) => {
    const [sessionId, setSessionId] = useState();
    const [textArea, setTextArea] = useState([]);

    return (
        <Box color="black" width={4}>
            <Text color="green">Hello World</Text>
        </Box>
    )
}

export default GameTerminal

