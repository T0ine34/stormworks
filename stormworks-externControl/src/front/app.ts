import { getCurrentLayout } from "./utils";


declare var io: any;
declare type Socket<ServerToClientEvents, ClientToServerEvents> = any;


interface ServerToClientEvents {
    noArg: () => void;
    basicEmit: (a: string) => void;
    data: (data: { [key: string]: any }) => void;
}

interface ClientToServerEvents {
    noArg: () => void;
    basicEmit: (a: string) => void;
    button: (data: { id: string, state: boolean|number }) => void;
}


type Callback = (data : string) => void;



export class App {
    private static instance: App;

    private socket: Socket<ServerToClientEvents, ClientToServerEvents> = {} as Socket<ServerToClientEvents, ClientToServerEvents>;
    private inputCallbacks: { [id: string]: Function[] } = {};
    private outputCallbacks: { [id: string]: Function[] } = {};
    private layout: string = '';

    constructor() {
        if (App.instance) {
            return App.instance;
        }
        App.instance = this;

        this.socket = io('http://localhost:3000');

        this.inputCallbacks = {};
        this.outputCallbacks = {};

        this.layout = getCurrentLayout(window);

        this.registerEventListeners();
    }

    registerEventListeners() {
        this.socket.on('connect', () => {
            console.log('Connected to server');
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
        });

        this.socket.on('data', (data : Object) => {
            if (!data) {
                return;
            }
            let elements = Object.entries(data);
            for (let i = 0; i < elements.length; i++) {
                const [id, value] = elements[i] as [string, string];
                if (this.inputCallbacks[id]) {
                    this.inputCallbacks[id].forEach((callback) => {
                        callback(value);
                    });
                }
            }
        });
    }

    update(id : string, state : boolean|number) {
        let layout = this.layout;
        this.socket.emit('button', { id, state, layout });
        if (this.outputCallbacks[id]) {
            this.outputCallbacks[id].forEach((callback) => {
                callback(state);
            });
        }
    }

    registerInputCallback(id : string, callback : Callback) { // id is the id of the button "b1", "n21", etc.
        if (!this.inputCallbacks[id]) {
            this.inputCallbacks[id] = [];
        }
        this.inputCallbacks[id].push(callback);
        console.log("Input callback registered for", id);
    }

    registerOutputCallback(id : string, callback : Callback) {
        if (!this.outputCallbacks[id]) {
            this.outputCallbacks[id] = [];
        }
        this.outputCallbacks[id].push(callback);
        console.log("Output callback registered for", id);
    }
}