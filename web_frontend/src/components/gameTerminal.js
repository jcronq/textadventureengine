import React, {useState} from 'react';
import axios from 'axios';
import Terminal from 'terminal-in-react';
// import bcrypt from 'bcrypt';

const GameTerminal = function(props){
    const [sessionId, setSessionId] = useState();

    const test = ()=>{
        return "Hello World"
    }
    
    const listGames = (print) =>{
        fetch('http://127.0.0.1:8000/game/list')
            .then(res => res.json()
            .then(
                (result) => {
                    print(result.games.join('\n'));
                }    
            )
        )
    }

    const printGameBlock = (txt, print) => {
        for(var paragraph of txt){
            // const lines = paragraph.split('<br>');
            // for(var line of lines){
            //     print(line)
            // }
            const lines = paragraph.split('<br>').join('\n');
            console.log(lines);
            print(lines);
        }
    }

    const startGame = (cmd, print) => {
        cmd.shift();
        var user_id = "";
        var game_id = "";
        var pass = "";

        while(cmd.length > 0){
            const argId = cmd.shift();
            switch(argId){
                case '-u':
                case '--user':
                    user_id = cmd.shift();
                    break;
                case '-s':
                case '--secret':
                    pass = cmd.shift();
                    break;
                default:
                    if(game_id === ''){
                        game_id = argId;
                    }
                    else{
                        print(`Unkown argument ${argId}.`);
                        return;
                    }
            }
        }

        if(user_id === ''){
            print('Missing -u (--user) argument');
            return;
        }
        if(pass === ''){
            print('Missing argument -s (--secret)');
            return;
        }
        if(game_id === ''){
            print('Missing argument game');
            return;
        }

        // bcrypt.hash(pass, 10, (err, hash) => {
        //     if(err){
        //         console.error(err);
        //         return;
        //     }
        axios.post('/game/start', {
            user: user_id,
            password: pass,
            game: game_id
        })
        .then(response => {
            console.log(response);
            setSessionId(response.data.session_id);
            printGameBlock(response.data.text, print);
        });
    }

    const handleCommand = (cmd, print) => {
        if(sessionId){
            axios.post('/game/update', {
                session_id: sessionId,
                command: cmd.join(" ")
            })
            .then(response=>{
                console.log(response);
                printGameBlock(response.data.text, print);
            })
        }
        else{
            switch(cmd[0]) {
                case 'ls':
                case 'list':
                    listGames(print);
                    break;
                case 'start':
                    startGame(cmd, print);
                    break;
                default:
                    print(`Unknown command ${cmd}.`)
            }    
        }
    }
    return (
        <div
            style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                height: "100vh"
            }}
        >
            <Terminal
                color='green'
                backgroundColor='black'
                barColor='black'
                style={{ fontWeight: "bold", fontSize: "1em" }}
                commandPassThrough={handleCommand}
            />
        </div>
    )
}

export default GameTerminal;

