import PluginBase from 'terminal-in-react/lib/js/components/Plugin';
import axios from 'axios';

class GameTerminalPlugin extends PluginBase {
    static displayName = "GameTerminalPlugin";
    static version = "1.0.0";

    constructor(api, config){
        super(api, config);
        
        this.session_id = null;
        this.api.printLine("Intro line");
    }

    commands = {
        'list': this.list(),
        'ls': this.list(),
        // 'start': this.startGame(),
    }

    list(){
        return {
            method: (args) => {
                console.log(args);
                this.listGames()
            }
        }
    }

    descriptions = {
        'list': 'List all the available games.',
        'start': 'Start playing a game'
    }

    listGames(){
        console.log('listGames');
        fetch('/game/list')
            .then(res => res.json())
            .then((result) => {
                this.api.printLine('Ok prune stuff and more stuff')
                this.api.printLine(result.games.join('\n'))
            })
    }

    startGame(cmd, print){
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
            // helpText(["start", "help"], print);
            return;
        }
        if(pass === ''){
            print('Missing argument -s (--secret)');
            // helpText(["start", "help"], print);
            return;
        }
        if(game_id === ''){
            print('Missing argument game');
            // helpText(["start", "help"], print);
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
            this.session_id = response.data.session_id;
            this.printGameBlock(response.data.text, print);
        });
    }

    printGameBlock(txt, print){
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
}

export default GameTerminalPlugin;

