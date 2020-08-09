import React, {Component} from 'react';
import './App.css';
import XTerm, {Terminal} from "react-xterm";
import axios from 'axios';
import "xterm/css/xterm.css";
interface IState {
}
interface IProps {
}
class App extends Component<IProps, IState> {

    constructor(props: IProps, context?: any) {
        super(props, context);
        this.inputRef=React.createRef()
    }
    componentDidMount() {
        runFakeTerminal(this.inputRef.current!!);
    }
    componentWillUnmount() {
        this.inputRef.current?.componentWillUnmount();
    }

    private inputRef: React.RefObject<XTerm>;

    render() {
        return (
            <div className="App">
                <XTerm ref={this.inputRef}
                       addons={['fit', 'fullscreen', 'search']}
                       style={{
                        overflow: 'hidden',
                        position: 'relative',
                        width: '100%',
                        height: '100%'
                       }}/>
            </div>
        );
    }
}

interface StartResposne {
    session_id: string
    text: string
}

function runFakeTerminal(xterm: XTerm) {
    const term: Terminal = xterm.getTerminal();
    var shellprompt = '$ ';
    var curline = '';
    var sessionId: string = '';

    function prompt () {
        curline = '';
        xterm.write('\r\n' + shellprompt);
    }
    xterm.writeln('\u001b[31mWelcome to xterm.js\u001b[0m');
    xterm.writeln('This is a local terminal emulation, without a real terminal in the back-end.');
    xterm.writeln('Type some keys and commands to play around.');
    xterm.writeln('');
    prompt();

    term.on('key', function (key, ev) {
        var printable = (
            !ev!!.altKey && !ev!!.ctrlKey && !ev!!.metaKey
        );

        const printGameBlock = (txt: string[]) => {
            txt.forEach((paragraph, index) => {
                const lines = paragraph.split('<br>').join('\r\n');
                console.log(lines);
                xterm.write(lines);
                if(index != txt.length - 1)
                    xterm.write('\r\n')
            });
        }

        if (ev!!.keyCode == 13) {
            console.log(curline);
            xterm.write('\r\n');
            const cmd = curline.split(' ')
            
            if(sessionId.length > 0){
                axios.post('/game/update', {
                    session_id: sessionId,
                    command: curline
                })
                .then(response => {
                    console.log(response);
                    printGameBlock(response.data.text);
                    prompt();
                })
            }
            else{
                switch(cmd[0]){

                    case 'list':
                    case 'ls':
                        fetch('/game/list')
                            .then(res => res.json())
                            .then(result =>{
                                xterm.write(result.games.join('\r\n'));
                                curline = '';
                                prompt();
                            });
                        break;

                    case 'start':
                        const uname = cmd[1];
                        const secret = cmd[2];
                        const game_id = cmd[3];
                        try{
                            axios.post('/game/start',{
                                user:     uname,
                                password: secret,
                                game:     game_id
                            })
                            .then(response => {
                                console.log(response);
                                sessionId = response.data.session_id;
                                printGameBlock(response.data.text);
                                prompt();
                            });
                        }
                        catch(e) {
                            xterm.write(e);
                            prompt();
                        }
                        break;

                    default:
                        xterm.write(`Unknown command ${cmd[0]}`)
                        prompt();
                        break;
                }
            }
        } else if (ev!!.keyCode == 8) {
            // Do not delete the prompt
            if (curline.length > 0) {
                curline = curline.slice(0, -1);
                xterm.write('\b \b');
            }
        } else if (printable) {
            curline += key;
            xterm.write(key);
        }
    });

    term.on('paste', function (data, ev) {
        xterm.write(data);
    });
}

export default App;
