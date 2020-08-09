import React, {useState} from 'react';
import axios from 'axios';
import Terminal from 'terminal-in-react';
import GameTerminalPlugin from './gameTerminalPlugin';
// import bcrypt from 'bcrypt';

const GameTerminal = function(props){
    const [sessionId, setSessionId] = useState();

    const test = ()=>{
        return "Hello World"
    }
    
    const listGames = (print) =>{
        fetch('/game/list')
            .then(res => res.json()
            .then(
                (result) => {
                    print('<code><span style="color: green">'+result.games.join('\n')+'</code></span>');
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
            helpText(["start", "help"], print);
            return;
        }
        if(pass === ''){
            print('Missing argument -s (--secret)');
            helpText(["start", "help"], print);
            return;
        }
        if(game_id === ''){
            print('Missing argument game');
            helpText(["start", "help"], print);
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

    const load = (cmd, print) => {
        print("not implemented")
    }

    const helpText = (cmd, print) => {
        const cmd_target = cmd[0];
        if(cmd_target === "help"){
            const print_text = [
                "Welcome, this is a Text Adventure engine. You're not currently playing a game, as you have likely noticed. When you are in a game, the commands listed belowe will not be work.",
                "Available commands:",
                "  list - list available games",
                "  start - Starts a specific game",
                "  load - load's a currently running game"
            ];
            print(print_text.join('\n'))
        }
        if(cmd_target === "list"){
            print("list (or just ls)" )
            print("  - no arguments")
        }
        if(cmd_target === "start"){
            const help_text = [
                "start -u <username> -s <secret> <game_name>", 
                "  -u (--user) : the username you will save your progress as.",
                "  -s (--secret) : A secret that will allow only you to edit/join your game. DO NOT USE A REAL PASSWORD, I MAKE NO GUARANTEES WITH REGARDS TO SECURITY.",
                "  <game_name> : This is the game you want to start.  Use list to get a 'list' of available opetions",
                " ",
                "  Use this command to start a new game.  If you have a game-in-progress, you will not be able to start a new game. Use 'load' instead to load the running game."
            ]
            print(help_text.join("\n"))
        }
        if(cmd_target === "load"){
            const help_text = [
                "load -u <username> -s <secret> <game_name>", 
                "  -u (--user) : The username you used to start the game",
                "  -s (--secret) : The secret you used to start the game with",
                "  <game_name> : The game you wish to resume.",
                " ",
                "  Use this command resume a game where you left off."
            ]
            print(help_text.join("\n"))
        }
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
            if(cmd.includes("help")){
                helpText(cmd, print)
            }
            switch(cmd[0]) {
                // case 'ls':
                // case 'list':
                //     listGames(print);
                //     break;
                case 'login':
                    print("not implemented yet.")
                    break;
                case 'start':
                    startGame(cmd, print);
                    break;
                case 'load':
                    load(cmd, print);
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
                plugins={[GameTerminalPlugin]}

            />
        </div>
    )
}

                // commandPassThrough={handleCommand}
                // commands={{
                //     list:{
                //         method: (args, print, runCommand) =>{
                //             listGames(print)
                //         }
                //     }
                // }}
                // descriptions={{list: "list available games to play."}}
                // msg={"Try 'help' if you're not sure where to begin."}
export default GameTerminal;

