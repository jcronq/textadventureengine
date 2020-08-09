import React, {Component} from 'react';
import './App.css';
import XTerm, {Terminal} from 'react-xterm';
import 'xterm/css/xterm.css';

const GameTerminal = (props) => {

    const inputRef = React.createRef();

    const runFakeTerminal = (xterm) => {
        const term = xterm.getTerminal();
        var shellprompt = '$ ';

        const prompt = () =>{
            xterm.write('\r\n' + shellprompt);
        }
        xterm.writeln('Welcome to xterm.js');
        xterm.writeln('This is local terminal emulation, without a real terminal in the back-end');
        xterm.writeln('Type some keys and commands to play around.');
        xterm.writeln('');
        prompt();

        term.on('key', (key, ev) => {
            var printable = (
                true
                // !ev!!.altKey && !ev!!.ctrlKey && !ev!!.metaKey
            );

            if(ev.keyCode == 13 ) {
                prompt();
            } else if (printable) {
                xterm.write(key);
            }
        });

        xterm.on('paste', function(data, ev){
            xterm.write(data);
        });
    }

    return(
        <XTerm ref={inputRef}
            addons={['fit', 'fullscreen', 'search']}
            style={{
                overflow: 'hidden',
                position: 'relative',
                width: '100%',
                height: '100%'
            }}/>
    )
}

export default GameTerminal;

